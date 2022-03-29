from datetime import datetime, timedelta

from django.shortcuts import reverse
from django.test import Client, TestCase
from .helpers import get_banxico_data


class UdisTest(TestCase):

    def test_banxico_api_helper_one_data(self):
        data = get_banxico_data(start_date='2022-3-28')

        self.assertEqual(data[0]['dato'], 7.236109)

    def test_banxico_api_helper_many_data(self):
        data = get_banxico_data(start_date='2022-3-1', end_date='2022-3-20')

        self.assertEqual(len(data), 20)

    def test_get_udis(self):
        client = Client()

        response = client.get(reverse('udis:index'))

        self.assertEqual(200, response.status_code)
        self.assertContains(response, 'form')
        self.assertContains(response, 'start_date')
        self.assertContains(response, 'end_date')
        self.assertTrue('udis_today' in response.context)

    def test_get_udis_range_only_start_date(self):
        client = Client()

        response = client.get(
            reverse('udis:index'),
            {
                'start_date': '2020-02-20',
                'end_date': '',
            }
        )

        self.assertEqual(200, response.status_code)

    def test_get_udis_range_ok(self):
        client = Client()

        response = client.get(
            reverse('udis:index'),
            {
                'start_date': '2020-02-01',
                'end_date': '2020-02-20',
            }
        )

        self.assertEqual(200, response.status_code)

        data = response.context.get('udis')

        self.assertEqual(len(data), 20)

    def test_get_udis_wrong_data_range(self):
        client = Client()

        response = client.get(
            reverse('udis:index'),
            {
                'start_date': '2020-02-20',
                'end_date': '2020-02-01',
            }
        )

        self.assertEqual(200, response.status_code)

        form = response.context.get('form')

        self.assertTrue(
            'La fecha inicial debe ser menor a la fecha final.' in form.non_field_errors()
        )

    def test_get_udis_1995_5_fail(self):
        client = Client()

        response = client.get(
            reverse('udis:index'),
            {
                'start_date': '1995-04-02',
                'end_date': '1995-04-20',
            }
        )

        self.assertEqual(200, response.status_code)

        form = response.context.get('form')

        self.assertTrue(
            'La fecha inicial no debe ser menor al mes de mayo de 1995' in form.non_field_errors()
        )
