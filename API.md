# Conversational AI REST API Specification

## Overview

This document describes the REST API endpoints.

**Base URL**: `http://localhost:5000`
**Content-Type**: `application/json`  
**API Version**: 1.0

## Authentication

Currently, the API does not require authentication. All endpoints are publicly accessible.

## HTTP Status Codes

- `200 OK` - Successful request
- `201 Created` - Resource created successfully
- `400 Bad Request` - Invalid request data
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

---

## Endpoints

### 1. Health Check

Check if the API server is running and healthy.

**Endpoint**: `GET /health`

**Parameters**: None

**Response**:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00.000Z"
}
```

**Example**:
```bash
curl -X GET http://localhost:5000/health
```

---

### 2. Create Conversation

Create a new conversation with an optional title.

**Endpoint**: `POST /conversations`

**Request Body**:
```json
{
  "title": "string (optional, default: 'New Conversation')"
}
```

**Response** (`201 Created`):
```json
{
  "success": true,
  "conversation": {
    "id": "string",
    "title": "string",
    "messages": []
  }
}
```

**Example**:
```bash
curl -X POST http://localhost:5000/conversations \
  -H "Content-Type: application/json" \
  -d '{"title": "Planning my vacation"}'
```

**Response Example**:
```json
{
  "success": true,
  "conversation": {
    "id": "conv_12345",
    "title": "Planning my vacation",
    "messages": []
  }
}
```

---

### 3. List Conversations

Retrieve a list of all conversations (without message details).

**Endpoint**: `GET /conversations`

**Parameters**: None

**Response** (`200 OK`):
```json
{
  "success": true,
  "conversations": [
    {
      "id": "string",
      "title": "string"
    }
  ],
  "total": "integer"
}
```

**Example**:
```bash
curl -X GET http://localhost:5000/conversations
```

**Response Example**:
```json
{
  "success": true,
  "conversations": [
    {
      "id": "conv_12345",
      "title": "Planning my vacation"
    },
    {
      "id": "conv_67890",
      "title": "Recipe ideas"
    }
  ],
  "total": 2
}
```

---

### 4. Get Conversation Details

Retrieve a specific conversation with its complete message history.

**Endpoint**: `GET /conversations/{conversation_id}`

**Path Parameters**:
- `conversation_id` (string, required) - The unique identifier of the conversation

**Response** (`200 OK`):
```json
{
  "success": true,
  "conversation": {
    "id": "string",
    "title": "string", 
    "messages": [
      {
        "actor": "string", // "user" or "assistant"
        "content": "string"
      }
    ]
  }
}
```

**Error Response** (`404 Not Found`):
```json
{
  "success": false,
  "error": "Conversation not found"
}
```

**Example**:
```bash
curl -X GET http://localhost:5000/conversations/conv_12345
```

**Response Example**:
```json
{
  "success": true,
  "conversation": {
    "id": "conv_12345",
    "title": "Planning my vacation",
    "messages": [
      {
        "actor": "user",
        "content": "I want to plan a trip to Japan"
      },
      {
        "actor": "assistant", 
        "content": "Japan is a wonderful destination! What time of year are you thinking of visiting?"
      }
    ]
  }
}
```

---

### 5. Send Message

Send a message to a conversation and receive an AI-generated response.

**Endpoint**: `POST /conversations/{conversation_id}/messages`

**Path Parameters**:
- `conversation_id` (string, required) - The unique identifier of the conversation

**Request Body**:
```json
{
  "message": "string (required)"
}
```

**Response** (`200 OK`):
```json
{
  "success": true,
  "user_message": {
    "actor": "user",
    "content": "string"
  },
  "ai_response": {
    "actor": "assistant", 
    "content": "string"
  }
}
```

**Error Responses**:
- `400 Bad Request` - Missing or empty message
- `404 Not Found` - Conversation not found

**Example**:
```bash
curl -X POST http://localhost:5000/conversations/conv_12345/messages \
  -H "Content-Type: application/json" \
  -d '{"message": "What are the best places to visit in Tokyo?"}'
```

**Response Example**:
```json
{
  "success": true,
  "user_message": {
    "actor": "user",
    "content": "What are the best places to visit in Tokyo?"
  },
  "ai_response": {
    "actor": "assistant",
    "content": "Tokyo has many amazing places to visit!"
  }
}
```

## Rate Limiting

Currently, there are no rate limiting restrictions. Consider implementing rate limiting for production usage.
