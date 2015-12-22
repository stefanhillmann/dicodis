# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 14:24:24 2013

@author: Stefan Hillmann (stefan.hillmann@tu-berlin.de)
"""

import numpy as np
import unittest

import common.ngram.smoothing as smoothing


class TestSmoothing(unittest.TestCase):

    def test_compute_probability_case_1(self):
        num_unique_ngrams   = 17
        num_ngrams          = 8
        l                   = 0.5
        ngram_frequency     = 0

        p = smoothing.compute_probability(num_unique_ngrams, num_ngrams, l, ngram_frequency)
        p = round(p, 4)

        self.assertEqual(p, 0.0303)

    def test_compute_probability_case_2(self):
        num_unique_ngrams   = 17
        num_ngrams          = 9
        l                   = 0.5
        ngram_frequency     = 1

        p = smoothing.compute_probability(num_unique_ngrams, num_ngrams, l, ngram_frequency)
        p = round(p, 4)

        self.assertEqual(p, 0.0857)

    def test_compute_probability_case_3(self):
        num_unique_ngrams   = 17
        num_ngrams          = 19
        l                   = 0.0
        ngram_frequency     = 2

        p = smoothing.compute_probability(num_unique_ngrams, num_ngrams, l, ngram_frequency)
        p = round(p, 4)

        self.assertEqual(p, 0.1053)

    def test_compute_probabilities_case_1(self):
        a = 1. / 19.
        b = 2. / 19.
        frequencies             = np.array([1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
        l = 0.0

        smoothed_probabilities = smoothing.compute_probabilities(frequencies, l)

        self.assertEqual(smoothed_probabilities[1], a)
        self.assertEqual(smoothed_probabilities[2], b)
