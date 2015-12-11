__author__ = 'stefan'


import configparser
from common.util import persistence
import boris_analysis.cross_validation_configuration as cvc



# read configuration
config = configparser.ConfigParser()
config.read('local_config.ini')

evaluation_id = config.get('cross_validation', 'evaluation_id')

distances_collection = config.get('collections', 'distances')
performance_collection = config.get('collections', 'performance')

db_distances = persistence.get_collection(distances_collection)
db_performance = persistence.get_collection(performance_collection)
db_distance_performance = persistence.get_collection(config.get('database', 'distance_performance'))

configurations = cvc.getConfigurations()

criteria = db_performance.distinct('criteria')

criteria_to_data_set = {"juged_bad": 'user_judgement',
                        "juged_good": 'user_judgement',
                        "long_interactions": 'dialogue_length',
                        "short_interactions": 'dialogue_length',
                        "real": 'real_vs_best_sim',
                        "simulated": 'real_vs_best_sim',
                        "simulated_worst_vs_real": 'real_vs_worst_sim',
                        "real_vs_simulated_worst": 'real_vs_worst_sim',
                        "simulation_quality_best": 'simulation_quality',
                        "simulation_quality_worst": 'simulation_quality',
                        "task_failed": 'success',
                        "task_successful": 'success',
                        "word_accuracy_100": 'word_accuracy',
                        "word_accuracy_60": 'word_accuracy'}


def get_distance(data_set, n, classifier, ft, sv):
    query = {'evaluation_id': evaluation_id, 'frequency_threshold': ft, 'smoothing_value': sv,
             'classifier': classifier, 'size': n, 'data_set': data_set}

    d = db_distances.find_one(query, {'distance': 1})

    return d['distance']


def get_performance_value(criteria, n, classifier, ft, sv, value_name):
    query = {'evaluation_id': evaluation_id, 'frequency_threshold': ft, 'smoothing_value': sv,
             'classifier_name': classifier, 'n_gram_size': n, 'criteria': criteria}

    f = db_performance.find_one(query, {value_name: 1})

    return f[value_name]


def get_f_measure(criteria, n, classifier, ft, sv):
    return get_performance_value(criteria, n, classifier, ft, sv, 'f_measure')


def get_precision(criteria, n, classifier, ft, sv):
    return get_performance_value(criteria, n, classifier, ft, sv, 'precision')


def get_recall(criteria, n, classifier, ft, sv):
    return get_performance_value(criteria, n, classifier, ft, sv, 'recall')


results = list()
for criteria in criteria_to_data_set.keys():
    print('Criteria: ' + criteria)

    data_set = criteria_to_data_set[criteria]

    for c in configurations:
        n = c.size
        classifier = c.classifier
        ft = c.frequency_threshold
        sv = c.smoothing_value

        distance = get_distance(data_set, n, classifier, ft, sv)
        f_measure = get_f_measure(criteria, n, classifier, ft, sv)
        precision = get_precision(criteria, n, classifier, ft, sv)
        recall = get_recall(criteria, n, classifier, ft, sv)

        result = {'criteria': criteria, 'data_set': data_set, 'distance': distance, 'f_measure': f_measure,
                  'precision': precision, 'recall': recall}
        result.update(c.__dict__)

        results.append(result)

db_distance_performance.insert(results)
persistence.close()
