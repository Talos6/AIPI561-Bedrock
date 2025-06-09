from models import Conversation, Message

class Manager:
    def __init__(self):
        self.conversations = {}
    
    def create_conversation(self, title):
        conversation = Conversation(title)
        self.conversations[conversation.id] = conversation
        return conversation
    
    def get_conversation(self, conversation_id):
        return self.conversations.get(conversation_id)
    
    def list_conversations(self):
        return list(self.conversations.values())
    
    def send_message(self, conversation_id, message_content):
        """Send a message to a conversation and get AI response"""
        conversation = self.get_conversation(conversation_id)
        if not conversation:
            return None, None, "Conversation not found"
        
        # Add user message
        user_message = conversation.add_message("user", message_content)
        
        # Generate AI response
        ai_response_content = self.generate_ai_response(message_content, conversation.messages)
        ai_message = conversation.add_message("assistant", ai_response_content)
        
        return user_message, ai_message, None
    
    def generate_ai_response(self, user_message, conversation_history):
        return 'Hello, how can I help you today?'