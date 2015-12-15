"""
Created on Tue Jul 22 15:05:10 2015

@author: Stefan Hillmann (stefan.hillmann@tu-berlin.de)
"""

from pymongo import MongoClient
import configparser
from common.util.names import Class
from enum import Enum

config = configparser.ConfigParser()
config.read('local_config.ini')


class Collection(Enum):
    doc_result = 1
    performance = 2
    distances = 3
    distance_performance = 4
    n_grams = 5
    dialogues = 6


COLLECTION_NAMES = {
    Collection.doc_result: "documents_result",
    Collection.performance: "performance",
    Collection.distances: "distances",
    Collection.distance_performance: "distance_performance",
    Collection.n_grams: "n_grams",
    Collection.dialogues: "dialogues"
}


class Database(Enum):
    production = 1
    unit_testing = 2


DATABASE_NAMES = {
    Database.production: "cross_validation_mixed_TEST",
    Database.unit_testing: "UNITTEST_classification_cross_validation"
}

current_database = Database.production


class DbClient(object):
    __state = {}

    def __init__(self, host, port):
        self.__dict__ = self.__state
        self.host = host
        self.port = port

    def connect(self):
        try:
            # does client exist?
            self.client
        except AttributeError:
            # no! Create it!
            print("Create MongoClient.")
            self.client = MongoClient(self.host, self.port, connect=False)

    def get_connection(self, database):
        self.connect()
        if type(database) is not Database:
            raise TypeError(
                "Parameter database has to be from type Database (see persistence.py). Current type and value: {0} ({1}".format(
                    type(database), str(database)
                ))

        return self.client[DATABASE_NAMES[database]]

    def close(self):
        self.client.close()

    def reset(self):
        self.close()
        self.client = MongoClient(self.host, self.port, connect=False)

host = "host"
port = 0
if config.has_section('database'):
    host = config.get('database', 'host')
    port = config.getint('database', 'port')
else:
    print('Could not load database configuration. Empty values are used.')

db_client = DbClient(host, port)


def close():
    db_client.close()


def reset():
    db_client.reset()


def get_collection(collection):
    if type(collection) is not Collection:
        raise TypeError("Parameter collection has to be from type Collection (see persistence.py.")

    db_connection = db_client.get_connection(current_database)
    collection_name = COLLECTION_NAMES[collection]
    return db_connection[collection_name]


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


def write_results_to_database(results):

        # transform instances to dict
        dicts = list()
        for r in results:
            dicts.append(r.dict_representation())

        collection = get_collection(Collection.doc_result)
        collection.insert(dicts)


def write_evaluation_results_to_database(evaluation_id, single_results, size, classifier_name, frequency_threshold,
                                         smoothing_value, criteria):
    evaluation_results = []
    for sr in single_results:
        er = EvaluationResult(evaluation_id, criteria, sr.document.dialog_id, classifier_name, size,
                              frequency_threshold, smoothing_value, sr.classification_result.estimated_class,
                              sr.true_class, sr.classification_result.positive_class_distance,
                              sr.classification_result.negative_class_distance, Class.POSITIVE, Class.NEGATIVE)
        evaluation_results.append(er)

    write_results_to_database(evaluation_results)

