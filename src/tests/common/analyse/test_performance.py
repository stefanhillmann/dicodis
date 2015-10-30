__author__ = 'stefan'
import unittest
from common.analyse import performance


class TestPerformance(unittest.TestCase):

    def test_compute_precision(self):
        true_positive = 80
        false_positive = 20

        precision = performance.compute_precision(true_positive, false_positive)

        self.assertEqual(precision, float(true_positive) / (true_positive + false_positive))

    def test_compute_recall(self):
        true_positive = 80
        false_negative = 20

        recall = performance.compute_recall(true_positive, false_negative)

        self.assertEqual(recall, float(true_positive) / (true_positive + false_negative))

    def test_compute_f_measure(self):
        true_positive = 80
        false_positive = 20
        false_negative = 20

        f_measure = performance.compute_f_measure(true_positive, false_positive, false_negative)

        _f_measure = float((2 * true_positive)) / ( 2 * true_positive + false_positive + false_negative )

        self.assertEqual(f_measure, _f_measure)
