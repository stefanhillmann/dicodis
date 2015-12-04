__author__ = 'stefan'

import common.util.persistence as pe
import boris_analysis.cross_validation_configuration as cvc
from common.analyse import performance as per
import configparser
import pyRserve as pyr
import numpy as np

config = configparser.ConfigParser()
config.read('local_config.ini')

host = config.get('database', 'host')
port = config.getint('database', 'port')
database = config.get('database', 'db_name')
evaluation_id = config.get('cross_validation', 'evaluation_id')

configurations = cvc.getConfigurations()

dbm = pe.DbManager(host, port, database)
db = dbm.get_connection()

# Prepare R connection
rc = pyr.connect()
rc.voidEval("library(pROC)")
rc.r.levels = ['positive', 'negative']


results = db[config.get('database', 'doc_result_collection')]
performance = db[config.get('database', 'performance_collection')]

# get criteria from database
criteria = results.distinct('criteria')


def get_auc(data):

    predictions = list()
    true_classes = list()
    for cursor in data:
        predictions.append(cursor['positive_class_distance'] - cursor['negative_class_distance'])
        true_classes.append(cursor['true_class'])

    rc.r.predictor = np.array(predictions)
    rc.r.response = np.array(true_classes)
    rc.voidEval("roc <- roc(response = response, predictor = predictor, levels = levels)")
    auc = rc.eval("roc$auc")
    print(auc[0])

    return auc[0]


def get_precision_recall_and_f_measure(evaluation_id, classifier_name, frequency_threshold, n_gram_size, smoothing_value,
                                       cri, database_collection):
    tp = per.get_db_true_positive_count(evaluation_id, classifier_name, frequency_threshold, n_gram_size, smoothing_value,
                                                cri, database_collection)
    fp = per.get_db_false_positive_count(evaluation_id, classifier_name, frequency_threshold, n_gram_size, smoothing_value,
                                                 cri, database_collection)

    fn = per.get_db_false_negative_count(evaluation_id, classifier_name, frequency_threshold, n_gram_size, smoothing_value,
                                                 cri, database_collection)

    precision = per.compute_precision(tp, fp)
    recall = per.compute_recall(tp, fn)
    f_measure = per.compute_f_measure(tp, fp, fn)

    return {'precision': precision, 'recall': recall, 'f_measure': f_measure, 'true_positives': tp,
            'false_positives': fp, 'false_negatives': fn}

for cri in criteria:
    print('Computing performance results for criteria {0}'.format(cri))
    # collect performance results for each criteria and write them into the database
    performance_results = []
    for conf in configurations:
        query = {'evaluation_id': evaluation_id,
                 'classifier_name': conf.classifier,
                 'frequency_threshold': conf.frequency_threshold,
                 'n_gram_size': conf.size,
                 'smoothing_value': conf.smoothing_value,
                 'criteria': cri}

        query_results = results.find(query)
        auc = get_auc(query_results)

        classificator_performance = {'evaluation_id': evaluation_id,
                                     'classifier_name': conf.classifier,
                                     'frequency_threshold': conf.frequency_threshold,
                                     'n_gram_size': conf.size,
                                     'smoothing_value': conf.smoothing_value,
                                     'criteria': cri,
                                     'auc': auc}

        # add precision, recall and f-value to performance
        p_r_f = get_precision_recall_and_f_measure(evaluation_id, conf.classifier, conf.frequency_threshold, conf.size,
                                                   conf.smoothing_value, cri, results)
        classificator_performance.update(p_r_f)

        # add result for classificator to result collector
        performance_results.append(classificator_performance)

    # write results collected for the current criteria into database
    print('Start writing results for criteria {0}'.format(cri))
    performance.insert(performance_results)
    print('Results for criteria {0} were written to database\n'.format(cri))

dbm.close()



