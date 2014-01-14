from ngram import model_generator, export
import util.list as lu
import dialogs
from util import time_util
from corpora_distance import distance
from ngram.model_generator import NGramSize
from measures.measures import MeasureName


l_values = [
            0.05,
            0.25,
            0.5
            ]

n_size = [
              NGramSize.ONE,
              NGramSize.TWO,
              NGramSize.THREE,
              NGramSize.FOUR,
              NGramSize.FIVE,
              NGramSize.SIX,
              NGramSize.SEVEN,
              NGramSize.EIGHT
             ]

measures = [
                    MeasureName.COSINE,
                    MeasureName.JENSEN,
                    MeasureName.KULLBACK_LEIBLER,
                    MeasureName.MEAN_KULLBACK_LEIBLER,
                    MeasureName.SYMMETRIC_KULLBACK_LEIBLER
                    ]

file_turns_succeeded        = '../data/turnsSucceeded.csv'
file_turns_failed           = '../data/turnsFailed.csv'

file_best_simulation        = '../data/bestSimulation.csv'
file_worst_simulation       = '../data/worstSimulation.csv'

file_shortest_interaction   = '../data/shortest49Interactions.csv'
file_longest_interaction    = '../data/longest49Interactions.csv'

file_wa_100                 = '../data/WA_60.csv'
file_wa_60                  = '../data/WA_100.csv'

file_reference              = '../data/annotatedData_corrected.csv'


def printResult():
    for line in data:
        print ' '.join(line)
        
def writeCsvFile():
    file_name = time_util.humanReadableTimestamp() + '__distancies.csv'
    path = '../results/' + file_name
    f = open(path, 'w')
    for line in data:
        f.write( ";".join(line) + '\n' )
    f.close()
        
def createNGramModel(documents, n):
    documents_contents = []
    for document in documents:
        documents_contents.append(document.content)
    n_grams = model_generator.create_ngrams(documents_contents, n)
    class_model = model_generator.createNgramModel( lu.uniqueValues(n_grams), n_grams )
    
    return class_model

def getReaderDocuments(reader):
    documents_contents = []
    documents = dialogs.createDialogsDocuments(reader, 'iteration', 'default_class')
    for document in documents:
        documents_contents.append(document.content)
        
    return documents_contents

def getFileDocuments(f):
    reader = dialogs.DialogsReader(f)
        
    return getReaderDocuments(reader)

def getDistance(f_1, f_2, n, l, calculator):
    documents_1 = getFileDocuments(f_1)
    documents_2 = getFileDocuments(f_2)
    n_grams_1 = model_generator.create_ngrams(documents_1, n)
    n_grams_2 = model_generator.create_ngrams(documents_2, n)
        
    # create all list of all n-grams (reference and other corpus), in order to
    # compute the unique n-grams from both corpora.
    all_n_grams = list(n_grams_1)
    all_n_grams.extend(n_grams_2)
    unique_n_grams = lu.uniqueValues(all_n_grams)
        
    # create smoothed n-gram-models
    model_1 = model_generator.createNgramModel(unique_n_grams, n_grams_1)
    model_2 = model_generator.createNgramModel(unique_n_grams, n_grams_2)
    
    # for debugging
    #export.toCSV(model_1, '/home/stefan/temp/reference_model.csv')
    #export.toCSV(model_2, '/home/stefan/temp/other_model.csv')
    
    # smooth both models
    smoothed_1 = model_generator.smoothModel(model_1, l)
    smoothed_2 = model_generator.smoothModel(model_2, l)
        
        
    # compute distance
    distance = calculator.computeDistance(smoothed_1, smoothed_2)
        
    return distance
        
data = [['measure', 'reference', 'other', 'l','n', 'distance']]

for measure_name in measures:
    for n in n_size:
        for l in l_values:

            calculator = distance.getDistanceCalculator(measure_name)
            print 'Run for {} with n = {} and l = {}'.format(calculator.name, n, l)
            
            # reference vs reference
            print 'reference vs reference'
            d = getDistance(file_reference, file_reference, n, l, calculator)
            data.append( [calculator.name, 'reference', 'reference', str(l), str(n), str(d)] )
            
            # reference vs worst_simulation
            print 'reference vs worst_simulation'
            d = getDistance(file_reference, file_worst_simulation, n, l, calculator)
            data.append( [calculator.name, 'reference', 'worst_sim', str(l), str(n), str(d)] )
            
            # reference vs best simulation
            print 'reference vs best simulation'
            d = getDistance(file_reference, file_best_simulation, n, l, calculator)
            data.append( [calculator.name, 'reference', 'best_sim', str(l), str(n), str(d)] )
            
            # succeeded vs failed
            print 'succeeded vs failed'
            d = getDistance(file_turns_succeeded, file_turns_failed, n, l, calculator)
            data.append( [calculator.name, 'successful', 'failed', str(l), str(n), str(d)] )
            
            # longest vs shortest
            print 'longest vs shortest'
            d = getDistance(file_longest_interaction, file_shortest_interaction, n, l, calculator)
            data.append( [calculator.name, 'longest', 'shortest', str(l), str(n), str(d)] )
            
            # wa_100 vs wa_60
            print 'wa_100 vs wa_60'
            d = getDistance(file_wa_100, file_wa_60, n, l, calculator)
            data.append( [calculator.name, 'wa_100', 'wa_60', str(l), str(n), str(d)] )
        
printResult()
writeCsvFile()     
        
