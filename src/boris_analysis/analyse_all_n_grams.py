"""
Created on Tue Jul 22 14:37:10 2015

@author: Stefan Hillmann (stefan.hillmann@tu-berlin.de)
"""

import common.util.persistence as pe

# connect to database
host = 'localhost'
port = 27017
database = 'dialog_ngrams'
dbm = pe.DbManager(host, port, database)
db = dbm.get_connection()

# analyse frequencies
# absolute number of n-grams
n_grams = db.n_grams
print('Total number of n-grams in database: {}'.format( n_grams.count() ))


sizes = sorted(n_grams.distinct('n_gram_size'))
print("Distinct n's: {}".format(sizes))

# total number per n
for n in sizes:
    number = n_grams.find({'n_gram_size': n}).count()
    print("Total n-grams for n = {0}: {1}".format(n, number))

    distinct_count = len(n_grams.find({'n_gram_size': n}).distinct("n_gram"))
    print("Distinct n-grams for n = {0}: {1}".format(n, distinct_count))
    print("\n")
