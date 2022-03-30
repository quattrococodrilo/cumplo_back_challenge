from django.shortcuts import reverse
from django.test import Client, TestCase


class UdisTest(TestCase):

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

        dates = response.context.get('udis_dates')
        values = response.context.get('udis_values')

        self.assertEqual(len(dates), 20)
        self.assertEqual(len(values), 20)

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
