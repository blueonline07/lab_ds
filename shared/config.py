"""
Configuration - Kafka topics and system settings
"""
import os
import dotenv
dotenv.load_dotenv()

class Config:
    HOST = os.getenv("GRPC_SERVER_HOST", "localhost")
    PORT = int(os.getenv("GRPC_SERVER_PORT", "50051"))
    MONITORING_TOPIC = "metrics"
    COMMAND = "command"
    KAFKA_BOOTSTRAP_SERVER = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
    ETCD_HOST = os.getenv("ETCD_HOST", "localhost")
    ETCD_PORT = int(os.getenv("ETCD_PORT", "2379"))
