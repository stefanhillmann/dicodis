# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 14:34:56 2013

@author: Stefan Hillmann (stefan.hillmann@tu-berlin.de)
"""

import logging

import common.util.list as lu
import common.ngram.model_generator as mg
import common.classify.classifier as classifier
from common.util.names import Class
import common.analyse.roc as roc




class CrossValidator:
    """Constructs a new CrossValidator.
    
    Keyword arguments:
    classifier_name -- Name of the classifier to be used. The related classifier is the one that will be tested.
    Please see and use classifier.ClassifierNames for valid names.
    n_gram_size -- Size of the n-grams to be used by the classifier. See and use ngram.NGramSize for valid values. 
        
    """
    def __init__(self, classifier_name, n_gram_size, frequency_threshold, smoothing_value):
        self.logger = logging.getLogger('cross_validation.CrossValidator')

        self.classifier_name        = classifier_name
        self.n_gram_size            = n_gram_size
        self.frequency_threshold    = frequency_threshold
        self.smoothing_value        = smoothing_value

        """
        Dictionary which holds for each class (by class name) a list of related documents.
        """
        self.documents = []

    def add_documents(self, documents):
        self.documents.extend(documents)

    def run_cross_validation(self):
        self.logger.info('Run cross validation for: classifier = %s, n = %s, threshold = %s.', self.classifier_name, self.n_gram_size, self.frequency_threshold)
        """
        Iterate over the documents and select the i-th one for classifying.
        The remaining are used for training. 
        """
        test_results = []
        self.logger.info("Run cross validation for %s documents (dialogs).", len(self.documents))
        for i in range( len(self.documents) ):
            """
            Select documents for training and the document for testing the classifier_name
            """
            documents_before_i = self.documents[:i]    # all documents _before_ that one on position i
            documents_behind_i = self.documents[i + 1:]  # all documents _behind_ that one on position i
            training_documents = []
            training_documents.extend(documents_before_i)
            training_documents.extend(documents_behind_i)
            test_document = self.documents[i]

            """
            Create (train) the classifier_name and test it with the document
            """
            test_classifier = classifier.get_classifier(self.classifier_name)
            test_classifier.set_smoothing_value(self.smoothing_value)
            fold_validator = FoldValidator(training_documents, [test_document], test_classifier,
                                           self.n_gram_size, self.frequency_threshold, self.smoothing_value)
            test_results.extend( fold_validator.test_classifier() )

        return test_results


class FoldValidator:

    def __init__(self, training_set, test_set, classifier, n, frequency_threshold, smoothing_value):
        self.logger = logging.getLogger('cross_validation.FoldValidator')

        self.classifier         = classifier
        self.test_set           = test_set
        self.n                  = n
        self.smoothing_value    = smoothing_value
        self.test_results       = []

        self.train_classifier(training_set, n, frequency_threshold)

    """
    Trains the classifier with the training_set
    
    Parameters:
    training_set: List of dialogs.Document    
    """
    def train_classifier(self, training_set, n, frequency_threshold):
        self.logger.info("trainClassifier starts")

        # get the unique class identifiers
        classes = lu.unique_object_values(training_set, 'true_class')

        # train each class with its documents
        for class_name in classes:
            class_documents = lu.filter_by_field_value(training_set, 'true_class', class_name)

            self.logger.info('Train class %s in classifier %s with %s documents', class_name, self.classifier.name, len(class_documents))

            # ... create the n-grams for training
            # class_n_grams = mg.create_n_grams_from_document_list(class_documents, n)
            class_n_grams = mg.get_n_grams_from_database_for_documents(class_documents, n)
            self.classifier.add_class(class_name, class_n_grams, frequency_threshold)

    def test_classifier(self):
        """
        Classify each document in test_set and returns the single results.
        """
        self.logger.debug('Test classifier %s by classifying %s dialogs.', self.classifier.name, len(self.test_set))
        for document in self.test_set:
            n_grams = mg.get_n_grams_from_database_for_single_document(document, self.n)

            classification_result = self.classifier.classify(n_grams)
            self.logger.debug("testClassifier(): Calculated class = %s - Actual class: %s.",
                              classification_result.estimated_class, document.true_class)

            result = SingleTestResult(document, self.classifier.name, classification_result, self.n)
            self.test_results.append(result)

        return self.test_results

"""
Data transfer object for a single trial when testing a classifier_name in frame of
a fold based cross validation.
"""
class SingleTestResult:

    def __init__(self, document, classifier_name, classification_result, n_gram_size):
        self.document                = document
        self.classifier_name         = classifier_name
        self.true_class              = document.true_class
        self.classification_result   = classification_result
        self.n_gram_size             = n_gram_size

class SummarizedTestResults:
    def __init__(self, true_positive, false_positive, true_negative, false_negative,
                 classifier_name, n_gram_size, criteria, frequency_threshold, smoothing_value):
        self.true_positive      = true_positive
        self.false_positive     = false_positive
        self.true_negative      = true_negative
        self.false_negative     = false_negative
        self.classifier_name    = classifier_name
        self.n_gram_size        = n_gram_size
        self.criteria           = criteria
        self.frequency_threshold = frequency_threshold
        self.smoothing_value    = smoothing_value

    def __repr__(self):
        return 'Classifier = {}    n = {}\nTP = {}  FP = {}    TN = {}  FN = {}'\
            .format(self.classifier_name, self.n_gram_size,
                    self.true_positive, self.false_positive, self.true_negative, self.false_negative)
"""
TODO
"""
class ResultAssessor:
    def __init__(self, cross_validation_results, positive_class, negative_class,
                 classifier_name, n_gram_size, frequency_threshold, criteria, smoothing_value):
        self.logger = logging.getLogger("analyse.cross_validation.ResultAssessor")
        self.logger.debug( ("Initialize ResultAssor with %s single results.", len(cross_validation_results)) )

        self.data               = cross_validation_results
        self.positive_class     = positive_class
        self.negative_class     = negative_class

        self.criteria               = criteria
        self.classifier_name        = classifier_name
        self.n_gram_size            = n_gram_size
        self.frequency_threshold    = frequency_threshold
        self.smoothing_value        = smoothing_value

        self.counter_true_positive  = 0.0
        self.counter_false_positive = 0.0
        self.counter_true_negative  = 0.0
        self.counter_false_negative = 0.0

    def count_results(self):
        """ reset the true/false positive/negative counter to zero """
        self.counter_true_positive  = 0.0
        self.counter_false_positive = 0.0
        self.counter_true_negative  = 0.0
        self.counter_false_negative = 0.0

        for result in self.data:
            cr = result.classification_result

            # POSITIVE
            if cr.estimated_class == Class.POSITIVE:
                # TRUE
                if result.true_class == Class.POSITIVE:
                    self.counter_true_positive += 1
                # FALSE
                else:
                    self.counter_false_positive += 1

            # NEGATIVE
            if cr.estimated_class == Class.NEGATIVE:
                # TRUE
                if result.true_class == Class.NEGATIVE:
                    self.counter_true_negative += 1
                # FALSE
                else:
                    self.counter_false_negative += 1

    def getResultAnalysis(self):
        self.count_results()
        return SummarizedTestResults(self.counter_true_positive, self.counter_false_positive,
                                     self.counter_true_negative, self.counter_false_negative,
                                     self.classifier_name, self.n_gram_size, self.criteria,
                                     self.frequency_threshold, self.smoothing_value)

    def get_tpr_and_fpr_for_roc(self):

        # collect input values for true/false positive rate calculation
        # classification_results = []
        positives = 0
        negatives = 0
        for result in self.data:
            # classification_results.append(result.classification_result)  # collect classification results
            # count number of positive and negative documents
            if result.document.true_class == Class.POSITIVE:
                positives += 1
            else:
                negatives += 1

        sorted_results = self.sort_results_by_positive_class_distance(self.data)

        fp = 0  # counter for false positives
        tp = 0  # counter for true positives

        f_prev = float("inf")

        # start calculation
        roc_points = []
        for result in sorted_results:
            f = result.classification_result.positive_class_distance
            if f != f_prev:
                roc_points.append((fp / negatives, tp / positives))
                f_prev = f

            if result.true_class == Class.POSITIVE:
                tp += 1
            else:
                fp += 1

        roc_points.append((fp / negatives, tp / positives))  # this is (1, 1)

        return roc_points

    def get_roc_points(self):

        # collect input data for roc points calculation
        ids = list()
        probabilities = dict()
        true_classes = dict()

        for result in self.data:
            id = result.document.dialog_id
            ids.append(id)
            probabilities[id] = result.classification_result.positive_class_distance
            true_classes[id] = result.true_class

        roc_points = roc.get_roc_points(ids, probabilities, true_classes, Class.POSITIVE, Class.NEGATIVE)
        return roc_points


    def sort_results_by_positive_class_distance(self, results):
        return sorted(results, key=lambda x: x.classification_result.positive_class_distance)




"""
Creates from a list of assessor results (results of different classifier) a table like structure
for further processing (e.g. plotting).

Classifier n TP FP TN FN
"""
def create_result_table(assessor_results, separator):
    rows = []
    # create header
    header = separator.join( ['Criteria', 'Classifier', 'n', 'l', 'Freq. Threshold', 'TP', 'FP', 'TN', 'FN', 'Recall', 'Precision', 'F-Measure'] )
    rows.append(header)

    # create one row per assessor result
    for values in assessor_results:
        recall = compute_recall(values.true_positive, values.false_negative)
        precision = compute_precision(values.true_positive, values.false_positive)
        f_measure = compute_f_measure(values.true_positive, values.false_positive, values.false_negative)

        row_values = [values.criteria, values.classifier_name, values.n_gram_size, values.smoothing_value,
                      values.frequency_threshold, values.true_positive, values.false_positive,
                      values.true_negative, values.false_negative, recall, precision, f_measure]
        row = separator.join( str(value) for value in row_values)
        rows.append(row)

    return rows


def write_result_table_to_file(assessor_results, separator, file_path):
    data = create_result_table(assessor_results, separator)

    f = open(file_path, 'w')
    for line in data:
        f.write("".join( [line, "\n"] ))

    f.close()


def compute_f_measure(true_positive, false_positive, false_negative):
    f = 0
    if true_positive != 0.0:
        f = float((2 * true_positive)) / ( (2 * true_positive) + false_positive + false_negative)
    return f


def compute_precision(true_positive, false_positive):
    p = 0
    if true_positive != 0.0:
        p = float(true_positive) / ( true_positive + false_positive )
    return p


def compute_recall(true_positive, false_negative):
    r = 0
    if true_positive != 0.0:
        r = float(true_positive) / ( true_positive + false_negative )
    return r


