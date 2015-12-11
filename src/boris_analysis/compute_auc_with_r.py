import common.util.persistence as pe
import configparser
import pyRserve as pyr
import numpy as np


config = configparser.ConfigParser()
config.read('local_config.ini')

results = pe.get_collection(config.get('collections', 'doc_result'))

# , 'positive_class_distance:': {'$gt': 0.8}

query = {'classifier_name': 'cosine',
         'frequency_threshold': 1,
         'n_gram_size': 1,
         'evaluation_id': 'complete_2015_07_27',
         'smoothing_value': 0.5,
         'criteria': 'long_interactions'}

query_results = results.find(query)
predictions = list()
true_classes = list()
for cursor in query_results:
    predictions.append(cursor['positive_class_distance'] - cursor['negative_class_distance'])
    true_classes.append(cursor['true_class'])


rc = pyr.connect()

rc.voidEval("library(pROC)")
rc.r.predictor = np.array(predictions)
rc.r.response = np.array(true_classes)
rc.r.levels = ['positive', 'negative']
print(rc.eval("sum(predictor)"))
rc.voidEval("roc <- roc(response = response, predictor = predictor, levels = levels)")
auc = rc.eval("roc$auc")

print(auc)

rc.close()
pe.close()


