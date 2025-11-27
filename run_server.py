#!/usr/bin/env python3
"""
Entry point for running the gRPC server
"""

from shared.config import Config

if __name__ == "__main__":
    from grpc_server.server import serve

    port = Config.PORT
    kafka_bootstrap_servers = Config.KAFKA_BOOTSTRAP_SERVER
    
    serve(
        port=int(port) if port else None,
        bootstrap_servers=kafka_bootstrap_servers,
    )
