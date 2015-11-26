from common.ngram.model_generator import NGramSize
from common.measuring.measures import MeasureName
import ConfigParser

# read configuration
config = ConfigParser.ConfigParser()
config.read('local_config.ini')
validation_processes = config.getint('cross_validation', 'jobs')

sizes = [
              NGramSize.ONE,
              NGramSize.TWO,
              NGramSize.THREE,
              NGramSize.FOUR,
              NGramSize.FIVE,
              NGramSize.SIX,
              NGramSize.SEVEN,
              NGramSize.EIGHT
             ]

class Configuration:
    def __init__(self, size, classifier, frequency_threshold, smoothing_value):
        self.size                   = size
        self.classifier             = classifier
        self.frequency_threshold    = frequency_threshold
        self.smoothing_value        = smoothing_value
        
    def __repr__(self):
        return '[Size: {}, Classifier: {}, Threshold: {}, Smoothing Value: {}]'.format(self.size, self.classifier,
                                                                            self.frequency_threshold, self.smoothing_value)


def getConfigurations():
    configurations = list()

    # Rank Order
    # configurations.append(Configuration(sizes, MeasureName.RANK_ORDER, 1, 0.5))
    configurations.append(Configuration(sizes, MeasureName.RANK_ORDER, 2, 0.5))

    return configurations
