"""
Created on Tue Jul 23 09:09:30 2015

@author: Stefan Hillmann (stefan.hillmann@tu-berlin.de)
"""

from common.ngram import model_generator as mg
from common.dialog_document.dialog_reader import DialogsReader
from common.util.names import Class
import boris_analysis.dialogs as dialogs
import common.util.persistence as pe
import configparser

# read configuration
config = configparser.ConfigParser()
config.read('local_config.ini')

ngram_collection_name = config.get('database', 'corpus_ngram_model_collection')

base_directory = config.get('cross_validation', 'source_directory')
id_column_name = 'iteration'


file_turns_succeeded        = base_directory + 'data/turnsSucceeded.csv'
file_turns_failed           = base_directory + 'data/turnsFailed.csv'
file_best_simulation        = base_directory + 'data/bestSimulation.csv'
file_worst_simulation       = base_directory + 'data/worstSimulation.csv'
file_shortest_interaction   = base_directory + 'data/shortest49Interactions.csv'
file_longest_interaction    = base_directory + 'data/longest49Interactions.csv'
file_wa_100                 = base_directory + 'data/WA_60.csv'
file_wa_60                  = base_directory + 'data/WA_100.csv'
file_judged_bad             = base_directory + 'data/badJudged.csv'
file_judged_good            = base_directory + 'data/goodJudged.csv'
file_experiment             = base_directory + 'data/annotatedData_corrected.csv'

corpus_to_file = {
    'task success': file_turns_succeeded,
    'task failed': file_turns_failed,
    'simulation good': file_best_simulation,
    'simulation bad': file_worst_simulation,
    'interaction short': file_shortest_interaction,
    'interaction long': file_longest_interaction,
    'word accuracy 100': file_wa_100,
    'word accuracy 60': file_wa_60,
    'judged bad': file_judged_bad,
    'judged good': file_judged_good,
    'real user': file_experiment
}

n_gram_size_list = range(1, 8 + 1)  # [1, ..., 8]
f_min_list = [1, 2]
db_items = list()


def generate_n_gram_model(dialog_list, n, f_min):
    n_grams = mg.create_n_grams_from_document_list(dialog_list, n)
    model = mg.generate_model(n_grams)
    model = mg.remove_rare_n_grams(model, f_min)
    return model

for corpus in corpus_to_file.keys():
    print("Create n-grams for corpus '{0}' from file '{1}'.".format(corpus, corpus_to_file[corpus]))

    dialog_reader = DialogsReader(corpus_to_file[corpus])
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
ngram_collection = pe.get_collection(pe.Collection.n_grams)
ngram_collection.insert(db_items)
pe.close()
print("Finished.")





