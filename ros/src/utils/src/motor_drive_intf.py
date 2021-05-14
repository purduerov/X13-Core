#! /usr/bin/python3
"""
This file is for running a motor and being able to set speeds for
a motor or thruster. It is intended as a backup for the ESC Black
Box or to test with the full ROV.
"""


import sys
import can
import time
import signal

from .thrust_range_test import writeToCan, getSignal, zeroOutThrusters
from .esc_1by1_test import BASE_PACKET


N_CAN_BYTES = 8
ZERO_THROTTLE = 127


def discoverCanId() -> int:
    """"""
    canIdStr = input("Enter the ESC CAN ID (usually 0x201-0x203) to be driven: ").strip().lower()
    base = 10 + 6 * ('x' in canIdStr)
    try:
        canId = int(canIdStr, base = base)
    except ValueError:
        print(f"Error: Not a valid decimal or hexadecimal ID entered. Got {canIdStr}.")
        sys.exit(1)
    return canId


def discoverEscId() -> int:
    """"""
    escIdStr = input("Enter which ESC to be driven (1-4): ").strip().lower()
    try:
        escId = int(escIdStr)
        if(not 1 <= escId <= 4):
            print(f"Error: Need an esc number between 1 and 4, not {escId}.")
            sys.exit(1)
    except ValueError:
        print(f"Error: Not a valid number, got {escIdStr}")
        sys.exit(1)
    return escId


def main() -> None:
    """"""
    can_bus = can.interface.Bus(channel = 'can0', bustype = 'socketcan')
    signal.signal(signal.SIGINT, getSignal(can_bus))

    canId = discoverCanId()
    escNum = discoverEscId()

    print(f"Enter speeds for the ESC. 0 is full reverse, {ZERO_THROTTLE} is stationary, 255 is full forward.")
    while(True):
        try:
            speed = int(input("Speed>").strip())
            if(speed > 255 or speed < 0):
                raise ValueError()
            packet = BASE_PACKET.copy()
            packet[canId][4 + escNum] = speed
            writeToCan(packet)
        except ValueError:
            zeroOutThrusters()
            sys.exit(1)
        # send CAN packet


if(__name__ == "__main__"):
    main()
