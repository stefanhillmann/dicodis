"""
Created on Tue Jul 24 13:13:00 2015

@author: Stefan Hillmann (stefan.hillmann@tu-berlin.de)
"""

import unittest
import common.ngram.cached_pads as cp

class TestPadding(unittest.TestCase):

    def test_padding(self):
        self.assertEqual(cp.get_pads(1), "")
        self.assertEqual(cp.get_pads(2), "_")
        self.assertEqual(cp.get_pads(2), "_")  # caching
        self.assertEqual(cp.get_pads(1), "")  # caching
        self.assertEqual(cp.get_pads(15), "______________")
        self.assertEqual(cp.get_pads(15), "______________")
