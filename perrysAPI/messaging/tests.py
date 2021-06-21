from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from .models import Message, Conversation, Like


class MessageTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create(username='test', email='', password='example')
        self.user2 = User.objects.create(username='example', email='', password='test')
        self.conversation = Conversation()
        self.conversation.save()
        self.conversation.users.add(self.user1, self.user2)
        self.message1 = Message.objects.create(conversation=self.conversation, sender=self.user1, text='Hello there')
        self.message2 = Message.objects.create(conversation=self.conversation, sender=self.user2, text='Ah general')

    def tearDown(self):
        self.message1.delete()
        self.message2.delete()
        self.conversation.delete()
        self.user1.delete()
        self.user2.delete()

    def test_get_message(self):
        response = self.client.get('/messages/{}/'.format(self.message1.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], self.message1.id)
        self.assertEqual(response.data['conversation'], self.message1.conversation.id)
        self.assertEqual(response.data['sender'], self.message1.sender.id)
        self.assertEqual(response.data['text'], self.message1.text)

    def test_get_messages(self):
        response = self.client.get('/messages/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['id'], self.message1.id)
        self.assertEqual(response.data[1]['id'], self.message2.id)

    def test_create_message_fail(self):
        data = {'conversation': self.conversation.id, 'sender': self.user1.id, 'text': 'this will fail'}
        response = self.client.post('/messages/', data=data)
        self.assertEqual(response.status_code, 403)
    
    def test_create_message(self):
        self.client.force_authenticate(user=self.user1)
        data = {'conversation': self.conversation.id, 'sender': self.user1.id, 'text': 'this will pass'}
        response = self.client.post('/messages/', data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['conversation'], data['conversation'])
        self.assertEqual(response.data['sender'], data['sender'])
        self.assertEqual(response.data['text'], data['text'])

    def test_update_message(self):
        self.client.force_authenticate(user=self.user1)
        data = {'text': 'has been updated'}
        response = self.client.put('/messages/{}/'.format(self.message1.id), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], self.message1.id)
        self.assertEqual(response.data['text'], data['text'])

    def test_delete_message(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.delete('/messages/{}/'.format(self.message1.id))
        self.assertEqual(response.status_code, 204)

class ConversationTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create(username='test', email='', password='example')
        self.user2 = User.objects.create(username='example', email='', password='test')
        self.conversation = Conversation()
        self.conversation.save()
        self.conversation.users.add(self.user1, self.user2)

    def tearDown(self):
        self.conversation.delete()
        self.user1.delete()
        self.user2.delete()

    def test_get_conversation(self):
        response = self.client.get('/conversations/{}/'.format(self.conversation.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], self.conversation.id)
        self.assertEqual(response.data['users'][0]['id'], self.user1.id)
        self.assertEqual(response.data['users'][1]['id'], self.user2.id)

    def test_get_conversations(self):
        response = self.client.get('/conversations/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.conversation.id)

    def test_create_conversation_fail(self):
        self.client.force_authenticate(user=self.user1)
        data = {'users': [self.user2.id]}
        response = self.client.post('/conversations/', data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {'users': ['Cannot have more than 1 conversation with the same user.']})

    def test_create_conversation(self):
        user3 = User.objects.create(username='testing', email='', password='example')
        self.client.force_authenticate(user=self.user1)
        data = {'users': [user3.id]}
        response = self.client.post('/conversations/', data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['users'][0], self.user1.id)
        self.assertEqual(response.data['users'][1], user3.id)
        user3.delete()

    def test_delete_conversation(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.delete('/conversations/{}/'.format(self.conversation.id))
        self.assertEqual(response.status_code, 204)


class LikeTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create(username='test', email='', password='example')
        self.user2 = User.objects.create(username='example', email='', password='test')
        self.conversation = Conversation()
        self.conversation.save()
        self.conversation.users.add(self.user1, self.user2)
        self.message1 = Message.objects.create(conversation=self.conversation, sender=self.user1, text='Hello there')
        self.message2 = Message.objects.create(conversation=self.conversation, sender=self.user2, text='Ah general')
        self.like1 = Like.objects.create(user=self.user1, message=self.message2)

    def tearDown(self):
        self.like1.delete()
        self.message1.delete()
        self.message2.delete()
        self.conversation.delete()
        self.user1.delete()
        self.user2.delete()

    def test_get_like(self):
        response = self.client.get('/likes/{}/'.format(self.like1.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], self.like1.id)
        self.assertEqual(response.data['user']['id'], self.user1.id)

    def test_get_likes(self):
        response = self.client.get('/likes/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_create_like(self):
        self.client.force_authenticate(user=self.user2)
        data = {'user': self.user2.id, 'message': self.message1.id}
        response = self.client.post('/likes/', data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['user'], data['user'])
        self.assertEqual(response.data['message'], data['message'])

    def test_delete_like(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.delete('/likes/{}/'.format(self.like1.id))
        self.assertEqual(response.status_code, 204)
