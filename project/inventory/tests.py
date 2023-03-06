from rest_framework.test import APITestCase
from rest_framework import status
from project.inventory.models import Product
from project.inventory.serializers import ProductSerializer
from project.inventory.constants import *


class TestProduct(APITestCase):
    def setUp(self):
        self.product_data = {
            'name': 'Product 1',
            'description': 'This is the description for product 1.',
            'status': ACTIVE,
            'category': 1
        }
        self.url = '/api/v1.0/products/'

    def test_create_product(self):
        response = self.client.post(self.url, self.product_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(Product.objects.get().name, 'Product 1')

    def test_read_product_list(self):
        response = self.client.get(self.url)
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_read_product_detail(self):
        product = Product.objects.create(name='Product 2', description='Description 2', status=ACTIVE, category_id=1)
        response = self.client.get(f'{self.url}{product.id}/')
        serializer = ProductSerializer(product)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_update_product(self):
        product = Product.objects.create(name='Product 3', description='Description 3', status=ACTIVE, category_id=1)
        data = {'name': 'Product 3 - Updated', 'description': 'Updated description', 'price': 22.99, 'category': 1}
        response = self.client.put(f'{self.url}{product.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        product.refresh_from_db()
        self.assertEqual(product.name, 'Product 3 - Updated')
        self.assertEqual(product.price, 22.99)

    def test_delete_product(self):
        product = Product.objects.create(name='Product 4', description='Description 4', status=ACTIVE, category_id=1)
        response = self.client.delete(f'{self.url}{product.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)
