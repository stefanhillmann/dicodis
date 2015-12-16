import unittest
from common.util import dict as du


class TestDictUtil(unittest.TestCase):

    def test_convert_string_to_integer(self):
        test_data = {"a": 1, "b": "foo", "c": 2}

        du.convert_string_to_integer(test_data, ["a", "c"])

        self.assertEqual(test_data["a"], 1)
        self.assertEqual(test_data["b"], "foo")
        self.assertEqual(test_data["c"], 2)

    def test_replace_dots_in_keys(self):
        old_keys = ["a.b", "c_d", "e.f"]
        new_keys = ["a_b", "c_d", "e_f"]

        test_dict = dict(zip(old_keys, [1, 1, 1]))
        du.replace_dots_in_keys(test_dict)

        self.assertEqual(set(new_keys), set(test_dict.keys()))
