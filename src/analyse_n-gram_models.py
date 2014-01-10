from ngram import model_generator, export
import util.list as lu
import dialogs
from util import time_util


def printResult():
    for line in data:
        print SEPARATOR.join(line)
        
def writeCsvFile():
    file_name = time_util.humanReadableTimestamp() + '__n-ngram_counts.csv'
    path = '../results/' + file_name
    f = open(path, 'w')
    for line in data:
        f.write( ";".join(line) + '\n' )
    f.close()
        
def countTotalNGrams(model):
    count = 0
    for key in model.keys():
        count += model[key]
        
    return count
    

SEPARATOR = " "
N_MIN = 1
N_MAX = 8
T_MIN = 1
T_MAX = 7

file_turns_succeeded        = '../data/turnsSucceeded.csv'
file_turns_failed           = '../data/turnsFailed.csv'

file_best_simulation        = '../data/bestSimulation.csv'
file_worst_simulation       = '../data/worstSimulation.csv'

file_shortest_interaction   = '../data/shortest49Interactions.csv'
file_longest_interaction    = '../data/longest49Interactions.csv'

file_wa_100                 = '../data/WA_60.csv'
file_wa_60                  = '../data/WA_100.csv'

files = {'successful' : file_turns_succeeded, 'failed' : file_turns_failed, 'best_sim' : file_best_simulation,
         'worst_sim' : file_worst_simulation, 'shortest' : file_shortest_interaction,
         'longest': file_longest_interaction, 'wa_100' : file_wa_100, 'wa_60' : file_wa_60}
data = [['name', 'n', 'threshold','unique_n-grams', 'total_n-grams']]

for n in xrange(N_MIN, N_MAX + 1):
    print 'Run for n = {}'.format(n)
    for name in files.keys():
        print '    Run for class {}'.format(name)
        reader = dialogs.DialogsReader( files[name] )
        dialog_documents = dialogs.createDialogsDocuments(reader, 'iteration', 'default_class')
        
        documents_contents = []
        for document in dialog_documents:
            documents_contents.append(document.content)
        
        n_grams = model_generator.create_ngrams(documents_contents, n)
        class_model = model_generator.createNgramModel( lu.uniqueValues(n_grams), n_grams )
        
        for t in xrange(T_MIN, T_MAX + 1):
            print '        Run for t = {}'.format(t)
            class_model = model_generator.remove_rare_n_grams(class_model, t)
            
            number_of_unique_n_grams = len(class_model)
            total_n_grams = int( countTotalNGrams(class_model) )
        
            line = [name, str(n), str(t), str(number_of_unique_n_grams), str(total_n_grams)]
            data.append(line)
        
printResult()
writeCsvFile()     
        
