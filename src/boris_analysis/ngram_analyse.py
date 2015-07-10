import operator
import numpy as np

import common.dialog_document.dialog_reader
from boris_analysis import dialogs
import common.ngram.model_generator as mg
import matplotlib.pyplot as plt
import common.util.list as lu


def remove_rare_n_grams(model, treshold):
    new_model = {}
    for key in model.keys():
        if model[key] >= treshold:
            new_model[key] = model[key]
    return new_model

        

failed_reader = common.dialog_document.dialog_reader.DialogsReader('/home/stefan/workspace/DialogueClassifying/data/turnsSucceeded.csv')
failed_dialogs = dialogs.create_dialogs_documents(failed_reader, 'iteration', 'test_class')
n = 3

class_n_grams = mg.create_n_grams_from_document_list(failed_dialogs, n)

class_model = mg.create_n_gram_model(lu.unique_values(class_n_grams), class_n_grams)

class_model = remove_rare_n_grams(class_model, 2)


sorted_class_model = sorted( class_model.iteritems(), key=operator.itemgetter(1) )

for n_gram in sorted_class_model:
    print n_gram


print class_model.values()
value_count = len( lu.unique_values(class_model.values()) )
print 'Anzahl verschiedene Haeufigkeiten: {}'.format(value_count)
print 'Anzahl n-Gramme: {}'.format( len(class_model) )

plt.hist( class_model.values(), np.arange(1, max(class_model.values())) )
plt.show()