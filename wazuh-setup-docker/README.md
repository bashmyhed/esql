# Wazuh Docker Setup for NLP SIEM Integration

This directory contains a complete Docker Compose setup for running Wazuh Manager, Elasticsearch, Kibana, and Filebeat to provide log data for the NLP-powered Conversational SIEM Assistant.

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Wazuh Manager │────▶│    Filebeat     │────▶│  Elasticsearch  │
│  (Log Analysis) │    │ (Log Shipping)  │    │ (Log Storage)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                                               │
         │                                               ▼
         ▼                                     ┌─────────────────┐
┌─────────────────┐                           │     Kibana      │
│  Log Generator  │                           │ (Visualization) │
│ (Test Data)     │                           └─────────────────┘
└─────────────────┘
```

## 📦 Components

1. **Wazuh Manager**: Core SIEM engine for log analysis and rule processing
2. **Elasticsearch**: Document store for indexed security events
3. **Kibana**: Web interface for data visualization and exploration
4. **Filebeat**: Log shipper to send Wazuh alerts to Elasticsearch
5. **Log Generator**: Generates sample security events for testing

## 🚀 Quick Start

### 1. Start the Stack

```bash
# Clone the repository and navigate to this directory
cd wazuh-setup-docker/

# Start all services
docker-compose up -d

# Check service status
docker-compose ps
```

### 2. Verify Services

```bash
# Check Elasticsearch health
curl http://localhost:9200/_cluster/health

# Check Wazuh Manager API
curl -u wazuh-wui:MyS3cr37P450r.*- http://localhost:55000/

# Access Kibana (web browser)
# http://localhost:5601
```

### 3. Wait for Log Generation

The system will start generating sample security events immediately. You should see logs flowing within 30 seconds.

## 🔧 Configuration Files

### Wazuh Manager Configuration
- **`wazuh_manager/ossec.conf`**: Main Wazuh configuration with comprehensive monitoring rules
- **`wazuh_manager/local_rules.xml`**: Custom security rules for enhanced detection
- **`wazuh_manager/local_decoders.xml`**: Custom log parsing decoders

### Filebeat Configuration
- **`filebeat/filebeat.yml`**: Ships Wazuh alerts to Elasticsearch

## 📊 Generated Log Types

The setup automatically generates various types of security events:

### Authentication Events
- SSH login failures
- Multiple authentication attempts
- Successful logins

### System Events
- Service failures
- System errors
- Process monitoring

### Network Security
- Firewall blocks
- Suspicious connections
- Network traffic patterns

### Web Security
- Apache/HTTP errors
- Web application attacks
- Access violations

### File Integrity
- Critical file modifications
- System file changes
- Configuration updates

## 🔍 Testing the NLP Integration

### 1. Verify Data in Elasticsearch

```bash
# Check available indices
curl http://localhost:9200/_cat/indices

# Search for Wazuh alerts
curl -X GET "localhost:9200/wazuh-alerts-*/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "query": {
    "match_all": {}
  },
  "size": 5,
  "sort": [
    {
      "@timestamp": {
        "order": "desc"
      }
    }
  ]
}
'
```

### 2. Sample NLP Queries to Test

Once your NLP system is running, try these example queries:

```
"Show me recent authentication failures"
"Find critical security events from the last hour"
"Display SSH login attempts from external IPs"
"Show me firewall blocks from suspicious sources"
"List system service failures"
"Find web server errors"
"Show me file integrity violations"
"Display rootkit detection events"
```

## 📋 Service Details

### Ports

| Service | Port | Description |
|---------|------|-------------|
| Elasticsearch | 9200 | HTTP API |
| Kibana | 5601 | Web Interface |
| Wazuh Manager | 55000 | Wazuh API |
| Wazuh Manager | 1514 | Agent Communication |
| Wazuh Manager | 1515 | Agent Registration |

### Credentials

| Service | Username | Password |
|---------|----------|----------|
| Wazuh API | wazuh-wui | MyS3cr37P450r.*- |
| Elasticsearch | none | none (security disabled) |
| Kibana | none | none (no authentication) |

**Note**: This is a development setup. In production, enable proper authentication and use strong passwords.

## 🗄️ Data Persistence

All data is stored in Docker volumes:

- `wazuh-elasticsearch-data`: Elasticsearch indices and data
- `wazuh-manager-logs`: Wazuh logs and alerts
- `wazuh-manager-config`: Wazuh configuration files
- `filebeat-data`: Filebeat processing state

## 🐛 Troubleshooting

### Services Won't Start

```bash
# Check Docker logs
docker-compose logs wazuh-manager
docker-compose logs wazuh-elasticsearch
docker-compose logs wazuh-filebeat

# Check system resources
docker stats
```

### No Data in Elasticsearch

```bash
# Check Filebeat status
docker-compose logs wazuh-filebeat

# Check if Wazuh is generating alerts
docker exec wazuh-manager tail -f /var/ossec/logs/alerts/alerts.json

# Check Elasticsearch indices
curl http://localhost:9200/_cat/indices
```

### Wazuh Manager Issues

```bash
# Check Wazuh Manager status
docker exec wazuh-manager /var/ossec/bin/wazuh-control status

# Check Wazuh logs
docker exec wazuh-manager tail -f /var/ossec/logs/ossec.log
```

### Memory Issues

If services are crashing due to memory constraints:

```bash
# Reduce Elasticsearch heap size
# Edit docker-compose.yml and change:
# - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
```

## 🔧 Customization

### Adding More Log Sources

Edit `wazuh_manager/ossec.conf` to add more log files:

```xml
<localfile>
  <log_format>syslog</log_format>
  <location>/path/to/your/logfile.log</location>
</localfile>
```

### Custom Rules

Add custom detection rules in `wazuh_manager/local_rules.xml`:

```xml
<rule id="100025" level="8">
  <match>your_custom_pattern</match>
  <description>Your custom security rule</description>
  <group>custom,security,</group>
</rule>
```

### Elasticsearch Index Configuration

Modify Filebeat template in `filebeat/filebeat.yml`:

```yaml
setup.template.name: "your-custom-index"
setup.template.pattern: "your-custom-index-*"
```

## 📈 Performance Tuning

### For Higher Log Volume

1. **Increase Wazuh queue size**:
   ```xml
   <remote>
     <queue_size>262144</queue_size>
   </remote>
   ```

2. **Tune Elasticsearch**:
   ```yaml
   environment:
     - "ES_JAVA_OPTS=-Xms2g -Xmx2g"
   ```

3. **Optimize Filebeat**:
   ```yaml
   filebeat.inputs:
     - type: log
       scan_frequency: 1s
       harvester_buffer_size: 32768
   ```

## 🛡️ Security Considerations

**Development Use Only**: This setup disables security features for ease of development. For production:

1. Enable Elasticsearch security
2. Use strong passwords
3. Enable TLS/SSL
4. Implement proper firewall rules
5. Regular security updates

## 📚 Integration with NLP System

This Wazuh setup is designed to work with the NLP SIEM middleware. The alerts generated here will be queryable using natural language through:

1. **Terminal Chat App**: Frontend interface
2. **NLP SIEM Middleware**: Session management and query routing
3. **Elasticsearch Query Automater**: NLP to Elasticsearch DSL translation

### Sample Rule Data Structure

The rules generated by this setup follow this structure for NLP integration:

```json
{
  "id": 100001,
  "description": "SSH authentication failure from external IP",
  "type": "authentication",
  "level": 7
}
```

## 🔄 Maintenance

### Cleanup

```bash
# Stop all services
docker-compose down

# Remove volumes (⚠️ This deletes all data)
docker-compose down -v

# Remove images
docker-compose down --rmi all
```

### Updates

```bash
# Pull latest images
docker-compose pull

# Restart with new images
docker-compose up -d
```

---

**Ready to test your Conversational SIEM Assistant!** 🚀

This setup provides a complete testing environment with realistic security events that can be queried using natural language through your NLP system.
