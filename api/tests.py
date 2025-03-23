from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status

class ProductsTestCase(APITestCase):

    def product_creation(self):
        response = self.client.get(reverse('create_product'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], '')

# testing creating user


# testing login
# POST http://127.0.0.1:8000/api/

# Create your tests here.
