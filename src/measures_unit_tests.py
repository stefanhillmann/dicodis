# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 15:17:13 2013

@author: Stefan Hillmann (stefan.hillmann@tu-berlin.de)
"""

import measures
import numpy as np
import smoothing


def testCosineSimilarityCase1():
    p = getTestProbabilitiesVector(0.0)
    q = p
    cosine_distance = 1 - measures.cosineSimilarity(p, q)
    print "testCosineSimilarityCase1: {}".format(cosine_distance)
    assert cosine_distance == 0.0
    print "Passed."
    
def testKullbackLeiblerCase1():
    p = getTestProbabilitiesVector(0.0)
    q = p
    kl_distance = measures.kullbackLeiblerDivergence(p, q)
    print "testKullbackLeiblerCase1: {}".format(kl_distance)
    assert kl_distance == 0.0
     print "Passed."
    

def getTestProbabilitiesVector(l):
    v = getTestFrequenciesVector()
    p = smoothing.computeProbabilities(v, l)
    return p
    

def getTestFrequenciesVector():
    v = np.array([3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
    return v
    