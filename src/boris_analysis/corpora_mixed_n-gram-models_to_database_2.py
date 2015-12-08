"""
Created on Tue Jul 23 09:09:30 2015

@author: Stefan Hillmann (stefan.hillmann@tu-berlin.de)
"""

from common.ngram import model_generator as mg
from common.util.names import Class
import boris_analysis.dialogs as dialogs
import common.util.persistence as db
import configparser
import boris_analysis.corpora_names as cns
import pymongo

# read configuration
config = configparser.ConfigParser()
config.read('local_config.ini')

host = config.get('database', 'host')
port = config.getint('database', 'port')
database = config.get('database', 'db_name')
corpus_ngram_model = config.get('database', 'corpus_ngram_model_collection')
db_analysis = db.DbManager(host, port, database)
conn_analysis = db_analysis.get_connection()

n_gram_size_list = list(range(1, 8 + 1))  # [1, ..., 8]
f_min_list = [1, 2]
db_items = list()

corpora = cns.get_all_names()


def generate_n_gram_model(dialog_list, n, f_min):
    n_grams = mg.create_n_grams_from_document_list(dialog_list, n)
    model = mg.generate_model(n_grams)
    model = mg.remove_rare_n_grams(model, f_min)
    return model


db_items = list()
for corpus in corpora:
    print("Create n-grams for corpus '{0}'.".format(corpus))

    corpus_n_grams = list()

    # create models for n_gram_size and f_min from current corpus
    for f_min in f_min_list:
        for size in n_gram_size_list:
            corpus_documents = dialogs.create_dialogs_documents_from_database(corpus, Class.POSITIVE)
            for document in corpus_documents:
                n_gram_model = generate_n_gram_model([document], size, f_min)
                # create database entries
                for n_gram in n_gram_model.keys():
                    db_entry = {
                        'corpus': corpus,
                        'document_id': document.dialog_id,
                        'n': size,
                        'f_min': f_min,
                        'n_gram': n_gram,
                        'freq': n_gram_model[n_gram]
                    }
                    db_items.append(db_entry)

print("Writing {0} n-grams into database...".format(len(db_items)))
model_collection = conn_analysis[corpus_ngram_model]
model_collection.insert(db_items)

print("Creating index with 'n' and 'document_id'.")
model_collection.create_index([("n", pymongo.ASCENDING), ("document_id", pymongo.ASCENDING)])

db_analysis.close()
print("Finished.")





