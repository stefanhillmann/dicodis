from ngram import model_generator, export
import util.list as lu
import dialogs

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
n = 3

for name in files.keys():
    reader = dialogs.DialogsReader( files[name] )
    dialog_documents = dialogs.createDialogsDocuments(reader, 'iteration', 'default_class')
    
    documents_contents = []
    for document in dialog_documents:
        documents_contents.append(document.content)
    
    n_grams = model_generator.create_ngrams(documents_contents, n)
    class_model = model_generator.createNgramModel( lu.uniqueValues(n_grams), n_grams )
    number_of_unique_n_grams = len(class_model)

    line = [name, str(n), str(number_of_unique_n_grams)]
    print " ".join(line)
