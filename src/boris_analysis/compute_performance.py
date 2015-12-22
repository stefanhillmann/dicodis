import configparser

import numpy as np
import pyRserve as pyr
from pyRserve.rexceptions import REvalError

import boris_analysis.cross_validation_configuration_manual as cvc
import common.util.persistence as pe

config = configparser.ConfigParser()
config.read('local_config.ini')
evaluation_id = config.get('cross_validation', 'evaluation_id')

configurations = cvc.getConfigurations()

# Prepare R connection
rc = pyr.connect()
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

    rc.r.predictor = np.array(predictions)
    rc.r.response = np.array(true_classes)
    try:
        rc.voidEval("roc <- roc(response = response, predictor = predictor, levels = levels)")
    except REvalError as e:
        print("Error while computing ROC with predictions: '{0}' and true_classes: '{1}. Will re-raise the error."
              .format(str(predictions), str(true_classes)))
        raise e

    auc = rc.eval("roc$auc")

    return auc[0]

for cri in criteria:
    print("Computing performance results for criteria '{0}'.".format(cri))
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
        auc_for_conf = get_auc(query_results)

        classificator_performance = {'evaluation_id': evaluation_id,
                                     'classifier_name': conf.classifier,
                                     'frequency_threshold': conf.frequency_threshold,
                                     'n_gram_size': conf.size,
                                     'smoothing_value': conf.smoothing_value,
                                     'criteria': cri,
                                     'auc': auc_for_conf}

        # add result for classificator to result collector
        performance_results.append(classificator_performance)

    # write results collected for the current criteria into database
    print('Start writing {1} results for criteria {0}'.format(cri, len(performance_results)))
    performance.insert_many(performance_results)
    print('Results for criteria {0} were written to database\n'.format(cri))

print("Finished")

pe.close()



