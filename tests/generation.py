from random import randint, choice, choices
from typing import Set
from ib110hw.automaton.dfa import DFA
from ib110hw.automaton.nfa import NFA
from ib110hw.automaton.utils import automaton_to_graphviz, remove_unreachable_states


def r_dfa(min_deg: int,
          max_deg: int,
          min_states: int,
          max_states: int,
          min_fin_states: int,
          max_fin_states: int,
          alphabet: Set[str]) -> DFA:
    """
    Generates random DFA:
        Generate random set of states (length between min_states and max_states)
        Pick an initial state from the generated set of states.

        For each state (starting with the initial state):
            Generate degree (between min_deg and max_deg)
            Generate set of next states (the amount depends on the generated degree)
            For every next state, pick a transition symbol

    Args:
        min_deg: The minimum degree of each state.
        max_deg: The maximum degree of each state.
        min_states: The minimum amount of states.
        max_states: The maximum amount of states.
        min_fin_states: The minimum amount of final states.
        max_fin_states: The maximum amount of final states.
        alphabet: Alphabet used by the automaton. (Not every symbol may be used)

    Returns:
        Random DFA. (Can be disjointed)
    """
    def add_next_states(_min_deg: int, _state: str) -> None:
        s_deg = randint(_min_deg, max_deg)
        next_states = choices(states, k=s_deg)
        symbols = choices(list(alphabet), k=s_deg)

        for next_s, symbol in zip(next_states, symbols):
            result.add_transition(_state, next_s, symbol)

    states = [f"s{i}" for i in range(randint(min_states, max_states))]
    result = DFA(
        set(states),
        alphabet,
        choice(states),
        set(choices(states, k=randint(min_fin_states, max_fin_states))),
        {}
    )

    add_next_states(1, result.initial_state)

    for state in result.states.difference([result.initial_state]):
        add_next_states(min_deg, state)

    return result


def r_nfa(min_deg: int,
          max_deg: int,
          min_states: int,
          max_states: int,
          min_fin_states: int,
          max_fin_states: int,
          alphabet: Set[str]) -> NFA:
    """
    Generates random NFA:
        Generate random set of states (length between min_states and max_states)
        Pick an initial state from the generated set of states.

        For each state (starting with the initial state):
            Generate list of integers (sums up to the max_deg)->each integer is the amount of next states for a symbol.
            For each integer i, sample set of next states of size i.
            Add symbol to every sampled set.

    Args:
        min_deg: The minimum degree of each state.
        max_deg: The maximum degree of each state.
        min_states: The minimum amount of states.
        max_states: The maximum amount of states.
        min_fin_states: The minimum amount of final states.
        max_fin_states: The maximum amount of final states.
        alphabet: Alphabet used by the automaton. (Not every symbol may be used)

    Returns:
        Random NFA. (Can be disjointed)
    """
    def add_next_states(_min_deg: int, _max_deg: int, _state: str) -> None:
        s_deg = randint(_min_deg, max_deg)
        symbols = choices(list(alphabet), k=s_deg)

        degs_by_symbol = []
        for _ in range(len(symbols)):
            curr_deg = 0 if _max_deg < min_deg else randint(_min_deg, _max_deg)
            degs_by_symbol.append(curr_deg)
            _max_deg -= curr_deg

        for deg, symbol in zip(degs_by_symbol, set(symbols)):
            result.add_transition(_state, set(choices(states, k=deg)), symbol)

    states = [f"s{i}" for i in range(randint(min_states, max_states))]
    result = NFA(
        set(states),
        alphabet,
        choice(states),
        set(choices(states, k=randint(min_fin_states, max_fin_states))),
        {}
    )

    add_next_states(1, max_deg, result.initial_state)

    for state in result.states.difference([result.initial_state]):
        add_next_states(max_deg, min_deg, state)

    return result


if __name__ == "__main__":
    r_dfa_automaton = r_dfa(1, 3, 2, 10, 2, 5, {"a", "b"})
    print(r_dfa_automaton)
    r_reachable = remove_unreachable_states(r_dfa_automaton)
    print(r_reachable)

    r_nfa_automaton = r_nfa(1, 3, 2, 10, 2, 5, {"a", "b"})
    print(r_nfa_automaton)
    r_reachable = remove_unreachable_states(r_nfa_automaton)
    print(r_reachable)

    r_name = f"r_dfa_{randint(0, 10 ** 10)}"
    automaton_to_graphviz(r_dfa_automaton, f"C:\\Skola\\SBAPR\\r_automatons\\r_dfa\\{r_name}.dot")
    automaton_to_graphviz(r_reachable, f"C:\\Skola\\SBAPR\\r_automatons\\r_dfa\\{r_name}_reach.dot")

    r_name = f"r_nfa_{randint(0, 10 ** 10)}"
    automaton_to_graphviz(r_nfa_automaton, f"C:\\Skola\\SBAPR\\r_automatons\\r_nfa\\{r_name}.dot")
    automaton_to_graphviz(r_reachable, f"C:\\Skola\\SBAPR\\r_automatons\\r_nfa\\{r_name}_reach.dot")
