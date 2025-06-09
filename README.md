# Conversational AI Application

Flask REST API for conversational AI powered by AWS Bedrock Claude. Create conversations, send messages, and get intelligent AI responses with conversation context.

## Documentation

📋 **[API Specification](./API.md)** - Complete endpoint documentation with examples  
🔧 **[Technical Overview](./OVERVIEW.md)** - Architecture, components, and implementation details

## How to Run

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure AWS credentials in `config.yaml`:**

3. **Start the server:**
   ```bash
   python app.py
   ```

4. **Test the API:**
   ```bash
   # Health check
   curl http://localhost:5000/health
   
   # Create conversation and send message
   curl -X POST http://localhost:5000/conversations \
     -H "Content-Type: application/json" \
     -d '{"title": "My Chat"}'
   ```

Server runs at `http://localhost:5000` - see [API.md](./API.md) for complete usage examples. 