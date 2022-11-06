from typing import Union, Set, Deque
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

                if s_from not in transitions or symbol not in transitions[
                        s_from]:
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


def remove_empty_transitions(automaton: NFA) -> None:
    """
    Removes all epsilon (ε) transitions.

    Args:
        automaton (NFA): Automaton to be updated
    """
    raise NotImplemented()


def minimalize(automaton: FA) -> None:
    """
    Minimalizes the provided automaton. 

    Args:
        automaton (FA): Automaton to be minimalized
    """
    raise NotImplemented()


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

    switches = DFA(alphabet={"a", "b", "c"},
                   final_states={"s2", "s3", "s4", "s7"},
                   initial_state="s4",
                   states={"s1", "s2", "s3", "s4", "s5", "s6", "s7"},
                   transitions=transitions_switches)

    test_word = "cabbacac"

    print(switches, "\n")

    automaton_to_graphviz(switches, r"C:\Skola\SBAPR\dfa_demo_switches.dot")
    print(f"Is '{test_word}' accepted:", switches.is_accepted(test_word))


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


if __name__ == "__main__":
    dfa_demo()
