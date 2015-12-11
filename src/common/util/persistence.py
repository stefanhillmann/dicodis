"""
Created on Tue Jul 22 15:05:10 2015

@author: Stefan Hillmann (stefan.hillmann@tu-berlin.de)
"""

from pymongo import MongoClient
import configparser
from common.util.names import Class


config = configparser.ConfigParser()
config.read('local_config.ini')

if config.has_section('database'):
    host = config.get('database', 'host')
    port = config.getint('database', 'port')
    database = config.get('database', 'name')
    client = MongoClient(host, port)
    connection = client[database]
else:
    print('Could not load database configuration. Empty values will be used.')
    client = None
    connection = None


def close():
    client.close()


def get_collection(collection_name):
    return connection[collection_name]


def get_database_name():
    return database


def create_client(_host, _port):
    return MongoClient(_host, _port)


class EvaluationResult:

    def __init__(self, evaluation_id, criteria, document_id, classifier_name, n_gram_size, frequency_threshold, smoothing_value,
                 estimated_class, true_class, positive_class_distance, negative_class_distance, positive_class_name,
                 negative_class_name):
        self.evaluation_id = evaluation_id
        self.criteria = criteria
        self.document_id = document_id
        self.classifier_name = classifier_name
        self.n_gram_size = n_gram_size
        self.frequency_threshold = frequency_threshold
        self.smoothing_value = smoothing_value
        self.estimated_class = estimated_class
        self.true_class = true_class
        self.positive_class_distance = positive_class_distance
        self.negative_class_distance = negative_class_distance
        self.positive_class_name = positive_class_name
        self.negative_class_name = negative_class_name

    def dict_representation(self):
        d = {'evaluation_id': self.evaluation_id, 'criteria': self.criteria, 'document_id': self.document_id, 'classifier_name': self.classifier_name,
             'n_gram_size': self.n_gram_size, 'frequency_threshold': self.frequency_threshold, 'smoothing_value': self.smoothing_value,
             'estimated_class': self.estimated_class, 'true_class': self.true_class,
             'positive_class_distance': self.positive_class_distance, 'negative_class_distance': self.negative_class_distance,
             'positive_class_name': self.positive_class_name, 'negative_class_name': self.negative_class_name}

        return d


def write_results_to_database(self, results, collection_name):

        # transform instances to dict
        dicts = list()
        for r in results:
            dicts.append(r.dict_representation())

        collection = self.db[collection_name]
        collection.insert(dicts)


def write_evaluation_results_to_database(evaluation_id, single_results, size, classifier_name, frequency_threshold,
                                         smoothing_value, criteria, **kwargs):
    evaluation_results = []
    for sr in single_results:
        er = EvaluationResult(evaluation_id, criteria, sr.document.dialog_id, classifier_name, size,
                              frequency_threshold, smoothing_value, sr.classification_result.estimated_class,
                              sr.true_class, sr.classification_result.positive_class_distance,
                              sr.classification_result.negative_class_distance, Class.POSITIVE, Class.NEGATIVE)
        evaluation_results.append(er)

    if 'collection_name' in kwargs.keys():
        doc_result_collection = kwargs['collection_name']
    else:
        doc_result_collection = config.get('collections', 'doc_result')
    coll_documents = get_collection(doc_result_collection)
    write_results_to_database(evaluation_results, coll_documents)


