__author__ = 'stefan'

import ConfigParser
from common.util import persistence
import pymongo as mongo


# read configuration
config = ConfigParser.ConfigParser()
config.read('local_config.ini')

evaluation_id = config.get('cross_validation', 'evaluation_id')
host = config.get('database', 'host')
port = config.getint('database', 'port')
database = config.get('database', 'db_name')
distances_collection = config.get('database', 'distances_collection')

dbm = persistence.DbManager(host, port, database)
db = dbm.get_connection()

db_distances = db[distances_collection]
db_performance = db[config.get('database', 'performance_collection')]


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

classifiers = db_performance.distinct('classifier_name')
print 'Classifiers: ' + str(classifiers)

criteria = db_performance.distinct('criteria')
print 'Criteria: ' + str(criteria)

print 'Searching best configurations for all classifiers.\n'
for crit in criteria:
    for classifier in classifiers:
        result = db_performance.find({'criteria': crit, 'classifier_name': classifier}).sort('f_measure', mongo.DESCENDING)
        best = result[0]
        print "{0} and {1} with f = {2} is n: {3}, t: {4}, l: {5}".format(crit, classifier, best['f_measure'],
                                                                          best['n_gram_size'], best['frequency_threshold'],
                                                                          best['smoothing_value'])

criteria = db_performance.distinct('criteria')
print 'Criteria: ' + str(criteria)
print '\n\nSearching best configuration for best classifier.\n'
for crit in criteria:
    result = db_performance.find({'criteria': crit}).sort('f_measure', mongo.DESCENDING)
    best = result[0]

    distance = db_distances.find_one({'frequency_threshold': best['frequency_threshold'],
                                      'size': best['n_gram_size'],
                                      'smoothing_value': best['smoothing_value'],
                                      'data_set': criteria_to_data_set[crit],
                                      'classifier': best['classifier_name']})

    print "{0} and {1} with f = {2} is n: {3}, t: {4}, l: {5} => distance: {6}".format(crit, best['classifier_name'], best['f_measure'],
                                                                      best['n_gram_size'], best['frequency_threshold'],
                                                                      best['smoothing_value'], distance['distance'])


