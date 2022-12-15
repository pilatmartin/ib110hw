import copy
from typing import Union, Set, Deque, Dict, List
from ib110hw.automaton.fa import FA
from ib110hw.automaton.nfa import NFA, NFATransitions
from ib110hw.automaton.dfa import DFA
from tests.minimization.test_cases import *
from tests.determinization.test_cases import *
from collections import deque


def automaton_to_graphviz(automaton: Union[NFA, DFA], path: str) -> None:
    """ 
    Converts automaton to the graphviz format (.dot file) and saves
    the result in the specified location.

    Args:
        automaton (Union[NFA, DFA]): Automaton to be converted.
        path (str): Path where the file will be created.
    """
    with open(path, "w", encoding="utf-8") as file:
        file.write("digraph G {\n")
        file.write("\t__init__[shape=none label=\"\"]\n")
        file.write(f"\t__init__ -> {automaton.initial_state}\n")

        for s_from in automaton.states:
            for symbol in automaton.alphabet:
                s_to = automaton.get_transition(s_from, symbol)
                if not s_to and not s_from not in automaton.transitions.keys():
                    file.write(f"\t{s_from}\n")
                    continue

                if isinstance(automaton, NFA):
                    for state in s_to:
                        file.write(f"\t{s_from} -> {state}[label=\"{'ε' if not symbol else symbol}\"]\n")
                else:
                    file.write(f"\t{s_from} -> {s_to}[label={'ε' if not symbol else symbol}]\n")

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

            if not new_state:
                continue

            det_transitions[str_state][key] = ''.join(sorted(new_state))
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
    for state in automaton.states:
        next1[state] = {state}.union(automaton.get_transition(state, ""))

        for next_state in automaton.get_transition(state, ""):
            next1[state] = next1[state].union(next1.get(next_state, set()))

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
                result.add_transition(state, next1.get(next_state, set()), symbol)

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

        return [new_groups[key] for key in sorted(new_groups.keys())]

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

        prev_len = len(groups)
        groups = get_groups(marked_transitions)
        if prev_len == len(groups):
            break

    result.states = set([f"{i}" for i in range(0, len(groups))])

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
    renamed = {}
    states = deque()
    states.append(automaton.initial_state)

    # used for renaming the states
    rank = 0

    while states:
        current_state = states.popleft()
        renamed[current_state] = f"{rank}"

        for symbol in sorted(automaton.alphabet):
            next_state = automaton.get_transition(current_state, symbol)
            if next_state in renamed.keys():
                continue
            states.append(next_state)

        rank += 1

    renamed_transitions = {
        renamed[state]: automaton.transitions[state] for state in automaton.transitions.keys()
    }

    for state in renamed_transitions.keys():
        for symbol in renamed_transitions[state].keys():
            prev = renamed_transitions[state][symbol]
            renamed_transitions[state][symbol] = renamed[prev]

    result = DFA(
        set([renamed[state] for state in automaton.states]),
        automaton.alphabet,
        renamed[automaton.initial_state],
        set([renamed[state] for state in automaton.final_states]),
        renamed_transitions
    )

    return result


def compare_automatons(a1: Union[NFA, DFA], a2: Union[NFA, DFA]) -> bool:
    if isinstance(a1, NFA):
        a1 = determinize(a1)

    if isinstance(a2, NFA):
        a2 = determinize(a2)

    a1 = canonize(minimize(a1))
    a2 = canonize(minimize(a2))

    return a1.states == a2.states and \
           a1.final_states == a2.final_states and \
           a1.alphabet == a2.alphabet and \
           a1.transitions == a2.transitions


if __name__ == "__main__":
    print(ex1_a)
    print(ex2_a)
    print(ex3_a)
    print(ex4_a)

    # automaton_to_graphviz(ex1_a, r"C:\Skola\SBAPR\minimization\ex1.dot")
    # automaton_to_graphviz(minimize(ex1_a), r"C:\Skola\SBAPR\minimization\ex1_min.dot")
    # automaton_to_graphviz(ex2_a, r"C:\Skola\SBAPR\minimization\ex2.dot")
    # automaton_to_graphviz(minimize(ex2_a), r"C:\Skola\SBAPR\minimization\ex2_min.dot")
    # automaton_to_graphviz(ex3_a, r"C:\Skola\SBAPR\minimization\ex3.dot")
    # automaton_to_graphviz(minimize(ex3_a), r"C:\Skola\SBAPR\minimization\ex3_min.dot")
    # automaton_to_graphviz(ex4_a, r"C:\Skola\SBAPR\minimization\ex4.dot")
    # automaton_to_graphviz(minimize(ex4_a), r"C:\Skola\SBAPR\minimization\ex4_min.dot")
    # automaton_to_graphviz(ex5_a, r"C:\Skola\SBAPR\minimization\ex5.dot")
    # automaton_to_graphviz(minimize(ex5_a), r"C:\Skola\SBAPR\minimization\ex5_min.dot")
    # automaton_to_graphviz(ex6_a, r"C:\Skola\SBAPR\minimization\ex6.dot")
    # automaton_to_graphviz(minimize(ex6_a), r"C:\Skola\SBAPR\minimization\ex6_min.dot")
    # automaton_to_graphviz(ex7_a, r"C:\Skola\SBAPR\minimization\ex7.dot")
    # automaton_to_graphviz(minimize(ex7_a), r"C:\Skola\SBAPR\minimization\ex7_min.dot")

    automaton_to_graphviz(star_a, r"C:\Skola\SBAPR\determinization\star.dot")
    automaton_to_graphviz(determinize(star_a), r"C:\Skola\SBAPR\determinization\star_det.dot")
    automaton_to_graphviz(star2_a, r"C:\Skola\SBAPR\determinization\star2.dot")
    automaton_to_graphviz(determinize(star2_a), r"C:\Skola\SBAPR\determinization\star2_det.dot")
    automaton_to_graphviz(star3_a, r"C:\Skola\SBAPR\determinization\star3.dot")
    automaton_to_graphviz(determinize(star3_a), r"C:\Skola\SBAPR\determinization\star3_det.dot")
    automaton_to_graphviz(idk1_a, r"C:\Skola\SBAPR\determinization\idk1.dot")
    automaton_to_graphviz(determinize(idk1_a), r"C:\Skola\SBAPR\determinization\idk1_det.dot")
    automaton_to_graphviz(complete_a, r"C:\Skola\SBAPR\determinization\complete.dot")
    automaton_to_graphviz(determinize(complete_a), r"C:\Skola\SBAPR\determinization\complete_det.dot")
