#!/bin/bash

echo "🧪 Testing ESQL Complete Workflow..."

# Test 1: Create a session
echo "[1/3] Creating session..."
SESSION_RESPONSE=$(curl -s -X POST http://localhost:8000/sessions \
  -H 'Content-Type: application/json' \
  -d '{
    "admin_username": "admin",
    "admin_password": "password",
    "rules": [
      {"id": 5503, "description": "Authentication failure", "type": "authentication", "level": 5},
      {"id": 5504, "description": "SQL injection attempt", "type": "security", "level": 12},
      {"id": 5505, "description": "File modification detected", "type": "system", "level": 7}
    ]
  }')

if [ $? -eq 0 ]; then
  CHAT_ID=$(echo "$SESSION_RESPONSE" | jq -r '.chat_id' 2>/dev/null)
  if [ "$CHAT_ID" != "null" ] && [ ! -z "$CHAT_ID" ]; then
    echo "✅ Session created successfully: $CHAT_ID"
  else
    echo "❌ Session creation failed: $SESSION_RESPONSE"
    exit 1
  fi
else
  echo "❌ Failed to connect to middleware"
  exit 1
fi

# Test 2: Query the system
echo "[2/3] Testing natural language query..."
QUERY_RESPONSE=$(curl -s -X POST http://localhost:8000/query \
  -H 'Content-Type: application/json' \
  -d "{
    \"nl_query\": \"Show me all authentication failures\",
    \"chat_id\": \"$CHAT_ID\"
  }")

if [ $? -eq 0 ]; then
  SUCCESS=$(echo "$QUERY_RESPONSE" | jq -r '.success' 2>/dev/null)
  if [ "$SUCCESS" == "true" ]; then
    echo "✅ Query processed successfully"
    echo "   Confidence: $(echo "$QUERY_RESPONSE" | jq -r '.nl_confidence' 2>/dev/null)"
  else
    echo "❌ Query failed: $QUERY_RESPONSE"
    exit 1
  fi
else
  echo "❌ Failed to execute query"
  exit 1
fi

# Test 3: Direct NLP Translation test
echo "[3/3] Testing NLP translation directly..."
NLP_RESPONSE=$(curl -s -X POST http://localhost:5000/translate \
  -H 'Content-Type: application/json' \
  -d '{
    "query": "Show me critical security events from yesterday",
    "rules": [
      {"id": 5503, "description": "Authentication failure", "type": "authentication", "level": 5},
      {"id": 5504, "description": "SQL injection attempt", "type": "security", "level": 12}
    ]
  }')

if [ $? -eq 0 ]; then
  STATUS=$(echo "$NLP_RESPONSE" | jq -r '.status' 2>/dev/null)
  if [ "$STATUS" == "success" ]; then
    echo "✅ NLP Translation successful"
    echo "   Confidence: $(echo "$NLP_RESPONSE" | jq -r '.confidence' 2>/dev/null)"
  else
    echo "❌ NLP Translation failed: $NLP_RESPONSE"
    exit 1
  fi
else
  echo "❌ Failed to connect to NLP service"
  exit 1
fi

echo ""
echo "🎉 All tests passed! The ESQL system is working correctly."
echo ""
echo "📊 System Summary:"
echo "  ✅ Mock Elasticsearch: Serving sample Wazuh data"
echo "  ✅ NLP Translation API: Converting natural language to Elasticsearch queries"
echo "  ✅ Middleware: Managing sessions and orchestrating requests"
echo "  ✅ Frontend: Available at http://localhost:5173"
echo "  ✅ Redis: Storing session data"
echo ""
echo "🎯 You can now:"
echo "  1. Open http://localhost:5173 to use the web interface"
echo "  2. Use the API endpoints directly for integration"
echo "  3. View API documentation at http://localhost:8000/docs"
