import configparser
import logging

import common.util.persistence as pe
from boris_analysis import cross_validation_configuration_manual, dialogs
import boris_analysis.corpora_names as cd
from common.corpora_distance import distance as d
from common.ngram import model_generator as mg
from common.util.names import Class
from boris_analysis import criteria

logging.basicConfig(level=logging.WARNING)


# read configuration
config = configparser.ConfigParser()
config.read('local_config.ini')
evaluation_id = config.get('cross_validation', 'evaluation_id')


corpora_pairs = {
    criteria.TASK_SUCCESS: (cd.SUCCESSFUL, cd.NOT_SUCCESSFUL),
    criteria.SIMULATION_QUALITY: (cd.SIMULATION_GOOD, cd.SIMULATION_BAD),
    criteria.DIALOGUE_LENGTH: (cd.DIALOGUES_SHORT, cd.DIALOGUES_LONG),
    criteria.DIALOGUE_LENGTH: (cd.WORD_ACCURACY_60, cd.WORD_ACCURACY_100),
    criteria.USER_JUDGEMENT: (cd.USER_JUDGMENT_GOOD, cd.USER_JUDGMENT_BAD),
    criteria.SIM_BAD_VS_REAL: (cd.REAL_USER, cd.SIMULATION_BAD),
    criteria.SIM_GOOD_VS_REAL: (cd.REAL_USER, cd.SIMULATION_GOOD),
    criteria.SIM_SAMPlED_VS_REAL: (cd.REAL_USER, cd.GOOD_SIMULATION_SUB_SET_SAMPLE),
    criteria.SIM_NO_SUCCESS_VS_REAL: (cd.REAL_USER, cd.GOOD_SIMULATION_NOT_SUCCESSFUL),
    criteria.SIM_SAMPLED_VS_SIM_NO_SUCCESS: (cd.GOOD_SIMULATION_SUB_SET_SAMPLE, cd.GOOD_SIMULATION_NOT_SUCCESSFUL)
}

configurations = cross_validation_configuration_manual.getConfigurations()


def read_dialogs(corpus):
    dialogues = dialogs.create_dialogs_documents_from_database(corpus, Class.POSITIVE)
    return dialogues


def generate_n_gram_model(dialog_list, n, threshold):
    n_grams = mg.get_n_grams_from_database_for_documents(dialog_list, n)
    model = mg.generate_model(n_grams)
    model.remove_rare_n_grams(threshold)

    return model


distances_list = list()
for _criteria in corpora_pairs.keys():
    print('Computing distances for {0}.'.format(_criteria.name))
    pair = corpora_pairs[_criteria]
    c1_dialogs = read_dialogs(pair[0])
    c2_dialogs = read_dialogs(pair[1])

    for con in configurations:
        c1_model = generate_n_gram_model(c1_dialogs, con.size, con.frequency_threshold)
        c2_model = generate_n_gram_model(c2_dialogs, con.size, con.frequency_threshold)

        measure = d.get_distance_calculator(con.classifier)
        distance = measure.compute_distance(c1_model, c2_model, con.smoothing_value)

        db_distance = {'criteria': _criteria.name, 'distance': distance, 'evaluation_id': evaluation_id}
        db_distance.update(con.__dict__)
        distances_list.append(db_distance)

distances = pe.get_collection(pe.Collection.distances)
print("Drop existing collection '{0}'".format(pe.get_collection_name(pe.Collection.distances)))
distances.drop()
distances = pe.get_collection(pe.Collection.distances)
print('Write {0} results to database.'.format(len(distances_list)))
distances.insert_many(distances_list)

pe.close()
