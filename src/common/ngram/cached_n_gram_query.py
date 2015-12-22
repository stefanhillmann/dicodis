"""
Created on Tue Jul 24 12:58:40 2015

@author: Stefan Hillmann (stefan.hillmann@tu-berlin.de)
"""

import collections
import functools
import common.util.persistence as persistence


class Memorized(object):
    '''Decorator. Caches a function's return value each time it is called.
    If called later with the same arguments, the cached value is returned
    (not reevaluated).
    '''

    def __init__(self, func):
        self.func = func
        self.cache = {}

    def __call__(self, *args):
        if not isinstance(args, collections.Hashable):
            # uncacheable. a list, for instance.
            # better to not cache than blow up.
            return self.func(*args)
        if args in self.cache:
            return self.cache[args]
        else:
            value = self.func(*args)
            self.cache[args] = value
            return value

    def __repr__(self):
        '''Return the function's docstring.'''
        return self.func.__doc__

    def __get__(self, obj, objtype):
        '''Support instance methods.'''
        return functools.partial(self.__call__, obj)


@Memorized
def get_n_grams_from_database(document_id, sizes):
    # connect to database
    coll_n_grams = persistence.get_collection(persistence.Collection.n_grams)

    # get n-grams for each n-gram size and the current document
    # Hint: currently we use the precomputed n-grams from the database.
    # As all post-processing is done by the classifier, we get the n-grams for frequency threshold == 1.
    query = {'document_id': document_id, 'n': {'$in': list(sizes)}, 'f_min': 1}
    db_n_grams = coll_n_grams.find(query)

    # copy query result into list
    n_grams = list()
    for cursor in db_n_grams:
        n_grams.append(cursor['n_gram'])

    return n_grams
