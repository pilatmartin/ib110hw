from ib110hw.automaton.dfa import DFA, DFATransitions

ex1_transitions: DFATransitions = {
    "0": {
        "a": "1",
        "b": "2",
    },
    "1": {
        "a": "1",
        "b": "3",
    },
    "2": {
        "a": "1",
        "b": "2",
    },
    "3": {
        "a": "1",
        "b": "4",
    },
    "4": {
        "a": "1",
        "b": "2",
    }
}

ex1_transitions_expected: DFATransitions = {
    "02": {
        "a": "1",
        "b": "02",
    },
    "1": {
        "a": "1",
        "b": "3",
    },
    "3": {
        "a": "1",
        "b": "4",
    },
    "4": {
        "a": "1",
        "b": "02",
    },
}

ex1_automaton: DFA = DFA(
    {"0", "1", "2", "3", "4"},
    {"a", "b"},
    "0",
    {"4"},
    ex1_transitions
)

ex1_automaton_expected: DFA = DFA(
    {"02", "1", "3", "4"},
    {"a", "b"},
    "02",
    {"4"},
    ex1_transitions_expected,
)

ex2_transitions: DFATransitions = {
    "0": {
        "a": "1",
        "b": "0",
    },
    "1": {
        "a": "2",
        "b": "1",
    },
    "2": {
        "a": "1",
        "b": "2",
    },
    "3": {
        "a": "1",
        "b": "2",
    }
}

ex2_transitions_expected: DFATransitions = {
    "0": {
        "a": "12",
        "b": "0",
    },
    "12": {
        "a": "12",
        "b": "12",
    },
}

ex2_automaton: DFA = DFA(
    {"0", "1", "2", "3"},
    {"a", "b"},
    "0",
    {"1", "2"},
    ex2_transitions
)

ex2_automaton_expected: DFA = DFA(
    {"0", "12"},
    {"a", "b"},
    "0",
    {"12"},
    ex2_transitions_expected
)

ex3_transitions: DFATransitions = {
    "0": {
        "a": "1",
        "b": "3",
    },
    "1": {
        "a": "2",
        "b": "4",
    },
    "2": {
        "a": "1",
        "b": "4",
    },
    "3": {
        "a": "2",
        "b": "4",
    },
    "4": {
        "a": "4",
        "b": "4",
    },
}

ex3_transitions_expected: DFATransitions = {
    "0": {
        "a": "123",
        "b": "123",
    },
    "123": {
        "a": "123",
        "b": "4",
    },
    "4": {
        "a": "4",
        "b": "4",
    }
}

ex3_automaton: DFA = DFA(
    {"0", "1", "2", "3", "4"},
    {"a", "b"},
    "0",
    {"4"},
    ex3_transitions
)

ex3_automaton_expected: DFA = DFA(
    {"0", "123", "4"},
    {"a", "b"},
    "0",
    {"4"},
    ex3_transitions_expected,
)

ex4_transitions: DFATransitions = {
    "0": {
        "a": "1",
        "b": "2",
    },
    "1": {
        "a": "2",
        "b": "3",
    },
    "2": {
        "a": "2",
        "b": "4",
    },
    "3": {
        "a": "3",
        "b": "3",
    },
    "4": {
        "a": "4",
        "b": "4",
    },
    "5": {
        "a": "5",
        "b": "4",
    },
}

ex4_transition_expected: DFATransitions = {
    "0": {
        "a": "125",
        "b": "125",
    },
    "125": {
        "a": "125",
        "b": "34",
    },
    "34": {
        "a": "34",
        "b": "34",
    },
}

ex4_automaton: DFA = DFA(
    {"0", "1", "2", "3", "4", "5"},
    {"a", "b"},
    "0",
    {"3", "4"},
    ex4_transitions
)

ex4_automaton_expected: DFA = DFA(
    {"0", "125", "34"},
    {"a", "b"},
    "0",
    {"34"},
    ex4_transition_expected,
)

ex5_transitions = {
    "A": {
        "a": "B",
        "b": "C",
    },
    "B": {
        "a": "D",
        "b": "E",
    },
    "C": {
        "a": "C",
        "b": "C",
    },
    "D": {
        "a": "B",
        "b": "E",
    },
    "E": {
        "a": "F",
        "b": "E",
    },
    "F": {
        "a": "G",
        "b": "E",
    },
    "G": {
        "a": "D",
        "b": "E",
    },
}

ex5_transitions_expected: DFATransitions = {
    "A": {
        "a": "BDFG",
        "b": "C",
    },
    "C": {
        "a": "C",
        "b": "C",
    },
    "BDFG": {
        "a": "BDFG",
        "b": "E",
    },
    "E": {
        "a": "BDFG",
        "b": "E",
    }
}

ex5_automaton = DFA(
    {"A", "B", "C", "D", "E", "F", "G"},
    {"a", "b"},
    "A",
    {"B", "D", "F", "G"},
    ex5_transitions
)
ex5_automaton_expected: DFA = DFA(
    {"A", "C", "E", "BDFG"},
    {"a", "b"},
    "A",
    {"BDFG"},
    ex5_transitions_expected,
)

minimal_transitions: DFATransitions = {
    "1": {
        "a": "2",
        "b": "4",
    },
    "2": {
        "a": "4",
        "b": "3",
    },
    "3": {
        "a": "3",
        "b": "6",
    },
    "4": {
        "a": "4",
        "b": "5",
    },
    "5": {
        "a": "5",
        "b": "5",
    },
    "6": {
        "a": "2",
        "b": "5",
    },
}

minimal_transitions_expected: DFATransitions = minimal_transitions

minimal_automaton: DFA = DFA(
    {"1", "2", "3", "4", "5", "6"},
    {"a", "b"},
    "1",
    {"3", "5"},
    minimal_transitions
)

minimal_automaton_expected: DFA = minimal_automaton

minimal2_transitions = {
    "A": {
        "a": "B",
        "b": "D",
    },
    "B": {
        "a": "D",
        "b": "C",
    },
    "C": {
        "a": "C",
        "b": "F",
    },
    "D": {
        "a": "D",
        "b": "E",
    },
    "E": {
        "a": "E",
        "b": "E",
    },
    "F": {
        "a": "B",
        "b": "E",
    },
}

minimal2_transitions_expected: DFATransitions = minimal2_transitions

minimal2_automaton: DFA = DFA(
    {"A", "B", "C", "D", "E", "F"},
    {"a", "b"},
    "A",
    {"C", "E"},
    minimal2_transitions
)

minimal2_automaton_expected = minimal2_automaton

two_equivalent_states_transitions: DFATransitions = {
    "1": {
        "a": "2",
        "b": "2",
    },
    "2": {
        "a": "1",
        "b": "1",
    },
}

two_equivalent_states_transitions_expected = {
    "1": {
        "a": "1",
        "b": "1",
    },
}

two_equivalent_states_automaton: DFA = DFA(
    {"1", "2"},
    {"a", "b"},
    "1",
    {"1", "2"},
    two_equivalent_states_transitions,
)

two_equivalent_states_automaton_expected = DFA(
    {"1"},
    {"a", "b"},
    "1",
    {"1"},
    two_equivalent_states_transitions_expected,
)

disjoint_transitions: DFATransitions = {
    "1": {"a": "1"},
}

disjoint_transitions_expected: DFATransitions = {
    "1": {"a": "1"},
}

disjoint_automaton: DFA = DFA(
    {"1", "2", "3", "4", "5"},
    {"a", "b"},
    "1",
    set(),
    disjoint_transitions
)

disjoint_automaton_expected: DFA = DFA(
    {"1"},
    {"a", "b"},
    "1",
    set(),
    disjoint_transitions_expected
)
