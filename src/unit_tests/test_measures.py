import unittest

from common.measuring import measures as m


class TestMeasures(unittest.TestCase):
    
    def setUp(self):
        self.p = [0.1, 0.2, 0.2, 0.5]
        self.q = self.p
    
    def testCosineSimilarity(self):
        s = m.cosine_similarity(self.p, self.q)
        self.assertEqual(s, 1)
        
    def testJensenDistance(self):
        d = m.jensen_distance(self.p, self.q)
        self.assertEqual(d, 0)
        
    def testKullbackLeiblerDivergence(self):
        d = m.kullback_leibler_divergence(self.p, self.q)
        self.assertEqual(d, 0)
        
    def testMeanKullbackLeiblerDivergence(self):
        d = m.mean_kullback_leibler_distance(self.p, self.q)
        self.assertEqual(d, 0)
        
    def testSymmetricKullbackLeiblerDivergence(self):
        d = m.symmetric_kullback_leibler_distance(self.p, self.q)
        self.assertEqual(d, 0)

if __name__ == '__main__':
        unittest.main()
