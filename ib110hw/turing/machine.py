from typing import Set


class TuringMachine:
    """Represents a abstract Turing machine class
    """

    def __init__(self,
                 states: Set[str],
                 input_alphabet: Set[str],
                 acc_states: Set[str],
                 rej_states: Set[str] = set(),
                 initial_state: str = "init",
                 start_symbol: str = ">",
                 empty_symbol: str = "") -> None:
        self.states = states
        self.input_alphabet = input_alphabet
        self.acc_states = acc_states
        self.rej_states = rej_states
        self.initial_state = initial_state
        self.start_symbol = start_symbol
        self.empty_symbol = empty_symbol

        # After exceeding max_steps value, the turing machine will be considered as looping.
        # Change this value for more complex scenarios.
        self.max_steps = 100

    def add_state(self,
                  state: str,
                  is_acc: bool = False,
                  is_rej: bool = False) -> bool:
        """Adds state to the machine.

        Args:
            state (str): State to be added.
            is_acc (bool, optional): True if the state is accepting. Defaults to False.
            is_rej (bool, optional): True if the state is rejecting. Defaults to False.

        Returns:
            bool: False if the state is already present or 'is_acc' and 'is_rej' arguments are both True.
                  True otherwise.
        """
        if state in self.states or (is_acc and is_rej):
            return False

        if is_acc:
            self.acc_states.add(state)

        if is_rej:
            self.rej_states.add(state)

        return True

    def remove_state(self, state: str) -> bool:
        """
        Removes the state from the machine.

        Args:
            state (str): State to be removed.

        Returns:
            bool: Returns True if the state was added successfully, False otherwise.
        """
        if state not in self.states:
            return False

        if state in self.acc_states:
            self.acc_states.remove(state)

        if state in self.rej_states:
            self.rej_states.remove(state)

        self.states.remove(state)

        return True


if __name__ == "__main__":
    pass
