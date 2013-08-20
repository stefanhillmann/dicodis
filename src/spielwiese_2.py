from util import list as lu
import dialogs
import ngram
import classifier

id_column_name = 'iteration'
positive_class = 'succeeded'
negative_class = 'failed'

file_turns_succeeded        = '/home/stefan/git/dialogue_classifier/data/turnsSucceeded.csv'

positive_reader = dialogs.DialogsReader(file_turns_succeeded)
positive_dialogs = dialogs.createDialogsDocuments(positive_reader, id_column_name, positive_class)

contents = [positive_dialogs[0].content]

contents_2 = [positive_dialogs[1].content]

n_grams = ngram.create_ngrams(contents, 1)
n_grams_2 = ngram.create_ngrams(contents_2, 1)

c = classifier.getCosineClassifier()

c.addClass("foo", n_grams, 1);

c.classify(n_grams_2)