# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 11:56:52 2013

@author: Stefan Hillmann (stefan.hillmann@tu-berlin.de)
"""
import logging
from collections import Counter

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
    pads = []
    for i in range(1, n):
        pads.append('_')
        
    return pads
        
        
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
    
def smoothModel(model):
    for key in model:
        model[key] = model[key] + 0.5
        
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