# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 17:19:42 2013

@author: Stefan Hillmann (stefan.hillmann@tu-berlin.de)
"""
import numpy as np
from math import sqrt
import logging
from abc import ABCMeta, abstractmethod
from common.util import dict as du
from common.ngram import model_generator as mg


module_logger = logging.getLogger('measures')


def cosine_similarity(p, q):
    """
    Computes the cosine similarity between the vectors p and q.
    p and q can contain either frequencies or relative probabilities.
    """
    module_logger.debug('Computing cosine similarity for p = %s and q = %s', p, q)
    
    cs = np.dot(p, q) / ( sqrt( np.dot(p, p) * np.dot(q, q) ) )
    return cs


def kullback_leibler_divergence(p, q):
    """
    Computes the Kullback-Leibler divergence between vectors p and q.
    p and q have to contain probabilities.
    """
    
    _p = np.array(p)
    _q = np.array(q)
    
    t = -_q * np.log(_p)
    s = -_q * np.log(_q)
    
    return np.sum(t - s)


def mean_kullback_leibler_distance(p, q):
    """
    Commutes the Mean Kullback-Leibler Divergence between vectors p and q.
    p and q have to contain probabilities.
    """
    # compute KBL(p, q)
    kbl_p_q = kullback_leibler_divergence(p, q)
    
    # compute KBL(q, p)
    kbl_q_p = kullback_leibler_divergence(q, p)
    
    # compute mean of both divergences
    mean_kbl = (kbl_p_q + kbl_q_p) / 2
    
    return mean_kbl


def symmetric_kullback_leibler_distance(p, q):
    """
    Commutes the Symmetric Kullback-Leibler Divergence between vectors p and q.
    Symmetric means that D(p||q) == D(q||p), but it is not just a mean value
    as the Mean Kullback-Leibler Divergence.
    p and q have to contain probabilities.
    """
    _p = np.array(p)
    _q = np.array(q)
    
    v = (_p - _q) * np.log(_p / _q)
    
    return sum(v)


def jensen_distance(p, q):
    """
    Computes the Jensen Distance between vectors p and q.
    p and q have to contain probabilities.
    """
    module_logger.debug('Computing jensen for p = %s and q = %s', p, q)
    
    _p = np.array(p)
    _q = np.array(q)
        
    s = _p * np.log(_p)
    t = _q * np.log(_q)
    u = (_p + _q) / 2
    
    v = ((s + t) / 2) - (u * np.log(u))
    
    return sum(v)


def rank_order_distance(x, y):
    """
    Computes the Rank Order Distance between the rank models x and y.
    x and y have to contain n-grams and their related ranks (which are usually
    not equal to the frequency of the n-grams!).
    """
    module_logger.debug('Computing rank order distance for x = %s and y = %s', x, y)

    distance = 0
    min_rank = min(min(x.values()), min(y.values()))  # get minimum rank from both models (probably always 1)
    max_rank = max(max(x.values()), max(y.values()))  # get the maximum rank from both models

    # The default difference is used, if a n-gram is only part of one list.
    # The default distance should be greater than any other distance. -> +1
    default_difference = max_rank - min_rank + 1

    # collect all unique n_grams
    n_grams = set()
    n_grams.update(x.keys())
    n_grams.update(y.keys())

    # compute for each n-gram the rank difference between both models
    # if a n-gram is contained in only on model, then use the default difference
    for n_gram in n_grams:
        difference = default_difference

        if n_gram in x and n_gram in y:
            difference = abs(x[n_gram] - y[n_gram])  # compute the difference

        distance += difference  # add n-gram difference to total distance

    return distance


"""
Measure implementations
"""


def prepare_for_probability_based_measure(x, y, l):
    """
    Prepares the n-gram models (dict) *x* and *y* in a way, that they can be used with measures which base on the
    comparison of probability distributions. In short it does the following:
    1. synchronize both models (afterwards both model have the same length, i.e. contain the same n-grams (with
    different values about the frequencies!)
    2. order n-gram in both models alphabetical
    3. compute the relative probabilities of n-grams and smooth the model (if l > 0.0 and the model contains a n-gram
    with a frequency of 0)
    :param x: a n-gram model with absolute frequencies
    :param y: a n-gram model with absolute frequencies
    :param l: smoothing factor lambda
    :return: nothing, but *x* and *y* are changed in place. *x* and *y* contain relative probabilities when the method
    returns.
    """
    # both models need to have same length
    mg.synchronize_n_grams(x, y)

    # sort both models by their n-grams
    du.sort_by_key(x)
    du.sort_by_key(y)

    # compute relative probabilities (depending on *l*, smoothing is either performed or not performed)
    mg.compute_probabilities(x, l)
    mg.compute_probabilities(y, l)



class Measure:
    __metaclass__ = ABCMeta

    @abstractmethod
    def distance(self, x, y, l):
        print 'Has to be implemented by sub classes.'
        pass


class CosineMeasure(Measure):
    def distance(self, x, y, l):
        """
        Computes the _cosine distance_ between *x* and *y*.
        The computed distance ranges
        from 0 (no difference) to 1 (maximal possible difference).
        Internally it computes the cosine similarity between *x* and *y* and subtracts the result from 1.
        Usually one will perform smoothing, otherwise it leads to a division by zero if a n-gram exists in the one model
        but not in the other.
        :param x: n-grm model (dict) with absolute frequencies
        :param y: n-gram model (dict) with absolute frequencies
        :param l: smoothing factor (lambda). I *l* == 0, smoothing is _not_ executed.
        :return: a float value between 0 and 1.
        """
        _x = x.copy()
        _y = y.copy()
        prepare_for_probability_based_measure(_x, _y, l)

        similarity = cosine_similarity(_x.values(), _y.values())
        
        """
        In order to get the distance we subtract the similarity from 1.
        That works because the similarity is always between 1 and 0.
        We do that to follow the behavior of the other distance measures:
        The higher the distance, the higher the difference between p and q.
        """
        return 1 - similarity

class KullbackLeiblerMeasure(Measure):
    def distance(self, x, y, l):
        """
        Computes the _Kullback-Leibler distance_ (klb) between *x* and *y*.
        The computed distance ranges
        from 0 (no difference) to 1 (maximal possible difference).
        Usually one will perform smoothing, otherwise it leads to a division by zero if a n-gram exists in the one model
        but not in the other.
        :param x: n-grm model (dict) with absolute frequencies
        :param y: n-gram model (dict) with absolute frequencies
        :param l: smoothing factor (lambda). I *l* == 0, smoothing is _not_ executed.
        :return: a float value between 0 and 1.
        """
        _x = x.copy()
        _y = y.copy()
        prepare_for_probability_based_measure(_x, _y, l)
        divergence = kullback_leibler_divergence(_x.values(), _y.values())
        return divergence

class MeanKullbackLeiblerMeasure(Measure):
    def distance(self, x, y, l):
        """
        Computes the _mean Kullback-Leibler distance_ between (mklb) *x* and *y*.
        mklb = (klb(x, y) + klb(y, x) / 2), compare KullbackLeiblerMeasure.distance().
        mklb(x, y) is equal to mklb(y, x).
        2 * mklb(x, y) = sklb(x, y), compare SymmetricKullbackLeiblerMeasure.distance(). ATTENTION: the implementation
        uses the original formula.
        The computed distance ranges
        from 0 (no difference) to 1 (maximal possible difference).
        Usually one will perform smoothing, otherwise it leads to a division by zero if a n-gram exists in the one model
        but not in the other.
        :param x: n-grm model (dict) with absolute frequencies
        :param y: n-gram model (dict) with absolute frequencies
        :param l: smoothing factor (lambda). I *l* == 0, smoothing is _not_ executed.
        :return: a float value between 0 and 1.
        """
        _x = x.copy()
        _y = y.copy()
        prepare_for_probability_based_measure(_x, _y, l)
        distance = mean_kullback_leibler_distance(_x.values(), _y.values())
        return distance

class SymmetricKullbackLeiblerDistance(Measure):
    def distance(self, x, y, l):
        """
        Computes the _symmetric Kullback-Leibler distance_ (sklb) between *x* and *y*.
        sklb(x, y) is equal to sklb(y, x).
        sklb(x, y) = 2 * mklb(x, y), compare MeanKullbackLeiblerMeasure.distance().
        The computed distance ranges
        from 0 (no difference) to 1 (maximal possible difference).
        Usually one will perform smoothing, otherwise it leads to a division by zero if a n-gram exists in the one model
        but not in the other.
        :param x: n-grm model (dict) with absolute frequencies
        :param y: n-gram model (dict) with absolute frequencies
        :param l: smoothing factor (lambda). I *l* == 0, smoothing is _not_ executed.
        :return: a float value between 0 and 1.
        """
        _x = x.copy()
        _y = y.copy()
        prepare_for_probability_based_measure(_x, _y, l)
        distance = symmetric_kullback_leibler_distance(_y.values(), _y.values())
        return distance

class JensenMeasure(Measure):
    def distance(self, x, y, l):
        """
        Computes the _jensen divergence_ between *x* and *y*. The computed distance ranges
        from 0 (no difference) to 1 (maximal possible difference).
        Usually one will perform smoothing, otherwise it leads to a division by zero if a n-gram exists in the one model
        but not in the other.
        :param x: n-grm model (dict) with absolute frequencies
        :param y: n-gram model (dict) with absolute frequencies
        :param l: smoothing factor (lambda). I *l* == 0, smoothing is _not_ executed.
        :return: a float value between 0 and 1.
        """
        _x = x.copy()
        _y = y.copy()
        prepare_for_probability_based_measure(_x, _y, l)
        distance = jensen_distance(_x.values(), _y.values())
        return distance

class RankOrderDistanceMeasure(Measure):
    def distance(self, x, y, l):
        """
        Computes the _rank order distance_ between *x* and *y*. The computed distance ranges from 0 (no distance)
        til any value less than infinite. As greater the value, as higher the distance.
        :param x: n-grm model (dict) with absolute frequencies
        :param y: n-gram model (dict) with absolute frequencies
        :param l: _not used_ in the rank order algorithm, but defined by the interface.
        :return: an integer value between 0 (no difference) and any integer value greater than 0.
        """
        x_rank_model = mg.create_rank_model(x)
        y_rank_model = mg.create_rank_model(y)

        distance = rank_order_distance(x_rank_model, y_rank_model)
        return distance

class MeasureName:
    COSINE                      = 'cosine'
    KULLBACK_LEIBLER            = 'kullback leibler'
    MEAN_KULLBACK_LEIBLER       = 'mean kullback leibler'
    SYMMETRIC_KULLBACK_LEIBLER  = 'symmetric kullback leibler'
    JENSEN                      = 'jensen'
    RANK_ORDER                  = 'rank order'


