# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 13:41:29 2013

@author: Stefan Hillmann (stefan.hillmann@tu-berlin.de)
"""

import ngram
import util.list as lu
import classifier
import dialogs
import analyse.cross_validation as cv
from pprint import pprint
from classifier import ClassifierName
from ngram import NGramSize
import logging

#example_ngrams = ['_#_#a', '_#a#b', 'a#b#c', 'b#c#d', 'c#d#_', 'd#_#_', '_#_#a', '_#a#b', 'a#b#x', 'b#x#y', 'x#y#z', 'y#z#_', 'z#_#_']

#n = 1
#doc_1 = ['a' 'a']
#n_grams_1 = ngram.create_ngrams(doc_1, n)

#doc_2 = ['b' 'b']
#n_grams_2 = ngram.create_ngrams(doc_2, n)

#cosineClassifier = classifier.getCosineClassifier()
#cosineClassifier.addClass('a_class', n_grams_1)
#cosineClassifier.addClass('b_class', n_grams_2)

#doc_3 = {'a'}
#n_grams_3 = ngram.create_ngrams(doc_3, n)

#distancies = cosineClassifier.computeDistancies(n_grams_3)

logging.basicConfig(level=logging.DEBUG)

id_column_name = 'iteration'

failed_reader = dialogs.DialogsReader('/home/stefan/workspace/DialogueClassifying/data/turnsFailed.csv')
failed_dialogs = dialogs.createDialogsDocuments(failed_reader, id_column_name, 'failed')

succeeded_reader = dialogs.DialogsReader('/home/stefan/workspace/DialogueClassifying/data/turnsSucceeded.csv')
succeeded_dialogs = dialogs.createDialogsDocuments(succeeded_reader, id_column_name, 'succeeded')

cross_validator = cv.CrossValidator(ClassifierName.COSINE, NGramSize.THREE)
cross_validator.addDocuments(failed_dialogs)
cross_validator.addDocuments(succeeded_dialogs)

cross_validator.runCrossValidation()

# for validation_results in cross_validator.runCrossValidation():
#    print validation_results[0]

