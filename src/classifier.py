# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 15:05:29 2013

@author: Stefan Hillmann (stefan.hillmann@tu-berlin.de)
"""

import measures
import util.list as lu
import ngram

class Classifier:
    
    def __init__(self, measure, classifier_name):
        self.classes = {}
        self.measure = measure
        self.name = classifier_name
    
    def addClass(self, class_name, n_grams):
        self.classes[class_name] = n_grams
        
    def classify(self, document_n_grams):
        # compute distances for all classes in classifier
        all_distancies = self.computeDistancies(document_n_grams)
        
        # find and return class (the 'best_class') with lowest distance (lowest_distance)
        best_class = ""
        lowest_distance = float('inf') # each distance will be lower than infinity...
        for class_name in all_distancies:
            distance = all_distancies[class_name]
            
            if distance < lowest_distance:
                best_class = class_name
                lowest_distance = distance
                
        return ClassificationResult(best_class, lowest_distance)
            
            
    
    def computeDistancies(self, n_grams):
        class_distances = {}
        
        for key in self.classes:
            class_n_grams = self.classes[key]
            all_n_grams = []
            all_n_grams.extend(n_grams)
            all_n_grams.extend(class_n_grams)
            all_unique = lu.uniqueValues(all_n_grams)
            
            n_grams_model = ngram.createNgramModel(all_unique, n_grams)
            self.prepareModel(n_grams_model)
            
            class_model = ngram.createNgramModel(all_unique, class_n_grams)
            self.prepareModel(class_model)
                        
            distance = self.measure.distance(
            class_model.values(), n_grams_model.values())
            
            class_distances[key] = distance
        # end for key
        return class_distances
        
    def prepareModel(self, model):
        ngram.smoothModel(model)
        ngram.computeProbabilities(model)

"""
Data object used to return the result (class name and distance to class) of
classification.
"""
class ClassificationResult:
    def __init__(self, class_name, distance):
        self.class_name = class_name
        self.distance = distance


"""
Measure implementations
"""
    
class CosineMeasure:
    def distance(self, p, q):
        similarity = measures.cosineSimilarity(p, q)
        
        """
        In order to get the distance we subtract the similartiy from 1.
        That works because the similarity is always between 1 and 0.
        We do that to follow the behavoiur of the other distance measure:
        The hihger the distance, the hihger the difference between p and q.
        """
        return 1 - similarity
        
class KullbackLeiblerMeasure:
    def distance(self, p, q):
        divergence = measures.kullbackLeiblerDivergence(p, q)
        return divergence
        
class MeanKullbackLeiblerMeasure:
    def distance(self, p, q):
        distance = measures.meanKullbackLeiblerDistance(p, q)
        return distance
        
class SymmetricKullbackLeiblerDistance:
    def distance(self, p, q):
        distance = measures.symmetricKullbackLeiblerDistance(p, q)
        return distance
        
class JensenMeasure:
    def distance(self, p, q):
        distance = measures.jensenDistance(p, q)
        return distance


"""
Factory methods for Classifiers using different measurements
"""

def getCosineClassifier():
    return Classifier(CosineMeasure(), "cosine")
    
def getKullbackLeiblerClassifier():
    return Classifier(KullbackLeiblerMeasure(), "kullback_leibler")
    
def getMeanKullbackLeiblerClassifier():
    return Classifier(MeanKullbackLeiblerMeasure(), "mean_kullback_leibler")
    
def getSymmetricKullbackLeiblerClassifier():
    return Classifier(SymmetricKullbackLeiblerDistance(), "symmetric_kullback_leibler")
    
def getJensenClassifier():
    return Classifier(JensenMeasure(), "jensen")

