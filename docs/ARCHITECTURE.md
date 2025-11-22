# Architecture Documentation

## Project Structure

```
lab_ds/
├── shared/                          # Shared protocol definitions and config
│   ├── __init__.py
│   ├── config.py                    # Kafka topics configuration
│   ├── monitoring.proto             # gRPC protocol definition
│   ├── monitoring_pb2.py            # Generated protobuf messages
│   └── monitoring_pb2_grpc.py       # Generated gRPC stubs
│
├── grpc_server/                     # gRPC Server Module
│   ├── __init__.py
│   ├── server.py                    # gRPC server implementation
│   └── kafka_producer.py            # Kafka producer service
│
├── analysis_app/                    # Analysis Application Module
│   ├── __init__.py
│   └── consumer.py                  # Kafka consumer implementation
│
├── mock_agent.py                    # Mock agent (generates test data)
├── send_command.py                  # Send START/STOP commands to agents
│
├── run_agent.py                     # ⭐ Entry point for agent
├── run_server.py                    # ⭐ Entry point for gRPC server
├── run_analysis.py                  # ⭐ Entry point for analysis app
│
├── docker-compose.yml               # Kafka infrastructure
├── requirements.txt                 # Python dependencies
└── README.md                        # Main documentation
```

## Module Descriptions

### 1. Shared Module (`shared/`)

**Purpose**: Contains protocol definitions and configuration

**Components**:
- `config.py` - Kafka topics configuration
- `monitoring.proto` - Protocol buffer definitions for gRPC
- `monitoring_pb2.py` & `monitoring_pb2_grpc.py` - Auto-generated gRPC code

**Key Classes**:
- `KafkaTopics` - Kafka topic names

**Protocol Definitions**:
- `SystemMetrics` - System metrics data structure
- `MetricsRequest` - Metrics sent from agent
- `Command` - START/STOP commands
- `CommandResponse` - Response to command send request

### 2. Mock Agent (`mock_agent.py`)

**Purpose**: Generates mock monitoring data and sends to gRPC server

**Key Class**: `MockAgent`

**Features**:
- Generates random system metrics
- Bidirectional streaming with gRPC server
- Responds to START/STOP commands
- Configurable collection interval

**Usage**:
```python
from mock_agent import MockAgent

agent = MockAgent(
    agent_id="agent-001",
    server_address="localhost:50051"
)
agent.run_streaming()
```

### 3. gRPC Server Module (`grpc_server/`)

**Purpose**: Acts as a broker between agents (gRPC) and Kafka

**Components**:
- `server.py` - gRPC service implementation
- `kafka_producer.py` - Kafka producer service for message forwarding

**Key Classes**:
- `MonitoringServiceServicer` - gRPC service that receives agent data
- `KafkaProducerService` - Kafka producer wrapper

**Features**:
- Bidirectional streaming with agents
- Forwards metrics to Kafka
- Routes commands to agents
- Handles agent connections/disconnections

**RPC Methods**:
- `StreamMetrics` - Bidirectional streaming for metrics and commands
- `SendCommand` - Send START/STOP commands to agents

### 4. Analysis App Module (`analysis_app/`)

**Purpose**: Consumes monitoring data from Kafka and displays it

**Components**:
- `consumer.py` - Kafka consumer implementation

**Key Class**: `AnalysisApp`

**Features**:
- Subscribes to `monitoring-data` topic
- Displays metrics in readable format
- Continuous consumption

### 5. Command Sender (`send_command.py`)

**Purpose**: Send START/STOP commands to agents via gRPC server

**Usage**:
```bash
python3 send_command.py --agent-id agent-001 --command start
python3 send_command.py --agent-id agent-001 --command stop
```

## Communication Flow

### 1. Metrics Flow

```
Mock Agent → StreamMetrics(MetricsRequest) → gRPC Server → Kafka → Analysis App
```

1. Agent generates metrics
2. Agent sends `MetricsRequest` via bidirectional stream
3. Server receives metrics
4. Server forwards to Kafka topic `monitoring-data`
5. Analysis app consumes from Kafka
6. Analysis app displays metrics

### 2. Command Flow

```
send_command.py → SendCommand(Command) → gRPC Server → StreamMetrics(Command) → Agent
```

1. External client calls `SendCommand` RPC
2. Server queues command for agent
3. Server sends command via bidirectional stream
4. Agent receives and processes command (START/STOP)

## Data Flow Diagram

```
┌─────────────────┐                ┌─────────────────┐                ┌─────────────────┐
│  Mock Agent     │─── gRPC ──────►│  gRPC Server    │──── Kafka ────►│  Analysis App   │
│                 │◄── Stream ─────│  (Broker)       │◄─── Kafka ─────│                 │
│ • Generates     │                │ • Forwards data │                │ • Consumes data │
│   mock metrics  │                │ • Routes cmds   │                │ • Displays data │
│ • Handles       │                │                 │                │                 │
│   START/STOP    │                │                 │                │                 │
└─────────────────┘                └─────────────────┘                └─────────────────┘
         ▲                                   ▲
         │                                   │
         └─────────── SendCommand ──────────┘
                    (from CLI)
```

## Key Design Decisions

### 1. Bidirectional Streaming
- Agent and server maintain persistent connection
- Real-time communication, no polling
- Commands sent immediately when available

### 2. Kafka as Message Broker
- Decouples gRPC server from analysis app
- Persistent storage of metrics
- Scalable consumption

### 3. Simplified Data Model
- No custom metrics
- No hostname in metrics
- Only essential system metrics

### 4. Command-Only Control
- START/STOP commands only
- Configuration handled separately
- Simple, focused interface

### 5. Protocol Buffers
- Efficient serialization
- Language-agnostic
- Type-safe communication

## Configuration

### Kafka Topics

Defined in `shared/config.py`:
```python
class KafkaTopics:
    MONITORING_DATA = "monitoring-data"  # gRPC Server → Analysis App
```

### gRPC Server

- Default port: `50051`
- Default Kafka: `localhost:9092`

### Mock Agent

- Default server: `localhost:50051`
- Default interval: `5` seconds
- Default agent ID: `agent-001`

## Deployment

### Development

```bash
# Terminal 1: Start Kafka
docker-compose up -d

# Terminal 2: Start gRPC Server
python3 run_server.py

# Terminal 3: Start Analysis App
python3 run_analysis.py

# Terminal 4: Start Agent
python3 run_agent.py
```

### Production

- Run each component as a separate service
- Use environment variables for configuration
- Monitor Kafka topics for message flow
- Scale analysis app horizontally

## Error Handling

### Agent Disconnection
- Server detects disconnection
- Cleans up agent command queue
- Logs disconnection event

### Kafka Failures
- Producer retries on failure
- Logs error messages
- Continues processing other agents

### gRPC Errors
- Agent reconnects automatically
- Server handles connection errors gracefully
- Commands queued until agent reconnects

## Future Enhancements

- Real system metrics collection (not just mock)
- Multiple metric collection plugins
- Configuration management system
- Agent health monitoring
- Metrics aggregation and alerting

---

**Last Updated:** 2025-11-22
