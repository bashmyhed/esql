#!/bin/bash
set -e

echo "🚀 Starting ESQL System Services (Fixed Version)..."

# Kill any existing processes
echo "🧹 Cleaning up existing processes..."
pkill -f "mock_elasticsearch.py" || true
pkill -f "main.py" || true
sudo fuser -k 9200/tcp 2>/dev/null || true
sudo fuser -k 5000/tcp 2>/dev/null || true  
sudo fuser -k 8000/tcp 2>/dev/null || true
sleep 3

# Check if Redis is running, start if needed
if ! docker ps | grep -q redis; then
    echo "📦 Starting Redis..."
    docker run -d -p 6379:6379 --name redis redis:alpine || docker start redis
else
    echo "📦 Redis is already running"
fi
sleep 2

# Start Mock Elasticsearch on port 9200
echo "🔍 Starting Mock Elasticsearch..."
cd /home/paul/projects/esql/mock-elasticsearch
source venv/bin/activate
nohup python3 mock_elasticsearch.py > mock_es.log 2>&1 &
MOCK_ES_PID=$!
sleep 5

# Test Mock Elasticsearch
if curl -s http://localhost:9200/_cluster/health > /dev/null 2>&1; then
    echo "✅ Mock Elasticsearch started successfully on port 9200"
else
    echo "❌ Mock Elasticsearch failed to start"
    exit 1
fi

# Start NLP Translation API on port 5000
echo "🧠 Starting NLP Translation API..."
cd /home/paul/projects/esql/ElasticSearch_Query_Automater
source venv/bin/activate
nohup python3 main.py --host 0.0.0.0 --port 5000 > nlp_api.log 2>&1 &
NLP_PID=$!
sleep 5

# Test NLP API
if curl -s http://localhost:5000/health > /dev/null 2>&1; then
    echo "✅ NLP Translation API started successfully on port 5000"
else
    echo "❌ NLP Translation API failed to start"
    exit 1
fi

# Start Middleware on port 8000
echo "🔗 Starting Middleware..."
cd /home/paul/projects/esql/nlp_siem_middleware
source venv/bin/activate
nohup python3 main.py > middleware.log 2>&1 &
MIDDLEWARE_PID=$!
sleep 5

# Test Middleware
if curl -s http://localhost:8000/docs > /dev/null 2>&1; then
    echo "✅ Middleware started successfully on port 8000"
else
    echo "❌ Middleware failed to start"
    exit 1
fi

echo ""
echo "✅ All services started successfully!"
echo "📊 Services running:"
echo "  - Mock Elasticsearch: http://localhost:9200 (PID: $MOCK_ES_PID)"
echo "  - NLP Translation API: http://localhost:5000 (PID: $NLP_PID)"  
echo "  - Middleware: http://localhost:8000 (PID: $MIDDLEWARE_PID)"
echo "  - Frontend: http://localhost:5173 (Already running in Docker)"
echo "  - Redis: localhost:6379"
echo ""
echo "🧪 Quick health check:"
echo "  Mock ES Health: $(curl -s http://localhost:9200/_cluster/health | jq -r '.status' 2>/dev/null || echo 'Error')"
echo "  NLP API Health: $(curl -s http://localhost:5000/health | jq -r '.status' 2>/dev/null || echo 'Error')"
echo "  Middleware API: $(curl -s http://localhost:8000/docs >/dev/null 2>&1 && echo 'OK' || echo 'Error')"
echo ""
echo "🎯 To test the complete workflow:"
echo "  curl -X POST http://localhost:8000/sessions \\"
echo "    -H 'Content-Type: application/json' \\"
echo "    -d '{\"admin_username\": \"admin\", \"admin_password\": \"password\", \"rules\": [{\"id\": 5503, \"description\": \"Authentication failure\", \"type\": \"authentication\", \"level\": 5}]}'"
echo ""
echo "📁 Service logs:"
echo "  - Mock ES: /home/paul/projects/esql/mock-elasticsearch/mock_es.log"
echo "  - NLP API: /home/paul/projects/esql/ElasticSearch_Query_Automater/nlp_api.log"
echo "  - Middleware: /home/paul/projects/esql/nlp_siem_middleware/middleware.log"
echo ""
echo "🛑 To stop all services:"
echo "  pkill -f 'mock_elasticsearch.py'"
echo "  pkill -f 'main.py'"
echo "  docker stop redis"
