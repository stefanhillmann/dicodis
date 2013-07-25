# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 17:19:42 2013

@author: Stefan Hillmann (stefan.hillmann@tu-berlin.de)
"""
import numpy as np
from math import log
from math import sqrt

def cosineSimilarity(p, q):
    """
    Computes the cosine similarity between the vectors p and q
    p and q can contain either frequencies or relative probabilities.
    """
    cs = np.dot(p, q) / ( sqrt( np.dot(p, p) * np.dot(q, q) ) )
    return cs


def kullbackLeiblerDivergence(p, q):
    """
    Computes the Kullback-Leibler divergence between vectors p and q.
    p and q must contain probabilities.
    """
    t = -q * log(p)
    s = -q * log(q)
    
    return np.sum(t - s)


def meanKullbackLeiblerDistance(p, q):
    """
    Comuptes the Mean Kullback-Leibler Divergence between vectors p and q.
    p and q must contain probabilities.
    """
    # compute KBL(p, q)
    kbl_p_q = kullbackLeiblerDivergence(p, q)
    
    # compute KBL(q, p)
    kbl_q_p = kullbackLeiblerDivergence(q, p)
    
    # compute mean of both divergencies
    mean_kbl = (kbl_p_q + kbl_q_p) / 2
    
    return mean_kbl
    
def symmetricKullbackLeiblerDistance(p, q):
    """
    Comuptes the Symmetric Kullback-Leibler Divergence between vectors p and q.
    Symmetric means that D(p||q) == D(q||p), but it is not just a mean value
    as the Mean Kullback-Leibler Divergence.
    p and q must contain probabilities.
    """
    v = (p - q) * log(p / q)
    
    return sum(v)


def jensenDistance(p, q):
    """
    Comuptes the Jensen Distance between vectors p and q.
    p and q must contain probabilities.
    """
    s = p * log(p)
    t = q + log(q)
    u = (p + q) / 2
    
    v = ((s + t) / 2) - (u * log(u))
    
    return sum(v)
    