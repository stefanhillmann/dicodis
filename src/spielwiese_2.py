import ngram
import util.list as lu

docs = [['a', 'a' , 'a', 'b']]


class_n_grams = ngram.create_ngrams(docs, 1)
print class_n_grams


class_model = ngram.createNgramModel( lu.uniqueValues(class_n_grams), class_n_grams )
class_model, class_n_grams = ngram.remove_rare_n_grams(class_model, class_n_grams, 2)

print class_model
print class_n_grams

