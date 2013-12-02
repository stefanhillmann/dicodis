# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 14:34:56 2013

@author: Stefan Hillmann (stefan.hillmann@tu-berlin.de)
"""

import util.list as lu
import ngram.model_generator as mg
import classify.classifier as classifier
import logging

class CrossValidator:
    """Constructs a new CrossValidator.
    
    Keyword arguments:
    classifier_name -- Name of the classifier to be used. The related classifier is the one that will be tested.
    Please see and use classifier.ClassifierNames for valid names.
    n_gram_size -- Size of the n-grams to be used by the classifier. See and use ngram.NGramSize for valid values. 
        
    """
    def __init__(self, classifier_name, n_gram_size, frequency_threshold):
        self.logger = logging.getLogger('cross_validation.CrossValidator')
        
        self.classifier_name    = classifier_name
        self.n_gram_size        = n_gram_size
        self.frequency_threshold = frequency_threshold
        
        """
        Dictionary which holds for each class (by class name) a list of related documents.
        """
        self.documents = []
        
    def addDocuments(self, documents):
        self.documents.extend(documents)
        
    def runCrossValidation(self):
        self.logger.info('Run cross validation for: classifier = %s, n = %s, threshold = %s.', self.classifier_name, self.n_gram_size, self.frequency_threshold)
        """
        Iterate over the documents and select the i-th one for classifying.
        The remaining are used for training. 
        """
        test_results = []
        for i in range( len(self.documents) ):
            """
            Select documents for training and the document for testing the classifier_name
            """
            documents_before_i = self.documents[:i] # all documents before that one on position i
            documents_behind_i = self.documents[i+1:] # all documents behind that one on position i
            training_documents = []
            training_documents.extend(documents_before_i)
            training_documents.extend(documents_behind_i)
            test_document = self.documents[i]
            
            """
            Create (train) the classifier_name and test it with the document
            """
            test_classifier = classifier.getClassifier(self.classifier_name)
            fold_validator = FoldValidator(training_documents, [test_document], test_classifier, self.n_gram_size, self.frequency_threshold)
            test_results.extend(fold_validator.testClassifier())
            
        return test_results
            
             
class FoldValidator:
    
    def __init__(self, training_set, test_set, classifier, n, frequency_threshold):
        self.logger = logging.getLogger('cross_validation.FoldValidator')
        
        self.classifier = classifier
        self.test_set = test_set
        self.n = n
        self.test_results = []
        
        self.trainClassifier(training_set, n, frequency_threshold)
        
    
    """
    Trains the classifier with the training_set
    
    Parameters:
    training_set: List of dialogs.Document    
    """    
    def trainClassifier(self, training_set, n, frequency_threshold):
        # get the unique class identifiers
        classes = lu.uniqueObjectValues(training_set, 'label')

        # train each class with its documents
        for class_name in classes:
            class_documents = lu.filterByFieldValue(training_set, 'label', class_name)
            
            self.logger.debug('Train class %s in classifier %s with %s documents', class_name, self.classifier.name, len(class_documents))
            
            # collect content of all documents (of the current class, and ...)
            document_contents = []            
            for document in class_documents:
                document_contents.append(document.content)
            
            # ... create the n-grams for training
            class_n_grams = mg.create_ngrams(document_contents, n)
            self.classifier.addClass(class_name, class_n_grams, frequency_threshold)
            
    
    
    
    def testClassifier(self):
        """
        Classify each document in test_set and returns the single results.
        """
        self.logger.debug('Test classifier %s by classifying %s dialogs.', self.classifier.name, len(self.test_set))
        for document in self.test_set:
            class_n_grams = mg.create_ngrams([document.content], self.n)
            
            classification_result = self.classifier.classify(class_n_grams)
            self.logger.debug("testClassifier(): Calculated class = %s - Actual class: %s.", classification_result.class_name, document.label)
            
            result = SingleTestResult(document, self.classifier.name, classification_result, self.n)
            self.test_results.append(result)
        
        return self.test_results

"""
Data transfer object for a single trial when testing a classifier_name in frame of
a fold based cross validation.
"""        
class SingleTestResult:
    def __init__(self, document, classifier_name, classification_result, n_gram_size):
        self.document               = document
        self.classifier_name        = classifier_name
        self.actual_class           = document.label
        self.calculated_class       = classification_result.class_name
        self.calculated_distance    = classification_result.distance
        self.n_gram_size            = n_gram_size
        
    def __repr__(self):
        return 'Classifier: {}, Calculated class: {}, Actual class: {}, Distance: {}, n-Gram size: {}'.format(self.classifier_name, 
                  self.calculated_class, self.actual_class, self.calculated_distance, self.n_gram_size)

class SummarizedTestResults:
    def __init__(self, true_positive, false_positive, true_negative, false_negative, classifier_name, n_gram_size, criteria, frequency_threshold):
        self.true_positive      = true_positive
        self.false_positive     = false_positive
        self.true_negative      = true_negative
        self.false_negative     = false_negative
        self.classifier_name    = classifier_name
        self.n_gram_size        = n_gram_size
        self.criteria           = criteria
        self.frequency_threshold = frequency_threshold
        
    def __repr__(self):
        return 'Classifier = {}    n = {}\nTP = {}  FP = {}    TN = {}  FN = {}'\
            .format(self.classifier_name, self.n_gram_size,
                    self.true_positive, self.false_positive, self.true_negative, self.false_negative)
"""
TODO
"""
class ResultAssessor:
    def __init__(self, cross_validation_results, positive_class, negative_class, classifier_name, n_gram_size, frequency_threshold, criteria):
        self.logger = logging.getLogger("analyse.cross_validation.ResultAssessor")
        self.logger.debug( ("Initialize ResultAssor with %s single results.", len(cross_validation_results)) )
        
        self.data               = cross_validation_results
        self.positive_class     = positive_class
        self.negative_class     = negative_class
        
        self.criteria           = criteria
        self.classifier_name    = classifier_name
        self.n_gram_size        = n_gram_size
        self.frequency_threshold = frequency_threshold
        
        self.resetCounter()

    def resetCounter(self):
        self.counter_true_positive  = 0.0
        self.counter_false_positive = 0.0
        self.counter_true_negative  = 0.0
        self.counter_false_negative = 0.0
    
    
    def countResults(self):
        """ reset the true/false positive/negative counter to zero """
        for result in self.data:
            
            """
            If actual class and calculated class are equal, it is a TRUE
            result. We have just to decide if TRUE POSITVIE or TRUE NEGATIVE 
            """
            if result.calculated_class == result.actual_class:
                if result.actual_class == self.positive_class:
                    # TRUE POSITIVE 
                    self.counter_true_positive += 1
                else:
                    # TRUE negative
                    self.counter_true_negative += 1
                    
            """
            If actual class and calculated class are NOT equal, it is a FALSE
            result. We have just to decide if FALSE POSITVIE or FALSE NEGATIVE 
            """
            if result.calculated_class != result.actual_class:
                if result.calculated_class == self.positive_class:
                    # FALSE POSITIVE
                    self.counter_false_positive += 1
                else:
                    # FALSE NEGATIVE
                    self.counter_false_negative += 1

    def getResultAnalysis(self):
        self.countResults()
        
        return SummarizedTestResults(self.counter_true_positive, self.counter_false_positive, 
                                     self.counter_true_negative, self.counter_false_negative,
                                     self.classifier_name, self.n_gram_size, self.criteria,
                                     self.frequency_threshold)
"""
Creates from a list of assessor results (results of different classifier) a table like structure
for further processing (e.g. plotting).

Classifier n TP FP TN FN
"""        
def createResultTable(assessor_results, separator):
    rows = []
    # create header
    header = separator.join( ['Criteria', 'Classifier', 'n', 'Freq. Threshold', 'TP', 'FP', 'TN', 'FN', 'Recall', 'Precision', 'F-Measure'] )
    rows.append(header)
    
    # create one row per assessor result
    for values in assessor_results:
        recall = computeRecall(values.true_positive, values.false_negative)
        precision = computePrecision(values.true_positive, values.false_positive)
        f_measure = computeFMeasure(values.true_positive, values.false_positive, values.false_negative)
        
        row_values = [values.criteria, values.classifier_name, values.n_gram_size, values.frequency_threshold,
                      values.true_positive, values.false_positive, values.true_negative, values.false_negative,
                      recall, precision, f_measure]
        row = separator.join( str(value) for value in  row_values)
        rows.append(row)
        
    return rows
        
def writeResultTableToFile(assessor_results, separator, file_path):
    data = createResultTable(assessor_results, separator)
    
    
    f = open(file_path, 'w')
    for line in data:
        f.write("".join( [line, "\n"] ))
        
    f.close()
    
def computeFMeasure(true_positive, false_positive, false_negative):
    f = (2 * true_positive) / ( (2 * true_positive) + false_positive + false_negative)
    return f

def computePrecision(true_positive, false_positive):
    p = 0
    if true_positive != 0.0:
        p = true_positive / ( true_positive + false_positive )
    return p

def computeRecall(true_positive, false_negative):
    r = 0
    if true_positive != 0.0: 
        r = true_positive / ( true_positive + false_negative )
    return r
     
    
    