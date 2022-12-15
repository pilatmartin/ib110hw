import unittest
from utils.utils import minimize, canonize
from tests.minimization.test_cases import *
from tests.test_utils import *


class TestMinimization(unittest.TestCase):
    def are_valid(self, expected, actual):
        self.assertEqual(expected.states, actual.states, INVALID_STATES)
        self.assertEqual(expected.alphabet, actual.alphabet, INVALID_ALPHABET)
        self.assertEqual(expected.initial_state, actual.initial_state, INVALID_INITIAL_STATE)
        self.assertEqual(expected.final_states, actual.final_states, INVALID_FINAL_STATES)
        self.assertEqual(expected.transitions, actual.transitions, INVALID_TRANSITIONS)

    def test_lecture(self):
        actual = canonize(minimize(ex1_a))
        expected = canonize(ex1_a_exp)
        self.are_valid(expected, actual)
