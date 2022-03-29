from django.test import Client, TestCase
from django.shortcuts import reverse


class UdisTest(TestCase):

    def test_get_udis_range(self):

        client = Client()

        response = client.get(reverse('udis:index'))

        self.assertEqual(200, response.status_code)
        self.assertContains(response, 'form')
        self.assertContains(response, 'start_date')
        self.assertContains(response, 'end_date')
