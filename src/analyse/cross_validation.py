# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 14:34:56 2013

@author: Stefan Hillmann (stefan.hillmann@tu-berlin.de)
"""

import util.list as lu
import ngram

class FoldValidator:
    
    def __init__(self, training_set, test_set, classifier, n):
        self.classifier = classifier
        self.test_set = test_set
        self.n = n
        self.test_results = []
        
        self.trainClassifier(training_set, n)
        
    
    """
    Trains the classivier with the training_set
    
    Parameters:
    training_set: List of dialogs.Document    
    """    
    def trainClassifier(self, training_set, n):
        # get the unique class identifiers
        classes = lu.uniqueObjectValues(training_set, 'label')

        # train each class with its documents
        for class_name in classes:
            class_documents = lu.filterByFieldValue(training_set, 'label', class_name)
            
            # collect content of all documents (of the current class, and ...)
            document_contents = []            
            for document in class_documents:
                document_contents.append(document.content)
            
            # ... create the n-grams for training
            n_grams = ngram.create_ngrams(document_contents, n)
            self.classifier.addClass(class_name, n_grams)
            
    
    
    
    def testClassifier(self):
        """
        Classify each document in test_set and returns the single results.
        """
        for document in self.test_set:
            n_grams = ngram.create_ngrams([document.content], self.n)
            
            classification_result = self.classifier.classify(n_grams)
            result = SingleTestResult(document, self.classifier.name, classification_result, self.n)
            self.test_results.append(result)
        
        return self.test_results

"""
Data transfer object for a single trial when testing a classifier in frame of
a fold based cross validation.
"""        
class SingleTestResult:
    def __init__(self, document, classifier_name, classification_result, n_gram_size):
        self.document               = document
        self.classifier_name        = classifier_name
        self.actual_class           = classification_result.class_name
        self.calculated_class       = document.label
        self.calculated_distance    = classification_result.distance
        self.n_gram_size            = n_gram_size
        