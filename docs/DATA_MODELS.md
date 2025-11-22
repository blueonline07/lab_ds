# Data Models Reference

Complete reference for all data structures used in the monitoring system.

## Overview

The system uses Protocol Buffers for gRPC communication and JSON for Kafka messages.

---

## gRPC Models (`shared/monitoring.proto`)

### Service Definition

```protobuf
service MonitoringService {
    // Bidirectional streaming: Agent sends metrics, receives commands
    rpc StreamMetrics(stream MetricsRequest) returns (stream Command);
    
    // Send command to an agent (from external clients)
    rpc SendCommand(Command) returns (CommandResponse);
}
```

### SystemMetrics

System performance metrics.

```protobuf
message SystemMetrics {
    double cpu_percent = 1;        // CPU usage (0-100)
    double memory_percent = 2;      // Memory usage (0-100)
    double memory_used_mb = 3;     // Memory used in MB
    double memory_total_mb = 4;    // Total memory in MB
    double disk_read_mb = 5;       // Disk read rate (MB/s)
    double disk_write_mb = 6;       // Disk write rate (MB/s)
    double net_in_mb = 7;          // Network in rate (MB/s)
    double net_out_mb = 8;         // Network out rate (MB/s)
}
```

### MetricsRequest

Metrics sent from agent to server.

```protobuf
message MetricsRequest {
    string agent_id = 1;           // Agent identifier
    int64 timestamp = 2;           // Unix timestamp
    SystemMetrics metrics = 3;     // System metrics
    map<string, string> metadata = 4; // Additional metadata
}
```

### Command

Start/Stop commands for agents.

```protobuf
enum CommandType {
    START = 0;
    STOP = 1;
}

message Command {
    string agent_id = 1;           // Target agent ID
    CommandType type = 2;          // Command type (START or STOP)
}
```

### CommandResponse

Response to command send request.

```protobuf
message CommandResponse {
    bool success = 1;              // Whether command was queued successfully
    string message = 2;            // Response message
}
```

---

## Kafka Messages

### Topic: `monitoring-data`

Messages sent from gRPC server to Kafka containing monitoring metrics.

**Schema:**
```json
{
  "agent_id": "string",
  "timestamp": "string (ISO 8601)",
  "metrics": {
    "cpu_percent": "float",
    "memory_percent": "float",
    "memory_used_mb": "float",
    "memory_total_mb": "float",
    "disk_read_mb": "float",
    "disk_write_mb": "float",
    "net_in_mb": "float",
    "net_out_mb": "float"
  },
  "metadata": "dict"
}
```

**Example:**
```json
{
  "agent_id": "agent-001",
  "timestamp": "2025-11-22T10:30:00Z",
  "metrics": {
    "cpu_percent": 45.2,
    "memory_percent": 62.5,
    "memory_used_mb": 5000.0,
    "memory_total_mb": 8000.0,
    "disk_read_mb": 12.5,
    "disk_write_mb": 8.3,
    "net_in_mb": 5.2,
    "net_out_mb": 3.1
  },
  "metadata": {"os": "Linux", "version": "Ubuntu 22.04"}
}
```

---

## Configuration

### Kafka Topics (`shared/config.py`)

```python
class KafkaTopics:
    MONITORING_DATA = "monitoring-data"  # gRPC Server → Analysis App
```

---

## Data Flow

```
Agent → StreamMetrics(MetricsRequest) → Server → Kafka → Analysis App
Agent ← StreamMetrics(Command) ← Server
```

**Commands:**
- `START` - Start metrics collection
- `STOP` - Stop metrics collection

**Note:** Configuration (interval, metrics, plugins) is handled separately, not via commands.

---

## Key Points

1. **No Custom Metrics** - Removed from SystemMetrics
2. **No Hostname** - Removed from metrics data
3. **Commands Only** - Server sends START/STOP commands only
4. **Single Kafka Topic** - Only `monitoring-data`
5. **Bidirectional Streaming** - Agent ↔ Server via gRPC
6. **CommandResponse** - Used for SendCommand RPC method

---

## Usage Examples

### Creating SystemMetrics (Protobuf)

```python
from shared import monitoring_pb2

metrics = monitoring_pb2.SystemMetrics(
    cpu_percent=45.2,
    memory_percent=62.5,
    memory_used_mb=5000.0,
    memory_total_mb=8000.0,
    disk_read_mb=12.5,
    disk_write_mb=8.3,
    net_in_mb=5.2,
    net_out_mb=3.1
)
```

### Creating Command

```python
from shared import monitoring_pb2

command = monitoring_pb2.Command(
    agent_id="agent-001",
    type=monitoring_pb2.START
)
```

### Sending Command and Getting Response

```python
from shared import monitoring_pb2, monitoring_pb2_grpc
import grpc

channel = grpc.insecure_channel("localhost:50051")
stub = monitoring_pb2_grpc.MonitoringServiceStub(channel)

command = monitoring_pb2.Command(
    agent_id="agent-001",
    type=monitoring_pb2.STOP
)

response = stub.SendCommand(command)
if response.success:
    print(f"✓ {response.message}")
else:
    print(f"✗ {response.message}")
```

---

## Field Descriptions

### SystemMetrics Fields

| Field | Type | Description | Range |
|-------|------|-------------|-------|
| `cpu_percent` | double | CPU usage percentage | 0-100 |
| `memory_percent` | double | Memory usage percentage | 0-100 |
| `memory_used_mb` | double | Memory used in MB | ≥ 0 |
| `memory_total_mb` | double | Total memory in MB | ≥ 0 |
| `disk_read_mb` | double | Disk read rate in MB/s | ≥ 0 |
| `disk_write_mb` | double | Disk write rate in MB/s | ≥ 0 |
| `net_in_mb` | double | Network incoming rate in MB/s | ≥ 0 |
| `net_out_mb` | double | Network outgoing rate in MB/s | ≥ 0 |

### Command Fields

| Field | Type | Description |
|-------|------|-------------|
| `agent_id` | string | Target agent identifier |
| `type` | CommandType | Command type: START or STOP |

### CommandResponse Fields

| Field | Type | Description |
|-------|------|-------------|
| `success` | bool | Whether command was queued successfully |
| `message` | string | Response message |

---

**Last Updated:** 2025-11-22
