from flask import Flask, request, jsonify
from datetime import datetime
from manager import Manager

app = Flask(__name__)

manager = Manager()

@app.route('/conversations', methods=['POST'])
def create_conversation():
    """Create a new conversation"""
    try:
        data = request.get_json() or {}
        title = data.get('title', 'New Conversation')
        
        conversation = manager.create_conversation(title)
        
        return jsonify({
            "success": True,
            "conversation": conversation.to_dict()
        }), 201
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
    
@app.route('/conversations/<conversation_id>', methods=['GET'])
def get_conversation(conversation_id):
    """Get a specific conversation with all messages"""
    try:
        conversation = manager.get_conversation(conversation_id)
        if not conversation:
            return jsonify({
                "success": False,
                "error": "Conversation not found"
            }), 404
        
        return jsonify({
            "success": True,
            "conversation": conversation.to_dict()
        }), 200
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/conversations', methods=['GET'])
def list_conversations():
    """List all existing conversations"""
    try:
        conversations = manager.list_conversations()
        conversation_list = [conv.to_dict() for conv in conversations]
        
        return jsonify({
            "success": True,
            "conversations": conversation_list,
            "total": len(conversation_list)
        }), 200
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/conversations/<conversation_id>/messages', methods=['POST'])
def send_message(conversation_id):
    """Send a message to a conversation and get response"""
    try:
        data = request.get_json()
        
        user_message, ai_message, error = manager.send_message(
            conversation_id, data.get('message', '')
        )
        
        if error:
            return jsonify({
                "success": False,
                "error": error
            }), 400
        
        return jsonify({
            "success": True,
            "user_message": user_message.to_dict(),
            "ai_response": ai_message.to_dict(),
        }), 200
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 