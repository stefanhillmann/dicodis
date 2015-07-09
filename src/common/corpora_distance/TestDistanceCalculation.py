
"""TestDistanceCalculation.py: Runs unit test on calculation of distance between n-gram models."""

__author__ = 'Stefan Hillmann (public@stefan-hillmann.net)'
__date__ = "2015-07-09"

import unittest
import common.corpora_distance.distance as d

class TestDistanceCalculation(unittest.TestCase):

    def setUp(self):
        self.model_a = {'d': 2, 'b': 1, 'c': 2, 'a': 2}
        self.model_b = {'a': 1, 'b': 1, 'c': 2}

    def test_rank_order_distance(self):
        calc = d.get_rank_order_calculator()
        distance = calc.compute_distance(self.model_a, self.model_b)
        self.assertEqual(distance, 6)

if __name__ == "__main__":
    unittest.main()
