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

star_t = {
    "s1": {
        "a": {"s2", "s4", "s6"},
        "b": {"s3", "s5", "s7"},
    }
}

star_a = NFA(
    {"s1", "s2", "s3", "s4", "s5", "s6", "s7"},
    {"a", "b"},
    "s1",
    {"s2", "s3", "s4", "s5", "s6", "s7"},
    star_t,
)

star2_t = {
    "s1": {
        "a": {"s2", "s3", "s4", "s5", "s6", "s7"},
        "b": {"s2", "s3", "s4", "s5", "s6", "s7"},
    }
}

star2_a = NFA(
    {"s1", "s2", "s3", "s4", "s5", "s6", "s7"},
    {"a", "b"},
    "s1",
    {"s2", "s3", "s4", "s5", "s6", "s7"},
    star2_t,
)

star3_t = {
    "s1": {
        "a": {"s2", "s4", "s6"},
        "b": {"s3", "s5", "s7"},
    }
}

star3_a = NFA(
    {"s1", "s2", "s3", "s4", "s5", "s6", "s7"},
    {"a", "b"},
    "s1",
    {"s2", "s3", "s5", "s6"},
    star3_t,
)

idk1_t = {
    "s1": {
        "": {"s2"},
        "a": {"s3"}
    }
}
idk1_a = NFA(
    {"s1", "s2", "s3"},
    {"", "a"},
    "s1",
    {"s2"},
    idk1_t
)

# empty transition goes to the only final state
empty_to_fin_t_exp = {
    "s1": {"a": {"s3"}}
}
empty_to_fin_a_exp = NFA({"s1", "s3"}, {"a"}, "s1", set(), empty_to_fin_t_exp)

# all states are disconnected
disjoint_t = {}
disjoint_a = NFA({"s1", "s2", "s3", "s4"}, {"a"}, "s1", {"s2"}, disjoint_t)

disjoint_t_exp = {}
disjoint_a_exp = NFA({"s1"}, set(), "s1", set(), disjoint_t_exp)

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
