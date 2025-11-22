"""
Simple Mock Agent - Generates and sends mock monitoring data
"""

import grpc
import socket
import time
import random
from datetime import datetime

from shared import monitoring_pb2
from shared import monitoring_pb2_grpc


def generate_mock_metrics():
    """Generate random mock system metrics"""
    return {
        "cpu_percent": random.uniform(20.0, 80.0),
        "memory_percent": random.uniform(40.0, 90.0),
        "memory_used_mb": random.uniform(2000.0, 7000.0),
        "memory_total_mb": 8192.0,
        "disk_read_mb": random.uniform(5.0, 50.0),
        "disk_write_mb": random.uniform(2.0, 30.0),
        "net_in_mb": random.uniform(1.0, 20.0),
        "net_out_mb": random.uniform(0.5, 15.0),
    }


def send_metrics(stub, agent_id, hostname, metrics):
    """Send metrics to gRPC server"""
    try:
        # Create protobuf message
        system_metrics = monitoring_pb2.SystemMetrics(
            cpu_percent=metrics["cpu_percent"],
            memory_percent=metrics["memory_percent"],
            memory_used_mb=metrics["memory_used_mb"],
            memory_total_mb=metrics["memory_total_mb"],
            disk_read_mb=metrics["disk_read_mb"],
            disk_write_mb=metrics["disk_write_mb"],
            net_in_mb=metrics["net_in_mb"],
            net_out_mb=metrics["net_out_mb"],
            custom_metrics={},
        )

        request = monitoring_pb2.MetricsRequest(
            agent_id=agent_id,
            hostname=hostname,
            timestamp=int(datetime.now().timestamp()),
            metrics=system_metrics,
            metadata={},
        )

        # Send via gRPC
        response = stub.SendMetrics(request)

        if response.success:
            print("✓ Metrics sent successfully")
            return True
        else:
            print(f"✗ Failed: {response.message}")
            return False

    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def run_mock_agent(agent_id, server_address, interval=5, iterations=10):
    """
    Run mock agent that generates and sends data

    Args:
        agent_id: Agent identifier
        server_address: gRPC server address
        interval: Time between sends (seconds)
        iterations: Number of iterations (0 = infinite)
    """
    hostname = socket.gethostname()

    # Connect to gRPC server
    print("=" * 60)
    print(f"Mock Agent: {agent_id}")
    print("=" * 60)
    print(f"  Hostname: {hostname}")
    print(f"  Server: {server_address}")
    print(f"  Interval: {interval}s")
    print(f"  Iterations: {iterations if iterations > 0 else 'infinite'}")
    print("=" * 60)
    print()

    channel = grpc.insecure_channel(server_address)
    stub = monitoring_pb2_grpc.MonitoringServiceStub(channel)

    print("✓ Connected to gRPC server\n")

    try:
        count = 0
        while True:
            count += 1
            print(f"[{count}] Generating and sending mock metrics...")

            # Generate mock data
            metrics = generate_mock_metrics()

            print(f"  CPU: {metrics['cpu_percent']:.2f}%")
            print(f"  Memory: {metrics['memory_percent']:.2f}%")

            # Send to server
            send_metrics(stub, agent_id, hostname, metrics)

            # Check if we should stop
            if iterations > 0 and count >= iterations:
                print(f"\n✓ Completed {iterations} iterations. Stopping.")
                break

            # Wait for next interval
            print()
            time.sleep(interval)

    except KeyboardInterrupt:
        print("\n\nShutting down mock agent...")
    finally:
        channel.close()
        print("✓ Disconnected")


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="Simple Mock Agent")
    parser.add_argument(
        "--agent-id",
        type=str,
        default="agent-001",
        help="Agent identifier",
    )
    parser.add_argument(
        "--server",
        type=str,
        default="localhost:50051",
        help="gRPC server address",
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=5,
        help="Interval between sends (seconds)",
    )
    parser.add_argument(
        "--iterations",
        type=int,
        default=10,
        help="Number of iterations (0 = infinite)",
    )

    args = parser.parse_args()

    run_mock_agent(
        agent_id=args.agent_id,
        server_address=args.server,
        interval=args.interval,
        iterations=args.iterations,
    )


if __name__ == "__main__":
    main()

