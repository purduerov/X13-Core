#! /usr/bin/python3
"""This script is good for testing the individual actuation and mapping of bits to
solenoids and tools. It can be run either statefully or non-statefully. Stateful
will keep previous solenoids on before "circling back" to turn them off one by one.
"""

import argparse
import sys
import time

import can

from thrust_range_test import N_CAN_BYTES

DELAY = 1.5


def main(args: list) -> None:
    parser = argparse.ArgumentParser(description = __doc__)
    parser.add_argument("--channel", default = "can0", help = "The CAN channel to use")
    parser.add_argument("--wait", default = DELAY, type = int, help = "The time to wait between toggling solenoids.")
    parser.add_argument("--canId", default = 0x204, type = int, help = "The CAN ID of the solenoid board.")
    parser.add_argument("--byteIndex", default = None, type = int, help = "The index of the solenoid control byte in the 8 CAN packet bytes.")
    parser.add_argument("--stateful", default = False, type = bool, help = "Whether to turn solenoids on one by one (False) or turn them all on one by one then off one by one (True).")
    parsed = parser.parse_args(args)

    channel = parsed.channel
    can_bus = can.interface.Bus(channel = channel, bustype = 'socketcan')
    # If you are not sure which byte of the 8 that are sent in a CAN packet is used
    #  by the solenoid board, then set this value to none. Otherwise, set it between 0 and 7.
    solenoidByteIndex = parsed.byteIndex
    # Setting stateful to true will go through and toggle each solenoid such that they
    #  won't turn off until the loop comes around a second time.
    stateful = parsed.stateful
    can_id = parsed.canId

    if solenoidByteIndex is not None and not (0 <= solenoidByteIndex <= 7):
        raise ValueError(f"solenoidByteIndex must be None or between 0 and 7, not {solenoidByteIndex}.")

    print(f"Running {'' if stateful else 'non-'}statefully on {'all indices' if solenoidByteIndex is None else f'index {solenoidByteIndex}'}")

    lastValue = 0x0
    while True:
        for bit_index in reversed(range(7+1)):
            value = 1 << bit_index
            if stateful:
                value = lastValue ^ value
                lastValue = value

            if solenoidByteIndex is None:
                data_array = [value] * N_CAN_BYTES
            else:
                data_array = [0] * N_CAN_BYTES
                data_array[solenoidByteIndex] = value

            data = bytearray(data_array)

            print(f"SOL: {value:#010b}  hex: 0x{value:02X}  index: {bit_index}")
            can_tx = can.Message(arbitration_id=can_id, data=data, extended_id=False)
            can_bus.send(can_tx, timeout=0.1)

            time.sleep(DELAY)
        print('')


if __name__ == "__main__":
    main(sys.argv[1:])
