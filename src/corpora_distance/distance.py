import logging
from measuring import measures
from measuring.measures import MeasureName

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
        
    def computeDistance(self, n_gram_model, other_model):
        """
        Returns distance between a n_gram_model and a array of a corpus' n-grams.
        n_gram_model is used as reference model. That means, the distance calculation
        will only use n-grams which occurs in n_gram_model.
        
        Parameter:
        ----------
        n_gram_model: Dictionary
            n-gram-model of the original/reference corpus.
        other_n_grams: array
            ALL n-grams (NOT just the unique ones) of a corpus. These n-grams are
            used to compute a n-gram-model of the corpus to be compared against the
            original corpus (given by n-gram-model).
        """
        
        # compute distance between n_gram_model and other_model
        distance = self.measure.distance( n_gram_model.values(), other_model.values() )
        self.logger.debug('Computed distance with measure %s is %s', self.measure.__class__.__name__, distance)
        
        return distance
        
        

"""
Factory methods for Classifiers using different measurements
"""
    
def getCosineCalculator():
    return DistanceCalculator(measures.CosineMeasure(), "cosine")
    
def getKullbackLeiblerCalculator():
    return DistanceCalculator(measures.KullbackLeiblerMeasure(), "kullback_leibler")
    
def getMeanKullbackLeiblerCalculator():
    return DistanceCalculator(measures.MeanKullbackLeiblerMeasure(), "mean_kullback_leibler")
    
def getSymmetricKullbackLeiblerCalculator():
    return DistanceCalculator(measures.SymmetricKullbackLeiblerDistance(), "symmetric_kullback_leibler")
    
def getJensenCalculator():
    return DistanceCalculator(measures.JensenMeasure(), "jensen")


def getDistanceCalculator(measure_name):
    """
    Creates an instance of DistanceCalculator. The calculator will be
    initialized with the named distance measure.
    
    Parameters
    ----------
    measure_name: String (see MeasureName)
        Identifier of the  measure to be used.
    """
    
    created_calculator = "";
    
    if measure_name == MeasureName.COSINE:
        created_calculator = getCosineCalculator()
    elif measure_name == MeasureName.KULLBACK_LEIBLER:
        created_calculator = getKullbackLeiblerCalculator()
    elif measure_name == MeasureName.MEAN_KULLBACK_LEIBLER:
        created_calculator = getMeanKullbackLeiblerCalculator()
    elif measure_name == MeasureName.SYMMETRIC_KULLBACK_LEIBLER:
        created_calculator = getSymmetricKullbackLeiblerCalculator()
    elif measure_name == MeasureName.JENSEN:
        created_calculator = getJensenCalculator()
    else:
        """
        We return nothing, and the following code will crash, when trying to to do something
        with a not existing classifier 
        """
        print 'Unknown classifier was requested. Empty string will be returned'
        
    return created_calculator

        
