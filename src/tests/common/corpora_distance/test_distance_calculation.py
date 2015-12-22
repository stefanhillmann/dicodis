
"""test_distance_calculation.py: Runs unit test on calculation of distance between n-gram models."""

__author__ = 'Stefan Hillmann (public@stefan-hillmann.net)'
__date__ = "2015-07-09"

import unittest

import common.corpora_distance.distance as d
from common.ngram.n_gram_model import NGramModel


class TestDistanceCalculation(unittest.TestCase):

    def setUp(self):
        self.model_a = NGramModel({'d': 20, 'b': 10, 'c': 20, 'a': 20})
        self.model_b = NGramModel({'a': 10, 'b': 10, 'c': 20})

    def test_rank_order_distance(self):
        calc = d.get_rank_order_calculator()
        distance = calc.compute_distance(self.model_a, self.model_b, 0.0)
        self.assertEqual(distance, 3)

if __name__ == "__main__":
    unittest.main()
