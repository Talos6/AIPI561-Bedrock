import boto3
import json
from loguru import logger
from config import get_config

class BedrockClient:
    def __init__(self):
        self.config = get_config()
        self.client = self._initialize_client()
        
    def _initialize_client(self):
        try:
            client = boto3.client(
                service_name='bedrock-runtime',
                region_name=self.config['aws']['region'],
                aws_access_key_id=self.config['aws']['access_key_id'],
                aws_secret_access_key=self.config['aws']['secret_access_key']
            )
            logger.info(f"Bedrock client initialized for region: {self.config['aws']['region']}")
            return client
        except Exception as e:
            logger.error(f"Failed to initialize Bedrock client: {e}")
            raise
    
    def _format_history(self, history):
        formatted_messages = []
        for msg in history:
            role = "User" if msg.actor == "user" else "Assistant"
            formatted_messages.append(f"{role}: {msg.content}")
        return "\n".join(formatted_messages)
    
    def _create_prompt(self, message, history):
        """Create a simple prompt with conversation history and current message"""
        formatted_history = self._format_history(history)
        
        if formatted_history:
            prompt = f"""You are a helpful AI assistant. Here is the conversation history:

                        {formatted_history}

                        User: {message}

                        Please provide a helpful and relevant response to the user's message."""
        else:
            prompt = f"""You are a helpful AI assistant. Please provide a helpful and relevant response to the following message:

                        User: {message}"""
        
        return prompt
    
    def generate_response(self, message, history):
        try:
            prompt = self._create_prompt(message, history)
            
            # Prepare the payload for Claude model
            payload = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": self.config['bedrock']['max_tokens'],
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            }
            
            response = self.client.invoke_model(
                modelId=self.config['bedrock']['model_id'],
                body=json.dumps(payload)
            )
            
            response_body = json.loads(response['body'].read())
            logger.info(f"Bedrock response: {response_body}")
            generated_text = response_body['content'][0]['text']
            return generated_text

        except Exception as e:
            logger.error(f"Error generating response from Bedrock: {e}")
            return "I apologize, but I'm having trouble generating a response right now. Please try again."
