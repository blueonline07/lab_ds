"""
Command Sender - Send START/STOP commands to agents via gRPC server
"""

import sys
import grpc

from shared import monitoring_pb2
from shared import monitoring_pb2_grpc


def send_command(
    agent_id: str, command_type: str, server_address: str = "localhost:50051"
):
    """
    Send START or STOP command to an agent via gRPC

    Args:
        agent_id: Target agent ID
        command_type: "start" or "stop"
        server_address: gRPC server address (default: localhost:50051)
    """
    # Parse command type
    command_type = command_type.lower()
    if command_type == "start":
        cmd_type = monitoring_pb2.START
    elif command_type == "stop":
        cmd_type = monitoring_pb2.STOP
    else:
        print(f"✗ Invalid command type: {command_type} (must be 'start' or 'stop')")
        return False

    # Connect to gRPC server
    try:
        channel = grpc.insecure_channel(server_address)
        stub = monitoring_pb2_grpc.MonitoringServiceStub(channel)

        # Create command message
        command = monitoring_pb2.Command(agent_id=agent_id, type=cmd_type)

        print(f"📤 Sending {command_type.upper()} command to agent: {agent_id}")

        # Send command via gRPC
        response = stub.SendCommand(command)

        channel.close()

        if response.success:
            print(f"✓ {response.message}")
            return True
        else:
            print(f"✗ {response.message}")
            return False

    except grpc.RpcError as e:
        print(f"✗ gRPC Error: {e.code()} - {e.details()}")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def main():
    """Main entry point for command-line usage"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Send START/STOP commands to agents",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Start an agent
  python3 send_command.py --agent-id agent-001 --command start

  # Stop an agent
  python3 send_command.py --agent-id agent-001 --command stop
        """,
    )

    parser.add_argument(
        "--agent-id",
        type=str,
        required=True,
        help="Target agent ID",
    )
    parser.add_argument(
        "--command",
        type=str,
        required=True,
        choices=["start", "stop"],
        help="Command to send (start or stop)",
    )
    parser.add_argument(
        "--server",
        type=str,
        default="localhost:50051",
        help="gRPC server address (default: localhost:50051)",
    )

    args = parser.parse_args()

    # Send command
    success = send_command(
        agent_id=args.agent_id,
        command_type=args.command,
        server_address=args.server,
    )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
