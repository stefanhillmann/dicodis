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
smoothing_unit_tests.testComputeProbabilityCase1()
smoothing_unit_tests.testComputeProbabilityCase2()
smoothing_unit_tests.testComputeProbabilityCase3()
smoothing_unit_tests.testComputeProbabilitiesCase1()

"""
Test measures with equal data. Each measure has to detect equality.
"""
print "Test measures with equal data..."
measures_unit_tests.testCosineSimilarityCase1()
measures_unit_tests.testKullbackLeiblerCase1()
measures_unit_tests.testMeanKullbackLeiblerDistanceCase1()
measures_unit_tests.testSymmetricKullbackLeiblerDistanceCase1()
measures_unit_tests.testJensenDistanceCase1()
