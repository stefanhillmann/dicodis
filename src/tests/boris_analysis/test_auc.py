import unittest

# import boris_analysis.compute_performance as cp
import pyRserve as pyr
from pyRserve.rexceptions import REvalError
import numpy as np

def get_auc(data):
    # Prepare R connection
    rc = pyr.connect()
    rc.voidEval("library(pROC)")
    rc.r.levels = ['positive', 'negative']

    predictions = list()
    true_classes = list()
    for cursor in data:
        predictions.append(cursor['positive_class_distance'] - cursor['negative_class_distance'])
        # predictions.append(cursor['negative_class_distance'] - cursor['positive_class_distance'])
        true_classes.append(cursor['true_class'])

    rc.r.predictor = np.array(predictions)
    rc.r.response = np.array(true_classes)
    try:
        rc.voidEval("roc <- roc(response = response, predictor = predictor, levels = levels)")
    except REvalError as e:
        print("Error while computing ROC with predictions: '{0}' and true_classes: '{1}. Will re-raise the error."
              .format(str(predictions), str(true_classes)))
        raise e

    auc = rc.eval("roc$auc")

    return auc[0]


class TestAuc(unittest.TestCase):

    def test_perfect_auc(self):
        pc = 'positive'
        nc = 'negative'
        pcd = 'positive_class_distance'
        ncd = 'negative_class_distance'
        tc = 'true_class'

        # positive samples
        d_1 = dict()
        d_1[pcd] = 0.9
        d_1[ncd] = 0.1
        d_1[tc] = pc

        d_5 = d_4 = d_3 = d_2 = d_1

        # d_7 = dict()
        # d_7[pcd] = 0.1
        # d_7[ncd] = 0.9
        # d_7[tc] = pc

        # negative sample
        d_6 = dict()
        d_6[pcd] = 0.1
        d_6[ncd] = 0.9
        d_6[tc] = nc

        d = [d_1, d_2, d_3, d_4, d_5, d_6]

        auc = get_auc(d)

        print("AUC: {0}".format(auc))

        self.assertEqual(auc, 1.0)




