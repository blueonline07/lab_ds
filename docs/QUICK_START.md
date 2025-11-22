# Quick Start Guide

## ⚡ Fast Setup (5 minutes)

### 1. Start Kafka
```bash
docker-compose up -d
```

Wait 30 seconds for Kafka to initialize.

### 2. Install Dependencies
```bash
# Create virtual environment (if not exists)
python3 -m venv .venv

# Activate
source .venv/bin/activate

# Install
pip install -r requirements.txt
```

### 3. Clear Cache (Important!)
```bash
# Clear Python cache to ensure fresh start
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null
find . -name "*.pyc" -delete 2>/dev/null
```

### 4. Run the System

**Terminal 1 - gRPC Server:**
```bash
source .venv/bin/activate
python3 run_server.py
```

**Terminal 2 - Analysis App:**
```bash
source .venv/bin/activate
python3 run_analysis.py
```

**Terminal 3 - Agent:**
```bash
source .venv/bin/activate
python3 run_agent.py --agent-id agent-001
```

## ✅ Expected Output

### Server
```
✓ Kafka producer initialized (bootstrap: localhost:9092)
======================================================================
gRPC Server Started (Bidirectional Streaming)
======================================================================
  Port: 50051
  Kafka: localhost:9092
  Kafka topic: monitoring-data
  Mode: Bidirectional streaming (no polling)
  Waiting for agent connections...
======================================================================

✓ Agent connected (streaming): agent-001
[Metrics Received - Stream]
  Agent: agent-001
  CPU: 45.23%
  Memory: 67.89%
✓ Forwarded to Kafka topic: monitoring-data
```

### Agent
```
✓ Connected to gRPC server
✓ Starting bidirectional stream...

[1] Generating metrics...
  CPU: 45.23%
  Memory: 67.89%
```

### Analysis App
```
======================================================================
Analysis Application Started
======================================================================
Waiting for monitoring data from Kafka...
======================================================================

[Message #1]

======================================================================
📊 MONITORING DATA RECEIVED
======================================================================
  Agent ID:   agent-001
  CPU Usage:       45.23%
  Memory Usage:    67.89%
======================================================================
```

## 🐛 Troubleshooting

### "Method not found!" Error

This means Python is using cached bytecode. **Solution:**

```bash
# Stop all components (Ctrl+C)

# Clear cache
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null
find . -name "*.pyc" -delete 2>/dev/null

# Restart components
python3 run_server.py  # Terminal 1
python3 run_analysis.py  # Terminal 2
python3 run_agent.py --agent-id agent-001  # Terminal 3
```

### "Connection refused"

**Kafka not running:**
```bash
docker-compose up -d
docker ps | grep kafka  # Should show kafka and zookeeper
```

**Server not running:**
```bash
# Check if server is listening
lsof -i :50051
```

### No messages in Analysis App

**Check Kafka:**
```bash
# Open Kafka UI
open http://localhost:8080

# Or check manually
docker exec kafka kafka-console-consumer \
    --bootstrap-server localhost:9092 \
    --topic monitoring-data \
    --from-beginning \
    --max-messages 5
```

## 🎯 Next Steps

Once everything works:
- Read [ARCHITECTURE.md](ARCHITECTURE.md) for system design
- Read [DATA_MODELS.md](DATA_MODELS.md) for data structures  
- Read [STREAMING.md](STREAMING.md) for streaming details
- Read [DEVELOPMENT.md](DEVELOPMENT.md) for development guide

## 💡 Tips

- Use `--help` on any script to see options
- Check [Kafka UI](http://localhost:8080) to monitor topics
- Send commands: `python3 send_command.py --agent-id agent-001 --command start`

---

Need more help? Check the [documentation index](README.md).

