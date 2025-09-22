#!/usr/bin/env python3
"""
Mock Elasticsearch service for Wazuh integration
This provides a simple HTTP API that mimics Elasticsearch responses
"""

from flask import Flask, request, jsonify
import json
import random
import time
from datetime import datetime, timedelta
import uuid

app = Flask(__name__)

# Sample Wazuh log data
SAMPLE_LOGS = [
    {
        "_index": "wazuh-alerts-2024.09.22",
        "_type": "_doc",
        "_id": str(uuid.uuid4()),
        "_score": 1.0,
        "_source": {
            "@timestamp": "2024-09-22T21:30:00.000Z",
            "agent": {
                "id": "001",
                "name": "web-server-01",
                "ip": "192.168.1.100"
            },
            "rule": {
                "id": 5503,
                "description": "Authentication failure",
                "level": 5,
                "groups": ["authentication_failed"],
                "category": "authentication"
            },
            "log": {
                "level": "info",
                "logger": "wazuh-authd"
            },
            "message": "Authentication failed for user 'admin' from '192.168.1.50'",
            "full_log": "Sep 22 21:30:00 web-server-01 sshd[1234]: Failed password for admin from 192.168.1.50 port 22 ssh2",
            "input": {
                "type": "log"
            },
            "location": {
                "file": "/var/log/auth.log",
                "line": 1234
            }
        }
    },
    {
        "_index": "wazuh-alerts-2024.09.22",
        "_type": "_doc",
        "_id": str(uuid.uuid4()),
        "_score": 1.0,
        "_source": {
            "@timestamp": "2024-09-22T21:25:00.000Z",
            "agent": {
                "id": "002",
                "name": "db-server-01",
                "ip": "192.168.1.101"
            },
            "rule": {
                "id": 5504,
                "description": "SQL injection attempt",
                "level": 12,
                "groups": ["web_attack"],
                "category": "security"
            },
            "log": {
                "level": "warning",
                "logger": "wazuh-web"
            },
            "message": "SQL injection attempt detected in web application",
            "full_log": "Sep 22 21:25:00 db-server-01 apache2[5678]: [client 192.168.1.200] GET /login.php?id=1' OR '1'='1 HTTP/1.1",
            "input": {
                "type": "log"
            },
            "location": {
                "file": "/var/log/apache2/access.log",
                "line": 5678
            }
        }
    },
    {
        "_index": "wazuh-alerts-2024.09.22",
        "_type": "_doc",
        "_id": str(uuid.uuid4()),
        "_score": 1.0,
        "_source": {
            "@timestamp": "2024-09-22T21:20:00.000Z",
            "agent": {
                "id": "003",
                "name": "file-server-01",
                "ip": "192.168.1.102"
            },
            "rule": {
                "id": 5505,
                "description": "File modification detected",
                "level": 7,
                "groups": ["file_integrity"],
                "category": "system"
            },
            "log": {
                "level": "info",
                "logger": "wazuh-syscheckd"
            },
            "message": "File /etc/passwd modified",
            "full_log": "Sep 22 21:20:00 file-server-01 wazuh-syscheckd: File /etc/passwd modified (size: 1234 -> 1256)",
            "input": {
                "type": "log"
            },
            "location": {
                "file": "/var/log/wazuh/syscheck.log",
                "line": 9012
            }
        }
    },
    {
        "_index": "wazuh-alerts-2024.09.22",
        "_type": "_doc",
        "_id": str(uuid.uuid4()),
        "_score": 1.0,
        "_source": {
            "@timestamp": "2024-09-22T21:15:00.000Z",
            "agent": {
                "id": "004",
                "name": "mail-server-01",
                "ip": "192.168.1.103"
            },
            "rule": {
                "id": 5506,
                "description": "Brute force attack detected",
                "level": 10,
                "groups": ["brute_force"],
                "category": "security"
            },
            "log": {
                "level": "warning",
                "logger": "wazuh-authd"
            },
            "message": "Multiple failed login attempts from 192.168.1.75",
            "full_log": "Sep 22 21:15:00 mail-server-01 sshd[3456]: 5 failed password attempts for user 'root' from 192.168.1.75",
            "input": {
                "type": "log"
            },
            "location": {
                "file": "/var/log/auth.log",
                "line": 3456
            }
        }
    },
    {
        "_index": "wazuh-alerts-2024.09.22",
        "_type": "_doc",
        "_id": str(uuid.uuid4()),
        "_score": 1.0,
        "_source": {
            "@timestamp": "2024-09-22T21:10:00.000Z",
            "agent": {
                "id": "005",
                "name": "web-server-02",
                "ip": "192.168.1.104"
            },
            "rule": {
                "id": 5507,
                "description": "XSS attack attempt",
                "level": 8,
                "groups": ["web_attack"],
                "category": "security"
            },
            "log": {
                "level": "warning",
                "logger": "wazuh-web"
            },
            "message": "XSS attack attempt detected in web form",
            "full_log": "Sep 22 21:10:00 web-server-02 apache2[7890]: [client 192.168.1.150] POST /contact.php - XSS payload detected",
            "input": {
                "type": "log"
            },
            "location": {
                "file": "/var/log/apache2/access.log",
                "line": 7890
            }
        }
    }
]

def generate_more_logs(count=50):
    """Generate more sample logs for testing"""
    logs = []
    base_time = datetime.now() - timedelta(hours=24)
    
    rule_templates = [
        {"id": 5503, "description": "Authentication failure", "level": 5, "groups": ["authentication_failed"], "category": "authentication"},
        {"id": 5504, "description": "SQL injection attempt", "level": 12, "groups": ["web_attack"], "category": "security"},
        {"id": 5505, "description": "File modification detected", "level": 7, "groups": ["file_integrity"], "category": "system"},
        {"id": 5506, "description": "Brute force attack detected", "level": 10, "groups": ["brute_force"], "category": "security"},
        {"id": 5507, "description": "XSS attack attempt", "level": 8, "groups": ["web_attack"], "category": "security"},
        {"id": 5508, "description": "Privilege escalation attempt", "level": 11, "groups": ["privilege_escalation"], "category": "security"},
        {"id": 5509, "description": "Malware detection", "level": 13, "groups": ["malware"], "category": "security"},
        {"id": 5510, "description": "Network intrusion", "level": 9, "groups": ["network"], "category": "security"}
    ]
    
    agent_templates = [
        {"id": "001", "name": "web-server-01", "ip": "192.168.1.100"},
        {"id": "002", "name": "db-server-01", "ip": "192.168.1.101"},
        {"id": "003", "name": "file-server-01", "ip": "192.168.1.102"},
        {"id": "004", "name": "mail-server-01", "ip": "192.168.1.103"},
        {"id": "005", "name": "web-server-02", "ip": "192.168.1.104"},
        {"id": "006", "name": "api-server-01", "ip": "192.168.1.105"},
        {"id": "007", "name": "backup-server-01", "ip": "192.168.1.106"}
    ]
    
    for i in range(count):
        rule = random.choice(rule_templates)
        agent = random.choice(agent_templates)
        timestamp = base_time + timedelta(minutes=random.randint(0, 1440))
        
        log = {
            "_index": "wazuh-alerts-2024.09.22",
            "_type": "_doc",
            "_id": str(uuid.uuid4()),
            "_score": random.uniform(0.5, 2.0),
            "_source": {
                "@timestamp": timestamp.isoformat() + "Z",
                "agent": agent,
                "rule": rule,
                "log": {
                    "level": random.choice(["info", "warning", "error", "critical"]),
                    "logger": f"wazuh-{random.choice(['authd', 'web', 'syscheckd', 'net'])}"
                },
                "message": f"{rule['description']} on {agent['name']}",
                "full_log": f"Sep 22 {timestamp.strftime('%H:%M:%S')} {agent['name']} wazuh: {rule['description']}",
                "input": {
                    "type": "log"
                },
                "location": {
                    "file": f"/var/log/{random.choice(['auth.log', 'apache2/access.log', 'wazuh/syscheck.log', 'nginx/access.log'])}",
                    "line": random.randint(1000, 9999)
                }
            }
        }
        logs.append(log)
    
    return logs

# Generate more sample data
ALL_LOGS = SAMPLE_LOGS + generate_more_logs(100)

@app.route('/')
def root():
    return jsonify({
        "name": "mock-elasticsearch",
        "cluster_name": "elasticsearch",
        "cluster_uuid": "mock-cluster-uuid",
        "version": {
            "number": "7.17.0",
            "build_flavor": "default",
            "build_type": "docker",
            "build_hash": "mock-build-hash",
            "build_date": "2024-01-01T00:00:00.000Z",
            "build_snapshot": False,
            "lucene_version": "8.11.1",
            "minimum_wire_compatibility_version": "6.8.0",
            "minimum_index_compatibility_version": "6.0.0-beta1"
        },
        "tagline": "You Know, for Search"
    })

@app.route('/_cluster/health')
def cluster_health():
    return jsonify({
        "cluster_name": "elasticsearch",
        "status": "green",
        "timed_out": False,
        "number_of_nodes": 1,
        "number_of_data_nodes": 1,
        "active_primary_shards": 1,
        "active_shards": 1,
        "relocating_shards": 0,
        "initializing_shards": 0,
        "unassigned_shards": 0,
        "delayed_unassigned_shards": 0,
        "number_of_pending_tasks": 0,
        "number_of_in_flight_fetch": 0,
        "task_max_waiting_in_queue_millis": 0,
        "active_shards_percent_as_number": 100.0
    })

@app.route('/wazuh-alerts-*/_search', methods=['POST'])
def search():
    """Mock Elasticsearch search endpoint"""
    try:
        query_data = request.get_json() or {}
        
        # Parse query to determine what logs to return
        query = query_data.get('query', {})
        size = query_data.get('size', 10)
        from_offset = query_data.get('from', 0)
        
        # Simple query matching
        filtered_logs = ALL_LOGS.copy()
        
        # Apply basic filters based on query
        if 'bool' in query:
            bool_query = query['bool']
            
            # Handle must clauses
            if 'must' in bool_query:
                for must_clause in bool_query['must']:
                    if 'term' in must_clause:
                        term_query = must_clause['term']
                        for field, value in term_query.items():
                            if field == 'rule.level':
                                filtered_logs = [log for log in filtered_logs 
                                               if log['_source']['rule']['level'] == value]
                            elif field == 'rule.category':
                                filtered_logs = [log for log in filtered_logs 
                                               if log['_source']['rule']['category'] == value]
                            elif field == 'agent.name':
                                filtered_logs = [log for log in filtered_logs 
                                               if value in log['_source']['agent']['name']]
            
            # Handle should clauses (OR conditions)
            if 'should' in bool_query:
                should_results = []
                for should_clause in bool_query['should']:
                    if 'term' in should_clause:
                        term_query = should_clause['term']
                        for field, value in term_query.items():
                            if field == 'rule.level':
                                should_results.extend([log for log in ALL_LOGS 
                                                     if log['_source']['rule']['level'] == value])
                            elif field == 'rule.category':
                                should_results.extend([log for log in ALL_LOGS 
                                                     if log['_source']['rule']['category'] == value])
                if should_results:
                    filtered_logs = should_results
        
        # Handle range queries for time
        if 'range' in query:
            range_query = query['range']
            if '@timestamp' in range_query:
                # For simplicity, just return all logs
                pass
        
        # Apply size and offset
        total_hits = len(filtered_logs)
        paginated_logs = filtered_logs[from_offset:from_offset + size]
        
        # Simulate search time
        search_time = random.randint(5, 50)
        time.sleep(search_time / 1000.0)  # Convert to seconds
        
        response = {
            "took": search_time,
            "timed_out": False,
            "_shards": {
                "total": 1,
                "successful": 1,
                "skipped": 0,
                "failed": 0
            },
            "hits": {
                "total": {
                    "value": total_hits,
                    "relation": "eq"
                },
                "max_score": 1.0,
                "hits": paginated_logs
            }
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({
            "error": {
                "type": "search_phase_execution_exception",
                "reason": str(e)
            }
        }), 500

@app.route('/_cat/indices')
def cat_indices():
    """Mock indices listing"""
    return jsonify([
        {
            "health": "green",
            "status": "open",
            "index": "wazuh-alerts-2024.09.22",
            "uuid": "mock-uuid-1",
            "pri": "1",
            "rep": "0",
            "docs.count": str(len(ALL_LOGS)),
            "docs.deleted": "0",
            "store.size": "1.2mb",
            "pri.store.size": "1.2mb"
        }
    ])

@app.route('/wazuh-alerts-*/_mapping')
def mapping():
    """Mock mapping endpoint"""
    return jsonify({
        "wazuh-alerts-2024.09.22": {
            "mappings": {
                "properties": {
                    "@timestamp": {"type": "date"},
                    "agent": {
                        "properties": {
                            "id": {"type": "keyword"},
                            "name": {"type": "keyword"},
                            "ip": {"type": "ip"}
                        }
                    },
                    "rule": {
                        "properties": {
                            "id": {"type": "integer"},
                            "description": {"type": "text"},
                            "level": {"type": "integer"},
                            "groups": {"type": "keyword"},
                            "category": {"type": "keyword"}
                        }
                    },
                    "log": {
                        "properties": {
                            "level": {"type": "keyword"},
                            "logger": {"type": "keyword"}
                        }
                    },
                    "message": {"type": "text"},
                    "full_log": {"type": "text"}
                }
            }
        }
    })

if __name__ == '__main__':
    print("Starting Mock Elasticsearch service...")
    print("Available endpoints:")
    print("  GET  / - Cluster info")
    print("  GET  /_cluster/health - Cluster health")
    print("  POST /wazuh-alerts-*/_search - Search logs")
    print("  GET  /_cat/indices - List indices")
    print("  GET  /wazuh-alerts-*/_mapping - Get mapping")
    print(f"\nSample data: {len(ALL_LOGS)} log entries")
    print("Running on http://localhost:9200")
    
    app.run(host='0.0.0.0', port=9200, debug=True)
