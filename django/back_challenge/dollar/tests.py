from django.shortcuts import reverse
from django.test import Client, TestCase


class DollarTest(TestCase):

    def test_get_dollar(self):
        client = Client()

        response = client.get(reverse('dollar:index'))

        self.assertEqual(200, response.status_code)
        self.assertContains(response, 'form')
        self.assertContains(response, 'start_date')
        self.assertContains(response, 'end_date')
        self.assertTrue('dollar_today' in response.context)

    def test_get_dollar_range_only_start_date(self):
        client = Client()

        response = client.get(
            reverse('dollar:index'),
            {
                'start_date': '2020-02-20',
                'end_date': '',
            }
        )

        self.assertEqual(200, response.status_code)

    def test_get_dollar_range_ok(self):
        client = Client()

        response = client.get(
            reverse('dollar:index'),
            {
                'start_date': '2020-02-01',
                'end_date': '2020-02-20',
            }
        )

        self.assertEqual(200, response.status_code)

        dates = response.context.get('dollar_dates')
        values = response.context.get('dollar_values')

        self.assertTrue(len(dates) > 10)
        self.assertTrue(len(values) > 10)

    def test_get_dollar_wrong_data_range(self):
        client = Client()

        response = client.get(
            reverse('dollar:index'),
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

    def test_get_dollar_1953_1_fail(self):
        client = Client()

        response = client.get(
            reverse('dollar:index'),
            {
                'start_date': '1953-04-02',
                'end_date': '1953-04-20',
            }
        )

        self.assertEqual(200, response.status_code)

        form = response.context.get('form')

        self.assertTrue(
            'La fecha inicial no puede ser menor a 1954.' in form.non_field_errors()
        )
