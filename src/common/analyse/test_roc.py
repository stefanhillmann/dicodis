"""
Created on Tue Jul 23 11:32:00 2015

@author: Stefan Hillmann (stefan.hillmann@tu-berlin.de)
"""

import unittest
import roc
from common.util.names import Class

class TestROC(unittest.TestCase):

    def test_get_roc_points(self):
        # TODO: Test an umgedehte Reihenfolge anpassen!

        ids = ['a', 'b', 'c', 'd', 'e']

        probabilities = {'a': 0.5, 'b': 0.7, 'c': 0.8, 'd': 0.3, 'e': 0.8}

        true_classes = {'a': Class.POSITIVE, 'b': Class.POSITIVE, 'c': Class.POSITIVE, 'd': Class.NEGATIVE,
                        'e': Class.NEGATIVE}

        roc_points = roc.get_roc_points(ids, probabilities, true_classes, Class.POSITIVE, Class.NEGATIVE)

        fp_rate = roc_points['fp_rate']
        tp_rate = roc_points['tp_rate']

        self.assertEqual(fp_rate[0], 0.0)
        self.assertEqual(fp_rate[1], 0.5)
        self.assertEqual(fp_rate[2], 0.5)
        self.assertEqual(fp_rate[3], 0.5)
        self.assertEqual(fp_rate[4], 1.0)

        self.assertEqual((round(tp_rate[0], 3)), 0.0)
        self.assertEqual((round(tp_rate[1], 3)), 0.0)
        self.assertEqual((round(tp_rate[2], 3)), 0.333)
        self.assertEqual((round(tp_rate[3], 3)), 0.667)
        self.assertEqual((round(tp_rate[4], 3)), 1.0)

        # plt = roc.create_plot(roc_points)
        # plt.show()

    def test_get_auc(self):

        ids = ['a', 'b', 'c', 'd', 'e']

        probabilities = {'a': 0.5, 'b': 0.7, 'c': 0.8, 'd': 0.3, 'e': 0.8}

        true_classes = {'a': Class.POSITIVE, 'b': Class.POSITIVE, 'c': Class.POSITIVE, 'd': Class.NEGATIVE,
                        'e': Class.NEGATIVE}

        auc = roc.get_auc(ids, probabilities, true_classes, Class.POSITIVE, Class.NEGATIVE)

        self.assertEqual(auc, 0.5)

