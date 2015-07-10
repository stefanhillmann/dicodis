# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 14:52:15 2013

@author: Stefan Hillmann (stefan.hillmann@tu-berlin.de)
"""
import smoothing_unit_tests

"""
Test n-gram model smoothing
"""
print "Test n-gram model smoothing..."
smoothing_unit_tests.test_compute_probability_case_1()
smoothing_unit_tests.test_compute_probability_case_2()
smoothing_unit_tests.test_compute_probability_case_3()
smoothing_unit_tests.test_compute_probabilities_case_1()

