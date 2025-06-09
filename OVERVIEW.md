# Overview

## Architecture

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Client    │───▶│   Flask     │───▶│   Manager  │───▶│   Bedrock   │
│   (REST)    │    │   (app.py)  │    │  (manager.py)│   │  (client.py)│
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
                           │                   │
                           ▼                   ▼
                   ┌─────────────┐    ┌─────────────┐
                   │   Config    │    │   Models    │
                   │ (config.py) │    │ (models.py) │
                   └─────────────┘    └─────────────┘
```

## Components

| Component | Purpose | Key Features |
|-----------|---------|-------------|
| **app.py** | REST API server | 5 endpoints, error handling, JSON responses |
| **manager.py** | Business logic | Conversation management, in-memory storage |
| **models.py** | Data models | Conversation & Message classes |
| **client.py** | AWS integration | Bedrock Claude API, prompt generation |
| **config.py** | Configuration | YAML config loader |

## Data Flow

1. **HTTP Request** → Flask endpoint
2. **Validation** → Manager business logic
3. **Model Update** → In-memory storage
4. **AI Request** → Bedrock client (if message)
5. **Response** → JSON back to client

## Error Handling

| Level | Strategy | Implementation |
|-------|----------|----------------|
| **API** | Try-catch blocks | Returns 400/404/500 with error messages |
| **Manager** | Validation checks | Returns error tuples `(None, None, "error")` |
| **Bedrock** | Graceful fallback | Returns apologetic message on AWS failures |
| **Config** | Safe defaults | Continues with fallback values on load errors |

## Test Coverage

| File | Test File | Coverage |
|------|-----------|----------|
| **app.py** | app_test.py |  All endpoints, error cases |
| **manager.py** | manager_test.py |  Business logic, edge cases |
| **models.py** | Indirect | Via manager tests |
| **client.py** | Manual | AWS integration testing |

## Configuration

```yaml
# config.yaml structure
server: {debug, host, port}
aws: {region, access_key_id, secret_access_key}
bedrock: {model_id, max_tokens}
```

## Lessons Learned
- **AWS Integrations** - Integrate with AWS client
- **Coonfiguration** -Needed for environmental variables and customizations
- **Error Handling** - Informative error response are good for troubleshooting

## Future Improvements

- **Data Persistency** - Use DB to collect activity data and log data
- **API improve** - API authentication, rate limiting, pagination
- **Deployment Redy** - Containerized production setup 
