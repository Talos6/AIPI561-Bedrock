import unittest
import json
from app import app, manager

class TestConversationalApp(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        manager.conversations.clear()
    
    def test_health_check(self):
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')
        self.assertIn('timestamp', data)
    
    def test_create_conversation_with_title(self):
        custom_title = "My Custom Conversation"
        response = self.app.post('/conversations',
                                json={'title': custom_title},
                                content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
        
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('conversation', data)
        
        conversation = data['conversation']
        self.assertIn('id', conversation)
        self.assertEqual(conversation['title'], custom_title)
        self.assertEqual(conversation['message_count'], 0)
        self.assertEqual(conversation['messages'], [])
    
    def test_create_conversation_without_title(self):
        response = self.app.post('/conversations', json={}, content_type='application/json')

        self.assertEqual(response.status_code, 201)

        
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['conversation']['title'], 'New Conversation')
    
    def test_get_conversation_success(self):
        create_response = self.app.post('/conversations', 
                                       json={'title': 'Test Conversation'})
        conversation_id = json.loads(create_response.data)['conversation']['id']
        
        response = self.app.get(f'/conversations/{conversation_id}')
        
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        
        conversation = data['conversation']
        self.assertEqual(conversation['id'], conversation_id)
        self.assertEqual(conversation['title'], 'Test Conversation')
        self.assertEqual(conversation['message_count'], 0)
        self.assertEqual(conversation['messages'], [])
    
    def test_get_conversation_not_found(self):
        fake_id = "nonexistent-id"
        response = self.app.get(f'/conversations/{fake_id}')
        
        self.assertEqual(response.status_code, 404)
        
        data = json.loads(response.data)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 'Conversation not found')
    
    def test_list_conversations_empty(self):
        response = self.app.get('/conversations')
        
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['conversations'], [])
        self.assertEqual(data['total'], 0)
    
    def test_list_conversations_with_data(self):
        self.app.post('/conversations', json={'title': 'First Conversation'})
        self.app.post('/conversations', json={'title': 'Second Conversation'})
        self.app.post('/conversations', json={'title': 'Third Conversation'})
        
        response = self.app.get('/conversations')
        
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['conversations']), 3)
        self.assertEqual(data['total'], 3)
        
        for conv in data['conversations']:
            self.assertIn('id', conv)
            self.assertIn('title', conv)
            self.assertIn('message_count', conv)
    
    def test_send_message_success(self):
        create_response = self.app.post('/conversations', 
                                       json={'title': 'Test Conversation'},
                                       content_type='application/json')
        conversation_id = json.loads(create_response.data)['conversation']['id']
        
        test_message = "Hello, how are you?"
        response = self.app.post(f'/conversations/{conversation_id}/messages',
                                json={'message': test_message},
                                content_type='application/json')
        print(response.data)
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        
        user_message = data['user_message']
        self.assertEqual(user_message['actor'], 'user')
        self.assertEqual(user_message['content'], test_message)
        
        ai_response = data['ai_response']
        self.assertEqual(ai_response['actor'], 'assistant')
        self.assertEqual(ai_response['content'], 'Hello, how can I help you today?')
    
    def test_send_message_to_nonexistent_conversation(self):
        fake_id = "nonexistent-id"
        response = self.app.post(f'/conversations/{fake_id}/messages',
                                json={'message': 'Hello'},
                                content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        
        data = json.loads(response.data)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 'Conversation not found')
    
    def test_send_empty_message(self):
        create_response = self.app.post('/conversations', 
                                       json={'title': 'Test Conversation'},
                                       content_type='application/json')
        conversation_id = json.loads(create_response.data)['conversation']['id']
        
        response = self.app.post(f'/conversations/{conversation_id}/messages',
                                json={'message': ''},
                                content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        
        data = json.loads(response.data)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 'Message content is required')

if __name__ == '__main__':
    unittest.main() 