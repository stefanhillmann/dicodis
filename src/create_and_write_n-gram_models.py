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

reader = dialogs.DialogsReader(file_turns_failed)
dialog_documents = dialogs.createDialogsDocuments(reader, 'iteration', 'default_class')

documents_contents = []
for document in dialog_documents:
    documents_contents.append(document.content)
    
n_grams = model_generator.create_ngrams(documents_contents, 3)
class_model = model_generator.createNgramModel( lu.uniqueValues(n_grams), n_grams )

export.toCSV(class_model, '/home/stefan/temp/csv_export_absolute.csv')

model_generator.computeProbabilities(class_model)

export.toCSV(class_model, '/home/stefan/temp/csv_export_relative.csv')

print class_model