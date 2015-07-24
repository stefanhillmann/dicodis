"""
Created on Tue Jul 24 12:58:40 2015

@author: Stefan Hillmann (stefan.hillmann@tu-berlin.de)
"""

import collections
import functools


class Memoized(object):
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

@Memoized
def get_pads(n):
    """
    Return the pad with n elements.
    Pads for a distinct n are 'cached' after first access.
    """

    pads = ""
    for i in range(n):
        pads = pads + "_"

    return pads