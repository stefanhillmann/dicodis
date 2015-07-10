from common.ngram.model_generator import NGramSize
from common.measuring.measures import MeasureName

validation_processes = 12

sizes = [
              #NGramSize.ONE,
              #NGramSize.TWO,
              NGramSize.THREE,
              #NGramSize.FOUR,
              #NGramSize.FIVE,
              #NGramSize.SIX,
              #NGramSize.SEVEN,
              #NGramSize.EIGHT
             ]

smoothing_values = [
                    0.05,
                    #0.25,
                    #0.5
                    ]

classifier_names = [
                    MeasureName.COSINE,
                    #MeasureName.JENSEN,
                    #MeasureName.KULLBACK_LEIBLER,
                    #MeasureName.MEAN_KULLBACK_LEIBLER,
                    #MeasureName.SYMMETRIC_KULLBACK_LEIBLER,
                    MeasureName.RANK_ORDER
                    ]

frequency_thresholds = [
                        1,
                        #2,
                        #3,
                        #4,
                        #5,
                        #6,
                        #7
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
    configurations = []
    for size in sizes:
        for classifier in classifier_names:
            for frequency_threshold in frequency_thresholds:
                for smoothing_value in smoothing_values:
                    configuration = Configuration(size, classifier, frequency_threshold, smoothing_value)
                    configurations.append(configuration)
    
    return configurations
