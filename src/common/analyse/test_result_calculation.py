from re import search

__author__ = 'Stefan Hillmann'

import unittest
from cross_validation import SingleTestResult, ResultAssessor, SummarizedTestResults
import cross_validation as cv

import common.measuring.measures as m
from common.dialog_document.document import Document
from common.classify.classifier import ClassificationResult

class TestResultCalculation(unittest.TestCase):

    def setUp(self):

        self.classifier_a = m.MeasureName.COSINE
        self.classifier_b = m.MeasureName.RANK_ORDER
        self.class_x = "class_x"
        self.class_y = "class_y"
        self.distance = 20
        self.n_gram_size = 3

        self.document_x = Document(self.class_x, ('a', 'b'), 1)
        self.document_y = Document(self.class_y, ('a', 'b'), 2)

        self.result_x = ClassificationResult(self.class_x, self.distance)
        self.result_y = ClassificationResult(self.class_y, self.distance)

    def getHit(self):
        return SingleTestResult(self.document_x, self.classifier_a, self.result_x, self.n_gram_size)

    def getMiss(self):
        return SingleTestResult(self.document_y, self.classifier_a, self.result_x, self.n_gram_size)

    def test_single_result_creation(self):
        r = SingleTestResult(self.document_x, self.classifier_a, self.result_y, self.n_gram_size)
        self.assertEqual(r.document, self.document_x)
        self.assertEqual(r.classifier_name, self.classifier_a)
        self.assertEqual(r.actual_class, self.class_x)
        self.assertEqual(r.calculated_class, self.class_y)
        self.assertEqual(r.calculated_distance, self.distance)
        self.assertEqual(r.n_gram_size, self.n_gram_size)

    def test_perfect_result(self):
        results = []
        for i in range(3):
            results.append(self.getHit())

        ra = ResultAssessor(results, self.class_x, self.class_y, self.classifier_a, self.n_gram_size, 1, "criteria_name", 0.0)

        analysis = ra.getResultAnalysis()

        self.assertEqual(analysis.n_gram_size, 3)
        self.assertEqual(analysis.classifier_name, self.classifier_a)
        self.assertEqual(analysis.criteria, "criteria_name")
        self.assertEqual(analysis.frequency_threshold, 1)
        self.assertEqual(analysis.smoothing_value, 0.0)

        self.assertEqual(analysis.false_negative, 0)
        self.assertEqual(analysis.false_positive, 0)
        self.assertEqual(analysis.true_negative, 0)
        self.assertEqual(analysis.true_positive, 3)

    def test_very_bad_result(self):
        results = []
        for i in range(3):
            results.append(self.getMiss())

        ra = ResultAssessor(results, self.class_x, self.class_y, self.classifier_a, self.n_gram_size, 1, "criteria_name", 0.0)
        analysis = ra.getResultAnalysis()

        self.assertEqual(analysis.n_gram_size, 3)
        self.assertEqual(analysis.classifier_name, self.classifier_a)
        self.assertEqual(analysis.criteria, "criteria_name")
        self.assertEqual(analysis.frequency_threshold, 1)
        self.assertEqual(analysis.smoothing_value, 0.0)

        self.assertEqual(analysis.false_negative, 0)
        self.assertEqual(analysis.false_positive, 3)
        self.assertEqual(analysis.true_negative, 0)
        self.assertEqual(analysis.true_positive, 0)

    def test_result_mix(self):
        sr_1 = SingleTestResult(self.document_x, self.classifier_a, self.result_x, self.n_gram_size)  # TP
        sr_2 = SingleTestResult(self.document_x, self.classifier_a, self.result_y, self.n_gram_size)  # FN
        sr_3 = SingleTestResult(self.document_y, self.classifier_a, self.result_x, self.n_gram_size)  # FP
        sr_4 = SingleTestResult(self.document_y, self.classifier_a, self.result_y, self.n_gram_size)  # TN

        results = [sr_1, sr_2, sr_3, sr_4]

        ra = ResultAssessor(results, self.class_x, self.class_y, self.classifier_a, self.n_gram_size, 1, "criteria_name", 0.0)

        analysis = ra.getResultAnalysis()

        self.assertEqual(analysis.true_positive, 1)
        self.assertEqual(analysis.false_positive, 1)
        self.assertEqual(analysis.true_negative, 1)
        self.assertEqual(analysis.false_negative, 1)

    def test_result_mix_table_creation(self):
        sr_1 = SingleTestResult(self.document_x, self.classifier_a, self.result_x, self.n_gram_size)  # TP
        sr_2 = SingleTestResult(self.document_x, self.classifier_a, self.result_y, self.n_gram_size)  # FN
        sr_3 = SingleTestResult(self.document_y, self.classifier_a, self.result_x, self.n_gram_size)  # FP
        sr_4 = SingleTestResult(self.document_y, self.classifier_a, self.result_y, self.n_gram_size)  # TN

        results = [sr_1, sr_2, sr_3, sr_4]
        ra = ResultAssessor(results, self.class_x, self.class_y, self.classifier_a, self.n_gram_size, 1, "criteria_name", 0.0)
        analysis = ra.getResultAnalysis()

        rows = cv.create_result_table([analysis], ",")
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0], ",".join( ['Criteria', 'Classifier', 'n', 'l', 'Freq. Threshold', 'TP', 'FP', 'TN',
                                             'FN', 'Recall', 'Precision', 'F-Measure'] ))
        self.assertEqual(rows[1], ",".join(['criteria_name', self.classifier_a, str(self.n_gram_size), str(0.0), str(1),
                                            str(1.0), str(1.0), str(1.0), str(1.0), str(0.5), str(0.5), str(0.5)]))

    def test_result_true_positive(self):
        sr_1 = SingleTestResult(self.document_x, self.classifier_a, self.result_x, self.n_gram_size)  # TP

        results = [sr_1]

        ra = ResultAssessor(results, self.class_x, self.class_y, self.classifier_a, self.n_gram_size, 1, "criteria_name", 0.0)

        analysis = ra.getResultAnalysis()

        self.assertEqual(analysis.true_positive, 1)

    def test_result_false_negative(self):
        sr_2 = SingleTestResult(self.document_x, self.classifier_a, self.result_y, self.n_gram_size)  # FN

        results = [sr_2]

        ra = ResultAssessor(results, self.class_x, self.class_y, self.classifier_a, self.n_gram_size, 1, "criteria_name", 0.0)

        analysis = ra.getResultAnalysis()

        self.assertEqual(analysis.false_negative, 1)

    def test_result_false_positive(self):
        sr_3 = SingleTestResult(self.document_y, self.classifier_a, self.result_x, self.n_gram_size)  # FP

        results = [sr_3]

        ra = ResultAssessor(results, self.class_x, self.class_y, self.classifier_a, self.n_gram_size, 1, "criteria_name", 0.0)

        analysis = ra.getResultAnalysis()

        self.assertEqual(analysis.false_positive, 1)

    def test_result_true_negative(self):
        sr_4 = SingleTestResult(self.document_y, self.classifier_a, self.result_y, self.n_gram_size)  # TN

        results = [sr_4]

        ra = ResultAssessor(results, self.class_x, self.class_y, self.classifier_a, self.n_gram_size, 1, "criteria_name", 0.0)

        analysis = ra.getResultAnalysis()

        self.assertEqual(analysis.true_negative, 1)

    def test_summarized_test_result_creation(self):
        r = SummarizedTestResults(1, 2, 3, 4, self.classifier_a, 5, "criteria_name", 1, 0.0)

        self.assertEqual(r.true_positive, 1)
        self.assertEqual(r.false_positive, 2)
        self.assertEqual(r.true_negative, 3)
        self.assertEqual(r.false_negative, 4)
        self.assertEqual(r.classifier_name, self.classifier_a)
        self.assertEqual(r.n_gram_size, 5)
        self.assertEqual(r.criteria, "criteria_name")
        self.assertEqual(r.frequency_threshold, 1)
        self.assertEqual(r.smoothing_value, 0.0)

    def test_recall_precision_f_measure_1(self):
        tp = 20
        fp = 0
        fn = 0

        precision = cv.compute_precision(tp, fp)
        self.assertEqual(precision, 1.0)

        recall = cv.compute_recall(tp, fn)
        self.assertEqual(recall, 1.0)

        f_measure = cv.compute_f_measure(tp, fp, fn)
        self.assertEqual(f_measure, 1.0)

    def test_recall_precision_f_measure_2(self):
        tp = 5
        fp = 5
        fn = 5

        precision = cv.compute_precision(tp, fp)
        self.assertEqual(precision, 0.5)

        recall = cv.compute_recall(tp, fn)
        self.assertEqual(recall, 0.5)

        f_measure = cv.compute_f_measure(tp, fp, fn)
        self.assertEqual(f_measure, 0.5)

    def test_recall_precision_f_measure_3(self):
        tp = 0
        fp = 0
        fn = 0

        precision = cv.compute_precision(tp, fp)
        self.assertEqual(precision, 0)

        recall = cv.compute_recall(tp, fn)
        self.assertEqual(recall, 0)

        f_measure = cv.compute_f_measure(tp, fp, fn)
        self.assertEqual(f_measure, 0)

