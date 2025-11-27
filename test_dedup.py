#!/usr/bin/env python3
"""
Test script to verify DeduplicationPlugin works correctly
Creates duplicate metrics to test deduplication behavior
"""

import time
from shared import monitoring_pb2
from agent.plugins.deduplication import DeduplicationPlugin


def create_metrics(cpu=50.0, memory=60.0, disk_read=100.0, disk_write=50.0, net_in=10.0, net_out=5.0):
    """Create a MetricsRequest with given values"""
    metrics = monitoring_pb2.SystemMetrics(
        cpu_percent=cpu,
        memory_percent=memory,
        memory_used_mb=8000.0,
        memory_total_mb=16000.0,
        disk_read_mb=disk_read,
        disk_write_mb=disk_write,
        net_in_mb=net_in,
        net_out_mb=net_out,
    )
    
    request = monitoring_pb2.MetricsRequest(
        agent_id="test-agent",
        timestamp=int(time.time()),
        metrics=metrics,
    )
    
    return request


def test_deduplication():
    """Test deduplication plugin behavior"""
    print("=" * 60)
    print("Testing DeduplicationPlugin")
    print("=" * 60)
    
    plugin = DeduplicationPlugin()
    plugin.initialize()
    
    print("\n1. Sending first metrics (should pass)...")
    req1 = create_metrics(cpu=50.0, memory=60.0)
    result1 = plugin.process(req1)
    print(f"   Result: {'✓ PASSED' if result1 is not None else '✗ DROPPED'}")
    
    print("\n2. Sending identical metrics (should be dropped)...")
    req2 = create_metrics(cpu=50.0, memory=60.0)
    result2 = plugin.process(req2)
    print(f"   Result: {'✗ PASSED (ERROR!)' if result2 is not None else '✓ DROPPED'}")
    
    print("\n3. Sending identical metrics again (should be dropped)...")
    req3 = create_metrics(cpu=50.0, memory=60.0)
    result3 = plugin.process(req3)
    print(f"   Result: {'✗ PASSED (ERROR!)' if result3 is not None else '✓ DROPPED'}")
    
    print("\n4. Sending different CPU metrics (should pass)...")
    req4 = create_metrics(cpu=75.0, memory=60.0)
    result4 = plugin.process(req4)
    print(f"   Result: {'✓ PASSED' if result4 is not None else '✗ DROPPED (ERROR!)'}")
    
    print("\n5. Sending same as #4 (should be dropped)...")
    req5 = create_metrics(cpu=75.0, memory=60.0)
    result5 = plugin.process(req5)
    print(f"   Result: {'✗ PASSED (ERROR!)' if result5 is not None else '✓ DROPPED'}")
    
    print("\n6. Sending different memory metrics (should pass)...")
    req6 = create_metrics(cpu=75.0, memory=80.0)
    result6 = plugin.process(req6)
    print(f"   Result: {'✓ PASSED' if result6 is not None else '✗ DROPPED (ERROR!)'}")
    
    print("\n7. Sending back to original values (should pass)...")
    req7 = create_metrics(cpu=50.0, memory=60.0)
    result7 = plugin.process(req7)
    print(f"   Result: {'✓ PASSED' if result7 is not None else '✗ DROPPED (ERROR!)'}")
    
    print("\n8. Sending identical to #7 (should be dropped)...")
    req8 = create_metrics(cpu=50.0, memory=60.0)
    result8 = plugin.process(req8)
    print(f"   Result: {'✗ PASSED (ERROR!)' if result8 is not None else '✓ DROPPED'}")
    
    plugin.finalize()
    
    # Calculate expected results
    expected_sent = 4  # req1, req4, req6, req7
    expected_dropped = 4  # req2, req3, req5, req8
    
    print("\n" + "=" * 60)
    print(f"Expected: Sent={expected_sent}, Dropped={expected_dropped}")
    print(f"Actual:   Sent={plugin.sent_count}, Dropped={plugin.dropped_count}")
    
    if plugin.sent_count == expected_sent and plugin.dropped_count == expected_dropped:
        print("\n✓✓✓ DEDUPLICATION WORKS CORRECTLY! ✓✓✓")
    else:
        print("\n✗✗✗ DEDUPLICATION HAS ISSUES! ✗✗✗")
    print("=" * 60)


if __name__ == "__main__":
    test_deduplication()
