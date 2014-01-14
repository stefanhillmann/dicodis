from ngram.model_generator import NGramSize
from measures.measures import MeasureName

validation_processes = 12

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

classifier_names = [
                    MeasureName.COSINE,
                    MeasureName.JENSEN,
                    MeasureName.KULLBACK_LEIBLER,
                    MeasureName.MEAN_KULLBACK_LEIBLER,
                    MeasureName.SYMMETRIC_KULLBACK_LEIBLER
                    ]

frequency_thresholds = [
                        1,
                        2,
                        3,
                        4,
                        5,
                        6,
                        7
                        ]

class Configuration:
    def __init__(self, size, classifier, frequency_threshold):
        self.size = size
        self.classifier = classifier
        self.frequency_threshold = frequency_threshold
        
def getConfigurations():
    configurations = []
    for size in sizes:
        for classifier in classifier_names:
            for frequency_threshold in frequency_thresholds:
                configuration = Configuration(size, classifier, frequency_threshold)
                configurations.append(configuration)
    
    return configurations
