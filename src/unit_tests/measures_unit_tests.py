# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 15:17:13 2013

@author: Stefan Hillmann (stefan.hillmann@tu-berlin.de)
"""

import numpy as np
import unittest

from common.measuring import measures
from common.ngram import smoothing


class TestMeasures(unittest.TestCase):

    """
    Comparing equal models.
    -----------------------
    """
    """
    Testing Cosine distance with equal models.
    """
    def test_cosine_similarity_case_1(self):
        p = get_test_probabilities_vector_r(0.0)
        q = p
        cosine_distance = 1 - measures.cosine_similarity(p, q)
        print "testCosineSimilarityCase1: {}".format(cosine_distance)
        self.assertEqual(cosine_distance, 0.0)
        print "Passed."

    """
    Testing Kullback-Leibler distance with equal models.
    """
    def test_kullback_leibler_case_1(self):
        p = get_test_probabilities_vector_r(0.0)
        q = p
        kl_distance = measures.kullback_leibler_divergence(p, q)
        print "testKullbackLeiblerDivergenceCase1: {}".format(kl_distance)
        self.assertEqual(kl_distance, 0.0)
        print "Passed."

    """
    Testing mean Kullback-Leibler distance with equal models.
    """
    def test_mean_kullback_leibler_distance_case_1(self):
        p = get_test_probabilities_vector_r(0.0)
        q = p
        mkl_distance = measures.mean_kullback_leibler_distance(p, q)
        print "testMeanKullbackLeiblerDistanceCase1: {}".format(mkl_distance)
        self.assertEqual(mkl_distance, 0.0)
        print "Passed."

    """
    Testing symmetric Kullback-Leibler distance with equal models.
    """
    def test_symmetric_kullback_leibler_distance_case_1(self):
        p = get_test_probabilities_vector_r(0.0)
        q = p
        skl_distance = measures.symmetric_kullback_leibler_distance(p, q)
        print "testSymmetricKullbackLeiblerDistanceCase1: {}".format(skl_distance)
        self.assertEqual(skl_distance, 0.0)
        print "Passed."

    """
    Testing Jensen difference divergence with equal models.
    """
    def test_jensen_distance_case_1(self):
        p = get_test_probabilities_vector_r(0.0)
        q = p
        jensen_distance = measures.jensen_distance(p, q)
        print "testJensenDistanceCase1: {}".format(jensen_distance)
        self.assertEqual(jensen_distance, 0.0)
        print "Passed."

    """
    Comparing different models.
    -----------------------
    """

    """
    Testing Cosine distance with different models.
    """
    def test_cosine_similarity_case_2(self):
        m = get_test_probabilities_vector_m(0.0)
        p = get_test_probabilities_vector_q(0.5)
        cosine_distance = 1 - measures.cosine_similarity(m, p)
        print "testCosineSimilarityCase2: {}".format(cosine_distance)
        self.assertEqual(round(cosine_distance, 3), 0.096)
        print "Passed."

    """
    Testing Kullback-Leibler distance with different models.
    """
    def test_kullback_leibler_case_2(self):
        m = get_test_probabilities_vector_m(0.0)
        p = get_test_probabilities_vector_q(0.5)
        kl_distance = measures.kullback_leibler_divergence(p, m)
        print "testKullbackLeiblerDivergenceCase1: {}".format(kl_distance)
        self.assertEqual(round(kl_distance, 4), 0.1198)
        print "Passed."

    """
    Testing mean Kullback-Leibler distance with different models.
    """
    def test_mean_kullback_leibler_distance_case_2(self):
        m = get_test_probabilities_vector_m(0.0)
        p = get_test_probabilities_vector_q(0.5)
        mkl_distance = measures.mean_kullback_leibler_distance(p, m)
        print "testMeanKullbackLeiblerDistanceCase1: {}".format(mkl_distance)
        self.assertEqual(round(mkl_distance, 4), 0.1203)
        print "Passed."

    """
    Testing symmetric Kullback-Leibler distance with different models.
    """
    def test_symmetric_kullback_leibler_distance_case_2(self):
        m = get_test_probabilities_vector_m(0.0)
        p = get_test_probabilities_vector_q(0.5)
        skl_distance = measures.symmetric_kullback_leibler_distance(p, m)
        print "testSymmetricKullbackLeiblerDistanceCase1: {}".format(skl_distance)
        self.assertEqual(round(skl_distance, 4), 0.2407)
        print "Passed."

    """
    Testing Jensen difference divergence with different models.
    """
    def test_jensen_distance_case_2(self):
        m = get_test_probabilities_vector_m(0.0)
        p = get_test_probabilities_vector_q(0.5)
        jensen_distance = measures.jensen_distance(p, m)
        print "testJensenDistanceCase1: {}".format(jensen_distance)
        self.assertEqual(round(jensen_distance, 4), 0.0297)
        print "Passed."



"""
Creating test data.
-------------------
"""
def get_test_probabilities_vector_r(l):
    v = get_test_frequencies_vector_r()
    p = smoothing.compute_probabilities(v, l)
    return p

def get_test_probabilities_vector_m(l):
    v = get_test_frequencies_vector_m()
    m = smoothing.compute_probabilities(v, l)
    return m

def get_test_probabilities_vector_p(l):
    v = get_test_frequencies_vector_p()
    p = smoothing.compute_probabilities(v, l)
    return p

def get_test_probabilities_vector_q(l):
    v = get_test_frequencies_vector_q()
    q = smoothing.compute_probabilities(v, l)
    return q
    
"""
Frequencies from participants 44 1-gram-model
"""
def get_test_frequencies_vector_r():
    v = np.array([3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
    return v

"""
Frequencies of an example of a 3-gram model.
"""
def get_test_frequencies_vector_m():
    v = np.array([1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
    return v

"""
Frequencies of an example of a 3-gram model.
"""
def get_test_frequencies_vector_p():
    v = np.array([0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1])
    return v

"""
Frequencies of another example of a 3-gram model.
"""
def get_test_frequencies_vector_q():
    v = np.array([1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0])
    return v
