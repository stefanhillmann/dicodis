# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 15:05:29 2013

@author: Stefan Hillmann (stefan.hillmann@tu-berlin.de)
"""

import logging

import common.util.list as lu
import common.ngram.model_generator as mg
from common.measuring import measures
import common.util.names as names


class Classifier:
    doc_model_file_name_counter = 1
    smoothing_value = 0  # use 0 as default value, which will not change a model
    
    def __init__(self, measure, classifier_name):
        self.logger = logging.getLogger('classifier.Classifier')
        self.logger.debug('Create new Classifier (%s) for with measure: %s', classifier_name, measure.__class__.__name__)
        
        self.classes = {}
        self.class_models = {}
        self.measure = measure
        self.name = classifier_name
        
    def set_smoothing_value(self, smoothing_value):
        self.smoothing_value = smoothing_value
    
    def add_class(self, class_name, n_grams, frequency_threshold):
        self.logger.debug('Add %s n-grams for class %s.', len(n_grams), class_name)
        
        self.classes[class_name] = n_grams
        
        # create class_model
        class_model = mg.generate_model(n_grams)  # create raw model
        class_model = mg.remove_rare_n_grams(class_model, frequency_threshold)  # remove rare n-grams

        # for debug and evaluation of the whole process one can 
        # export the  document model here:
        # export.toCSV(class_model, "/home/stefan/temp/csv/" + estimated_class + ".csv");
        
        self.class_models[class_name] = class_model
        
    def classify(self, document_n_grams):
        # compute distances between document an all classes in classifier
        positive_class_distance = self.compute_distances(document_n_grams, names.Class.POSITIVE)
        negative_class_distance = self.compute_distances(document_n_grams, names.Class.NEGATIVE)


        # find and return class (the 'best_class') with lowest distance (lowest_distance)
        best_class = ""
        if positive_class_distance < negative_class_distance:
            best_class = names.Class.POSITIVE
        else:
            best_class = names.Class.NEGATIVE

        return ClassificationResult(positive_class_distance, negative_class_distance, best_class)
            
    def compute_distances(self, doc_n_grams, class_name):
        class_model = self.class_models[class_name]
        document_model = mg.generate_model(doc_n_grams)

        class_distance = self.measure.distance(class_model, document_model, self.smoothing_value)

        return class_distance

"""
Data object used to return the result (class name and distance to class) of
classification.
"""
class ClassificationResult:
    def __init__(self, positive_class_distance, negative_class_distance, estimated_class):
        self.estimated_class = estimated_class
        self.negative_class_distance = negative_class_distance
        self.positive_class_distance = positive_class_distance

    def get_distance(self, class_name):
        assert class_name in names.valid_class_names()

        if class_name == names.Class.POSITIVE:
            return self.positive_class_distance
        else:
            return self.negative_class_distance

"""
Factory methods for Classifiers using different measurements
"""


def get_cosine_classifier():
    return Classifier(measures.CosineMeasure(), measures.MeasureName.COSINE)


def get_kullback_leibler_classifier():
    return Classifier(measures.KullbackLeiblerMeasure(), measures.MeasureName.KULLBACK_LEIBLER)


def get_mean_kullback_leibler_classifier():
    return Classifier(measures.MeanKullbackLeiblerMeasure(), measures.MeasureName.MEAN_KULLBACK_LEIBLER)


def get_symmetric_kullback_leibler_classifier():
    return Classifier(measures.SymmetricKullbackLeiblerDistance(), measures.MeasureName.SYMMETRIC_KULLBACK_LEIBLER)


def get_jensen_classifier():
    return Classifier(measures.JensenMeasure(), measures.MeasureName.JENSEN)


def get_rank_order_classifier():
    return Classifier(measures.RankOrderDistanceMeasure(), measures.MeasureName.RANK_ORDER)


def get_classifier(classifier_name):
    created_classifier = ""
    
    if classifier_name == measures.MeasureName.COSINE:
        created_classifier = get_cosine_classifier()
    elif classifier_name == measures.MeasureName.KULLBACK_LEIBLER:
        created_classifier = get_kullback_leibler_classifier()
    elif classifier_name == measures.MeasureName.MEAN_KULLBACK_LEIBLER:
        created_classifier = get_mean_kullback_leibler_classifier()
    elif classifier_name == measures.MeasureName.SYMMETRIC_KULLBACK_LEIBLER:
        created_classifier = get_symmetric_kullback_leibler_classifier()
    elif classifier_name == measures.MeasureName.JENSEN:
        created_classifier = get_jensen_classifier()
    elif classifier_name == measures.MeasureName.RANK_ORDER:
        created_classifier = get_rank_order_classifier()
    else:
        """
        We return nothing, and the following code will crash, when trying to to do something
        with a not existing classifier 
        """
        print 'Unknown classifier was requested. Empty string will be returned'
        
    return created_classifier
