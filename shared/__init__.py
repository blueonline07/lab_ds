"""
Shared module - Contains protocol definitions and configuration
"""

from .config import Config

from . import monitoring_pb2
from . import monitoring_pb2_grpc

__all__ = [
    "Config",
    "monitoring_pb2",
    "monitoring_pb2_grpc",
]
