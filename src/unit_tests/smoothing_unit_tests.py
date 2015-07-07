# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 14:24:24 2013

@author: Stefan Hillmann (stefan.hillmann@tu-berlin.de)
"""

import numpy as np

import common.ngram.smoothing as smoothing


def test_compute_probability_case_1():
    num_unique_ngrams   = 17
    num_ngrams          = 8
    l                   = 0.5
    ngram_frequency     = 0
    
    p = smoothing.compute_probability(num_unique_ngrams, num_ngrams, l, ngram_frequency)
    p = round(p, 4)
    print "test_computed_probability_case_1: {}".format(p)
    assert p == 0.0303

def test_compute_probability_case_2():
    num_unique_ngrams   = 17
    num_ngrams          = 9
    l                   = 0.5
    ngram_frequency     = 1
    
    p = smoothing.compute_probability(num_unique_ngrams, num_ngrams, l, ngram_frequency)
    p = round(p, 4)
    print "test_computed_probability_case_2: {}".format(p)
    assert p == 0.0857

def test_compute_probability_case_3():
    num_unique_ngrams   = 17
    num_ngrams          = 19
    l                   = 0.0
    ngram_frequency     = 2
    
    p = smoothing.compute_probability(num_unique_ngrams, num_ngrams, l, ngram_frequency)
    p = round(p, 4)
    print "test_computed_probability_case_3: {}".format(p)
    assert p == 0.1053

def test_compute_probabilities_case_1():
    a = 1. / 19.
    b = 2. / 19.
    frequencies             = np.array([1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
    reference_probabilities = np.array([a, a, a, a, a, b, b, a, a, a, a, a, a, a, a, a, a], dtype=float)
    l = 0.0
    
    probabilities = smoothing.compute_probabilities(frequencies, l)
    print "test_compute_probabilities_case_1: {}".format(probabilities)
    assert np.array_equal(reference_probabilities, probabilities)