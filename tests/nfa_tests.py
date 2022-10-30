import sys

sys.path.append("..")

from ib110hw.automaton.dfa import NFA
from hypothesis import given
from hypothesis.strategies import characters, booleans

TMP_AUTOMATON: NFA = NFA(alphabet={"a", "b"},
                    states={"s1", "s2", "s3"},
                    initial_state="s1",
                    final_states={"s2"},
                    transitions={
                        "s1": {
                            "a": {"s2"},
                        },
                        "s2": {
                            "a": {"s2"},
                            "b": {"s3"},
                        },
                        "s3": {
                            "a": {"s2"},
                            "b": {"s3"}
                        }
                    })


@given(characters(), booleans())
def test_add_state(state: str, is_final: bool) -> None:
    TMP_AUTOMATON.add_state(state, is_final)

    assert not (is_final and state not in TMP_AUTOMATON.final_states) and \
            state in [*TMP_AUTOMATON.states, *TMP_AUTOMATON.transitions.keys()]


@given(characters())
def test_remove_state(state: str) -> None:
    TMP_AUTOMATON.remove_state(state)

    assert state not in [
        *TMP_AUTOMATON.states, 
        *TMP_AUTOMATON.final_states, 
        *TMP_AUTOMATON.transitions.keys(), 
        #TODO add check of values in tranisitions
        ]

def test_add_transition() -> None:
    pass

def test_remove_transition() -> None:
    pass

def is_accepted() -> None:
    pass
