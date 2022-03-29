from audioop import reverse
from http import client
from urllib import response
from django.test import TestCase, Client
from django.shortcuts import reverse


class HomeTest(TestCase):

    def test_home_is_accesible(self):
        client = Client()

        response = client.get(reverse('core:home'))

        self.assertEqual(200, response.status_code)
