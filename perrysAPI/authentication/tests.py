from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from messaging.models import Conversation


class UserTestCase(TestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create(username='test', email='', password='example')
        self.user2 = User.objects.create(username='example', email='', password='test')

    def tearDown(self):
        self.user1.delete()
        self.user2.delete()

    def test_get_user(self):
        response = self.client.get('/users/{}/'.format(self.user1.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], self.user1.id)
        self.assertEqual(response.data['username'], self.user1.username)

    def test_get_users(self):
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['username'], self.user1.username)
        self.assertEqual(response.data[1]['username'], self.user2.username)

    def test_create_user(self):
        data = {'username': 'testing', 'email': '', 'password': 'password1'}
        response = self.client.post('/users/', data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['id'], 3)
        self.assertEqual(response.data['username'], data['username'])
    
    def test_delete_user_fail(self):
        response = self.client.delete('/users/2/')
        self.assertEqual(response.status_code, 403)

    def test_delete_user(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.delete('/users/{}/'.format(self.user2.id))
        self.assertEqual(response.status_code, 204)
        response = self.client.get('/users/')
        self.assertEqual(len(response.data), 1)

    def test_get_user_contacts(self):
        conv = Conversation()
        conv.save()
        conv.users.add(self.user1, self.user2)
        response = self.client.get('/users/{}/contacts/'.format(self.user1.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['id'], self.user1.id)
        self.assertEqual(response.data[1]['id'], self.user2.id)
