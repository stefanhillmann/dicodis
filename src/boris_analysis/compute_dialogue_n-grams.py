"""
Created on Tue Jul 23 09:09:30 2015

@author: Stefan Hillmann (stefan.hillmann@tu-berlin.de)
"""

import configparser

import pymongo

import boris_analysis.corpora_names as cd
import boris_analysis.dialogs as dialogs
import common.util.persistence as pe
from common.ngram import model_generator as mg
from common.util.names import Class

# read configuration
config = configparser.ConfigParser()
config.read('local_config.ini')

n_gram_size_list = list(range(1, 8 + 1))  # [1, ..., 8]
db_items = list()

corpora = cd.get_all_corpus_data()


def generate_n_gram_model(dialog_list, n):
    n_grams = mg.create_n_grams_from_document_list(dialog_list, n)
    model = mg.generate_model(n_grams)
    return model

n_grams_collection = pe.get_collection(pe.Collection.n_grams)
print("Create unique index for f_min, n, document_id, corpus and n_gram")
n_grams_collection.create_index([("n", pymongo.ASCENDING),
                                 ("document_id", pymongo.ASCENDING), ("corpus", pymongo.ASCENDING),
                                 ("n_gram", pymongo.ASCENDING)], unique=True)

db_items = list()
for corpus in corpora:
    print("Create n-grams for corpus '{0}'.".format(str(corpus)))

    corpus_n_grams = list()

    # create models for n_gram_size from current corpus
    for size in n_gram_size_list:
        corpus_documents = dialogs.create_dialogs_documents_from_database(corpus, Class.POSITIVE)
        for document in corpus_documents:
            n_gram_model = generate_n_gram_model([document], size)
            # create database entries
            for n_gram, freq in n_gram_model.get_tuples():
                db_entry = {
                    'corpus': corpus.name,
                    'document_id': document.dialog_id,
                    'n': size,
                    'n_gram': n_gram,
                    'freq': int(freq)
                }
                db_items.append(db_entry)

print("Writing {0} n-grams into database...".format(len(db_items)))
n_grams_collection.insert(db_items)

print("Creating index with 'n', 'document_id' and 'f_min.")
n_grams_collection.create_index([("n", pymongo.ASCENDING), ("document_id", pymongo.ASCENDING),
                                 ("f_min", pymongo.ASCENDING)])

pe.close()
print("Finished.")





