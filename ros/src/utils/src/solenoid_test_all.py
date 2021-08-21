#! /usr/bin/python3
"""This script alternates with all the solenoids on and all the solenoids off.
Useful for checking if anything works or flushing lines after a pool test.
"""

import argparse
import sys
import time

import can

from thrust_range_test import N_CAN_BYTES

DELAY = 1.5


def main(args: list) -> None:
    """"""
    parser = argparse.ArgumentParser(description = __doc__)
    parser.add_argument("--channel", default = "can0", help = "The CAN channel to use")
    parser.add_argument("--wait", default = DELAY, type = int, help = "The time to wait between toggling solenoids.")
    parser.add_argument("--canId", default = 0x204, type = int, help = "The CAN ID of the solenoid board.")
    parsed = parser.parse_args(args)
    channel = parsed.channel
    can_bus = can.interface.Bus(channel=channel, bustype='socketcan')
    can_id = parsed.canId

    values = [0xFF, 0x00]

    while True:
        for v in values:
            data = bytearray([v] * N_CAN_BYTES)

            print(f"SOL: {v:#010b}  hex: 0x{v:02X}")
            can_tx = can.Message(arbitration_id=can_id, data=data, extended_id=False)
            can_bus.send(can_tx, timeout=0.1)

            time.sleep(DELAY)


if __name__ == "__main__":
    main(sys.argv[1:])
