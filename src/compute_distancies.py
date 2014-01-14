from ngram import model_generator, export
import util.list as lu
import dialogs
from util import time_util
from corpora_distance import distance


def printResult():
    for line in data:
        print ' '.join(line)
        
def writeCsvFile():
    file_name = time_util.humanReadableTimestamp() + '__n-ngram_counts.csv'
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

def getDocuments(reader):
    documents_contents = []
    documents = dialogs.createDialogsDocuments(reader, 'iteration', 'default_class')
    for document in documents:
        documents_contents.append(document.content)
        
    return documents_contents
        

SMOOTHIG_VALUE = 0.25
N_MIN = 3
N_MAX = 3
T_MIN = 1
T_MAX = 1

file_turns_succeeded        = '../data/turnsSucceeded.csv'
file_turns_failed           = '../data/turnsFailed.csv'

file_best_simulation        = '../data/bestSimulation.csv'
file_worst_simulation       = '../data/worstSimulation.csv'

file_shortest_interaction   = '../data/shortest49Interactions.csv'
file_longest_interaction    = '../data/longest49Interactions.csv'

file_wa_100                 = '../data/WA_60.csv'
file_wa_60                  = '../data/WA_100.csv'

files = {#'successful' : file_turns_succeeded,
         #'failed' : file_turns_failed,
         'best_sim' : file_best_simulation,
         'worst_sim' : file_worst_simulation,
         #'shortest' : file_shortest_interaction,
         #'longest': file_longest_interaction,
         #'wa_100' : file_wa_100,
         #'wa_60' : file_wa_60
         }
data = [['measure', 'reference', 'other', 'threshold','n', 'distance']]


calculator = distance.getCosineCalculator()


reference_reader = dialogs.DialogsReader( '../data/annotatedData_corrected.csv' )
reference_documents = getDocuments(reference_reader)


for n in xrange(N_MIN, N_MAX + 1):
    print 'Run for n = {}'.format(n)
    for name in files.keys():
        print '    Run for corpus {}'.format(name)
        reader = dialogs.DialogsReader( files[name] )
        other_documents = getDocuments(reader)
        
        reference_n_grams = model_generator.create_ngrams(reference_documents, n)
        other_n_grams = model_generator.create_ngrams(other_documents, n)
        
        # create all list of all n-grams (reference and other corpus), in order to
        # compute the unique n-grams from both corpora.
        all_n_grams = list(reference_n_grams)
        all_n_grams.extend(other_n_grams)
        unique_n_grams = lu.uniqueValues(all_n_grams)
        
        # create smoothed n-gram-models
        reference_model = model_generator.createNgramModel(unique_n_grams, reference_n_grams)
        other_model     = model_generator.createNgramModel(unique_n_grams, other_n_grams)
        
        export.toCSV(reference_model, '/home/stefan/temp/reference_model.csv')
        export.toCSV(other_model, '/home/stefan/temp/other_model.csv')
        
        
        for t in xrange(T_MIN, T_MAX + 1):
            print '        Run for t = {}'.format(t)
            #reference_model = model_generator.remove_rare_n_grams(reference_model, t)
            #other_model     = model_generator.remove_rare_n_grams(other_model, t)
            
            smooth_reference_model = model_generator.smoothModel(reference_model, SMOOTHIG_VALUE)
            smooth_other_model     = model_generator.smoothModel(other_model, SMOOTHIG_VALUE)
            
            export.toCSV(smooth_reference_model, '/home/stefan/temp/smooth_reference_model.csv')
            export.toCSV(smooth_other_model, '/home/stefan/temp/smooth_other_model.csv')
                        
            distance = calculator.computeDistance(smooth_reference_model, smooth_other_model)
        
            line = [calculator.name, 'empirical', name, str(t), str(n), str( round(distance, 6) )]
            data.append(line)
        
printResult()
#writeCsvFile()     
        
