#! /usr/bin/python
import sys
import can
import time

IDS = [516]
POS_RANGE = 4
DEFAULT_POWER = 200
ZERO_POWER = 127
DELAY = 0.1


# This is a test script intended to simplify identification of hardware thruster
# configuration by sending commands to each possible thruster position one at a time.


if __name__ == "__main__":
    channel = 'can0'
    if len(sys.argv) == 2:
        channel = sys.argv[1]
    can_bus = can.interface.Bus(channel=channel, bustype='socketcan')

    values = [0xFF, 0x00]
    for _ in range(100000000000):
    	for v in values:
            data_array = [0] * 8;
            for i in range(0,8):
                data_array[i]=v
            #data_array[-1] = v
            data = bytearray(data_array)

            print("SOL: %s" % bin(v))
            can_tx = can.Message(arbitration_id=516, data=data, extended_id=False)
            can_bus.send(can_tx, timeout=0.1)

            time.sleep(DELAY)
