import unittest
from manager import Manager
from models import Conversation, Message

class TestManager(unittest.TestCase):
    
    def setUp(self):
        self.manager = Manager()
    
    def tearDown(self):
        self.manager.conversations.clear()
    
    def test_create_conversation(self):
        title = "Test Conversation"
        conversation = self.manager.create_conversation(title)
        
        self.assertIsInstance(conversation, Conversation)
        self.assertEqual(conversation.title, title)
        self.assertEqual(len(conversation.messages), 0)
        self.assertIn(conversation.id, self.manager.conversations)
    
    def test_get_conversation_existing(self):
        conversation = self.manager.create_conversation("Test")
        retrieved = self.manager.get_conversation(conversation.id)
        
        self.assertEqual(retrieved, conversation)
        self.assertEqual(retrieved.title, "Test")
    
    def test_get_conversation_nonexistent(self):
        result = self.manager.get_conversation("fake-id")
        self.assertIsNone(result)
    
    def test_list_conversations_empty(self):
        conversations = self.manager.list_conversations()
        self.assertEqual(conversations, [])
    
    def test_list_conversations_with_data(self):
        conv1 = self.manager.create_conversation("First")
        conv2 = self.manager.create_conversation("Second")
        conv3 = self.manager.create_conversation("Third")
        
        conversations = self.manager.list_conversations()
        self.assertEqual(len(conversations), 3)
        
        conversation_ids = [conv.id for conv in conversations]
        self.assertIn(conv1.id, conversation_ids)
        self.assertIn(conv2.id, conversation_ids)
        self.assertIn(conv3.id, conversation_ids)
    
    def test_send_message_success(self):
        conversation = self.manager.create_conversation("Test Chat")
        message_content = "Hello, world!"
        
        user_msg, ai_msg, error = self.manager.send_message(
            conversation.id, message_content
        )
        
        self.assertIsNone(error)
        self.assertIsInstance(user_msg, Message)
        self.assertIsInstance(ai_msg, Message)
        
        self.assertEqual(user_msg.actor, "user")
        self.assertEqual(user_msg.content, message_content)
        self.assertEqual(ai_msg.actor, "assistant")
        self.assertEqual(ai_msg.content, "Hello, how can I help you today?")
        
        self.assertEqual(len(conversation.messages), 2)
        self.assertEqual(conversation.messages[0], user_msg)
        self.assertEqual(conversation.messages[1], ai_msg)
    
    def test_send_message_nonexistent_conversation(self):
        user_msg, ai_msg, error = self.manager.send_message(
            "fake-id", "Hello"
        )
        
        self.assertIsNone(user_msg)
        self.assertIsNone(ai_msg)
        self.assertEqual(error, "Conversation not found")
    
    def test_send_none_message(self):
        conversation = self.manager.create_conversation("Test")
        
        user_msg, ai_msg, error = self.manager.send_message(
            conversation.id, None
        )
        
        self.assertIsNone(user_msg)
        self.assertIsNone(ai_msg)
        self.assertEqual(error, "Message content is required")

if __name__ == '__main__':
    unittest.main() 