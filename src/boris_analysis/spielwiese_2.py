import common.dialog_document.dialog_reader
from boris_analysis import dialogs
import common.ngram.model_generator as mg
import common.classify.classifier as classifier

id_column_name = 'iteration'
positive_class = 'succeeded'
negative_class = 'failed'

file_turns_succeeded        = '/home/stefan/git/DialogueClassifying/data/turnsSucceeded.csv'

positive_reader = common.dialog_document.dialog_reader.DialogsReader(file_turns_succeeded)
positive_dialogs = dialogs.create_dialogs_documents(positive_reader, id_column_name, positive_class)

n_grams = mg.create_n_grams_from_document(positive_dialogs[0], 1)
n_grams_2 = mg.create_n_grams_from_document(positive_dialogs[1], 1)

c = classifier.get_cosine_classifier()

c.add_class("foo", n_grams, 1)

c.classify(n_grams_2)