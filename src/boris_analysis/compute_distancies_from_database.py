import configparser
import logging

import common.util.persistence as pe
from boris_analysis import cross_validation_configuration_manual, dialogs
from boris_analysis.corpora_names import CorporaNames as CNs
from common.corpora_distance import distance as d
from common.ngram import model_generator as mg
from common.util.names import Class

logging.basicConfig(level=logging.WARNING)


# read configuration
config = configparser.ConfigParser()
config.read('local_config.ini')
evaluation_id = config.get('cross_validation', 'evaluation_id')


corpora_pairs = {
    'success': (CNs.SUCCESSFUL, CNs.NOT_SUCCESSFUL),
    'simulation_quality': (CNs.SIMULATION_GOOD, CNs.SIMULATION_BAD),
    'dialogue_length': (CNs.DIALOGUES_SHORT, CNs.DIALOGUES_LONG),
    'word_accuracy': (CNs.WORD_ACCURACY_60, CNs.WORD_ACCURACY_100),
    'user_judgement': (CNs.USER_JUDGMENT_GOOD, CNs.USER_JUDGMENT_BAD),
    'real_vs_worst_sim': (CNs.REAL_USER, CNs.SIMULATION_BAD),
    'real_vs_best_sim': (CNs.REAL_USER, CNs.SIMULATION_GOOD)
}

configurations = cross_validation_configuration_manual.getConfigurations()


def read_dialogs(corpus_name):
    dialogues = dialogs.create_dialogs_documents_from_database(corpus_name, Class.POSITIVE)
    return dialogues


def generate_n_gram_model(dialog_list, n, threshold):
    n_grams = mg.get_n_grams_from_database_for_documents(dialog_list, n)
    model = mg.generate_model(n_grams)
    model.remove_rare_n_grams(threshold)

    return model


distances_list = list()
for data_set_name in corpora_pairs.keys():
    print('Computing distances for {0}.'.format(data_set_name))
    pair = corpora_pairs[data_set_name]
    c1_dialogs = read_dialogs(pair[0])
    c2_dialogs = read_dialogs(pair[1])

    for con in configurations:
        c1_model = generate_n_gram_model(c1_dialogs, con.size, con.frequency_threshold)
        c2_model = generate_n_gram_model(c2_dialogs, con.size, con.frequency_threshold)

        measure = d.get_distance_calculator(con.classifier)
        distance = measure.compute_distance(c1_model, c2_model, con.smoothing_value)

        db_distance = {'data_set': data_set_name, 'distance': distance, 'evaluation_id': evaluation_id}
        db_distance.update(con.__dict__)
        distances_list.append(db_distance)

distances = pe.get_collection(pe.Collection.distances)
print('Write {0} results to database.'.format(len(distances_list)))
distances.insert_many(distances_list)

pe.close()
