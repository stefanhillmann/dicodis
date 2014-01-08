# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 11:56:52 2013

@author: Stefan Hillmann (stefan.hillmann@tu-berlin.de)
"""
import logging
from collections import Counter
from ngram import smoothing
from collections import OrderedDict

module_logger = logging.getLogger('ngram')

def create_ngrams(documents, n):
    ngrams = []    
    pads = createPads(n)
    
    for document in documents:
        padded_doc = addPads(document, pads)
        
        for idxTerm in xrange(len(padded_doc) - (n-1)):
            i = idxTerm
            j = idxTerm + n
            
            ngram_parts = []
            
            for k in xrange (i, j):
                ngram_parts.append(padded_doc[k])
                
            ngram = '#'.join(ngram_parts)
            ngrams.append(ngram)
            
    
    module_logger.debug('Calculated %s %s-grams from %s documents.', len(ngrams), n, len(documents))
    return ngrams
    
def createPads(n):
    
    pads = {
            NGramSize.ONE   : '',
            NGramSize.TWO   : '_',
            NGramSize.THREE : '__',
            NGramSize.FOUR  : '___',
            NGramSize.FIVE  : '____',
            NGramSize.SIX   : '_____',
            NGramSize.SEVEN : '______',
            NGramSize.EIGHT : '_______',
    }
      
    return pads[n]
        
        
def addPads(document, pads):
    padded_document = []
    padded_document.extend(pads)
    padded_document.extend(document)
    padded_document.extend(pads)
    
    return padded_document
    
def createNgramModel(unique_n_grams, n_grams):
    n_gram_model = {} 
    n_grams_counter = Counter(n_grams)
    
    for n_gram in unique_n_grams:
    #for n_gram in n_grams_counter.keys():
        n_gram_model[n_gram] = float( n_grams_counter[n_gram] )
        
    return n_gram_model

def remove_rare_n_grams(model, treshold):
    new_model = {}
        
    for key in model.keys():
        if model[key] >= treshold:
            new_model[key] = model[key]
    return new_model
    
def smoothModel(model, l):
    module_logger.debug("Smooth model with l = %s.", l)
    """
    Smoothes a n-gram model using the value l as 'add'.
    
    Parameters
    ----------
    model : dictionary
        an n-gram model with absolute frequencies
    l : float
        the value to be added
    
    Returns
    -------
    dictionary : a model with smoothed values for n-gram probabilities.  
    """
    # get the frequencies as array
    absolute_values = model.values()
    
    # compute relative probabilities and smooth them with value l
    smoothed_values = smoothing.computeProbabilities(absolute_values, l)
    
    # create new dictionary with with n-grams and the smoothed values
    n_grams = model.keys()
    smoothed_model = OrderedDict()
    for i in xrange( len(smoothed_values) ):
        n_gram = n_grams[i]
        probability = smoothed_values[i]
        smoothed_model[n_gram] = probability
    
    return smoothed_model
        
def computeProbabilities(model):
    sum_of_frequencies = sum(model.values())
    for key in model:
        model[key] = model[key] / sum_of_frequencies
        
class NGramSize:
    ONE     = 1
    TWO     = 2
    THREE   = 3
    FOUR    = 4
    FIVE    = 5
    SIX     = 6
    SEVEN   = 7
    EIGHT   = 8