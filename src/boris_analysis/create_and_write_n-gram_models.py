import common.dialog_document.dialog_reader
from common.ngram import export
from common.ngram import model_generator
import common.util.list as lu
from boris_analysis import dialogs

data_directory = '/home/stefan/git/DialogueClassifying/data/'


file_turns_succeeded        = data_directory + 'turnsSucceeded.csv'
file_turns_failed           = data_directory + 'turnsFailed.csv'

file_best_simulation        = data_directory + 'bestSimulation.csv'
file_worst_simulation       = data_directory + 'worstSimulation.csv'

file_shortest_interaction   = data_directory + 'shortest49Interactions.csv'
file_longest_interaction    = data_directory + 'longest49Interactions.csv'

file_wa_100                 = data_directory + 'WA_60.csv'
file_wa_60                  = data_directory + 'WA_100.csv'

reader = common.dialog_document.dialog_reader.DialogsReader(file_turns_failed)
dialog_documents = dialogs.create_dialogs_documents(reader, 'iteration', 'default_class')

documents_contents = []
for document in dialog_documents:
    documents_contents.append(document.content)
    
n_grams = model_generator.create_ngrams(documents_contents, 3)
class_model = model_generator.create_n_gram_model( lu.unique_values(n_grams), n_grams )

export.to_csv(class_model, '/home/stefan/temp/csv_export_absolute.csv')

model_generator.compute_probabilities(class_model)

export.to_csv(class_model, '/home/stefan/temp/csv_export_relative.csv')

print class_model