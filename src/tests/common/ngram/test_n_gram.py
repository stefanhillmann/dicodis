__author__ = 'Stefan Hillmann'

import unittest
import common.ngram.model_generator as mg
import common.util.names as names
import common.ngram.cached_n_grams as cng
from common.dialog_document.document import Document

class TestNGram(unittest.TestCase):

    def setUp(self):
        self.bi_gram_list = ['_#b', 'b#a', 'a#a', 'a#a', 'a#b', 'b#a', 'a#c', 'c#_']
        self.tri_gram_list = ['_#_#b', '_#b#a', 'b#a#a', 'a#a#a', 'a#a#b', 'a#b#a', 'b#a#c', 'a#c#_', 'c#_#_']
        self.token_list = ['b', 'a', 'a', 'a', 'b', 'a', 'c']

    def test_model_creation(self):
        model = mg.generate_model(self.bi_gram_list)
        self.assertEqual(model['_#b'], 1)
        self.assertEqual(model['b#a'], 2)
        self.assertEqual(model['a#a'], 2)
        self.assertEqual(model['a#b'], 1)
        self.assertEqual(model['a#c'], 1)
        self.assertEqual(model['c#_'], 1)

    def test_bi_gram_creation(self):
        document = Document(names.Class.POSITIVE, self.token_list, 'dialog_id')
        n_grams = mg.create_n_grams_from_document(document, 2)

        self.assertEqual(n_grams, self.bi_gram_list)

    def test_mixed_n_gram_creation(self):
        document = Document(names.Class.POSITIVE, self.token_list, 'dialog_id')
        n_grams = mg.create_n_grams_from_document(document, [2, 3])
        expected_result = list()
        expected_result.extend(self.bi_gram_list)
        expected_result.extend(self.tri_gram_list)

        # test if n_grams and expected_result contain the equal set of n-grams
        self.assertTrue(len(n_grams) is len(expected_result), "Number of elements has to be equal.")  # equal number of elements?

        # all expected elements are in n_grams?
        for x in expected_result:
            self.assertTrue(x in n_grams, "{0} is not in generated n-grams.".format(x))

    def test_get_n_grams_for_little_amount_of_tokens(self):
        tokens = ('a', 'b')
        expected_result = ['a', 'b', '_#a', 'a#b', 'b#_']
        document = Document(names.Class.POSITIVE, tokens, 'dialog_id')
        size = range(1, 8)
        result = mg.create_n_grams_from_document(document, size)

        self.assertEqual(len(result), len(expected_result))
        map(lambda x: self.assertTrue(x in result, "'{0}' is not in result.".format(x)), expected_result)

    def test_model_synchronization(self):
        # prepare to test models
        model = {'a': 1, 'b': 2}
        other_model = {'b': 3, 'c': 1}

        mg.synchronize_n_grams(model, other_model)  # synchronize models

        # check results
        self.assertEqual(len(model), 3)
        self.assertEqual(model['a'], 1)
        self.assertEqual(model['b'], 2)
        self.assertEqual(model['c'], 0)
        self.assertEqual(len(model), 3)
        self.assertEqual(other_model['a'], 0)
        self.assertEqual(other_model['b'], 3)
        self.assertEqual(other_model['c'], 1)

    def test_probability_computation_case_1(self):
        # model does not contain 0 and l == 0.0 -> no smoothing
        model = {'a': 1, 'b': 2, 'c': 3}
        mg.compute_probabilities(model, 0.0)
        self.assertEqual(model['a'], 1 / 6.0)
        self.assertEqual(model['b'], 2 / 6.0)
        self.assertEqual(model['c'], 3 / 6.0)

    def test_probability_computation_case_2(self):
        # model does not contain 0 and l > 0.0 -> no smoothing
        model = {'a': 1, 'b': 2, 'c': 3}
        mg.compute_probabilities(model, 0.5)
        self.assertEqual(model['a'], 1 / 6.0)
        self.assertEqual(model['b'], 2 / 6.0)
        self.assertEqual(model['c'], 3 / 6.0)

    def test_probability_computation_case_3(self):
        # model contains 0 and l == 0.0 -> no smoothing
        model = {'a': 0, 'b': 2, 'c': 3}
        mg.compute_probabilities(model, 0.0)
        self.assertEqual(model['a'], 0 / 5.0)
        self.assertEqual(model['b'], 2 / 5.0)
        self.assertEqual(model['c'], 3 / 5.0)

    def test_probability_computation_case_4(self):
        # model contains 0 and l > 0.0 -> no smoothing
        model = {'a': 0, 'b': 2, 'c': 3}
        mg.compute_probabilities(model, 0.5)
        self.assertEqual(model['a'], 0.5 / 6.5)
        self.assertEqual(model['b'], 2.5 / 6.5)
        self.assertEqual(model['c'], 3.5 / 6.5)



if __name__ == "__main__":
    unittest.main()
