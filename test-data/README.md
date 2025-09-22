Local API test data
====================

Prereqs
- Mock ES on 9200
- NLP API on 5000
- Middleware on 8000
- Redis on 6379

## Files Available:

### rules.json
- **Format**: Nested object with categories
- **Usage**: Drag & drop into frontend file picker
- **Contains**: 24 comprehensive Wazuh rules across 6 categories
- **Categories**: authentication, security, system, network, compliance, application

### rules-simple.json  
- **Format**: Flat array (frontend preferred format)
- **Usage**: Drag & drop into frontend file picker
- **Contains**: Same 24 rules in simplified format

### session.json
- **Format**: API request payload
- **Usage**: curl command or API testing
- **Contains**: Sample session with 5 basic rules

### query.json
- **Format**: API request payload  
- **Usage**: curl command with chat_id substitution
- **Contains**: Sample query "Show me all authentication failures"

## Quick Test:

1) Create session
```bash
curl -s -X POST http://localhost:8000/sessions \
  -H 'Content-Type: application/json' \
  -d @/home/paul/projects/esql/test-data/session.json
```

2) Run query (replace CHAT_ID)
```bash
CHAT_ID=PASTE_ID_HERE
jq --arg id "$CHAT_ID" '.chat_id=$id' /home/paul/projects/esql/test-data/query.json | \
  curl -s -X POST http://localhost:8000/query \
    -H 'Content-Type: application/json' \
    -d @-
```

3) One-shot test
```bash
./run_test.sh
```

## Frontend Testing:

1. Start all services: `../start_all_services.sh`
2. Open frontend: `http://localhost:5174`
3. During setup, drag & drop `rules-simple.json` into file picker
4. Enter username/password
5. Try queries like:
   - "Show me all authentication failures"
   - "Critical security events last hour"
   - "Malware detections on web servers"
   - "Network intrusions from external IPs"

Expected: Interactive dashboard with charts, logs, and insights.


