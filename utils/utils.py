import copy
from typing import Union, Set, Deque, Dict, List
from ib110hw.automaton.fa import FA
from ib110hw.automaton.nfa import NFA, NFATransitions
from ib110hw.automaton.dfa import DFA
from minimization_examples import *
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
            f"""digraph G {{\n\t_init[shape=none]\n\t_init[label=\"\"]\n\t_init -> {automaton.initial_state}\n"""
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
    Input automaton is not altered.

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
    Input automaton is not altered.

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


def remove_unreachable_states(automaton: Union[DFA, NFA]) -> Union[NFA, DFA]:
    """
    Removes unreachable states from the provided automaton.
    Input automaton is not altered.

    Args:
        automaton (Union[DFA, NFA]):

    Returns:
        Equal automaton without unreachable states.
    """
    result = copy.deepcopy(automaton)
    reachable = {automaton.initial_state}
    q = deque()
    q.append(automaton.initial_state)

    while q:
        state = q.popleft()

        if isinstance(automaton, NFA):
            next_s = set()
            for symbol in automaton.alphabet:
                next_s.update(automaton.get_transition(state, symbol))
        else:
            next_s = {*[automaton.get_transition(state, symbol) for symbol in automaton.alphabet]}

        q.extend(next_s.difference(reachable))
        reachable.update(next_s)

    for state in list(automaton.states.difference(reachable)):
        result.remove_state(state)

    return result


# rewrite
def minimize(automaton: DFA) -> DFA:
    """
    Returns a minimized version of the provided automaton.
    Input automaton is not altered.

    Args:
        automaton (FA): Automaton to be minimized

    Returns:
        DFA: Minimized version of the provided automaton.
    """

    def get_groups(_transitions: DFATransitions) -> List[Set[str]]:
        new_groups = {}

        for g_index, _group in enumerate(groups):
            for _state in sorted(_group):
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

    minimized_transitions: DFATransitions = {}
    reachable: DFA = remove_unreachable_states(automaton)

    result: DFA = DFA(
        reachable.states,
        reachable.alphabet,
        reachable.initial_state,
        set(),
        transitions=minimized_transitions
    )

    groups: List[Set[str]] = [
        reachable.final_states,
        reachable.states.difference(reachable.final_states)
    ]

    while True:
        # create transitions with group indexes instead of states
        # break when nothing changes
        marked_transitions = {}

        for state in reachable.transitions:
            for symbol in sorted(reachable.alphabet):
                for index, group in enumerate(groups):
                    if reachable.get_transition(state, symbol) not in group:
                        continue

                    if state not in marked_transitions.keys():
                        marked_transitions[state] = {}

                    marked_transitions[state][symbol] = f"{index}"

        if len(groups) == len(groups := get_groups(marked_transitions)):
            break

    result.states = set(map(lambda i: f"{i}", range(0, len(groups))))

    for index in range(len(groups)):
        if groups[index].intersection(reachable.final_states):
            result.final_states.add(f"{index}")

        if reachable.initial_state in groups[index]:
            result.initial_state = f"{index}"

        minimized_transitions[f"{index}"] = marked_transitions[groups[index].pop()]

    return result


def canonize(automaton: DFA) -> DFA:
    """
    Transforms provided automaton to its canonical form.
    Input automaton is not altered.

    Args:
        automaton (DFA): Automaton to be canonized

    Returns:
        Canonical form of the provided automaton.
    """
    ordered_states: List[str] = []
    for state in automaton.transitions.keys():
        if state not in ordered_states:
            ordered_states.append(state)

        for symbol in automaton.transitions[state].keys():
            if automaton.transitions[state][symbol] not in ordered_states:
                ordered_states.append(automaton.transitions[state][symbol])

    # append states that are not in the transitions
    ordered_states.extend([state for state in sorted(automaton.states) if state not in ordered_states])

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


def compare_automatons(a1: Union[NFA, DFA], a2: Union[NFA, DFA]) -> bool:
    a1 = canonize(minimize(determinize(a1)))
    a2 = canonize(minimize(determinize(a2)))

    return a1.states == a2.states and \
           a1.final_states == a2.final_states and \
           a1.alphabet == a2.alphabet and \
           a1.transitions == a2.transitions


if __name__ == "__main__":
    print(ex1_a)
    print(ex2_a)
    print(ex3_a)
    print(ex4_a)

    automaton_to_graphviz(ex1_a, r"C:\Skola\SBAPR\minimization\ex1.dot")
    automaton_to_graphviz(minimize(ex1_a), r"C:\Skola\SBAPR\minimization\ex1_min.dot")
    automaton_to_graphviz(ex2_a, r"C:\Skola\SBAPR\minimization\ex2.dot")
    automaton_to_graphviz(minimize(ex2_a), r"C:\Skola\SBAPR\minimization\ex2_min.dot")
    automaton_to_graphviz(ex3_a, r"C:\Skola\SBAPR\minimization\ex3.dot")
    automaton_to_graphviz(minimize(ex3_a), r"C:\Skola\SBAPR\minimization\ex3_min.dot")
    automaton_to_graphviz(ex4_a, r"C:\Skola\SBAPR\minimization\ex4.dot")
    automaton_to_graphviz(minimize(ex4_a), r"C:\Skola\SBAPR\minimization\ex4_min.dot")
    automaton_to_graphviz(ex5_a, r"C:\Skola\SBAPR\minimization\ex5.dot")
    automaton_to_graphviz(minimize(ex5_a), r"C:\Skola\SBAPR\minimization\ex5_min.dot")
    automaton_to_graphviz(ex6_a, r"C:\Skola\SBAPR\minimization\ex6.dot")
    automaton_to_graphviz(minimize(ex6_a), r"C:\Skola\SBAPR\minimization\ex6_min.dot")
    automaton_to_graphviz(ex7_a, r"C:\Skola\SBAPR\minimization\ex7.dot")
    automaton_to_graphviz(minimize(ex7_a), r"C:\Skola\SBAPR\minimization\ex7_min.dot")
