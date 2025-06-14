import uuid

class Message:
    def __init__(self, actor, content):
        self.actor = actor
        self.content = content
    
    def to_dict(self):
        return {
            "actor": self.actor,
            "content": self.content
        }

class Conversation:
    def __init__(self, title):
        self.id = str(uuid.uuid4())
        self.title = title
        self.messages = []
    
    def add_message(self, actor, content):
        message = Message(actor, content)
        self.messages.append(message)
        return message
    
    def to_dict(self, include_messages=True):
        result = {
            "id": self.id,
            "title": self.title,
            "message_count": len(self.messages)
        }
        if include_messages:
            result["messages"] = [msg.to_dict() for msg in self.messages]
        return result