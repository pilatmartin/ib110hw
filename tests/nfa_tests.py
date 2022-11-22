from ib110hw.automaton.nfa import NFA


def test_add_transition() -> None:
    automaton = NFA({"s"}, set("a"), "s", {"s"}, {})
    assert automaton.add_transition("s", {"s"}, "a")
    assert "s" in automaton.transitions.keys()
    assert "a" in automaton.transitions["s"].keys()
    assert {"s"} == automaton.transitions["s"]["a"]
    assert not automaton.add_transition("s", {"s"}, "a")

    assert not automaton.add_transition("not_exists", {"s"}, "a")
    assert not automaton.add_transition("s", {"not_exists"}, "a")
    assert not automaton.add_transition("s", {"s"}, "not_exists")

    t1 = {"s": {"a": {"s"}}}
    automaton = NFA({"s"}, {"a", "b"}, "s", {"s"}, t1)
    assert not automaton.add_transition("s", {"s"}, "a")
    assert automaton.add_transition("s", {"s"}, "b")
    assert not automaton.add_transition("s", {"s"}, "b")
    assert "s" in automaton.transitions.keys()
    assert "a" in automaton.transitions["s"].keys()
    assert "b" in automaton.transitions["s"].keys()
    assert {"s"} == automaton.transitions["s"]["a"]
    assert {"s"} == automaton.transitions["s"]["b"]


def test_remove_transition() -> None:
    t1 = {"s": {"a": {"s"}}}
    automaton = NFA({"s"}, {"a", "b"}, "s", {"s"}, t1)
    assert not automaton.remove_transition("s", "b", "s")
    assert not automaton.remove_transition("not_exists", "s",  "a")
    assert automaton.remove_transition("s", "s", "a")
    assert not automaton.transitions["s"]["a"]
    assert not automaton.remove_transition("s", "s", "a")

    t2 = {"s": {"a": {"s"}, "b": {"s"}}}
    automaton.transitions = t2
    assert not automaton.remove_transition("s", "s", "c")
    assert automaton.remove_transition("s", "s", "a")
    assert len(automaton.transitions.keys()) == 1
    assert len(automaton.transitions["s"].keys()) == 2
    assert len(automaton.transitions["s"]["a"]) == 0
    assert automaton.remove_transition("s", "s", "b")
    assert not automaton.transitions["s"]["a"]


def test_add_state() -> None:
    automaton = NFA({"s1"}, set(), "s1", {"s1"}, {})
    assert automaton.add_state("s2")
    assert not automaton.add_state("s2")
    assert not automaton.add_state("s2", True)

    assert "s2" in automaton.states
    assert "s2" not in automaton.final_states
    assert "s2" not in automaton.transitions.keys()

    assert automaton.add_state("s3", True)
    assert not automaton.add_state("s3")
    assert "s3" in automaton.states
    assert "s3" in automaton.final_states


def test_remove_state() -> None:
    automaton = NFA({"s1", "s2"}, set(), "s1", {"s1"}, {})
    assert automaton.remove_state("s2")
    assert "s2" not in automaton.states

    assert not automaton.remove_state("s1")
    assert not automaton.remove_state("s2")

    automaton.states.add("s2")
    automaton.initial_state = "s2"
    assert automaton.remove_state("s1")
    assert "s1" not in automaton.states
    assert "s1" not in automaton.final_states


def is_accepted() -> None:
    pass
