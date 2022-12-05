# DU demo - Príklad 1 (2,5b)

# Implementujte algoritmus konverzie ε-NFA na NFA.
# Inými slovami, zo vstupného NFA odstráňte všetky epsilon (ε) prechody.

from typing import Dict, Set
from ib110hw.automaton.nfa import NFA, NFATransitions


def remove_epsilon_transitions(automaton: NFA) -> NFA:
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


if __name__ == "__main__":
    transitions: NFATransitions = {
        "0": {
            "a": {"1"},
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

    automaton: NFA = NFA(
        states={"0", "1", "2"},
        alphabet={"a", "b", ""},
        initial_state="0",
        final_states={"2"},
        transitions=transitions
    )

    print(automaton)
    print(remove_epsilon_transitions(automaton))
