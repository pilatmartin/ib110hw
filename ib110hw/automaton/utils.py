from typing import Union, Set, Deque, Dict, List
from fa import FA
from nfa import NFA, NFATransitions
from dfa import DFA, DFATransitions
from collections import deque


def automaton_to_graphviz(automaton: Union[NFA, DFA], path: str) -> None:
    """ 
    Converts automaton to the graphviz format (.dot file) and saves
    the result in the specified location.

    Args:
        automaton (Union[NFA, DFA]): Automaton to be converted.
        path (str): Path where the file will be created.
    """
    with open(path, "w") as file:
        file.write(
            f"""digraph G {{\n\t_init[shape=none]\n\t_init[label=\"\"]\n\t_init -> {automaton.initial_state}"""
        )

        for s_from in automaton.states:
            for symbol in automaton.alphabet:
                transitions = automaton.transitions

                if s_from not in transitions or symbol not in transitions[s_from]:
                    continue

                if not (s_to := automaton.get_transition(s_from, symbol)):
                    file.write(f"\t{s_from};\n")
                    continue

                file.write(
                    f"\t{s_from} -> {str(s_to).replace(chr(39), '')}[label={symbol}];\n"
                )

        for fin_state in automaton.final_states:
            file.write(f"\t{fin_state} [shape=doublecircle]\n")

        file.write("}\n")


def determinize(automaton: NFA) -> DFA:
    """
    Returns equivalent DFA version of the provided NFA

    Args:
        automaton (NFA): NFA automaton to be determinized

    Returns:
        DFA: Determinized automaton
    """
    automaton = remove_empty_transitions(automaton)

    states: Deque[Set[str]] = deque()
    states.append({automaton.initial_state})

    det_states: Set[str] = set()
    det_final_states: Set[str] = set()
    det_transitions = {automaton.initial_state: {}}

    while states:
        state = states.popleft()
        str_state = "".join(sorted(state))

        if str_state in det_states:
            continue

        det_states.add(str_state)
        det_transitions[str_state] = {}

        if automaton.final_states.intersection(state):
            det_final_states.add(str_state)

        for key in automaton.alphabet:
            new_state = set()
            for s in state:
                new_state = new_state.union(automaton.get_transition(s, key))

            det_transitions[str_state][key] = f"{''.join(sorted(new_state))}"
            states.append(new_state)

    return DFA(states=det_states,
               alphabet=automaton.alphabet,
               final_states=det_final_states,
               initial_state=automaton.initial_state,
               transitions=det_transitions)


def remove_empty_transitions(automaton: NFA) -> NFA:
    """
    Removes all epsilon (ε) transitions.

    Args:
        automaton (NFA): Automaton to be updated

    Returns:
        NFA: Equivalent automaton without ε transitions.
    """
    if "" not in automaton.alphabet:
        return automaton

    next1: Dict[str, Set[str]] = {}
    transitions: NFATransitions = {}

    result: NFA = NFA(
        states=automaton.states,
        alphabet=automaton.alphabet.difference({""}),
        initial_state=automaton.initial_state,
        final_states=automaton.final_states,
        transitions=transitions
    )

    # next1
    for state in automaton.transitions:
        next1[state] = {state}.union(automaton.get_transition(state, ""))

        for next_state in automaton.get_transition(state, ""):
            next1[state] = next1[state].union(next1[next_state])

    # next2
    for state in next1:
        for symbol in result.alphabet:
            for next_state in next1[state]:
                result.add_transition(state, automaton.get_transition(next_state, symbol), symbol)

    # next3
    for state in result.transitions:
        for symbol in result.alphabet:
            next2_transition = {*result.get_transition(state, symbol)}

            for next_state in next2_transition:
                result.add_transition(state, next1[next_state], symbol)

    return result


# rewrite
def minimize(automaton: DFA) -> DFA:
    """
    Returns a minimized version of the provided automaton.

    Args:
        automaton (FA): Automaton to be minimized

    Returns:
        DFA: Minimized version of the provided automaton.
    """

    def get_groups(_transitions: DFATransitions) -> List[Set[str]]:
        new_groups = {}

        for g_index, _group in enumerate(groups):
            for _state in _group:
                # group key is prefixed with index
                # to distinguish the same transitions from different groups
                group_key = f"{g_index}_"
                if _state not in _transitions.keys():
                    continue

                for _symbol in automaton.alphabet:
                    if _symbol not in _transitions[_state].keys():
                        continue

                    if transition := _transitions[_state][_symbol]:
                        group_key += transition

                if group_key not in new_groups.keys():
                    new_groups[group_key] = set()

                new_groups[group_key].add(_state)

        return list(new_groups.values())

    minimized_transitions = {}

    result: DFA = DFA(
        automaton.states,
        automaton.alphabet,
        automaton.initial_state,
        set(),
        transitions=minimized_transitions
    )
    groups: List[Set[str]] = [
        automaton.final_states,
        automaton.states.difference(automaton.final_states)
    ]

    while True:
        # create transitions with group indexes instead of states
        # break when nothing changes
        marked_transitions = {}

        for state in automaton.transitions:
            for symbol in automaton.alphabet:
                for index, group in enumerate(groups):
                    if automaton.get_transition(state, symbol) not in group:
                        continue

                    if state not in marked_transitions.keys():
                        marked_transitions[state] = {}

                    marked_transitions[state][symbol] = f"{index}"

        if len(groups) == len(groups := get_groups(marked_transitions)):
            break

    result.states = set(map(lambda i: f"{i}", range(0, len(groups))))

    for index in range(len(groups)):
        if groups[index].intersection(automaton.final_states):
            result.final_states.add(f"{index}")

        if automaton.initial_state in groups[index]:
            result.initial_state = f"{index}"

        minimized_transitions[f"{index}"] = marked_transitions[groups[index].pop()]

    return result


def canonize(automaton: DFA) -> DFA:
    ordered_states: List[str] = []
    for state in automaton.transitions.keys():
        for symbol in automaton.transitions[state].keys():
            if automaton.transitions[state][symbol] not in ordered_states:
                ordered_states.append(automaton.transitions[state][symbol])

    # append states that are not in the transitions
    ordered_states.extend([state for state in automaton.states if state not in ordered_states])

    result_transitions: DFATransitions = {}
    result_final_states: Set[str] = set()
    result_initial_state = ""
    for state in ordered_states:
        new_state = f"{ordered_states.index(state)}"
        result_transitions[new_state] = {}

        if state == automaton.initial_state:
            result_initial_state = new_state

        if state in automaton.final_states:
            result_final_states.add(new_state)

        for symbol in automaton.transitions[state].keys():
            new_next_state = f"{ordered_states.index(automaton.transitions[state][symbol])}"
            result_transitions[new_state][symbol] = new_next_state

    return DFA(
        set(map(lambda i: f"{i}", range(0, len(ordered_states)))),
        automaton.alphabet,
        result_initial_state,
        result_final_states,
        result_transitions
    )


def dfa_demo():
    # Switches DFA (hw1)
    print("#### Switches DFA (hw1) ####\n")
    transitions_switches: DFATransitions = {
        "s1": {
            "a": "s3",
            "b": "s1",
            "c": "s2",
        },
        "s2": {
            "a": "s5",
            "b": "s1",
            "c": "s2",
        },
        "s3": {
            "a": "s3",
            "b": "s1",
            "c": "s6",
        },
        "s4": {
            "a": "s3",
            "b": "s7",
            "c": "s2",
        },
        "s5": {
            "a": "s5",
            "b": "s7",
            "c": "s2",
        },
        "s6": {
            "a": "s3",
            "b": "s7",
            "c": "s6",
        },
        "s7": {
            "a": "s5",
            "b": "s7",
            "c": "s6",
        },
    }

    switches = DFA(alphabet={"a", "b", "c", "d"},
                   final_states={"s2", "s3", "s4", "s7"},
                   initial_state="s4",
                   states={"s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8"},
                   transitions=transitions_switches)

    test_word = "cabbacac"

    print(switches, "\n")

    automaton_to_graphviz(switches, r"C:\Skola\SBAPR\dfa_demo_switches.dot")
    print(f"Is '{test_word}' accepted:", switches.is_accepted(test_word))

    switches.add_state("s8")
    print(switches)

    print(switches.add_transition("s7", "s8", "d"))
    print(switches)
    print(switches.add_transition("s7", "s8", "d"))
    automaton_to_graphviz(switches, r"C:\Skola\SBAPR\dfa_demo_switches2.dot")

    print(switches.remove_transition("s7", "d"))
    print(switches.remove_transition("s7", "d"))

    to_minimize_t = {
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

    to_minimize_a = DFA(
        {"A", "B", "C", "D", "E", "F", "G"},
        {"a", "b"},
        "A",
        {"B", "D", "F", "G"},
        to_minimize_t
    )

    minimize(to_minimize_a)


def nfa_demo():
    # NFA: last letter occurs at least twice
    print("#### Last letter occurs at least twice ####\n")
    transitions: NFATransitions = {
        "s1": {
            "a": {"s1", "s2"},
            "b": {"s1", "s3"},
            "c": {"s1", "s4"},
        },
        "s2": {
            "a": {"s2", "s5"},
            "b": {"s2"},
            "c": {"s2"},
        },
        "s3": {
            "a": {"s3"},
            "b": {"s3", "s5"},
            "c": {"s3"},
        },
        "s4": {
            "a": {"s4"},
            "b": {"s4"},
            "c": {"s4", "s5"},
        },
    }

    last_letter = NFA(states={"s1", "s2", "s3", "s4", "s5"},
                      alphabet={"a", "b", "c"},
                      initial_state="s1",
                      final_states={"s5"},
                      transitions=transitions)

    test_word = "cba"
    automaton_to_graphviz(last_letter,
                          r"C:\Skola\SBAPR\nfa_demo_last_letter.dot")

    print(f"Is accepted '{test_word}':", last_letter.is_accepted(test_word),
          "\n")
    print(last_letter)
    print("=" * 40, "\n")

    # NFA that accepts only 'a(b*a*)*a'
    print("#### Accepts only 'a(b*a*)*a' ####\n")

    transitions_abba: NFATransitions = {
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
    }

    abba = NFA(alphabet={"a", "b"},
               states={"s1", "s2", "s3"},
               initial_state="s1",
               final_states={"s2"},
               transitions=transitions_abba)

    test_word = "abaaab"

    automaton_to_graphviz(abba, r"C:\Skola\SBAPR\nfa_demo_abba.dot")
    print(f"Is accepted '{test_word}':", abba.is_accepted(test_word), "\n")
    print("=" * 40, "\n")

    # Determinization example from a lecture
    print("#### Determinization example from a lecture ####\n")
    transitions = {
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

    det_test = NFA(states={"0", "1", "2", "3"},
                   alphabet={"a", "b"},
                   initial_state="0",
                   final_states={"1", "2"},
                   transitions=transitions)

    print("Before determinization")
    print(det_test, "\n")
    print("After determinization")
    print(determinize(det_test))

    empty_t = {
        "0": {
            "a": {"1"}
        },
        "1": {
            "b": {"2"},
            "": {"0"},
        },
        "2": {
            "a": {"2"},
            "": {"1"},
        }
    }

    nfa_empty_t = NFA({"0", "1", "2"}, {"a", "b", ""}, "0", {"2"}, empty_t)

    print(nfa_empty_t)

    print(remove_empty_transitions(nfa_empty_t))


if __name__ == "__main__":
    to_minimize_t = {
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

    to_minimize_a = DFA(
        {"A", "B", "C", "D", "E", "F", "G"},
        {"a", "b"},
        "A",
        {"B", "D", "F", "G"},
        to_minimize_t
    )

    print(canonize(minimize(to_minimize_a)))
