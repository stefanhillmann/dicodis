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




dr = dialogs.DialogsReader('/home/stefan/workspace/DialogueClassifying/data/annotatedData_corrected.csv')

id_column = 'iteration'
dialog_rows = dr.getRows(id_column, '1')
dialog_document = dialogs.createDialogDocument(id_column,
    ['sysSA', 'sysRep.field'], ['userSA', 'userFields'], dialog_rows, 'testClass')



n = 3
classifier = classifier.getCosineClassifier();
validator = cv.FoldValidator([dialog_document], [dialog_document], classifier, n)
test_results = validator.testClassifier()

pprint(test_results[0])



#print dialog_document