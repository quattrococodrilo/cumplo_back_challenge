import unittest
from utils.helpers import get_banxico_data

from back_chanllenge.settings import BANXICO_UDIS_SERIES


class TestHelpers(unittest.TestCase):

    def test_banxico_api_helper_one_data(self):
        data = get_banxico_data(
            serie=BANXICO_UDIS_SERIES,
            start_date='2022-3-28'
        )

        self.assertEqual(data[0]['dato'], 7.236109)

    def test_banxico_api_helper_many_data(self):
        data = get_banxico_data(
            serie=BANXICO_UDIS_SERIES,
            start_date='2022-3-1',
            end_date='2022-3-20'
        )

        self.assertEqual(len(data), 20)
