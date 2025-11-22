# Monitoring Tool - Distributed System Monitoring

A modular monitoring system that collects metrics from multiple agents, forwards them through a gRPC server to Kafka, and enables real-time analysis.

## 🎯 Quick Start

### 1. Start Kafka
```bash
docker-compose up -d
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the System

```bash
# Terminal 1: Start gRPC Server
python3 run_server.py

# Terminal 2: Start Analysis App
python3 run_analysis.py

# Terminal 3: Start Agent
python3 run_agent.py --mode mock --iterations 10
```

## 🏗️ Architecture

```
┌─────────────────┐                ┌─────────────────┐                ┌─────────────────┐
│ Monitor Agent   │─── gRPC ──────►│  gRPC Server    │──── Kafka ────►│  Analysis App   │
│                 │◄── Stream ─────│  (Broker)       │◄─── Kafka ─────│                 │
│ • Collects data │                │ • Forwards data │                │ • Analyzes data │
│ • Mock/Real     │                │ • Routes cmds   │                │ • Stores data   │
└─────────────────┘                └─────────────────┘                └─────────────────┘
```

**Key Feature**: **Bidirectional streaming** between agent and server (no polling!)

## 📦 Module Structure

```
lab_ds/
├── shared/              # Protocol definitions & config
│   ├── monitoring.proto # gRPC protocol definition
│   ├── config.py        # Kafka topics configuration
│   └── monitoring_pb2*.py # Generated protobuf files
├── grpc_server/        # gRPC server + Kafka producer
├── analysis_app/       # Kafka consumer + analysis
├── mock_agent.py       # Mock agent (generates test data)
├── send_command.py     # Send START/STOP commands to agents
├── run_agent.py        # ⭐ Run agent
├── run_server.py       # ⭐ Run server
└── run_analysis.py     # ⭐ Run analysis app
```

## 🚀 Usage

### Agent Options
```bash
python3 run_agent.py \
    --agent-id agent-001 \
    --server localhost:50051
```

### Server Options
```bash
python3 run_server.py \
    --port 50051 \
    --kafka localhost:9092
```

### Analysis App Options
```bash
python3 run_analysis.py \
    --kafka localhost:9092 \
    --group-id my-team
```

## 📊 Data Models

### System Metrics
- CPU usage (%)
- Memory usage (%)
- Memory used/total (MB)
- Disk read/write (MB/s)
- Network in/out (MB/s)

### Commands
- **START** - Start metrics collection
- **STOP** - Stop metrics collection

### Kafka Topics
- `monitoring-data` - Agent metrics → Analysis app (via gRPC server)

## 🔧 Configuration

### Requirements
- Python 3.7+
- Docker (for Kafka)
- psutil (for real metrics mode)

### Kafka
Accessible at:
- Bootstrap server: `localhost:9092`
- Kafka UI: `http://localhost:8080`

## 📚 Documentation

- **[docs/DATA_MODELS.md](docs/DATA_MODELS.md)** - Complete data model reference
- **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)** - System architecture & design
- **[docs/STREAMING.md](docs/STREAMING.md)** - Bidirectional streaming details
- **[docs/DEVELOPMENT.md](docs/DEVELOPMENT.md)** - Development guide

## ✨ Features

✅ **Bidirectional Streaming** - Real-time communication, no polling  
✅ **Modular Architecture** - Independent, scalable components  
✅ **Mock Agent** - Easy testing with generated metrics  
✅ **Kafka Integration** - Persistent storage & decoupling  
✅ **Command Control** - START/STOP agents remotely  
✅ **Simple Configuration** - Clean, minimal setup  

## 🎓 Examples

### Basic Usage
```bash
# Terminal 1: Start gRPC Server
python3 run_server.py

# Terminal 2: Start Analysis App
python3 run_analysis.py

# Terminal 3: Start Mock Agent
python3 run_agent.py --agent-id agent-001
```

### Send Commands
```bash
# Send START command to agent
python3 send_command.py --agent-id agent-001 --command start

# Send STOP command to agent
python3 send_command.py --agent-id agent-001 --command stop
```

### Multiple Agents
```bash
# Run multiple agents simultaneously
python3 run_agent.py --agent-id agent-001 &
python3 run_agent.py --agent-id agent-002 &
python3 run_agent.py --agent-id agent-003 &
```

## 🔍 Monitoring

View Kafka messages in real-time:
```bash
open http://localhost:8080
```

Check active agents:
```bash
# Server logs show connected agents
✓ Agent connected (streaming): agent-001
[Metrics Received - Stream]
  Agent: agent-001
  CPU: 45.2%
  Memory: 62.5%
✓ Forwarded to Kafka topic: monitoring-data
```

## 🛠️ Development

### Generate gRPC Code
```bash
python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. shared/monitoring.proto
```

### Run Tests
```bash
# Start all components and verify data flow
./test_flow.sh  # TODO: Create test script
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

MIT License

## 🙏 Acknowledgments

Built with:
- gRPC - Efficient RPC framework
- Kafka - Distributed streaming platform
- Protocol Buffers - Data serialization

---

**Need help?** Check the [docs/](docs/) folder for detailed documentation.
