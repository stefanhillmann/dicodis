"""
Created on Tue Jul 23 09:09:30 2015

@author: Stefan Hillmann (stefan.hillmann@tu-berlin.de)
"""

from common.ngram import model_generator as mg
from common.dialog_document.dialog_reader import DialogsReader
from common.util.names import Class
import boris_analysis.dialogs as dialogs
import common.util.persistence as db
import configparser
import boris_analysis.corpora_names as cns

# read configuration
config = configparser.ConfigParser()
config.read('local_config.ini')

host = config.get('database', 'host')
port = config.getint('database', 'port')
database = config.get('database', 'db_name')

database_dialogues = config.get('dialogue_database', 'dialogues_db_name')
dialogues_collection = config.get('dialogue_database', 'dialogues_collection')
corpus_ngram_model = config.get('database', 'corpus_ngram_model_collection')

db_analysis = db.DbManager(host, port, database)
db_dialogues = db.DbManager(host, port, database_dialogues)

conn_analysis = db_analysis.get_connection()
conn_dialogues = db_dialogues.get_connection()

n_gram_size_list = range(1, 8 + 1)  # [1, ..., 8]
f_min_list = [1, 2]
db_items = list()

corpora = cns.get_all_names()


def generate_n_gram_model(dialog_list, n, f_min):
    n_grams = mg.create_n_grams_from_document_list(dialog_list, n)
    model = mg.generate_model(n_grams)
    model = mg.remove_rare_n_grams(model, f_min)
    return model

for corpus in corpora:
    print("Create n-grams for corpus '{0}'.".format(corpus))
    dialogues = conn_dialogues["dialogues"]
    turns = dialogues.find({"corpora": corpus})


    # TODO: create n-grams from list of turns?
    corpus_documents = dialogs.create_dialogs_documents(dialog_reader, id_column_name, Class.POSITIVE)

    # TODO: Only a test!!!
    # map(lambda d: d.content.pop(0), corpus_documents)

    corpus_n_grams = list()

    # create models for n_gram_size and f_min from current corpus
    for f_min in f_min_list:
        corpus_model = generate_n_gram_model(corpus_documents, n_gram_size_list, f_min)

        # create database entries
        for n_gram in corpus_model.keys():
            db_entry = {
                'corpus': corpus,
                'n': n_gram_size_list,
                'f_min': f_min,
                'n_gram': n_gram,
                'freq': corpus_model[n_gram]
            }
            db_items.append(db_entry)

print("Writing {0} n-grams into database...".format(len(db_items)))
db_connection = dbm.get_connection()
model_collection = db_connection[corpus_ngram_model]
model_collection.insert(db_items)
dbm.close()
print("Finished.")





