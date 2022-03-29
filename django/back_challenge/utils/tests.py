from lib2to3.pgen2 import token
import os
import unittest

from utils import BanxicoApi


class TestBanxicoApi(unittest.TestCase):

    def test_udis_one_day(self):

        api = BanxicoApi.create(
            api_url='https://www.banxico.org.mx/SieAPIRest/service/v1/series/',
            token='326fafac9dc7facc7048216652fcc83200ed186275f65eabf37c970da5855d38',
            entry_point='datos',
        )

        udis = api.get(
            serie='SP68257',
            start_date='2022-3-28',
        )

        self.assertEqual(udis[0]['dato'], '7.236109')

    def test_udis_four_days(self):

        api = BanxicoApi.create(
            api_url='https://www.banxico.org.mx/SieAPIRest/service/v1/series/',
            token='326fafac9dc7facc7048216652fcc83200ed186275f65eabf37c970da5855d38',
            entry_point='datos',
        )

        udis = api.get(
            serie='SP68257',
            start_date='2022-2-25',
            end_date='2022-2-28',
        )

        self.assertEqual(len(udis), 4)
