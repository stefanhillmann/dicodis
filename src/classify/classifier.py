# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 15:05:29 2013

@author: Stefan Hillmann (stefan.hillmann@tu-berlin.de)
"""

import util.list as lu
from util import dict as du
import ngram.model_generator as mg
import logging
from measuring import measures



class Classifier:
    doc_model_file_name_counter = 1
    smoothing_value = 0 # use 0 as default value, which will not change a model
    
    def __init__(self, measure, classifier_name):
        self.logger = logging.getLogger('classifier.Classifier')
        self.logger.debug('Create new Classifier (%s) for with measure: %s', classifier_name, measure.__class__.__name__)
        
        self.classes = {}
        self.class_models = {}
        self.measure = measure
        self.name = classifier_name
        
    def setSmoothingValue(self, smoothing_value):
        self.smoothing_value = smoothing_value
    
    def addClass(self, class_name, n_grams, frequency_treshold):
        self.logger.debug('Add %s n-grams for class %s.', len(n_grams), class_name)
        
        self.classes[class_name] = n_grams
        
        # create class_model
        class_model = mg.createNgramModel( lu.uniqueValues(n_grams), n_grams )
        class_model = mg.remove_rare_n_grams(class_model, frequency_treshold)
        
        # compute probabilities and do NOT smooth the model
        class_model = self.prepareModel(class_model, False)
        # order model by keys
        class_model = du.sortByKey(class_model)
        
        # for debug and evaluation of the whole process one can 
        # export the  document model here:
        # export.toCSV(class_model, "/home/stefan/temp/csv/" + class_name + ".csv");
        
        self.class_models[class_name] = class_model
        
        
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
            
            
    
    def computeDistancies(self, doc_n_grams):
        class_distances = {}
        
        for key in self.classes:
            class_model = self.class_models[key]
            unique_class_n_grams = class_model.keys()
                       
            doc_model = mg.createNgramModel(unique_class_n_grams, doc_n_grams)
            doc_model = self.prepareModel(doc_model, True)
            
            #ordered_class_model = du.sortByKey(class_model)
            ordered_doc_model = du.sortByKey(doc_model)
            
            # for debug and evaluation of the whole process one can 
            # export the  document model here:
            # export.toCSV(ordered_doc_model, "/home/stefan/temp/csv/" + key + "_" + str(Classifier.doc_model_file_name_counter) + ".csv");
            # Classifier.doc_model_file_name_counter = Classifier.doc_model_file_name_counter + 1
                        
            distance = self.measure.distance( class_model.values(), ordered_doc_model.values() )
            self.logger.debug("computeDistancies(): Class = %s \t\t Distance: %s.", key, distance)
            
            class_distances[key] = distance
        # end for key
        return class_distances
        
    def prepareModel(self, model, smooth_model):
        if smooth_model:
            return mg.smoothModel(model, self.smoothing_value)
        else:
            mg.computeProbabilities(model)
            return model

"""
Data object used to return the result (class name and distance to class) of
classification.
"""
class ClassificationResult:
    def __init__(self, class_name, distance):
        self.class_name = class_name
        self.distance = distance




"""
Factory methods for Classifiers using different measurements
"""

def getCosineClassifier():
    return Classifier(measures.CosineMeasure(), "cosine")
    
def getKullbackLeiblerClassifier():
    return Classifier(measures.KullbackLeiblerMeasure(), "kullback_leibler")
    
def getMeanKullbackLeiblerClassifier():
    return Classifier(measures.MeanKullbackLeiblerMeasure(), "mean_kullback_leibler")
    
def getSymmetricKullbackLeiblerClassifier():
    return Classifier(measures.SymmetricKullbackLeiblerDistance(), "symmetric_kullback_leibler")
    
def getJensenClassifier():
    return Classifier(measures.JensenMeasure(), "jensen")

def getClassifier(classifier_name):
    created_classifier = "";
    
    if classifier_name == measures.MeasureName.COSINE:
        created_classifier = getCosineClassifier()
    elif classifier_name == measures.MeasureName.KULLBACK_LEIBLER:
        created_classifier = getKullbackLeiblerClassifier()
    elif classifier_name == measures.MeasureName.MEAN_KULLBACK_LEIBLER:
        created_classifier = getMeanKullbackLeiblerClassifier()
    elif classifier_name == measures.MeasureName.SYMMETRIC_KULLBACK_LEIBLER:
        created_classifier = getSymmetricKullbackLeiblerClassifier()
    elif classifier_name == measures.MeasureName.JENSEN:
        created_classifier = getJensenClassifier()
    else:
        """
        We return nothing, and the following code will crash, when trying to to do something
        with a not existing classifier 
        """
        print 'Unknown classifier was requested. Empty string will be returned'
        
    return created_classifier
     

