__author__ = 'Stefan Hillmann'

import unittest
from common.analyse.cross_validation import SingleTestResult, ResultAssessor, SummarizedTestResults
import common.analyse.cross_validation as cv

import common.measuring.measures as m
from common.dialog_document.document import Document
from common.classify.classifier import ClassificationResult
from common.util.names import Class

class TestResultCalculation(unittest.TestCase):

    def setUp(self):

        self.classifier_a = m.MeasureName.COSINE
        self.classifier_b = m.MeasureName.RANK_ORDER
        self.distance = 20
        self.n_gram_size = 3

        self.document_pos = Document(Class.POSITIVE, ('a', 'b'), 1)
        self.document_neg = Document(Class.NEGATIVE, ('a', 'b'), 2)

        self.result_pos = ClassificationResult(10, 20, Class.POSITIVE)  # positive_class_distance, negative_class_distance, estimated_class
        self.result_neg = ClassificationResult(20, 10, Class.NEGATIVE)

    def getHit(self):
        return SingleTestResult(self.document_pos, self.classifier_a, self.result_pos, self.n_gram_size)

    def getMiss(self):
        return SingleTestResult(self.document_neg, self.classifier_a, self.result_pos, self.n_gram_size)

    def test_single_result_creation(self):
        r = SingleTestResult(self.document_pos, self.classifier_a, self.result_neg, self.n_gram_size)
        self.assertEqual(r.document, self.document_pos)
        self.assertEqual(r.classifier_name, self.classifier_a)
        self.assertEqual(r.true_class, Class.POSITIVE)
        self.assertEqual(r.classification_result.estimated_class, Class.NEGATIVE)
        self.assertEqual(r.classification_result.get_distance(Class.NEGATIVE), 10)
        self.assertEqual(r.classification_result.get_distance(Class.POSITIVE), 20)
        self.assertEqual(r.n_gram_size, self.n_gram_size)

    def test_perfect_result(self):
        results = []
        for i in range(3):
            results.append(self.getHit())

        ra = ResultAssessor(results, Class.POSITIVE, Class.NEGATIVE, self.classifier_a, self.n_gram_size, 1,
                            "criteria_name", 0.0)

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

        ra = ResultAssessor(results, Class.POSITIVE, Class.NEGATIVE, self.classifier_a, self.n_gram_size, 1, "criteria_name", 0.0)
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
        sr_1 = SingleTestResult(self.document_pos, self.classifier_a, self.result_pos, self.n_gram_size)  # TP
        sr_2 = SingleTestResult(self.document_pos, self.classifier_a, self.result_neg, self.n_gram_size)  # FN
        sr_3 = SingleTestResult(self.document_neg, self.classifier_a, self.result_pos, self.n_gram_size)  # FP
        sr_4 = SingleTestResult(self.document_neg, self.classifier_a, self.result_neg, self.n_gram_size)  # TN

        results = [sr_1, sr_2, sr_3, sr_4]

        ra = ResultAssessor(results, Class.POSITIVE, Class.NEGATIVE, self.classifier_a, self.n_gram_size, 1, "criteria_name", 0.0)

        analysis = ra.getResultAnalysis()

        self.assertEqual(analysis.true_positive, 1)
        self.assertEqual(analysis.false_positive, 1)
        self.assertEqual(analysis.true_negative, 1)
        self.assertEqual(analysis.false_negative, 1)

    def test_result_mix_table_creation(self):
        sr_1 = SingleTestResult(self.document_pos, self.classifier_a, self.result_pos, self.n_gram_size)  # TP
        sr_2 = SingleTestResult(self.document_pos, self.classifier_a, self.result_neg, self.n_gram_size)  # FN
        sr_3 = SingleTestResult(self.document_neg, self.classifier_a, self.result_pos, self.n_gram_size)  # FP
        sr_4 = SingleTestResult(self.document_neg, self.classifier_a, self.result_neg, self.n_gram_size)  # TN

        results = [sr_1, sr_2, sr_3, sr_4]
        ra = ResultAssessor(results, Class.POSITIVE, Class.NEGATIVE, self.classifier_a, self.n_gram_size, 1, "criteria_name", 0.0)
        analysis = ra.getResultAnalysis()

        rows = cv.create_result_table([analysis], ",")
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0], ",".join( ['Criteria', 'Classifier', 'n', 'l', 'Freq. Threshold', 'TP', 'FP', 'TN',
                                             'FN', 'Recall', 'Precision', 'F-Measure'] ))
        self.assertEqual(rows[1], ",".join(['criteria_name', self.classifier_a, str(self.n_gram_size), str(0.0), str(1),
                                            str(1.0), str(1.0), str(1.0), str(1.0), str(0.5), str(0.5), str(0.5)]))

    def test_result_true_positive(self):
        sr_1 = SingleTestResult(self.document_pos, self.classifier_a, self.result_pos, self.n_gram_size)  # TP

        results = [sr_1]

        ra = ResultAssessor(results, Class.POSITIVE, Class.NEGATIVE, self.classifier_a, self.n_gram_size, 1, "criteria_name", 0.0)

        analysis = ra.getResultAnalysis()

        self.assertEqual(analysis.true_positive, 1)

    def test_result_false_negative(self):
        sr_2 = SingleTestResult(self.document_pos, self.classifier_a, self.result_neg, self.n_gram_size)  # FN

        results = [sr_2]

        ra = ResultAssessor(results, Class.POSITIVE, Class.NEGATIVE, self.classifier_a, self.n_gram_size, 1, "criteria_name", 0.0)

        analysis = ra.getResultAnalysis()

        self.assertEqual(analysis.false_negative, 1)

    def test_result_false_positive(self):
        sr_3 = SingleTestResult(self.document_neg, self.classifier_a, self.result_pos, self.n_gram_size)  # FP

        results = [sr_3]

        ra = ResultAssessor(results, Class.POSITIVE, Class.NEGATIVE, self.classifier_a, self.n_gram_size, 1, "criteria_name", 0.0)

        analysis = ra.getResultAnalysis()

        self.assertEqual(analysis.false_positive, 1)

    def test_result_true_negative(self):
        sr_4 = SingleTestResult(self.document_neg, self.classifier_a, self.result_neg, self.n_gram_size)  # TN

        results = [sr_4]

        ra = ResultAssessor(results, Class.POSITIVE, Class.NEGATIVE, self.classifier_a, self.n_gram_size, 1, "criteria_name", 0.0)

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

    def test_roc_points_for_result_mix(self):
        sr_1 = SingleTestResult(self.document_pos, self.classifier_a, self.result_pos, self.n_gram_size)  # TP
        sr_2 = SingleTestResult(self.document_pos, self.classifier_a, self.result_neg, self.n_gram_size)  # FN
        sr_3 = SingleTestResult(self.document_neg, self.classifier_a, self.result_pos, self.n_gram_size)  # FP
        sr_4 = SingleTestResult(self.document_neg, self.classifier_a, self.result_neg, self.n_gram_size)  # TN

        results = [sr_1, sr_2, sr_3, sr_4]

        ra = ResultAssessor(results, Class.POSITIVE, Class.NEGATIVE, self.classifier_a, self.n_gram_size, 1, "criteria_name", 0.0)

        roc_points = ra.get_tpr_and_fpr_for_roc()


    def test_roc_points_for_result_mi_2(self):
        sr_1 = SingleTestResult(self.document_pos, self.classifier_a, self.result_pos, self.n_gram_size)  # TP
        sr_2 = SingleTestResult(self.document_pos, self.classifier_a, self.result_neg, self.n_gram_size)  # FN
        sr_3 = SingleTestResult(self.document_neg, self.classifier_a, self.result_pos, self.n_gram_size)  # FP
        sr_4 = SingleTestResult(self.document_neg, self.classifier_a, self.result_neg, self.n_gram_size)  # TN

        results = [sr_1, sr_2, sr_3, sr_4]

        ra = ResultAssessor(results, Class.POSITIVE, Class.NEGATIVE, self.classifier_a, self.n_gram_size, 1, "criteria_name", 0.0)

        roc_points = ra.get_roc_points()
        print(roc_points)

    def test_sort_results_by_positive_class_distance(self):
        sr_2 = SingleTestResult(self.document_pos, self.classifier_a, self.result_neg, self.n_gram_size)  # FN
        sr_1 = SingleTestResult(self.document_pos, self.classifier_a, self.result_pos, self.n_gram_size)  # TP

        results = [sr_2, sr_1]

        ra = ResultAssessor(results, Class.POSITIVE, Class.NEGATIVE, self.classifier_a, self.n_gram_size, 1, "criteria_name", 0.0)

        self.assertIs(ra.data[0], sr_2)
        self.assertIs(ra.data[1], sr_1)

        sorted_results = ra.sort_results_by_positive_class_distance(ra.data)

        self.assertIs(sorted_results[0], sr_1)
        self.assertIs(sorted_results[1], sr_2)
