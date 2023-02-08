from src.automaton.dfa import DFA
from hypothesis import given, assume
from hypothesis.strategies import integers, sets, characters, composite, DrawFn
from .generation import r_dfa


@composite
def r_test_dfa(
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

    r_automaton = r_dfa(
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


@given(r_test_dfa())
def test_add_state(automaton: DFA) -> None:
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


@given(r_test_dfa())
def test_remove_state(automaton: DFA):
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


@given(r_test_dfa())
def test_add_transition(automaton: DFA) -> None:
    automaton.add_state("test_state")
    automaton.alphabet.add("a")

    assert automaton.add_transition("test_state", "test_state", "a")
    assert "test_state" in automaton.transitions.keys()
    assert "a" in automaton.transitions["test_state"].keys()
    assert "test_state" == automaton.transitions["test_state"]["a"]
    assert not automaton.add_transition("test_state", "test_state", "a")

    assert not automaton.add_transition("not_exists", "test_state", "a")
    assert not automaton.add_transition("test_state", "not_exists", "a")
    assert not automaton.add_transition("test_state", "test_state", "not_exists")


@given(r_test_dfa())
def test_remove_transition(automaton: DFA) -> None:
    automaton.add_state("test_state")
    automaton.alphabet.add("a")
    automaton.add_transition("test_state", automaton.initial_state, "a")

    assert not automaton.remove_transition("test_state", "not_exists")
    assert not automaton.remove_transition(
        "test_state", automaton.alphabet.difference(["a"]).pop()
    )
    assert not automaton.remove_transition("not_exists", "a")
    assert automaton.remove_transition("test_state", "a")
    assert not automaton.get_transition("test_state", "a")
