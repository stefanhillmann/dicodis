# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 15:17:13 2013

@author: Stefan Hillmann (stefan.hillmann@tu-berlin.de)
"""

from classify import measures
import numpy as np
from ngram import smoothing

"""
Comparing equal models.
-----------------------
"""
"""
Testing Cosine distance with equal models.
"""
def testCosineSimilarityCase1():
    p = getTestProbabilitiesVectorR(0.0)
    q = p
    cosine_distance = 1 - measures.cosineSimilarity(p, q)
    print "testCosineSimilarityCase1: {}".format(cosine_distance)
    assert cosine_distance == 0.0
    print "Passed."
    
"""
Testing Kullback-Leibler distance with equal models.
"""
def testKullbackLeiblerCase1():
    p = getTestProbabilitiesVectorR(0.0)
    q = p
    kl_distance = measures.kullbackLeiblerDivergence(p, q)
    print "testKullbackLeiblerDivergenceCase1: {}".format(kl_distance)
    assert kl_distance == 0.0
    print "Passed."
  
"""
Testing mean Kullback-Leibler distance with equal models.
"""
def testMeanKullbackLeiblerDistanceCase1():
    p = getTestProbabilitiesVectorR(0.0)
    q = p
    mkl_distance = measures.meanKullbackLeiblerDistance(p, q)
    print "testMeanKullbackLeiblerDistanceCase1: {}".format(mkl_distance)
    assert mkl_distance == 0.0
    print "Passed."
     
"""
Testing symmetric Kullback-Leibler distance with equal models.
"""   
def testSymmetricKullbackLeiblerDistanceCase1():
    p = getTestProbabilitiesVectorR(0.0)
    q = p
    skl_distance = measures.symmetricKullbackLeiblerDistance(p, q)
    print "testSymmetricKullbackLeiblerDistanceCase1: {}".format(skl_distance)
    assert skl_distance == 0.0
    print "Passed."
    
"""
Testing Jensen difference divergence with equal models.
"""
def testJensenDistanceCase1():
    p = getTestProbabilitiesVectorR(0.0)
    q = p
    jensen_distance = measures.jensenDistance(p, q)
    print "testJensenDistanceCase1: {}".format(jensen_distance)
    assert jensen_distance == 0.0
    print "Passed."

"""
Comparing different models.
-----------------------
"""

"""
Testing Cosine distance with different models.
"""
def testCosineSimilarityCase2():
    m = getTestProbabilitiesVectorM(0.0)
    p = getTestProbabilitiesVectorQ(0.5)
    cosine_distance = 1 - measures.cosineSimilarity(m, p)
    print "testCosineSimilarityCase2: {}".format(cosine_distance)
    assert round(cosine_distance, 3) == 0.096
    print "Passed."
    
"""
Testing Kullback-Leibler distance with different models.
"""
def testKullbackLeiblerCase2():
    m = getTestProbabilitiesVectorM(0.0)
    p = getTestProbabilitiesVectorQ(0.5)
    kl_distance = measures.kullbackLeiblerDivergence(p, m)
    print "testKullbackLeiblerDivergenceCase1: {}".format(kl_distance)
    assert round(kl_distance, 4) == 0.1198
    print "Passed."
  
"""
Testing mean Kullback-Leibler distance with different models.
"""
def testMeanKullbackLeiblerDistanceCase2():
    m = getTestProbabilitiesVectorM(0.0)
    p = getTestProbabilitiesVectorQ(0.5)
    mkl_distance = measures.meanKullbackLeiblerDistance(p, m)
    print "testMeanKullbackLeiblerDistanceCase1: {}".format(mkl_distance)
    assert round(mkl_distance, 4) == 0.1203 
    print "Passed."
     
"""
Testing symmetric Kullback-Leibler distance with different models.
"""   
def testSymmetricKullbackLeiblerDistanceCase2():
    m = getTestProbabilitiesVectorM(0.0)
    p = getTestProbabilitiesVectorQ(0.5)
    skl_distance = measures.symmetricKullbackLeiblerDistance(p, m)
    print "testSymmetricKullbackLeiblerDistanceCase1: {}".format(skl_distance)
    assert round(skl_distance, 4) == 0.2407
    print "Passed."
    
"""
Testing Jensen difference divergence with different models.
"""
def testJensenDistanceCase2():
    m = getTestProbabilitiesVectorM(0.0)
    p = getTestProbabilitiesVectorQ(0.5)
    jensen_distance = measures.jensenDistance(p, m)
    print "testJensenDistanceCase1: {}".format(jensen_distance)
    assert round(jensen_distance, 4) == 0.0297
    print "Passed."



"""
Creating test data.
-------------------
"""
def getTestProbabilitiesVectorR(l):
    v = getTestFrequenciesVectorR()
    p = smoothing.computeProbabilities(v, l)
    return p

def getTestProbabilitiesVectorM(l):
    v = getTestFrequenciesVectorM()
    m = smoothing.computeProbabilities(v, l)
    return m

def getTestProbabilitiesVectorP(l):
    v = getTestFrequenciesVectorP()
    p = smoothing.computeProbabilities(v, l)
    return p
    
def getTestProbabilitiesVectorQ(l):
    v = getTestFrequenciesVectorQ()
    q = smoothing.computeProbabilities(v, l)
    return q
    
"""
Frequencies from participants 44 1-grammodel
"""
def getTestFrequenciesVectorR():
    v = np.array([3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
    return v

"""
Frequencies of an example of a 3-gram model.
"""    
def getTestFrequenciesVectorM():
    v = np.array([1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
    return v

"""
Frequencies of an example of a 3-gram model.
"""    
def getTestFrequenciesVectorP():
    v = np.array([0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1])
    return v

"""
Frequencies of another example of a 3-gram model.
"""    
def getTestFrequenciesVectorQ():
    v = np.array([1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0])
    return v


    