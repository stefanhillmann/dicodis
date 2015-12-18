import configparser
import logging

import common.util.persistence as pe
from boris_analysis import cross_validation_configuration_manual, dialogs
from common.corpora_distance import distance as d
from common.dialog_document.dialog_reader import DialogsReader
from common.ngram import model_generator as mg
from common.util.names import Class

logging.basicConfig(level=logging.WARNING)


# read configuration
config = configparser.ConfigParser()
config.read('local_config.ini')
distances_collection_name = config.get('collections', 'distances')
evaluation_id = config.get('cross_validation', 'evaluation_id')
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

corpora_pairs = {
    'success': (file_turns_succeeded, file_turns_failed),
    'simulation_quality': (file_best_simulation, file_worst_simulation),
    'dialogue_length': (file_shortest_interaction, file_longest_interaction),
    'word_accuracy': (file_wa_100, file_wa_60),
    'user_judgement': (file_judged_good, file_judged_bad),
    'real_vs_worst_sim': (file_experiment, file_worst_simulation),
    'real_vs_best_sim': (file_experiment, file_best_simulation)
}

configurations = cross_validation_configuration_manual.getConfigurations()


def read_dialogs(file_path):
    reader = DialogsReader(file_path)
    d = dialogs.create_dialogs_documents(reader, id_column_name, Class.POSITIVE)
    return d


def generate_n_gram_model(dialog_list, n, threshold):
    n_grams = mg.create_n_grams_from_document_list(dialog_list, n)
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
