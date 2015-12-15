import logging

from common.measuring import measures
from common.measuring.measures import MeasureName
from common.ngram import model_generator as mg
from common.ngram.n_gram_model import NGramModel
from common.util import rank as rank_util


class DistanceCalculator:
    
    SMOOTHING_VALUE = 0.05
    
    def __init__(self, measure, name):
        """
        Constructor of DistanceCalculator.
        
        Parameters
        ----------
        measure: Measure (a concrete implementation of it)
            The implementation of Measure to be used in the calculator.
        name: String
            Name of the calculator (e.g.; for the usage in log and result's files.
        """
        self.logger = logging.getLogger('corora_distance.distance.DistanceCalculator')
        self.logger.debug('Create new Classifier (%s) for with measure: %s', name, measure.__class__.__name__)
        
        self.classes = {}
        self.class_models = {}
        self.measure = measure
        self.name = name
        
    def compute_distance(self, n_gram_model, other_model, l):
        """
        Returns distance between a n_gram_model and a array of a corpus' n-grams.
        n_gram_model is used as reference model. That means, the distance calculation
        will only use n-grams which occurs in n_gram_model.
        
        Parameter:
        ----------
        n_gram_model: NGramModel
            n-gram-model of the original/reference corpus.
        other_n_grams: array
            ALL n-grams (NOT just the unique ones) of a corpus. These n-grams are
            used to compute a n-gram-model of the corpus to be compared against the
            original corpus (given by n-gram-model).
        l: float
            Smoothing factor lambda.
        """

        if type(n_gram_model) is not NGramModel:
            raise ValueError('Type of parameter n_gram_model is not NGramModel.')

        if type(n_gram_model) is not NGramModel:
            raise ValueError('Type of parameter other_model is not NGramModel.')
        
        # compute distance between n_gram_model and other_model
        distance = self.measure.distance(n_gram_model, other_model, l)
        self.logger.debug('Computed distance with measure %s is %s', self.measure.__class__.__name__, distance)
        
        return distance


"""
Factory methods for Classifiers using different measurements
"""


def get_cosine_calculator():
    return DistanceCalculator(measures.CosineMeasure(), MeasureName.COSINE)


def get_kullback_leibler_calculator():
    return DistanceCalculator(measures.KullbackLeiblerMeasure(), MeasureName.KULLBACK_LEIBLER)


def get_mean_kullback_leibler_calculator():
    return DistanceCalculator(measures.MeanKullbackLeiblerMeasure(), MeasureName.MEAN_KULLBACK_LEIBLER)


def get_symmetric_kullback_leibler_calculator():
    return DistanceCalculator(measures.SymmetricKullbackLeiblerDistance(), MeasureName.SYMMETRIC_KULLBACK_LEIBLER)


def get_jensen_calculator():
    return DistanceCalculator(measures.JensenMeasure(), MeasureName.JENSEN)


def get_rank_order_calculator():
    return DistanceCalculator(measures.RankOrderDistanceMeasure(), MeasureName.RANK_ORDER)


def get_normalized_rank_order_calculator():
    return DistanceCalculator(measures.NormalizedRankOrderDistanceMeasure(), MeasureName.NORMALIZED_RANK_ORDER)


def get_distance_calculator(measure_name):
    """
    Creates an instance of DistanceCalculator. The calculator will be
    initialized with the named distance measure.
    
    Parameters
    ----------
    measure_name: String (see MeasureName)
        Identifier of the  measure to be used.
    """
    
    created_calculator = ""
    
    if measure_name == MeasureName.COSINE:
        created_calculator = get_cosine_calculator()
    elif measure_name == MeasureName.KULLBACK_LEIBLER:
        created_calculator = get_kullback_leibler_calculator()
    elif measure_name == MeasureName.MEAN_KULLBACK_LEIBLER:
        created_calculator = get_mean_kullback_leibler_calculator()
    elif measure_name == MeasureName.SYMMETRIC_KULLBACK_LEIBLER:
        created_calculator = get_symmetric_kullback_leibler_calculator()
    elif measure_name == MeasureName.JENSEN:
        created_calculator = get_jensen_calculator()
    elif measure_name == MeasureName.RANK_ORDER:
        created_calculator = get_rank_order_calculator()
    elif measure_name == MeasureName.NORMALIZED_RANK_ORDER:
        created_calculator = get_normalized_rank_order_calculator()
    else:
        """
        We return nothing, and the following code will crash, when trying to to do something
        with a not existing classifier 
        """
        raise ValueError("Unknown measure name '{0}. Cannot create distance calculator.".format(measure_name))
        
    return created_calculator

"""
Special functions for the single measures.
"""


def rank_order_normalized_distance(p, q, distance_p_q):

    p_r = mg.create_rank_model(p)  # rank model of p
    q_r = mg.create_rank_model(q)  # rank model of q

    min_rank = rank_util.min_rank([p_r.values(), q_r.values()])  # get minimum rank from both models (probably always 1)
    max_rank = rank_util.max_rank([p_r.values(), q_r.values()])  # get the maximum rank from both models

    default_distance = max_rank + min_rank + 1  # distance for an n-gram which is contained by only one model (p or q)

    # maximum possible distance between p and q (all n-grams are only part of either p or q)
    max_distance = (len(p_r) + len(q_r)) * default_distance

    normalized_distance = distance_p_q / max_distance
    return normalized_distance
