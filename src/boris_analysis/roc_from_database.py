__author__ = 'stefan'

import common.util.persistence as pe
from common.analyse import roc
from common.util.names import Class
import configparser

config = configparser.ConfigParser()
config.read('local_config.ini')

host = config.get('database', 'host')
port = config.getint('database', 'port')
database = config.get('database', 'db_name')


dbm = pe.DbManager(host, port, database)
db = dbm.get_connection()

results = db[config.get('database', 'doc_result_collection')]

# , 'positive_class_distance:': {'$gt': 0.8}

query = {'classifier_name': 'cosine',
         'frequency_threshold': 1,
         'n_gram_size': 1,
         'evaluation_id': 'complete_2015_07_27',
         'smoothing_value': 0.5,
         'criteria': 'long_interactions'}

example_ids = list()
positive_probability_dict = dict()
true_class_dict = dict()

query_results = results.find(query)
print(query_results.count())
for cursor in query_results:
    id = cursor['document_id']
    example_ids.append(id)
    positive_probability_dict[id] = cursor['positive_class_distance']
    true_class_dict[id] = cursor['true_class']

roc_points = roc.get_roc_points(example_ids, positive_probability_dict, true_class_dict, Class.POSITIVE, Class.NEGATIVE)
plt = roc.create_plot(roc_points)
plt.show()




dbm.close()



