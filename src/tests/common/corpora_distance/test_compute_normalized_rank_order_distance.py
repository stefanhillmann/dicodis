

__author__ = 'stefan'

import unittest

import common.corpora_distance.distance as d
import common.ngram.model_generator as mg


class TestComputeNormalizedDistance(unittest.TestCase):

    def test_rank_order_normalized_distance(self):
        p_n_grams = ['a', 'b', 'b', 'c', 'c', 'd', 'd', 'd']
        q_n_grams = ['a', 'b', 'b', 'e', 'e', 'e']

        p = mg.generate_model(p_n_grams)
        q = mg.generate_model(q_n_grams)

        distance_calculator = d.get_normalized_rank_order_calculator()
        distance = distance_calculator.compute_distance(p, q, 0)

        msg = "Manually computed normalized distance was 9/21 (nine over twenty one) (~ 0.429). The current result is: {0}".format(
            distance)
        self.assertEqual(float(9) / float(21), distance, msg)



