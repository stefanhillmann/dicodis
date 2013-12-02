import dialogs
import ngram.model_generator as mg
import operator
import matplotlib.pyplot as plt
import util.list as lu
import numpy as np

def remove_rare_n_grams(model, treshold):
    new_model = {}
    for key in model.keys():
        if model[key] >= treshold:
            new_model[key] = model[key]
    return new_model

        

failed_reader = dialogs.DialogsReader('/home/stefan/workspace/DialogueClassifying/data/turnsSucceeded.csv')
failed_dialogs = dialogs.createDialogsDocuments(failed_reader, 'iteration', 'test_class')
n = 3

documents = []
for dialog in failed_dialogs:
    documents.append( dialog.content )

class_n_grams = mg.create_ngrams(documents, n);

class_model = mg.createNgramModel(lu.uniqueValues(class_n_grams), class_n_grams)

class_model = remove_rare_n_grams(class_model, 2)


sorted_class_model = sorted( class_model.iteritems(), key=operator.itemgetter(1) )

for n_gram in sorted_class_model:
    print n_gram


print class_model.values()
value_count = len( lu.uniqueValues(class_model.values()) )
print 'Anzahl verschiedene Haeufigkeiten: {}'.format(value_count)
print 'Anzahl n-Gramme: {}'.format( len(class_model) )

plt.hist( class_model.values(), np.arange(1, max(class_model.values())) )
plt.show()