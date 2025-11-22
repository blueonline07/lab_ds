"""
Shared module - Contains protocol definitions and configuration
"""

from .config import KafkaTopics

from . import monitoring_pb2
from . import monitoring_pb2_grpc

__all__ = [
    # Config
    "KafkaTopics",
    # Protobuf
    "monitoring_pb2",
    "monitoring_pb2_grpc",
]
