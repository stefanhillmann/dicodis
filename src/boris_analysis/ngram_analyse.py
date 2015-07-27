import operator
import numpy as np

import common.dialog_document.dialog_reader
from boris_analysis import dialogs
import common.ngram.model_generator as mg
import matplotlib.pyplot as plt
import common.util.list as lu
from common.util.names import Class


failed_reader = common.dialog_document.dialog_reader.DialogsReader('/home/stefan/git/DialogueClassifying/data/turnsSucceeded.csv')
failed_dialogs = dialogs.create_dialogs_documents(failed_reader, 'iteration', Class.POSITIVE)
n = 3

class_n_grams = mg.create_n_grams_from_document_list(failed_dialogs, n)
class_model = mg.generate_model(class_n_grams)
class_model = mg.remove_rare_n_grams(class_model, 2)

sorted_class_model = sorted( class_model.iteritems(), key=operator.itemgetter(1) )

for n_gram in sorted_class_model:
    print n_gram


print class_model.values()
value_count = len( lu.unique_values(class_model.values()) )
print 'Anzahl verschiedene Haeufigkeiten: {}'.format(value_count)
print 'Anzahl n-Gramme: {}'.format( len(class_model) )

plt.hist( class_model.values(), np.arange(1, max(class_model.values())) )
plt.show()