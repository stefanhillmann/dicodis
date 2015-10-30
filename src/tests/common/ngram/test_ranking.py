__author__ = 'Stefan Hillmann'

import unittest
from common.ngram import model_generator as mg

class TestRanking(unittest.TestCase):

    def test_create_rank_model_from_different_frequencies(self):
        f_model = {'a': 10, 'b': 30, 'c': 20}  # test data

        r_model = mg.create_rank_model(f_model)

        self.assertEqual(len(r_model), 3)
        self.assertEqual(r_model['a'], 3)
        self.assertEqual(r_model['b'], 1)
        self.assertEqual(r_model['c'], 2)

    def test_create_rank_model_from_overlapping_frequencies(self):
        f_model = {'a': 10, 'b': 30, 'c': 10}  # test data

        r_model = mg.create_rank_model(f_model)

        self.assertEqual(len(r_model), 3)
        self.assertEqual(r_model['a'], 2)
        self.assertEqual(r_model['b'], 1)
        self.assertEqual(r_model['c'], 2)

    def test_create_rank_model_from_overlapping_frequencies(self):
        f_model = {'a': 50, 'b': 50, 'c': 50}  # test data

        r_model = mg.create_rank_model(f_model)

        self.assertEqual(len(r_model), 3)
        self.assertEqual(r_model['a'], 1)
        self.assertEqual(r_model['b'], 1)
        self.assertEqual(r_model['c'], 1)

    def test_create_rank_model_from_empty_frequencies_model(self):
        f_model = {}  # test data

        r_model = mg.create_rank_model(f_model)

        self.assertEqual(len(r_model), 0)




