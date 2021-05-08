import unittest

from greatcircle.find_customers_within_circle import calculate_distance


class TestGreatCircle(unittest.TestCase):

    def test_calculating_distance_successful(self):
        location1 = {
            "name": "TCD",
            "latitude": "53.342781",
            "longitude": "-6.254610"
        }
        location2 = {
            "name": "UCD",
            "latitude": "53.306755",
            "longitude": "-6.220969"
        }
        expected_result = 5
        actual_result = calculate_distance(location1, location2)

        self.assertEqual(expected_result, actual_result, f'Distance from UCD to TCD should be {expected_result}')


if __name__ == "__main__":
    unittest.main()
