__author__ = 'stefan'


import ConfigParser
from common.util import persistence
import numpy as np
import texttable as tt
import cross_validation_configuration
import matplotlib.pyplot as plt
import numpy as np


# read configuration
config = ConfigParser.ConfigParser()
config.read('local_config.ini')

evaluation_id = config.get('cross_validation', 'evaluation_id')
host = config.get('database', 'host')
port = config.getint('database', 'port')
database = config.get('database', 'db_name')
distances_collection = config.get('database', 'distances_collection')
performance_collection = config.get('database', 'performance_collection')

dbm = persistence.DbManager(host, port, database)
db = dbm.get_connection()
db_distances = db[distances_collection]
db_performance = db[performance_collection]
db_distance_performance = db[config.get('database', 'distance_performance_collection')]

configurations = cross_validation_configuration.getConfigurations()

criteria = db_performance.distinct('criteria')

criteria_to_data_set = {"juged_bad": 'user_judgement',
                        "juged_good": 'user_judgement',
                        "long_interactions": 'dialogue_length',
                        "short_interactions": 'dialogue_length',
                        "real": 'real_vs_best_sim',
                        "simulated": 'real_vs_best_sim',
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


def get_f_measure(criteria, n, classifier, ft, sv):
    query = {'evaluation_id': evaluation_id, 'frequency_threshold': ft, 'smoothing_value': sv,
             'classifier_name': classifier, 'n_gram_size': n, 'criteria': criteria}

    f = db_performance.find_one(query, {'f_measure': 1})

    return f['f_measure']

results = list()
for criteria in criteria_to_data_set.keys():
    print 'Criteria: ' + criteria

    data_set = criteria_to_data_set[criteria]

    for c in configurations:
        n = c.size
        classifier = c.classifier
        ft = c.frequency_threshold
        sv = c.smoothing_value

        distance = get_distance(data_set, n, classifier, ft, sv)
        f_measure = get_f_measure(criteria, n, classifier, ft, sv)

        result = {'criteria': criteria, 'data_set': data_set, 'distance': distance, 'f_measure': f_measure}
        result.update(c.__dict__)

        results.append(result)

db_distance_performance.insert(results)
