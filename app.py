from flask import Flask, request, jsonify
from datetime import datetime
from manager import Manager
from loguru import logger
from config import get_config

config = get_config()
app = Flask(__name__)
manager = Manager()

@app.route('/conversations', methods=['POST'])
def create_conversation():
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
    try:
        conversations = manager.list_conversations()
        conversation_list = [conv.to_dict(include_messages=False) for conv in conversations]
        
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
    try:
        data = request.get_json() or {}
        
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
    debug = config['server']['debug']
    host = config['server']['host']
    port = config['server']['port']
    
    logger.info(f"Starting Flask server on {host}:{port} (debug={debug})")
    app.run(debug=debug, host=host, port=port) 