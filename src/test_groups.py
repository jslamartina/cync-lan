#!/usr/bin/env python3
"""
Test script for group commands. Run this from the addon container after it's started.
This works by connecting via MQTT to trigger the test.
"""
import asyncio
import sys
import os

# Add the cync-lan module to path
sys.path.insert(0, "/root/cync-lan")

from cync_lan.structs import GlobalObject


async def wait_for_server():
    """Wait for the server to be initialized"""
    g = GlobalObject()

    for i in range(30):  # Wait up to 30 seconds
        if g.ncync_server and g.ncync_server.devices:
            return True
        await asyncio.sleep(1)

    return False


async def test_group_commands():
    """Test sending commands to group IDs"""

    print("Waiting for cync-lan server to initialize...")
    if not await wait_for_server():
        print("ERROR: Server did not initialize in time!")
        return 1

    g = GlobalObject()

    if not g.ncync_server.devices:
        print("ERROR: No devices found!")
        return 1

    # Pick any device (we just need it to send commands)
    device = list(g.ncync_server.devices.values())[0]
    print(f"\nUsing device '{device.name}' (ID: {device.id}) to send test commands\n")

    # Test 1: Main group "Hallway" (ID 32768)
    print("=" * 70)
    print("TEST 1: Group 32768 (Hallway)")
    print("Expected devices to respond: [26, 160, 133]")
    print("Command: Turn ON")
    print("=" * 70)
    await device.test_group_command(32768, 1)
    print("\nWaiting 5 seconds for responses...")
    await asyncio.sleep(5)

    # Test 2: Subgroup "Hallway Lights" (ID 32771)
    print("\n" + "=" * 70)
    print("TEST 2: Group 32771 (Hallway Lights)")
    print("Expected devices to respond: [147, 199, 78, 149, 246, 11]")
    print("Command: Turn OFF")
    print("=" * 70)
    await device.test_group_command(32771, 0)
    print("\nWaiting 5 seconds for responses...")
    await asyncio.sleep(5)

    print("\n" + "=" * 70)
    print("Tests complete!")
    print("Check the addon logs for:")
    print("  - EXPERIMENTAL messages showing the command sent")
    print("  - 0x83 status packets from responding devices")
    print("=" * 70)

    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(test_group_commands())
    sys.exit(exit_code)

