from ib110hw.automaton.nfa import NFA
from ib110hw.automaton.dfa import DFA

# region example1: Determinization example from the lecture
lecture_t = {
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

lecture_t_exp = {
    "0": {
        "a": "12",
    },
    "12": {
        "a": "0123",
        "b": "3"
    },
    "0123": {
        "a": "0123",
        "b": "3",
    },
    "3": {
        "a": "23",
        "b": "3",
    },
    "23": {
        "a": "023",
        "b": "3",
    },
    "023": {
        "a": "0123",
        "b": "3",
    }
}

lecture_a = NFA(
    {"0", "1", "2", "3"},
    {"a", "b"},
    "0",
    {"1", "2"},
    lecture_t,
)

lecture_a_exp = DFA(
    {"0", "12", "0123", "3", "23", "023"},
    {"a", "b"},
    "0",
    {"12", "0123", "23", "023"},
    lecture_t_exp,
)
# endregion example1

# region example 2: star formation - every state is accepting (accepts "a", "b")
star1_t = {
    "s1": {
        "a": {"s2", "s4", "s6"},
        "b": {"s3", "s5", "s7"},
    }
}
star1_t_exp = {
    "s1": {
        "a": "s2s4s6",
        "b": "s3s5s7"
    },
    "s2s4s6": {},
    "s3s5s7": {},
}

star1_a = NFA(
    {"s1", "s2", "s3", "s4", "s5", "s6", "s7"},
    {"a", "b"},
    "s1",
    {"s2", "s3", "s4", "s5", "s6", "s7"},
    star1_t,
)

star1_a_exp = DFA(
    {"s1", "s2s4s6", "s3s5s7"},
    {"a", "b"},
    "s1",
    {"s2s4s6", "s3s5s7"},
    star1_t_exp,
)
# endregion example2

# region example3: star with every state being equivalent
star2_t = {
    "s1": {
        "a": {"s2", "s3", "s4", "s5", "s6", "s7"},
        "b": {"s2", "s3", "s4", "s5", "s6", "s7"},
    }
}

start2_t_exp = {
    "s1": {
        "a": "s2s3s4s5s6s7",
        "b": "s2s3s4s5s6s7",
    },
    "s2s3s4s5s6s7": {},
}

star2_a = NFA(
    {"s1", "s2", "s3", "s4", "s5", "s6", "s7"},
    {"a", "b"},
    "s1",
    {"s2", "s3", "s4", "s5", "s6", "s7"},
    star2_t,
)

star2_a_exp = DFA(
    {"s1", "s2s3s4s5s6s7"},
    {"a", "b"},
    "s1",
    {"s2s3s4s5s6s7"},
    start2_t_exp,
)
# endregion example3

# region example4: star with every other state being accepting
star3_t = {
    "s1": {
        "a": {"s2", "s4", "s6"},
        "b": {"s3", "s5", "s7"},
    }
}

star3_t_exp = {
    "s1": {
        "a": "s2s4s6",
        "b": "s3s5s7",
    },
    "s2s4s6": {},
    "s3s5s7": {},
}

star3_a = NFA(
    {"s1", "s2", "s3", "s4", "s5", "s6", "s7"},
    {"a", "b"},
    "s1",
    {"s2", "s3", "s5", "s6"},
    star3_t,
)

star3_a_exp = DFA(
    {"s1", "s2s4s6", "s3s5s7"},
    {"a", "b"},
    "s1",
    {"s2s4s6", "s3s5s7"},
    star3_t_exp,
)
# endregion example 4

# region example5: empty transition goes to the only accepting state
empty_to_acc_t = {
    "s1": {
        "": {"s2"},
        "a": {"s3"}
    }
}

empty_to_acc_t_exp = {
    "s1": {
        "a": "s3",
    },
    "s3": {},
}

empty_to_acc_a = NFA(
    {"s1", "s2", "s3"},
    {"", "a"},
    "s1",
    {"s2"},
    empty_to_acc_t
)

empty_to_acc_a_exp = DFA(
    {"s1", "s3"},
    {"a"},
    "s1",
    set(),
    empty_to_acc_t_exp
)
# endregion example5

# region example6: all states are disconnected and have no transitions
disjoint_t = {}
disjoint_a = NFA({"s1", "s2", "s3", "s4"}, {"a"}, "s1", {"s2"}, disjoint_t)

disjoint_t_exp = {"s1": {}}
disjoint_a_exp = DFA({"s1"}, {"a"}, "s1", set(), disjoint_t_exp)
# endregion example6

# region example7: automaton is a complete graph + every edge has whole alphabet
complete_t = {
    "s1": {
        "a": {"s2", "s3", "s4", "s5"},
        "b": {"s2", "s3", "s4", "s5"},
    },
    "s2": {
        "a": {"s1", "s3", "s4", "s5"},
        "b": {"s1", "s3", "s4", "s5"},
    },
    "s3": {
        "a": {"s1", "s2", "s4", "s5"},
        "b": {"s1", "s2", "s4", "s5"},
    },
    "s4": {
        "a": {"s1", "s2", "s3", "s5"},
        "b": {"s1", "s2", "s3", "s5"},
    },
    "s5": {
        "a": {"s1", "s2", "s3", "s4"},
        "b": {"s1", "s2", "s3", "s4"},
    },
}

complete_a = NFA(
    {"s1", "s2", "s3", "s4", "s5"},
    {"a", "b"},
    "s1",
    {"s1", "s2", "s3", "s4", "s5"},
    complete_t
)

complete_t_exp = {
    "s1": {
        "a": "s2",
        "b": "s2",
    },
    "s2": {
        "a": "s3",
        "b": "s3"
    },
    "s3": {
        "a": "s3",
        "b": "s3"
    },
}

complete_a_exp = DFA(
    {"s1", "s2", "s3"},
    {"a", "b"},
    "s1",
    {"s1", "s2", "s3"},
    complete_t_exp
)
# endregion example7

