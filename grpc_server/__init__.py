"""
gRPC Server module - Receives data from agents and forwards to Kafka
"""

from .server import MonitoringServiceServicer, serve

__all__ = ["MonitoringServiceServicer", "serve"]
