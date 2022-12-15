import unittest
from utils.utils import determinize, canonize
from tests.determinization.test_cases import *
from tests.test_utils import *


class TestDeterminization(unittest.TestCase):
    def are_valid(self, expected, actual):
        self.assertEqual(expected.states, actual.states, INVALID_STATES)
        self.assertEqual(expected.alphabet, actual.alphabet, INVALID_ALPHABET)
        self.assertEqual(expected.initial_state, actual.initial_state, INVALID_INITIAL_STATE)
        self.assertEqual(expected.final_states, actual.final_states, INVALID_FINAL_STATES)
        self.assertEqual(expected.transitions, actual.transitions, INVALID_TRANSITIONS)

    def test_lecture(self):
        actual = canonize(determinize(lecture_a))
        expected = canonize(lecture_a_exp)
        self.are_valid(expected, actual)

    def test_star(self):
        actual = canonize(determinize(star1_a))
        expected = canonize(star1_a_exp)
        self.are_valid(expected, actual)

    def test_star_equivalent_states(self):
        actual = canonize(determinize(star2_a))
        expected = canonize(star2_a_exp)
        self.are_valid(expected, actual)

    def test_star_every_other_accepting(self):
        actual = canonize(determinize(star3_a))
        expected = canonize(star3_a_exp)
        self.are_valid(expected, actual)

    def test_empty_to_only_accepting(self):
        actual = canonize(determinize(empty_to_acc_a))
        expected = canonize(empty_to_acc_a_exp)
        self.are_valid(expected, actual)

    def test_disjoint(self):
        actual = canonize(determinize(disjoint_a))
        expected = canonize(disjoint_a_exp)
        self.are_valid(expected, actual)

    def test_complete(self):
        actual = canonize(determinize(complete_a))
        expected = canonize(complete_a_exp)
        self.are_valid(expected, actual)
