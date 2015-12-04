"""
Created on Tue Jul 23 09:09:30 2015

@author: Stefan Hillmann (stefan.hillmann@tu-berlin.de)
"""

from common.ngram import model_generator as mg
from common.dialog_document.dialog_reader import DialogsReader
from common.util.names import Class
import common.util.persistence as pe
import boris_analysis.dialogs as dialogs

host = 'localhost'
port = 27017
database = 'dialog_ngrams'

id_column_name = 'iteration'

base_directory = '/home/stefan/git/DialogueClassifying/'
file_experiment             = base_directory + 'data/annotatedData_corrected.csv'

dbm = pe.DbManager(host, port, database)
db = dbm.get_connection()

# create collection of single n-grams with relation to documents
n_gram_size_list = range(1, 10 + 1)
dialog_reader = DialogsReader(file_experiment)
all_documents = dialogs.create_dialogs_documents(dialog_reader, id_column_name, Class.POSITIVE)

all_n_grams = list()
for n_gram_size in n_gram_size_list:
    print('n = {0}'.format(n_gram_size))
    for d in all_documents:
        d_n_grams = mg.create_n_grams_from_document_list([d], n_gram_size)
        for n_gram in d_n_grams:
            item = {'n_gram': n_gram, 'n_gram_size': n_gram_size, 'dialog_id': d.dialog_id}
            all_n_grams.append(item)

n_grams = db.n_grams
n_grams.insert(all_n_grams)

dbm.close()





