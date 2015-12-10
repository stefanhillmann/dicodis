"""
Created on Tue Jul 22 15:05:10 2015

@author: Stefan Hillmann (stefan.hillmann@tu-berlin.de)
"""

from pymongo import MongoClient
from common.util.names import Class


class DbManager:

    def __init__(self, host, port, database):
        self.client, self.db = get_mongo_db_connection(host, port, database)

    def write_results_to_database(self, results, collection_name):

        # transform instances to dict
        dicts = list()
        for r in results:
            dicts.append(r.dict_representation())

        collection = self.db[collection_name]
        collection.insert(dicts)

    def get_connection(self):
        return self.db

    def close(self):
        self.client.close()


def get_mongo_db_connection(host, port, database):
    client = MongoClient(host, port, connect=False)
    db = client[database]

    return client, db


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


def write_evaluation_results_to_database(evaluation_id, single_results, size, classifier_name, frequency_threshold,
                                         smoothing_value, criteria, host, port, database_name, collection_name):
    evaluation_results = []
    for sr in single_results:
        er = EvaluationResult(evaluation_id, criteria, sr.document.dialog_id, classifier_name, size,
                              frequency_threshold, smoothing_value, sr.classification_result.estimated_class,
                              sr.true_class, sr.classification_result.positive_class_distance,
                              sr.classification_result.negative_class_distance, Class.POSITIVE, Class.NEGATIVE)
        evaluation_results.append(er)

    con = DbManager(host, port, database_name)
    con.write_results_to_database(evaluation_results, collection_name)
    con.close()
