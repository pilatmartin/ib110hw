from ib110hw.automaton.nfa import NFA, NFATransitions

# Determinization example from a lecture
ex1_t = {
    "0": {
        "a": {"1", "2"},
    },
    "1": {
        "a": {"1", "2"},
        "b": {"3"},
    },
    "2": {
        "a": {"0", "3"},
        "b": {"3"},
    },
    "3": {
        "a": {"2", "3"},
        "b": {"3"},
    }
}

ex1_a = NFA(states={"0", "1", "2", "3"},
            alphabet={"a", "b"},
            initial_state="0",
            final_states={"1", "2"},
            transitions=ex1_t)
