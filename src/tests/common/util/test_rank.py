__author__ = 'stefan'

import unittest
import common.util.rank


class TestRank(unittest.TestCase):

    def test_min_rank(self):
        foo = [2, 1, 5, 4, 3]
        bar = [2, 5, 7, 6, 1]
        foobar = [2, 2, 3, 4, 7]

        result = common.util.rank.min_rank([foo, bar, foobar])

        self.assertEqual(1, result, "Minimum of all lists is 1")

    def test_max_rank(self):
        foo = [2, 1, 5, 4, 3]
        bar = [2, 5, 7, 6, 1]
        foobar = [2, 2, 3, 4, 7]

        result = common.util.rank.max_rank([foo, bar, foobar])

        self.assertEqual(7, result, "Maximum of all lists is 7")

