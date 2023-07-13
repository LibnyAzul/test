from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status


class VehicleTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_vehicle(self):
        data = {
            'plates': 'ABC123',
            'brand': 'Brand',
            'colour': 'Red',
        }

        response = self.client.post('/api/vehicle/add/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_vehicle(self):
        vehicle_id = 1  # Replace with a valid vehicle ID

        response = self.client.get(f'/api/vehicle/?id={vehicle_id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('entity', response.data)
        self.assertIn('plates', response.data)
        self.assertIn('brand', response.data)
        self.assertIn('colour', response.data)

    def test_get_vehicle_invalid_id(self):
        invalid_vehicle_id = 9999

        response = self.client.get(f'/api/vehicle/?id={invalid_vehicle_id}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('Error', response.data)

    def test_edit_vehicle(self):
        vehicle_id = 1  # Replace with a valid vehicle ID
        data = {
            'id': vehicle_id,
            'brand': 'New Brand',
        }

        response = self.client.post('/api/vehicle/edit/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_edit_vehicle_invalid_id(self):
        invalid_vehicle_id = 9999
        data = {
            'id': invalid_vehicle_id,
            'brand': 'New Brand',
        }

        response = self.client.post('/api/vehicle/edit/', data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('Error', response.data)

    def test_vehicle_map(self):
        response = self.client.get('/api/vehicle/map/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('vehicles', response.data)
