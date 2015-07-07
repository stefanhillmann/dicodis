# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 14:52:15 2013

@author: Stefan Hillmann (stefan.hillmann@tu-berlin.de)
"""
import measures_unit_tests
import smoothing_unit_tests

"""
Test n-gram model smoothing
"""
print "Test n-gram model smoothing..."
smoothing_unit_tests.test_compute_probability_case_1()
smoothing_unit_tests.test_compute_probability_case_2()
smoothing_unit_tests.test_compute_probability_case_3()
smoothing_unit_tests.test_compute_probabilities_case_1()

"""
Test measures with equal data. Each measure has to detect equality.
"""
print "Test measures with equal data..."
measures_unit_tests.test_cosine_similarity_case_1()
measures_unit_tests.test_kullback_leibler_case_1()
measures_unit_tests.test_mean_kullback_leibler_distance_case_1()
measures_unit_tests.test_symmetric_kullback_leibler_distance_case_1()
measures_unit_tests.test_jensen_distance_case_1()

"""
Test measures with different models. Each measure has to detect the correct distance.
"""
print "Test measures with different data..."
measures_unit_tests.test_cosine_similarity_case_2()
measures_unit_tests.test_kullback_leibler_case_2()
measures_unit_tests.test_mean_kullback_leibler_distance_case_2()
measures_unit_tests.test_symmetric_kullback_leibler_distance_case_2()
measures_unit_tests.test_jensen_distance_case_2()
