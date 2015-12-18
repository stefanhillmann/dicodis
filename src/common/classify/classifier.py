# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 15:05:29 2013

@author: Stefan Hillmann (stefan.hillmann@tu-berlin.de)
"""

import logging

import common.ngram.model_generator as mg
import common.util.names as names
from common.measuring import measures


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
        class_model.remove_rare_n_grams(frequency_threshold)  # remove rare n-grams

        # for debug and evaluation of the whole process one can 
        # export the  document model here:
        # export.toCSV(class_model, "/home/stefan/temp/csv/" + estimated_class + ".csv");
        
        self.class_models[class_name] = class_model
        
    def classify(self, document_n_grams):
        # compute distances between document an all classes in classifier
        # TODO: remove timing
        # start_pos = time.time()
        positive_class_distance = self.compute_distances(document_n_grams, names.Class.POSITIVE)
        # end_pos = time.time()
        # start_neg = time.time()
        negative_class_distance = self.compute_distances(document_n_grams, names.Class.NEGATIVE)
        # end_neg = time.time()

        # print("Compute pos distance lasts {0} second".format(end_pos - start_pos))
        # print("Compute neg distance lasts {0} second".format(end_neg - start_neg))


        # find and return class (the 'best_class') with lowest distance (lowest_distance)
        best_class = ""
        if positive_class_distance < negative_class_distance:
            best_class = names.Class.POSITIVE
        else:
            best_class = names.Class.NEGATIVE

        return ClassificationResult(positive_class_distance, negative_class_distance, best_class)
            
    def compute_distances(self, doc_n_grams, class_name):
        class_model = self.class_models[class_name]

        # TODO: remove timing
        # start_doc_model = time.time()
        document_model = mg.generate_model(doc_n_grams)
        # end_doc_model = time.time()
        # print("Doc model creation lasts {0} seconds".format(end_doc_model - start_doc_model))

        # start_distance = time.time()
        class_distance = self.measure.distance(class_model, document_model, self.smoothing_value)
        # end_distance = time.time()
        # print("Distance computation lasts {0} seconds.".format(end_distance - start_distance))

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


def get_normalized_rank_order_classifier():
    return Classifier(measures.NormalizedRankOrderDistanceMeasure(), measures.MeasureName.NORMALIZED_RANK_ORDER)


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
    elif classifier_name == measures.MeasureName.NORMALIZED_RANK_ORDER:
        created_classifier = get_normalized_rank_order_classifier()
    else:
        """
        We return nothing, and the following code will crash, when trying to to do something
        with a not existing classifier 
        """
        raise ValueError("Unknown classifier '{0} was requested.".format(classifier_name))
        
    return created_classifier
