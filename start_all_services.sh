#!/bin/bash
set -e

echo "🚀 Starting ESQL System Services..."

# Kill any existing processes
echo "🧹 Cleaning up existing processes..."
pkill -f "mock_elasticsearch.py" || true
pkill -f "main.py" || true
docker stop redis || true
docker rm redis || true

# Start Redis
echo "📦 Starting Redis..."
docker run -d -p 6379:6379 --name redis redis:alpine
sleep 2

# Start Mock Elasticsearch
echo "🔍 Starting Mock Elasticsearch..."
cd /home/paul/projects/esql/mock-elasticsearch
source venv/bin/activate
python3 mock_elasticsearch.py &
MOCK_ES_PID=$!
sleep 3

# Start NLP Translation API
echo "🧠 Starting NLP Translation API..."
cd /home/paul/projects/esql/ElasticSearch_Query_Automater
source venv/bin/activate
python3 main.py --host 0.0.0.0 --port 5000 &
NLP_PID=$!
sleep 3

# Start Middleware
echo "🔗 Starting Middleware..."
cd /home/paul/projects/esql/nlp_siem_middleware
source venv/bin/activate
python3 main.py &
MIDDLEWARE_PID=$!
sleep 3

# Test the system
echo "🧪 Testing system..."
cd /home/paul/projects/esql
./test-data/run_test.sh

echo "✅ All services started successfully!"
echo "📊 Services running:"
echo "  - Mock Elasticsearch: http://localhost:9200"
echo "  - NLP API: http://localhost:5000"
echo "  - Middleware: http://localhost:8000"
echo "  - Redis: localhost:6379"
echo ""
echo "🎯 To test manually:"
echo "  curl http://localhost:8000/health"
echo "  ./test-data/run_test.sh"
echo ""
echo "🛑 To stop all services:"
echo "  pkill -f 'mock_elasticsearch.py'"
echo "  pkill -f 'main.py'"
echo "  docker stop redis"

