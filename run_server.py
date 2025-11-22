#!/usr/bin/env python3
"""
Entry point for running the gRPC server
"""

import os

if __name__ == "__main__":
    from grpc_server.server import serve

    port = os.getenv("GRPC_SERVER_PORT")
    kafka_bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
    
    serve(
        port=int(port) if port else None,
        kafka_bootstrap_servers=kafka_bootstrap_servers,
    )
