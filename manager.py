from models import Conversation
from client import BedrockClient

class Manager:
    def __init__(self):
        self.conversations = {}
        self.bedrock_client = BedrockClient()
    
    def create_conversation(self, title):
        conversation = Conversation(title)
        self.conversations[conversation.id] = conversation
        return conversation
    
    def get_conversation(self, conversation_id):
        return self.conversations.get(conversation_id)
    
    def list_conversations(self):
        return list(self.conversations.values())
    
    def send_message(self, conversation_id, message_content):
        conversation = self.get_conversation(conversation_id)
        if not conversation:
            return None, None, "Conversation not found"
        
        if not message_content:
            return None, None, "Message content is required"
        
        # Add user message
        user_message = conversation.add_message("user", message_content)
        
        # Generate AI response
        ai_response_content = self.bedrock_client.generate_response(message_content, conversation.messages[:-1])
        ai_message = conversation.add_message("assistant", ai_response_content)
        
        return user_message, ai_message, None
