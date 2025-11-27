"""
gRPC Server - Broker between Agents and Kafka
- Receives metrics from agents via client streaming
- Forwards metrics to Kafka
"""

import grpc
import uuid
import socket
import threading
from concurrent import futures

from shared import monitoring_pb2, monitoring_pb2_grpc
from confluent_kafka import Producer, Consumer


class MonitoringServiceServicer(monitoring_pb2_grpc.MonitoringServiceServicer):
    """gRPC service implementation for receiving monitoring data from agents"""

    def __init__(
        self, kafka_producer: Producer, kafka_consumer: Consumer
    ):
        """
        Initialize the monitoring service

        Args:
            kafka_producer: Kafka producer service for forwarding data
            kafka_bootstrap_servers: Kafka bootstrap servers
        """
        self.producer = kafka_producer
        self.consumer = kafka_consumer
        self.agents = {}
        self.lock = threading.Lock()

    def StreamMetrics(self, request_iterator, context):
        """
        Client streaming: Agent sends metrics
        - Receives: stream MetricsRequest (periodic data from agent)
        - Forwards metrics to Kafka
        """

        def process_requests():
            try:
                for request in request_iterator:
                    print(request)
                    self.producer.flush()
                    
                    print(f"Received metrics from agent {request.agent_id}")
                    
            except Exception as e:
                print(f"Error processing requests: {e}")
        
        recv_thread = threading.Thread(target=process_requests, daemon=True)
        recv_thread.start()
        
        try:
            while context.is_active():
                message = self.consumer.poll(timeout=1.0)
                if message is not None and not message.error():
                    # Process message and yield command
                    yield monitoring_pb2.CommandResponse(
                        command=message.value().decode('utf-8')
                    )
        except Exception as e:
            print(f"Error in response stream: {e}")
        finally:
            recv_thread.join(timeout=2)

_server_servicer = None

def serve(
    port,
    bootstrap_servers
):
    """
    Start the gRPC server

    Args:
        port: Port to listen on (defaults to GRPC_SERVER_PORT env var or 50051)
        kafka_bootstrap_servers: Kafka bootstrap servers (defaults to KAFKA_BOOTSTRAP_SERVERS env var or localhost:9092)
    """

    global _server_servicer

    kafka_producer = Producer({
        "bootstrap.servers": bootstrap_servers,
        "client.id": socket.gethostname()
    })

    kafka_consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': str(uuid.uuid4()),
        'auto.offset.reset': 'smallest'
    })

    # Create gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    _server_servicer = MonitoringServiceServicer(
        kafka_producer, kafka_consumer
    )
    monitoring_pb2_grpc.add_MonitoringServiceServicer_to_server(
        _server_servicer, server
    )
    server.add_insecure_port(f"[::]:{port}")

    server.start()
    print(f"✓ gRPC Server running on port {port}")
    print(f"✓ Kafka: {bootstrap_servers}")

    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("\n\nShutting down server...")
        server.stop(0)
        kafka_producer.close()


def get_server_servicer():
    """Get the global server servicer instance"""
    return _server_servicer
