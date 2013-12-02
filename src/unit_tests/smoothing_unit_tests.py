# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 14:24:24 2013

@author: Stefan Hillmann (stefan.hillmann@tu-berlin.de)
"""

import numpy as np
import ngram.smoothing as smoothing

def testComputeProbabilityCase1():
    num_unique_ngrams   = 17
    num_ngrams          = 8
    l                   = 0.5
    ngram_frequency     = 0
    
    p = smoothing.computeProbability(num_unique_ngrams, num_ngrams, l, ngram_frequency)
    p = round(p, 4)
    print "testComputedProbabilityCase1: {}".format(p)
    assert p == 0.0303
    
def testComputeProbabilityCase2():
    num_unique_ngrams   = 17
    num_ngrams          = 9
    l                   = 0.5
    ngram_frequency     = 1
    
    p = smoothing.computeProbability(num_unique_ngrams, num_ngrams, l, ngram_frequency)
    p = round(p, 4)
    print "testComputedProbabilityCase2: {}".format(p)
    assert p == 0.0857
    
def testComputeProbabilityCase3():
    num_unique_ngrams   = 17
    num_ngrams          = 19
    l                   = 0.0
    ngram_frequency     = 2
    
    p = smoothing.computeProbability(num_unique_ngrams, num_ngrams, l, ngram_frequency)
    p = round(p, 4)
    print "testComputedProbabilityCase3: {}".format(p)
    assert p == 0.1053
    
def testComputeProbabilitiesCase1():
    a = 1./19.
    b = 2./19.    
    frequencies             = np.array([1,1,1,1,1,2,2,1,1,1,1,1,1,1,1,1,1])
    reference_probabilities = np.array([a,a,a,a,a,b,b,a,a,a,a,a,a,a,a,a,a], dtype=float)
    l = 0.0
    
    probabilities = smoothing.computeProbabilities(frequencies, l)
    print "testComputeProbabilitiesCase1: {}".format(probabilities)
    assert np.array_equal(reference_probabilities, probabilities)