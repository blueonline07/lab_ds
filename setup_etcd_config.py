#!/usr/bin/env python3
"""
Helper script to set up etcd configuration for monitoring agents
"""
import json
import argparse
import etcd3


def setup_config(
    agent_id: str,
    etcd_host: str = "localhost",
    etcd_port: int = 2379,
    interval: int = 5,
    metrics: list = None,
    plugins: list = None,
):
    """
    Set up configuration in etcd

    Args:
        agent_id: Agent identifier for config key
        etcd_host: etcd server hostname
        etcd_port: etcd server port
        interval: Metrics collection interval in seconds
        metrics: List of metrics to collect
        plugins: List of plugin paths
    """
    if metrics is None:
        metrics = [
            "cpu",
            "memory",
            "disk read",
            "disk write",
            "net in",
            "net out",
        ]

    if plugins is None:
        plugins = [
            "agent.plugins.deduplication.DeduplicationPlugin",
        ]

    config_key = f"/monitor/config/{agent_id}"
    config = {
        "interval": interval,
        "metrics": metrics,
        "plugins": plugins,
    }

    try:
        etcd = etcd3.client(host=etcd_host, port=etcd_port)
        etcd.put(config_key, json.dumps(config, indent=2))
        print("✓ Configuration set in etcd:")
        print(f"  Key: {config_key}")
        print(f"  Config: {json.dumps(config, indent=2)}")
    except Exception as e:
        print(f"✗ Error setting config in etcd: {e}")
        return False

    return True


def main():
    parser = argparse.ArgumentParser(
        description="Set up etcd configuration for monitoring agents"
    )
    parser.add_argument(
        "--etcd-host", type=str, default="localhost", help="etcd server hostname"
    )
    parser.add_argument("--etcd-port", type=int, default=2379, help="etcd server port")
    parser.add_argument(
        "--agent-id",
        type=str,
        required=True,
        help="Agent ID for config key",
    )
    parser.add_argument(
        "--interval", type=int, default=5, help="Metrics collection interval (seconds)"
    )
    parser.add_argument(
        "--metrics",
        nargs="+",
        default=None,
        help='Metrics to collect (default: ["cpu", "memory", "disk read", "disk write", "net in", "net out"])',
    )
    parser.add_argument(
        "--plugins",
        nargs="+",
        default=None,
        help="Plugin paths (default: [agent.plugins.deduplication.DeduplicationPlugin])",
    )

    args = parser.parse_args()

    setup_config(
        agent_id=args.agent_id,
        etcd_host=args.etcd_host,
        etcd_port=args.etcd_port,
        interval=args.interval,
        metrics=args.metrics,
        plugins=args.plugins,
    )


if __name__ == "__main__":
    main()
