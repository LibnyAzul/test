from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status


class TrackingTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_tracking(self):
        data = {
            'vehicle_plates': 'ABC123',
            'latitude': 20.123456,
            'longitude': -103.987654
        }

        response = self.client.post('/api/tracking/create/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_latest_tracking(self):
        vehicle_id = 1  # Replace with a valid vehicle ID

        response = self.client.get(f'/api/tracking/getLatestTracking/?id={vehicle_id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('latitude', response.data)
        self.assertIn('longitude', response.data)

    def test_get_latest_tracking_invalid_id(self):
        invalid_vehicle_id = 9999

        response = self.client.get(f'/api/tracking/getLatestTracking/?id={invalid_vehicle_id}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('Error', response.data)

    def test_trackings_view(self):
        response = self.client.post('/api/tracking/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertIn('count', response.data)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)

    def test_create_tracking_invalid_data(self):
        # Missing required fields
        data = {}

        response = self.client.post('/api/tracking/create/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Error', response.data)
        self.assertIn('Message', response.data)
