"""
Created on Tue Jul 27 10:25:00 2015

@author: Stefan Hillmann (stefan.hillmann@tu-berlin.de)
"""

from common.util.names import Class


def compute_f_measure(true_positive, false_positive, false_negative):
    f = 0
    if true_positive != 0.0:
        f = float((2 * true_positive)) / ( (2 * true_positive) + false_positive + false_negative)
    return f


def compute_precision(true_positive, false_positive):
    p = 0.0
    if true_positive != 0.0:
        p = float(true_positive) / ( true_positive + false_positive )
    return p


def compute_recall(true_positive, false_negative):
    r = 0.0
    if true_positive != 0.0:
        r = float(true_positive) / ( true_positive + false_negative )
    return r


def __get_db_performance_count(evaluation_id, classifier_name, frequency_threshold, n_gram_size, smoothing_value,
                               criteria, estimated_class, true_class, database_collection):

    query = {'evaluation_id': evaluation_id,
             'classifier_name': classifier_name,
             'frequency_threshold': frequency_threshold,
             'n_gram_size': n_gram_size,
             'smoothing_value': smoothing_value,
             'criteria': criteria,
             'estimated_class': estimated_class,
             'true_class': true_class}

    return database_collection.find(query).count()


def get_db_true_positive_count(evaluation_id, classifier_name, frequency_threshold, n_gram_size, smoothing_value,
                               criteria, database_collection):

    return __get_db_performance_count(evaluation_id, classifier_name, frequency_threshold, n_gram_size, smoothing_value,
                                      criteria, Class.POSITIVE, Class.POSITIVE, database_collection)


def get_db_true_negative_count(evaluation_id, classifier_name, frequency_threshold, n_gram_size, smoothing_value,
                               criteria, database_collection):

    return __get_db_performance_count(evaluation_id, classifier_name, frequency_threshold, n_gram_size, smoothing_value,
                                      criteria, Class.NEGATIVE, Class.NEGATIVE, database_collection)


def get_db_false_positive_count(evaluation_id, classifier_name, frequency_threshold, n_gram_size, smoothing_value,
                                criteria, database_collection):

    return __get_db_performance_count(evaluation_id, classifier_name, frequency_threshold, n_gram_size, smoothing_value,
                                      criteria, Class.POSITIVE, Class.NEGATIVE, database_collection)


def get_db_false_negative_count(evaluation_id, classifier_name, frequency_threshold, n_gram_size, smoothing_value,
                                criteria, database_collection):

    return __get_db_performance_count(evaluation_id, classifier_name, frequency_threshold, n_gram_size, smoothing_value,
                                      criteria, Class.NEGATIVE, Class.POSITIVE, database_collection)
