#! /usr/bin/python3
import sys
import can
import time

IDS = [516]
POS_RANGE = 4
DEFAULT_POWER = 200
ZERO_POWER = 127
DELAY = 1.5


if __name__ == "__main__":
    channel = 'can0'
    if len(sys.argv) == 2:
        channel = sys.argv[1]
    can_bus = can.interface.Bus(channel=channel, bustype='socketcan')

    values = [0x80, 0x40, 0x20, 0x10, 0x08, 0x04, 0x02, 0x01, 0x00]

	# If you are not sure which byte of the 8 that are sent in a CAN packet is used
	#  by the solenoid board, then set this value to none. Otherwise, set it between 0 and 7.
    solenoidByteIndex = None
	# Setting stateful to true will go through and toggle each solenoid such that they
	#  won't turn off until the loop comes around a second time.
    stateful = False

    assert solenoidByteIndex is None or 0 <= solenoidByteIndex <= 7
    lastValue = 0x0
    while(True):
        for bit_index in reversed(range(7+1)):
		# for bit_index in [4, 3, 2, 1]:
            value = 1 << bit_index
            if(stateful):
                value = lastValue ^ value
                lastValue = value

            if(solenoidByteIndex is None):
                data_array = [value] * 8
            else:
                data_array = [0] * 8
                data_array[solenoidByteIndex] = value

            data = bytearray(data_array)

            print(f"SOL: {value:#010b}  hex: 0x{value:02X}  index: {bit_index}")
            can_tx = can.Message(arbitration_id=0x204, data=data, extended_id=False)
            can_bus.send(can_tx, timeout=0.1)

            time.sleep(DELAY)
        print('')
