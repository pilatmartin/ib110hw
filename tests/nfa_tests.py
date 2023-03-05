from sys import path
from hypothesis import given, assume
from hypothesis.strategies import (
    integers,
    sets,
    characters,
    composite,
    DrawFn,
    lists,
    sampled_from,
)
from re import match
from tests.generation import r_nfa

path.append("../src/ib110hw")

from automaton.nfa import NFA
from automaton.utils import automaton_to_graphviz


@composite
def r_test_nfa(
    draw: DrawFn,
    min_deg=integers(min_value=1, max_value=10),
    max_deg=integers(min_value=1, max_value=10),
    min_states=integers(min_value=2, max_value=10),
    max_states=integers(min_value=2, max_value=10),
    min_fin_states=integers(min_value=1, max_value=10),
    max_fin_states=integers(min_value=2, max_value=10),
    alphabet=sets(characters(), min_size=2, max_size=20),
):
    max_deg = draw(max_deg)
    min_deg = min(draw(min_deg), max_deg)
    max_states = draw(max_states)
    min_states = min(draw(min_states), max_states)
    max_fin_states = draw(max_fin_states)
    min_fin_states = min(draw(min_fin_states), max_fin_states)

    r_automaton = r_nfa(
        min_deg,
        max_deg,
        min_states,
        max_states,
        min_fin_states,
        max_fin_states,
        draw(alphabet),
    )

    diff = r_automaton.states.difference(r_automaton.final_states)
    assume(diff and diff != {r_automaton.initial_state})

    return r_automaton


@given(r_test_nfa())
def test_add_state(automaton: NFA) -> None:
    assert automaton.add_state("test_state_1")

    # cannot add the same state twice
    assert not automaton.add_state("test_state_1")
    assert not automaton.add_state("test_state_1", True)
    assert "test_state_1" in automaton.states
    assert "test_state_1" not in automaton.final_states
    assert "test_state_1" not in automaton.transitions

    assert automaton.add_state("test_state_2", True)
    assert not automaton.add_state("test_state_2")
    assert "test_state_2" in automaton.states
    assert "test_state_2" in automaton.final_states


@given(r_test_nfa())
def test_remove_state(automaton: NFA) -> None:
    # pick state that can be safely removed
    state = next(
        s
        for s in automaton.states
        if s not in automaton.final_states and s != automaton.initial_state
    )

    assert automaton.remove_state(state)
    # cannot remove the same state twice
    assert not automaton.remove_state(state)
    assert state not in automaton.states
    assert not automaton.remove_state("not_existent")
    assert not automaton.remove_state(automaton.initial_state)

    prev_initial = automaton.initial_state
    automaton.states.add("test_init_state")
    automaton.initial_state = "test_init_state"

    # just in case the initial state is the only final state
    if prev_initial in automaton.final_states:
        automaton.final_states.remove(prev_initial)

    assert automaton.remove_state(prev_initial)
    assert prev_initial not in automaton.states
    assert prev_initial not in automaton.final_states
    assert not automaton.transitions.get(prev_initial, None)

    automaton.add_state("test_final_state", True)
    # just in case the final states was empty
    automaton.add_state("filler_state", True)

    assert automaton.remove_state("test_final_state")
    assert "test_final_state" not in automaton.final_states


@given(r_test_nfa())
def test_add_transition(automaton: NFA) -> None:
    automaton.add_state("test_state")
    automaton.alphabet.add("a")

    assert automaton.add_transition("test_state", {"test_state"}, "a")
    assert "test_state" in automaton.transitions.keys()
    assert "a" in automaton.transitions["test_state"]
    assert {"test_state"} == automaton.transitions["test_state"]["a"]
    assert not automaton.add_transition("test_state", {"test_state"}, "a")

    assert not automaton.add_transition("not_exists", {"test_state"}, "a")
    assert not automaton.add_transition("test_state", {"not_exists"}, "a")
    assert not automaton.add_transition("test_state", {"test_state"}, "not_exists")

    automaton.add_state("test_second_state")
    assert automaton.add_transition("test_state", {"test_second_state"}, "a")
    assert "test_second_state" not in automaton.transitions.keys()
    assert {"test_state", "test_second_state"} == automaton.get_transition(
        "test_state", "a"
    )
    assert not automaton.add_transition("test_state", {"test_second_state"}, "a")


@given(r_test_nfa())
def test_remove_transition(automaton: NFA) -> None:
    automaton.add_state("test_state")
    automaton.alphabet.add("a")
    automaton.add_transition("test_state", {"test_state"}, "a")

    assert not automaton.remove_transition(
        "test_state", automaton.alphabet.difference(["a"]).pop(), "test_state"
    )
    assert not automaton.remove_transition("not_exists", "test_state", "a")
    assert automaton.remove_transition("test_state", "test_state", "a")
    assert not automaton.get_transition("test_state", "a")
    assert not automaton.remove_transition("test_state", "test_state", "a")

    automaton.add_state("test_second_state")
    automaton.add_transition("test_state", {"test_state", "test_second_state"}, "a")
    assert automaton.remove_transition("test_state", "test_state", "a")
    assert automaton.get_transition("test_state", "a") == {"test_second_state"}


@composite
def r_input_string_acc(draw: DrawFn):
    length = draw(integers(min_value=1, max_value=50))
    insert_idx = draw(integers(min_value=0, max_value=length))
    substr = draw(sampled_from(["cba", "cbaa", "ca", "cb"]))
    fill_str = "".join(
        draw(lists(sampled_from("abc"), min_size=length, max_size=length))
    )

    return fill_str[:insert_idx] + substr + fill_str[insert_idx:]


@composite
def r_input_string_rej(draw: DrawFn):
    length = draw(integers(min_value=2, max_value=50))
    result = "".join(draw(lists(sampled_from("abc"), min_size=length, max_size=length)))

    while match(r".*(cba|cbaa|ca|cb).*", result):
        for acc_str in ["cba", "cbaa", "ca", "cb"]:
            result = result.replace(acc_str, "")

    assume(len(result) > 1)

    return result


@given(r_input_string_acc(), r_input_string_rej())
def test_is_accepted(acc_str: str, rej_str: str) -> None:
    automaton: NFA = NFA(
        states={f"s{i}" for i in range(10)},
        alphabet={"a", "b", "c"},
        initial_state="s0",
        final_states={"s3", "s5", "s7", "s9"},
        transitions={
            "s0": {"a": {"s0"}, "b": {"s0"}, "c": {"s0", "s1", "s6", "s8"}},
            "s1": {"b": {"s2"}},
            "s2": {"a": {"s3", "s4"}},
            "s3": {"a": {"s3"}, "b": {"s3"}, "c": {"s3"}},
            "s4": {"a": {"s5"}},
            "s5": {"a": {"s5"}, "b": {"s5"}, "c": {"s5"}},
            "s6": {"a": {"s7"}},
            "s7": {"a": {"s7"}, "b": {"s7"}, "c": {"s7"}},
            "s8": {"b": {"s9"}},
            "s9": {"a": {"s9"}, "b": {"s9"}, "c": {"s9"}},
        },
    )

    assert automaton.is_accepted(acc_str), f"Expected '{acc_str}' to be accepted."
    assert not automaton.is_accepted(rej_str), f"Expected '{rej_str}' to be rejected."
