from dtm import DTM
from mtm import MTM
from _helpers import (
    read_file,
    get_dtm_configuration,
    get_mtm_configuration,
    get_dtm_transition_function,
    validate_dtm_configuration,
    validate_mtm_configuration,
    validate_dtm_transitions,
    validate_mtm_transitions,
    get_mtm_transition_function,
)
from typing import Optional
from sys import stderr

from tape import Direction


def load_dtm_from_file(file_path: str) -> Optional[DTM]:
    """
    Loads a DTM from a file if it is valid.
    Returns None if the configuration is invalid and prints the error to stderr.

    Args:
        file_path (str): Path to the file with configuration.

    Returns:
        Optional[DTM]: DTM if the configuration is valid, None otherwise.
    """
    definition = read_file(file_path)

    config_err = validate_dtm_configuration(definition)
    transitions_err = validate_dtm_transitions(definition)
    if config_err or transitions_err:
        print(config_err or transitions_err, file=stderr)
        return None

    init, acc, rej, abc = get_dtm_configuration(definition)
    transitions = get_dtm_transition_function(definition)

    return DTM(
        states={*transitions.keys()},
        input_alphabet=abc,
        acc_states=acc,
        initial_state=init,
        rej_states=rej,
        transitions=transitions,
    )


def load_mtm_from_file(file_path: str) -> Optional[MTM]:
    """
    Loads a MTM from a file if it is valid.
    Returns None if the configuration is invalid and prints the error to stderr.

    Args:
        file_path (str): Path to the file with configuration.

    Returns:
        Optional[MTM]: MTM if the configuration is valid, None otherwise.
    """
    definition = read_file(file_path)

    config_err = validate_mtm_configuration(definition)
    transitions_err = validate_mtm_transitions(definition)
    if config_err or transitions_err:
        print(config_err or transitions_err, file=stderr)
        return None

    init, acc, rej, abc, tape_count = get_mtm_configuration(definition)
    transitions = get_mtm_transition_function(definition)

    return MTM(
        states={*transitions.keys()},
        input_alphabet=abc,
        acc_states=acc,
        initial_state=init,
        rej_states=rej,
        tape_count=tape_count,
        transitions=transitions,
    )


if __name__ == "__main__":
    machine = load_dtm_from_file("./test.txt")
    machine.write_to_tape("abbabba")
    machine.simulate(step_by_step=True)
