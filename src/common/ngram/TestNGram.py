__author__ = 'Stefan Hillmann'

import unittest
import model_generator as mg
from common.dialog_document.document import Document

class TestNGram(unittest.TestCase):

    def setUp(self):
        self.bi_gram_list = ['_#b', 'b#a', 'a#a', 'a#a', 'a#b', 'b#a', 'a#c', 'c#_']
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
        document = Document('label', self.token_list, 'dialog_id')
        n_grams = mg.create_n_grams_from_document(document, 2)

        self.assertEqual(n_grams, self.bi_gram_list)

if __name__ == "__main__":
    unittest.main()
