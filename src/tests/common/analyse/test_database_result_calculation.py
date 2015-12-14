import unittest
from common.analyse.cross_validation import SingleTestResult

import common.measuring.measures as m
from common.dialog_document.document import Document
from common.classify.classifier import ClassificationResult
from common.util.names import Class
from common.util import persistence as pe
from common.analyse import performance


class TestDatabaseResultCalculation(unittest.TestCase):

    def setUp(self):

        self.classifier_a = m.MeasureName.COSINE
        self.classifier_b = m.MeasureName.RANK_ORDER
        self.distance = 20
        self.n_gram_size = 3
        self.frequency_threshold = 1
        self.smoothing_vale = 0.05
        self.criteria = 'criteria_name'

        self.document_pos = Document(Class.POSITIVE, ('a', 'b'), 1)
        self.document_neg = Document(Class.NEGATIVE, ('a', 'b'), 2)

        self.result_pos = ClassificationResult(10, 20, Class.POSITIVE)  # positive_class_distance, negative_class_distance, estimated_class
        self.result_neg = ClassificationResult(20, 10, Class.NEGATIVE)

        self.host = 'localhost'
        self.port = 27017
        self.evaluation_id = '1'
        self.db_client = pe.DbClient(self.host, self.port)
        pe.db_client = self.db_client
        pe.current_database = pe.Database.unit_testing
        self.coll_doc_result = pe.get_collection(pe.Collection.doc_result)
        self.coll_doc_result.drop()
        self.coll_performance = pe.get_collection(pe.Collection.performance)
        self.coll_performance.drop()

    def tearDown(self):
        pe.close()

    def getHit(self):
        return SingleTestResult(self.document_pos, self.classifier_a, self.result_pos, self.n_gram_size)

    def getMiss(self):
        return SingleTestResult(self.document_neg, self.classifier_a, self.result_pos, self.n_gram_size)

    def test_result_true_positive(self):
        sr = SingleTestResult(self.document_pos, self.classifier_a, self.result_pos, self.n_gram_size)  # TP

        pe.write_evaluation_results_to_database(self.evaluation_id, [sr], self.n_gram_size, self.classifier_a,
                                                self.frequency_threshold, self.smoothing_vale,
                                                self.criteria)

        count = performance.get_db_true_positive_count(self.evaluation_id, self.classifier_a, self.frequency_threshold,
                                                       self.n_gram_size, self.smoothing_vale, self.criteria,
                                                       self.coll_doc_result)

        self.assertEqual(count, 1)

    def test_result_false_negative(self):
        sr = SingleTestResult(self.document_pos, self.classifier_a, self.result_neg, self.n_gram_size)  # FN

        pe.write_evaluation_results_to_database(self.evaluation_id, [sr], self.n_gram_size, self.classifier_a,
                                                self.frequency_threshold, self.smoothing_vale,
                                                self.criteria)

        count = performance.get_db_false_negative_count(self.evaluation_id, self.classifier_a, self.frequency_threshold,
                                                        self.n_gram_size, self.smoothing_vale, self.criteria,
                                                        self.coll_doc_result)

        self.assertEqual(count, 1)

    def test_result_false_positive(self):
        sr = SingleTestResult(self.document_neg, self.classifier_a, self.result_pos, self.n_gram_size)  # FP

        pe.write_evaluation_results_to_database(self.evaluation_id, [sr], self.n_gram_size, self.classifier_a,
                                                self.frequency_threshold, self.smoothing_vale,
                                                self.criteria)

        count = performance.get_db_false_positive_count(self.evaluation_id, self.classifier_a, self.frequency_threshold,
                                                        self.n_gram_size, self.smoothing_vale, self.criteria,
                                                        self.coll_doc_result)

        self.assertEqual(count, 1)

    def test_result_true_negative(self):
        sr = SingleTestResult(self.document_neg, self.classifier_a, self.result_neg, self.n_gram_size)  # TN

        pe.write_evaluation_results_to_database(self.evaluation_id, [sr], self.n_gram_size, self.classifier_a,
                                                self.frequency_threshold, self.smoothing_vale,
                                                self.criteria)

        count = performance.get_db_true_negative_count(self.evaluation_id, self.classifier_a, self.frequency_threshold,
                                                       self.n_gram_size, self.smoothing_vale, self.criteria,
                                                       self.coll_doc_result)

        self.assertEqual(count, 1)
