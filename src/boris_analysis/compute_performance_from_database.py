import configparser

import numpy as np
import pyRserve as pyR
from pyRserve.rexceptions import REvalError

import boris_analysis.cross_validation_configuration_manual as cvc
import common.util.persistence as pe
from common.analyse import performance as per

config = configparser.ConfigParser()
config.read('local_config.ini')
evaluation_id = config.get('cross_validation', 'evaluation_id')

configurations = cvc.getConfigurations()


# Prepare R connection
try:
    rc = pyR.connect()
except ConnectionRefusedError as cre:
    print("Could not connect to Reserve Server, .")
    print("Is the Reserve Server started in an R session?  Try in R:")
    print("R> library(Rserve)")
    print("R> Rserve()")

rc.voidEval("library(pROC)")
rc.r.levels = ['positive', 'negative']


results = pe.get_collection(pe.Collection.doc_result)
performance = pe.get_collection(pe.Collection.performance)

# get criteria from database
criteria = results.distinct('criteria')


def get_auc(data):

    predictions = list()
    true_classes = list()
    for cursor in data:
        predictions.append(cursor['positive_class_distance'] - cursor['negative_class_distance'])
        true_classes.append(cursor['true_class'])

    # if len(set(true_classes)) == 1:
    #     raise ValueError(
    #         "Only one class ('{0}') used for true classes. "
    #         "Two classes are necessary for further processing".format(set(true_classes)))

    rc.r.predictor = np.array(predictions)
    rc.r.response = np.array(true_classes)

    try:
        rc.voidEval("roc <- roc(response = response, predictor = predictor, levels = levels)")
    except REvalError as e:
        print("Error while computing ROC in R: {0}".format(e))

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
    performance.insert_many(performance_results)
    print('Results for criteria {0} were written to database\n'.format(cri))

pe.close()



