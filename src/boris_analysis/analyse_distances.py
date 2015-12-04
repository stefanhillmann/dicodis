import configparser
from common.util import persistence
import numpy as np
import texttable as tt
import boris_analysis.cross_validation_configuration as cvc
import matplotlib.pyplot as plt


# read configuration
config = configparser.ConfigParser()
config.read('local_config.ini')

evaluation_id = config.get('cross_validation', 'evaluation_id')
host = config.get('database', 'host')
port = config.getint('database', 'port')
database = config.get('database', 'db_name')
distances_collection = config.get('database', 'distances_collection')

dbm = persistence.DbManager(host, port, database)
db = dbm.get_connection()
db_distances = db[distances_collection]

configurations = cvc.getConfigurations()

# describing statistics real vs. best

table = tt.Texttable()
table.add_row(['Classifier', 'Min', 'Max', 'Mean', "STD"])
i = 0
for cn in cvc.classifier_names:
    i += 1
    distances = list()
    for d in db_distances.find({'data_set': 'real_vs_best_sim', 'classifier': cn}):
        distances.append(d['distance'])

    plt.subplot(4, 2, i * 2 -1)
    plt.title(cn)
    plt.hist(distances)
    table.add_row([cn, np.min(distances), np.max(distances), np.mean(distances), np.std(distances)])

print(table.draw())


# describing statistics real vs. best
table = tt.Texttable()
table.add_row(['Classifier', 'Min', 'Max', 'Mean', "STD"])
i = 0
for cn in cvc.classifier_names:
    i += 1
    distances = list()
    for d in db_distances.find({'data_set': 'real_vs_worst_sim', 'classifier': cn}):
        distances.append(d['distance'])

    plt.subplot(4, 2, i * 2)
    plt.title(cn + '(worst)')
    plt.hist(distances)
    table.add_row([cn, np.min(distances), np.max(distances), np.mean(distances), np.std(distances)])

print(table.draw())

plt.show()




