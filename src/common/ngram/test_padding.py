"""
Created on Tue Jul 24 13:13:00 2015

@author: Stefan Hillmann (stefan.hillmann@tu-berlin.de)
"""

import unittest
import cached_pads as cp

class TestPadding(unittest.TestCase):

    def test_padding(self):
        self.assertEqual(cp.get_pads(0), "")
        self.assertEqual(cp.get_pads(1), "_")
        self.assertEqual(cp.get_pads(2), "__")
        self.assertEqual(cp.get_pads(2), "__")  # caching
        self.assertEqual(cp.get_pads(1), "_")  # caching
        self.assertEqual(cp.get_pads(15), "_______________")
        self.assertEqual(cp.get_pads(15), "_______________")
