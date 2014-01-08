# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 13:30:45 2013

@author: Stefan Hillmann (stefan.hillmann@tu-berlin.de)
"""

import numpy as np
    
    
    
def computeProbability(num_unique_ngrams, num_ngrams, l, ngram_frequency):
    p = (ngram_frequency + l) / (num_ngrams + l * num_unique_ngrams)
    return p
    
def computeProbabilities(frequencies_array, l):
    num_unique_ngrams   = len(frequencies_array)
    num_ngrams          = np.sum(frequencies_array)
    
    probabilities_array = np.zeros(len(frequencies_array))
    unique_frequencies = np.unique(frequencies_array)
    
    for uf in unique_frequencies:
        uf_probability = computeProbability(num_unique_ngrams, num_ngrams, l, uf)
        probabilities_array[ np.where(frequencies_array == uf) ] = uf_probability
        
    return probabilities_array