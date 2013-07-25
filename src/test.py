# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 13:47:03 2013

@author: Stefan Hillmann (stefan.hillmann@tu-berlin.de)
"""

import dialogs
import ngram
import util.list as lu

dr = dialogs.DialogsReader('data/annotatedData_corrected.csv')


iterations = dr.getUniqueValues('iteration')


dialog_documents = []
for iteration_id in iterations:
    dialog_rows = dr.getRows('iteration', iteration_id)
    dialog_document = dialogs.createDialogDocument(
    ['sysSA', 'sysRep.field'], ['userSA', 'userFields'], dialog_rows)
    
    dialog_documents.append(dialog_document)
    
n_grams = ngram.create_ngrams(dialog_documents, 3)

unique_n_grams = lu.uniqueValues(n_grams)
n_gram_model = ngram.createNgramModel(unique_n_grams, n_grams)

print n_gram_model





