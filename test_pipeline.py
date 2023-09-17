import unittest
import pipeline
import json
from collections import namedtuple

with open(".\\product_data.json") as f:
    product_data = json.load(f)
PreferenceMatch = namedtuple("PreferenceMatch", ["product_name", "product_codes"])

class TestPipeline(unittest.TestCase):

    def test_red(self):
        """Tests a single inclusion tag and expected result"""
        result = pipeline.main(product_data, ["red"], [""])[0]  # result returns a list of namedtuples
        test = PreferenceMatch("T-Shirt", ["A21313"])
        self.assertEqual(result.product_name, test.product_name)
        self.assertEqual(test.product_codes[0], result.product_codes[0])

    def test_red_exc_sm(self):
        """Tests a single inclusion tag and two exclusion tags with one expected result"""
        result = pipeline.main(product_data, ["red"], ["small", "medium"])[0]
        test = PreferenceMatch("T-Shirt", ["A21313"])
        self.assertEqual(result.product_name, test.product_name)
        self.assertEqual(test.product_codes[0], result.product_codes[0])

    def test_green(self):
        """Tests a single inclusion tag with multiple expected results"""
        result = pipeline.main(product_data, ["green"], [""])
        test = [PreferenceMatch("T-Shirt", ["A21312"]), PreferenceMatch("Pants", ["A21455"]), 
                PreferenceMatch("Socks", ["A21412"])]
        for i in range(len(test)):
            self.assertEqual(test[i].product_name, result[i].product_name)
            for j in range(len(test[i].product_codes)):
                self.assertEqual(test[i].product_codes[j], result[i].product_codes[j])

    def test_green_yellow_exc_blue(self):
        """Tests multiple inclusion and exclusion tags with multiple expected results"""
        result = pipeline.main(product_data, ["green", "yellow"], ["blue"])
        test = [PreferenceMatch("T-Shirt", ["A21312"]), PreferenceMatch("Pants", ["A21455"]),
                PreferenceMatch("Socks", ["A21412"]), PreferenceMatch("Jacket", ["A21502"])]
        for i in range(len(test)):
            self.assertEqual(test[i].product_name, result[i].product_name)
            for j in range(len(test[i].product_codes)):
                self.assertEqual(test[i].product_codes[j], result[i].product_codes[j])


if __name__ == "__main__":
    unittest.main()