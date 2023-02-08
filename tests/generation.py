from random import randint, choice, sample
from typing import Set, List
from src.automaton.dfa import DFA
from src.automaton.nfa import NFA


def r_states(min_states: int, max_states: int) -> List[str]:
    return [f"s{i}" for i in range(randint(min_states, max_states))]


def r_dfa(
    min_deg: int,
    max_deg: int,
    min_states: int,
    max_states: int,
    min_fin_states: int,
    max_fin_states: int,
    alphabet: Set[str],
) -> DFA:
    """
    Generates random DFA:
        1. Generates random set of states (length between min_states and max_states)
        2. Picks an initial state from the generated set of states.

        3. For each state (starting with the initial state):
            3.1 Generate degree (between min_deg and max_deg)
            3.2 Generate set of next states (the amount depends on the generated degree)
            3.3 For every next state, pick a transition symbol

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
    assert min_deg <= max_deg
    assert min_states <= max_states
    assert min_fin_states <= max_fin_states

    def add_next_states(_min_deg: int, _state: str) -> None:
        s_deg = randint(_min_deg, max_deg)
        next_states = sample(states, k=min(s_deg, len(states)))
        symbols = sample(list(alphabet), k=s_deg)

        for next_s, symbol in zip(next_states, symbols):
            result.add_transition(_state, next_s, symbol)

    # state degree cannot be bigger than the size of DFA automatons alphabet
    max_deg = min(len(alphabet), max_deg)
    min_deg = min(min_deg, max_deg)

    states = r_states(min_states, max_states)
    fin_states_range = (
        min(len(states), min_fin_states),
        min(len(states), max_fin_states),
    )

    result = DFA(
        set(states),
        alphabet,
        choice(states),
        set(sample(states, k=randint(*fin_states_range))),
        {state: {symbol: state for symbol in alphabet} for state in states},
    )

    add_next_states(1, result.initial_state)

    for state in result.states.difference([result.initial_state]):
        add_next_states(min_deg, state)

    return result


def r_nfa(
    min_deg: int,
    max_deg: int,
    min_states: int,
    max_states: int,
    min_fin_states: int,
    max_fin_states: int,
    alphabet: Set[str],
) -> NFA:
    """
    Generates random NFA:
        1. Generate random set of states (length between min_states and max_states)
        2. Pick an initial state from the generated set of states.

        3. For each state (starting with the initial state):
            3.1 Generate list of integers (sums up to the max_deg) -> each integer is the amount of next states for a symbol.
            3.2 For each integer i, sample set of next states of size i.
            3.3 Add symbol to every sampled set.

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
        s_deg = randint(_min_deg, _max_deg)
        next_states = sample(states, k=min(s_deg, len(states)))

        for next_state in next_states:
            result.add_transition(_state, {next_state}, choice(list(alphabet)))

    states = r_states(min_states, max_states)
    fin_states_range = (
        min(len(states), min_fin_states),
        min(len(states), max_fin_states),
    )

    result = NFA(
        set(states),
        alphabet,
        choice(states),
        set(sample(states, k=randint(*fin_states_range))),
        {},
    )

    add_next_states(1, max_deg, result.initial_state)

    for state in result.states.difference([result.initial_state]):
        add_next_states(min_deg, max_deg, state)

    return result


if __name__ == "__main__":
    r_dfa_automaton = r_dfa(
        min_deg=2,
        max_deg=3,
        min_states=3,
        max_states=8,
        min_fin_states=1,
        max_fin_states=3,
        alphabet={"a", "b", "c", "d"},
    )

    print(r_dfa_automaton)
