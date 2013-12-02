import unittest
import classify.measures as m


class testMeasures(unittest.TestCase):
    
    def setUp(self):
        self.p = [0.1, 0.2, 0.2, 0.5]
        self.q = self.p
    
    def testCosineSimilarity(self):
        s = m.cosineSimilarity(self.p, self.q)
        self.assertEqual(s, 1)
        
    def testJensenDistance(self):
        d = m.jensenDistance(self.p, self.q)
        self.assertEqual(d, 0)
        
    def testKullbackLeiblerDivergence(self):
        d = m.kullbackLeiblerDivergence(self.p, self.q)
        self.assertEqual(d, 0)
        
    def testMeanKullbackLeiblerDivergence(self):
        d = m.meanKullbackLeiblerDistance(self.p, self.q)
        self.assertEqual(d, 0)
        
    def testSymmetricKullbackLeiblerDivergence(self):
        d = m.symmetricKullbackLeiblerDistance(self.p, self.q)
        self.assertEqual(d, 0)
    
    
    if __name__ == '__main__':
        unittest.main()