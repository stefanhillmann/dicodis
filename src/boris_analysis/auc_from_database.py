__author__ = 'stefan'

import common.util.persistence as pe
from common.analyse import roc
from common.util.names import Class
import cross_validation_configuration


def get_auc(data):
    example_ids = list()
    positive_probability_dict = dict()
    true_class_dict = dict()

    for cursor in data:
        id = cursor['document_id']
        example_ids.append(id)
        positive_probability_dict[id] = cursor['positive_class_distance']
        true_class_dict[id] = cursor['true_class']

    _auc = roc.get_auc(example_ids, positive_probability_dict, true_class_dict, Class.POSITIVE, Class.NEGATIVE)
    return _auc

host = 'localhost'
port = 27017
database = 'classification_cross_validation'
evaluation_id = '2015_07_24__15_55'

configurations = cross_validation_configuration.getConfigurations()

dbm = pe.DbManager(host, port, database)
db = dbm.get_connection()

results = db.document_results

# get criteria from database
criteria = results.distinct('criteria')

for cri in criteria:
    for conf in configurations:
        query = {'evaluation_id': evaluation_id,
                 'classifier_name': conf.classifier,
                 'frequency_threshold': conf.frequency_threshold,
                 'n_gram_size': conf.size,
                 'smoothing_value': conf.smoothing_value,
                 'criteria': cri}

        query_results = results.find(query)
        auc = get_auc(query_results)
        db.auc.insert({'evaluation_id': evaluation_id,
                       'classifier_name': conf.classifier,
                       'frequency_threshold': conf.frequency_threshold,
                       'n_gram_size': conf.size,
                       'smoothing_value': conf.smoothing_value,
                       'criteria': cri,
                       'auc': auc})

dbm.close()



