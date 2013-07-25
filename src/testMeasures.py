# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 10:15:11 2013

@author: Stefan Hillmann (stefan.hillmann@tu-berlin.de)
"""

import unittest
import measures
import numpy as np

class TestMeasures(unittest.TestCase):

    def setUp(self):
        self.a = np.array([0.25, 0.25, 0.25, 0.25, 0, 0, 0, 0])
        self.b = np.array([0, 0, 0, 0, 0.25, 0.25, 0.25, 0.25])
        self.c = np.array([0.25, 0.25, 0, 0, 0.25, 0.25, 0, 0])
        
    def testCosineEqual(self):
        cs = measures.cosineSimilarity(self.a, self.a)
        self.assertEqual(cs, 1)
        
    def testCosineNoSimilarity(self):
        cs = measures.cosineSimilarity(self.a, self.b)
        self.assertEqual(cs, 0)
        
    def testCosineSimilar(self):
        cs = measures.cosineSimilarity(self.a, self.c)
        self.assertEqual(cs, 0.5)
        
    def testKullbackLeibler(self):
        kbl = measures.kullbackLeiblerDivergence(self.a, self.a)
        self.assertEqual(kbl, 0)
        
if __name__ == '__main__':
    unittest.main()