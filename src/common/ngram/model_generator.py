# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 11:56:52 2013

@author: Stefan Hillmann (stefan.hillmann@tu-berlin.de)
"""
import logging
from collections import Counter
from collections import OrderedDict
from common.ngram import smoothing
from common.util import dict as du
import common.ngram.cached_n_grams as cached_n_grams
import common.ngram.cached_n_gram_query as cached_query
import configparser
import common.util.persistence as persistence
import common.ngram.n_gram_model as ngm


# read configuration
config = configparser.ConfigParser()
config.read('local_config.ini')
host = config.get('database', 'host')
port = config.getint('database', 'port')
database = config.get('database', 'db_name')
corpus_ngram_model = config.get('database', 'corpus_ngram_model_collection')
dbm = persistence.DbManager(host, port, database)

module_logger = logging.getLogger('ngram')


def create_n_grams_from_document(document, n):
    sizes = get_n_gram_sizes_as_list(n)

    n_grams = []
    # The tuple representation (instead of list) of the tokens is needed for the caching mechanism.
    # It is not possible (in Python) to compute the hash value of a list.
    tokens = tuple(document.content)

    for size in sizes:
        if len(tokens) >= size:
            n_grams.extend(cached_n_grams.get_n_grams(tokens, size))

    return n_grams


def create_n_grams_from_document_list(document_list, n):
    n_grams = []
    for document in document_list:
        n_grams.extend(create_n_grams_from_document(document, n))

    return n_grams


def get_n_gram_sizes_as_list(n_gram_sizes):
    sizes = list()
    if type(n_gram_sizes) is list:
        sizes.extend(n_gram_sizes)
    elif type(n_gram_sizes) is int:
        sizes.append(n_gram_sizes)
    else:
        raise ValueError("Unknown type '{0}' for parameter 'n'.".format(type(n_gram_sizes)))

    return sizes


def get_n_grams_from_database_for_documents(documents, n_gram_sizes):
    n_grams = list()
    for document in documents:
        n_grams.extend(get_n_grams_from_database_for_single_document(document, n_gram_sizes))

    return n_grams


def get_n_grams_from_database_for_single_document(document, n_gram_sizes):
    sizes = get_n_gram_sizes_as_list(n_gram_sizes)
    return cached_query.get_n_grams_from_database(document.dialog_id, tuple(sizes))


def sort_model_by_n_grams(model):
    return du.sort_by_key(model)


def generate_model(n_grams):
    # counter = Counter(n_grams)
    # model = dict(counter)
    model = ngm.NGramModel(n_grams)
    return model


def remove_rare_n_grams(model, threshold):
    new_model = OrderedDict()
        
    for key in model.keys():
        if model[key] >= threshold:
            new_model[key] = model[key]
            
    return new_model


def smooth_model(model, l):
    """
    Smoothes a n-gram model using the value l as 'add'.
    Parameters
    ----------
    model : dictionary
        an n-gram model with absolute frequencies
    l : float
        the value to be added
    Returns
    -------
    dictionary : a model with smoothed values for n-gram probabilities.
    """
    module_logger.debug("Smooth model with l = %s.", l)

    # get the frequencies as array
    absolute_values = list(model.values())
    
    # compute relative probabilities and smooth them with value l
    smoothed_values = smoothing.compute_probabilities(absolute_values, l)
    
    # create new dictionary with with n-grams and the smoothed values
    n_grams = list(model.keys())
    for i in range( len(smoothed_values) ):
        n_gram = n_grams[i]
        probability = smoothed_values[i]
        model[n_gram] = probability


def compute_probabilities(model, l):
    """
    Computes the relative probabilities for a model which has still absolute frequency values.
    If *l* (for lambda) is greater than 0.0 and the model contains a frequency with value 0.0,
    the model will be automatically smoothed using *l*.
    If *l* is less than or equal t 0.0, just the relative probabilities are computed.
    In both cases, the new values will replace the old values in *model*.
    :param model: A n-gram model (dict) with relative frequencies.
    :param l: The smoothing value. Has to be <= 0.0 to avoid smoothing.
    :return: nothing, *model* is directly changed.
    """
    if l > 0.0 and 0 in model.get_frequencies():
        smooth_model(model, l)
    else:
        sum_of_frequencies = sum(model.values())
        for key in model:
            model[key] = model[key] / float(sum_of_frequencies)


def synchronize_n_grams(model, other_model):
    """
    Adds all n-grams which are in model to other_model and vice versa.
    Afterwards both models contains the same n-grams. The frequency of the added n-grams is set to 0.
    :param model: a n-gram model (a dict)
    :param other_model: another n-gram model (a dict)
    :return: nothing
    """
    model.add_n_grams_if_new( set(other_model.get_n_grams()), 0 )
    other_model.add_n_grams_if_new( set(model.get_n_grams()), 0 )

    # TODO: Remove?
    # unique_n_grams = get_unique_n_grams_from_models([model, other_model])
    # for n_gram in unique_n_grams:
    #     if not model.contains_n_gram(n_gram):
    #        model[n_gram] = 0  # if n_gram is not already in *model*, add it with frequency 0
    #    if not other_model.contains_n_gram(n_gram):
    #        other_model[n_gram] = 0  # furthermore, if n_gram is not already in *other_model*, add it with frequency 0

# TODO: Remove?
# def get_unique_n_grams_from_models(n_gram_models):
#     unique_ngrams = set()
#     for model in n_gram_models:
#         unique_ngrams.update(model.get_n_grams())
#
#     return unique_ngrams


def create_rank_model(frequencies_model):
    # create a list of all unique frequency values
    unique_frequencies = list(set( list(frequencies_model.values()) ))

    # order this list downward
    unique_frequencies = sorted(unique_frequencies, reverse=True)

    # create ordered list of all possible ranks (1 to number of unique frequencies)
    ranks = list(range(1, len(unique_frequencies) + 1))

    # zip unique freq. and ranks together -> highest frequency will be related to lowest rank (i.e. 1) and so on
    rank_dict = dict(zip(unique_frequencies, ranks))

    # build rank model
    rank_model = {}
    for n_gram in frequencies_model.keys():
        frequency = frequencies_model[n_gram]  # get frequency of n_gram
        rank = rank_dict[frequency]            # get the rank of frequency
        rank_model[n_gram] = rank              # put n_gram and rank in rank_model

    return rank_model


class NGramSize:
    ONE     = 1
    TWO     = 2
    THREE   = 3
    FOUR    = 4
    FIVE    = 5
    SIX     = 6
    SEVEN   = 7
    EIGHT   = 8
