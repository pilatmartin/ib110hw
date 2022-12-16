import unittest
from utils.utils import minimize, canonize, automaton_to_graphviz
from tests.minimization.test_cases import *
from tests.test_utils import *


class TestMinimization(unittest.TestCase):
    def are_valid(self, expected, actual):
        with self.subTest():
            self.assertEqual(expected.states, actual.states, INVALID_STATES)
        with self.subTest():
            self.assertEqual(expected.alphabet, actual.alphabet, INVALID_ALPHABET)
        with self.subTest():
            self.assertEqual(expected.initial_state, actual.initial_state, INVALID_INITIAL_STATE)
        with self.subTest():
            self.assertEqual(expected.final_states, actual.final_states, INVALID_FINAL_STATES)
        with self.subTest():
            self.assertEqual(expected.transitions, actual.transitions, INVALID_TRANSITIONS)

    def test1(self):
        actual = canonize(minimize(ex1_automaton))
        expected = canonize(ex1_automaton_expected)
        self.are_valid(expected, actual)

    def test2(self):
        actual = canonize(minimize(ex2_automaton))
        expected = canonize(ex2_automaton_expected)
        self.are_valid(expected, actual)

    def test3(self):
        actual = canonize(minimize(ex3_automaton))
        expected = canonize(ex3_automaton_expected)
        self.are_valid(expected, actual)

    def test4(self):
        actual = canonize(minimize(ex4_automaton))
        expected = canonize(ex4_automaton_expected)
        self.are_valid(expected, actual)

    def test5(self):
        actual = canonize(minimize(ex5_automaton))
        expected = canonize(ex5_automaton_expected)
        self.are_valid(expected, actual)

    def test_minimal1(self):
        actual = canonize(minimize(minimal_automaton))
        expected = canonize(minimal_automaton_expected)
        self.are_valid(expected, actual)

    def test_minimal2(self):
        actual = canonize(minimize(minimal2_automaton_expected))
        expected = canonize(minimal2_automaton_expected)
        self.are_valid(expected, actual)

    def test_two_equivalent_states(self):
        actual = canonize(minimize(two_equivalent_states_automaton))
        expected = canonize(two_equivalent_states_automaton_expected)
        self.are_valid(expected, actual)

    def test_disjoint(self):
        actual = canonize(minimize(disjoint_automaton))
        expected = canonize(disjoint_automaton_expected)
        self.are_valid(expected, actual)
