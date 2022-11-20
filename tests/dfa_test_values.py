from ib110hw.automaton.dfa import DFA

one_state_no_transitions = DFA({"s"}, {}, "s", {"s"}, {})

t1 = {"s": {"a": "s", "b": "s"}}
one_state_with_transitions = DFA({"s"}, {"a", "b"}, "s", {"s"}, t1)
