"""
Created on Tue Jul 24 12:58:40 2015

@author: Stefan Hillmann (stefan.hillmann@tu-berlin.de)
"""

import collections
import functools
import common.ngram.cached_pads as cp


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


def add_pads(document, n):
    pads = cp.get_pads(n)
    padded_document = []
    padded_document.extend(pads)
    padded_document.extend(document)
    padded_document.extend(pads)

    return padded_document


@Memorized
def get_n_grams(tokens, size):
    padded_tokens = add_pads(tokens, size)
    n_grams = list()

    for idxTerm in range(len(padded_tokens) - (size - 1)):
            i = idxTerm
            j = idxTerm + size

            ngram_parts = []

            for k in range(i, j):
                ngram_parts.append(padded_tokens[k])

            ngram = '#'.join(ngram_parts)
            n_grams.append(ngram)

    return n_grams
