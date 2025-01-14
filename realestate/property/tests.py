from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from decimal import Decimal
from property.models import Property, PropertyImage, Shortlist
from django.core.files.uploadedfile import SimpleUploadedFile

class PropertyModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.property = Property.objects.create(
            user=self.user,
            latitude=Decimal('51.507351'),
            longitude=Decimal('-0.127758'),
            city='London',
            price=1000.00,
            property_type='student',
            room_count=2,
            status='available'
        )

    def test_property_creation(self):
        self.assertEqual(self.property.city, 'London')
        self.assertEqual(self.property.property_type, 'student')
        self.assertEqual(self.property.status, 'available')
        self.assertFalse(self.property.admin_approved)

class PropertyAPITests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        
        self.london_property = Property.objects.create(
            user=self.user,
            latitude=Decimal('51.507351'),
            longitude=Decimal('-0.127758'),
            city='London',
            price=1000.00,
            property_type='student',
            room_count=2,
            status='available',
            admin_approved=True
        )

    def test_create_property(self):
        property_data = {
            'latitude': '51.507351',
            'longitude': '-0.127758',
            'city': 'London',
            'price': 1000.00,
            'property_type': 'student',
            'room_count': 2,
            'status': 'available'
        }
        url = reverse('property-list-list')
        response = self.client.post(url, property_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_properties(self):
        url = reverse('property-list-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_filter_properties_by_price(self):
        url = reverse('property-list-list')
        
        # Should find the property
        response = self.client.get(f"{url}?min_price=500&max_price=1500")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        
        # Should not find the property
        response = self.client.get(f"{url}?min_price=2000")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)

    def test_filter_properties_by_city(self):
        url = reverse('property-list-list')
        response = self.client.get(f"{url}?city=London")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

        response = self.client.get(f"{url}?city=Paris")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)

    def test_property_sorting(self):
        Property.objects.create(
            user=self.user,
            latitude=Decimal('51.507351'),
            longitude=Decimal('-0.127758'),
            city='London',
            price=500.00, 
            property_type='student',
            room_count=2,
            status='available',
            admin_approved=True
        )
        
        url = reverse('property-list-list')
        response = self.client.get(f"{url}?sort_by=price")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['results'][0]['price'], 500.00)

class ShortlistAPITests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        
        self.property = Property.objects.create(
            user=self.user,
            latitude=Decimal('51.507351'),
            longitude=Decimal('-0.127758'),
            city='London',
            price=1000.00,
            property_type='student',
            room_count=2,
            status='available'
        )

    def test_add_to_shortlist(self):
        url = reverse('shortlist')
        response = self.client.post(url, {'property_id': self.property.property_id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Shortlist.objects.filter(user=self.user).exists())

    def test_get_shortlist(self):
        shortlist = Shortlist.objects.create(user=self.user)
        shortlist.properties.add(self.property)
        
        url = reverse('shortlist')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['properties']), 1)

    def test_remove_from_shortlist(self):
        shortlist = Shortlist.objects.create(user=self.user)
        shortlist.properties.add(self.property)
        
        url = reverse('shortlist')
        response = self.client.delete(url, {'property_id': self.property.property_id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(shortlist.properties.count(), 0)

class UserPortfolioAPITests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        
        self.property = Property.objects.create(
            user=self.user,
            latitude=Decimal('51.507351'),
            longitude=Decimal('-0.127758'),
            city='London',
            price=1000.00,
            property_type='student',
            room_count=2,
            status='available'
        )

    def test_get_user_portfolio(self):
        url = reverse('user-portfolio')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_empty_portfolio(self):
        Property.objects.all().delete()
        url = reverse('user-portfolio')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)