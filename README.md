# Conversational SIEM Assistant for Investigation and Automated Threat Reporting using NLP

A comprehensive Natural Language Processing (NLP) powered interface that connects directly with ELK-based SIEMs (Elastic SIEM/Wazuh) and supports conversational investigations through multi-turn natural language queries.

## 🎯 Problem Statement

ELK-based SIEMs such as Elastic SIEM and Wazuh provide powerful log collection, correlation, and detection capabilities. However, effective interaction with these systems requires constructing complex queries using KQL or Elasticsearch DSL. This system addresses this gap by enabling security analysts to conduct investigations and generate reports conversationally, without needing to know query syntax.

## 🏗️ System Architecture

The system consists of three main components working together to provide a seamless conversational SIEM experience:

```
┌─────────────────┐    ┌─────────────────────┐    ┌──────────────────────┐
│  Terminal Chat  │───▶│  NLP SIEM          │───▶│ Elasticsearch Query  │
│     App         │    │  Middleware        │    │    Automater         │
│  (Frontend)     │    │  (Session Mgmt)    │    │  (NLP Translation)   │
└─────────────────┘    └─────────────────────┘    └──────────────────────┘
         │                       │                           │
         │                       ▼                           ▼
         │              ┌─────────────────┐    ┌─────────────────────────┐
         │              │     Redis       │    │    Wazuh/Elastic       │
         └──────────────│   (Sessions)    │    │       SIEM              │
                        └─────────────────┘    └─────────────────────────┘
```

### Component Overview

1. **Terminal Chat App** (`terminal-chat-app/`)
   - Modern React frontend with terminal aesthetics
   - User authentication and credential management
   - Conversational chat interface
   - SIEM log viewer with advanced filtering
   - Export capabilities (JSON, CSV, text)

2. **NLP SIEM Middleware** (`nlp_siem_middleware/`)
   - FastAPI-based session management
   - Redis-powered conversation persistence
   - Multi-turn conversation context
   - Elasticsearch query execution

3. **Elasticsearch Query Automater** (`ElasticSearch_Query_Automater/`)
   - Flask-based NLP translation service
   - Natural language to Elasticsearch DSL conversion
   - Rule-based translation with confidence scoring
   - Advanced query validation

## 🔄 System Workflow

### Initialization Phase
1. **User Authentication**: Frontend captures user credentials and rule configurations
2. **Session Creation**: Middleware creates a new session in Redis with credentials and rules
3. **Component Verification**: System verifies connectivity to NLP service and Elasticsearch

### Query Execution Phase
1. **Natural Language Input**: User enters conversational query (e.g., "Show me authentication failures from yesterday")
2. **Session Context**: Middleware retrieves session context from Redis
3. **NLP Translation**: Query is sent to NLP service which:
   - Analyzes intent and extracts entities
   - Maps to appropriate Wazuh rule types
   - Generates optimized Elasticsearch DSL query
   - Returns confidence score and validation
4. **Query Execution**: Middleware executes the Elasticsearch query against Wazuh indices
5. **Response Processing**: Raw logs are processed and formatted for frontend display
6. **Context Preservation**: Query and response are stored in session for follow-up questions

### Multi-Turn Conversations
- **Context Awareness**: System maintains conversation history
- **Follow-up Queries**: Users can refine searches ("Filter only VPN-related attempts")
- **Session Management**: All interactions persist across browser sessions

## 🚀 Quick Start Guide

### Prerequisites
- Docker and Docker Compose
- Node.js 18+ (for frontend development)
- Python 3.8+ (for backend services)

### 1. Start Core Services

```bash
# Start Redis for session management
docker run -d -p 6379:6379 --name redis redis:alpine

# Start Wazuh/Elasticsearch stack (see wazuh-setup-docker/ directory)
cd wazuh-setup-docker/
docker-compose up -d
```

### 2. Start Backend Services

```bash
# Start NLP Translation Service (Port 5000)
cd ElasticSearch_Query_Automater/
pip install -r requirements.txt
python main.py --host 0.0.0.0 --port 5000

# Start NLP SIEM Middleware (Port 8000)
cd ../nlp_siem_middleware/
pip install -r requirements.txt
python main.py
```

### 3. Start Frontend

```bash
# Start Terminal Chat App (Port 5173)
cd terminal-chat-app/
npm install
npm run dev
```

### 4. Access the Application

Open your browser to `http://localhost:5173` and follow the setup wizard.

## 📊 Core Features

### Conversational Investigations
- **Multi-turn Queries**: "What suspicious login attempts occurred yesterday?" → "Filter only VPN-related attempts"
- **Context Preservation**: System remembers previous queries and results
- **Natural Language**: No need to learn KQL or Elasticsearch DSL syntax
- **Intent Recognition**: Advanced NLP understands security-specific terminology

### Supported Query Types

#### Time-Based Queries
```
"Show me recent authentication failures"
"Find security events from the last 24 hours" 
"Display critical alerts from this morning"
"List system errors from the past 3 hours"
```

#### Severity-Based Queries
```
"Show me critical security events"
"Find high priority authentication failures"
"Display all medium and high severity alerts"
"List urgent system warnings"
```

#### Rule-Specific Queries
```
"Show rule 5503 events from yesterday"
"Find all authentication rule violations"
"Display rootcheck detection events"
"Show SCA compliance failures"
```

#### Field-Specific Queries
```
"Show SSH connections from 192.168.1.100"
"Find events from server web-01"
"Display blocked connections on port 80"
"Show file modifications in /etc/"
```

#### Boolean Logic Queries
```
"Show login AND failure NOT success"
"Find critical OR high severity events"
"Display authentication failures NOT successful logins"
```

### Advanced Features
- **Fuzzy Matching**: Handles typos and variations in queries
- **Synonym Support**: Understands multiple ways to express the same concept
- **Confidence Scoring**: Indicates translation quality (0.0-1.0)
- **Query Validation**: Ensures generated Elasticsearch queries are valid
- **Smart Suggestions**: Provides recommendations for improving low-confidence queries

## 🔧 Configuration

### Wazuh Rule Types
The system supports comprehensive Wazuh rule categorization:

- **Authentication**: Login events, password changes, user authentication
- **System**: System events, service status, hardware issues
- **Security**: Security events, privilege escalation, suspicious activity
- **SCA**: Security Configuration Assessment, policy compliance
- **Rootcheck**: Rootkit detection, system integrity checks

### Severity Levels
- **0-3**: Informational/Low priority
- **4-6**: Medium priority, warnings
- **7-10**: High priority, significant events
- **11-15**: Critical priority, immediate attention required

## 📁 Project Structure

```
esql/
├── README.md                           # This comprehensive guide
├── terminal-chat-app/                  # React frontend application
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── App.jsx
│   ├── package.json
│   └── README.md
├── nlp_siem_middleware/                # FastAPI session management
│   ├── main.py                         # FastAPI application
│   ├── requirements.txt
│   └── README.md
├── ElasticSearch_Query_Automater/      # NLP translation service
│   ├── main.py                         # Flask API server
│   ├── nlp_translate.py               # NLP engine
│   ├── requirements.txt
│   └── README.md
└── wazuh-setup-docker/                # Wazuh infrastructure
    ├── docker-compose.yml             # Wazuh stack deployment
    ├── wazuh_manager/
    ├── elasticsearch/
    └── kibana/
```

## 🛠️ Development Setup

### Frontend Development
```bash
cd terminal-chat-app/
npm install
npm run dev           # Development server with hot reload
npm run build         # Production build
npm run preview       # Preview production build
```

### Backend Development
```bash
# NLP Translation Service
cd ElasticSearch_Query_Automater/
pip install -r requirements.txt
python main.py --debug --log-level DEBUG

# Middleware Service
cd nlp_siem_middleware/
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Testing
```bash
# Test NLP Translation Service
cd ElasticSearch_Query_Automater/
pytest test_api.py -v
python manual_test.py

# Test Middleware
cd nlp_siem_middleware/
python test_client.py
```

## 🐛 Troubleshooting

### Common Issues

#### Service Connection Issues
```bash
# Check if all services are running
curl http://localhost:5000/health    # NLP Service
curl http://localhost:8000/health    # Middleware
curl http://localhost:9200/_cluster/health  # Elasticsearch
```

#### Frontend Connection Issues
- Verify backend services are accessible from frontend
- Check CORS configuration in FastAPI middleware
- Ensure proper environment variables are set

#### Query Translation Issues
- **Low Confidence Scores**: Use more specific keywords matching rule types
- **No Results**: Verify rule types in query match provided rules
- **Invalid Queries**: Check Elasticsearch query validation output

#### Session Management Issues
```bash
# Check Redis connection
docker ps | grep redis
redis-cli ping

# Clear Redis sessions if needed
redis-cli FLUSHDB
```

## 📊 API Documentation

### Comprehensive API References
- **NLP Translation API**: See `ElasticSearch_Query_Automater/README.md`
- **Middleware API**: See `nlp_siem_middleware/README.md`
- **Frontend Features**: See `terminal-chat-app/README.md`

### Key Endpoints
- `POST /sessions` - Initialize new conversation session
- `POST /query` - Execute natural language queries
- `POST /translate` - Direct NLP translation (for testing)
- `GET /health` - Service health checks

## 🔒 Security Considerations

- **Credential Management**: Secure storage of SIEM credentials in Redis
- **Session Security**: TTL-based session expiration
- **Input Validation**: Comprehensive validation using Pydantic
- **Query Sanitization**: Elasticsearch query validation prevents injection
- **Network Security**: Service isolation and proper authentication

## 🚀 Production Deployment

### Docker Deployment
```bash
# Build all services
docker-compose -f docker-compose.prod.yml build

# Deploy stack
docker-compose -f docker-compose.prod.yml up -d

# Monitor services
docker-compose logs -f
```

### Environment Variables
```bash
# Set production configurations
export REDIS_URL="redis://production-redis:6379"
export ELASTICSEARCH_URL="https://production-es:9200"
export NLP_MODEL_URL="http://nlp-service:5000"
```

## 📈 Performance Considerations

- **Redis Session Storage**: Optimized for high-throughput session management
- **Elasticsearch Query Optimization**: Generated queries include size limits and sorting
- **Frontend Virtual Scrolling**: Handles large datasets (1000+ logs) efficiently
- **Connection Pooling**: Efficient database connections in middleware

## 🤝 Contributing

1. **Fork the Repository**
2. **Create Feature Branch**: `git checkout -b feature/amazing-feature`
3. **Make Changes**: Follow existing code patterns and documentation
4. **Add Tests**: Ensure comprehensive test coverage
5. **Submit Pull Request**: Detailed description of changes

## 📄 License

This project is licensed under the MIT License - see individual component README files for specific licensing information.

## 🆘 Support

For issues and questions:
1. Check component-specific README files
2. Review API documentation
3. Check troubleshooting sections
4. Open an issue on GitHub with detailed error information

## 🔄 Version History

- **v1.0.0**: Initial release with three-component architecture
- **v1.1.0**: Enhanced NLP translation with confidence scoring
- **v1.2.0**: Advanced frontend features and export capabilities
- **v1.3.0**: Comprehensive Docker deployment support

---

**Made with ❤️ for the cybersecurity community**

*This system demonstrates the power of combining natural language processing with security information and event management for more intuitive threat hunting and investigation workflows.*
