import common.util.persistence as pe
import boris_analysis.cross_validation_configuration_manual as cvc
import configparser
import pyRserve as pyr
import numpy as np

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
    rc.voidEval("roc <- roc(response = response, predictor = predictor, levels = levels)")
    auc = rc.eval("roc$auc")
    print(auc[0])

    return auc[0]

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
    print('Start writing results for criteria {0}'.format(cri))
    performance.insert(performance_results)
    print('Results for criteria {0} were written to database\n'.format(cri))

pe.close()



