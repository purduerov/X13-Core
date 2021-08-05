#! /usr/bin/python3
"""
This file is made for checking the functionality of each thruster. It goes over
every thruster of every ESC one by one.
"""

import sys
import time
from copy import deepcopy

import can
import signal

from thrust_range_test import getSignal, writeToCan
# from ...can_proc.scripts.thrust_proc import can_better_map

can_better_map = {
    0x201: [ 1, 5, 4, 8 ],
    0x202: [ 3, 7, 2, 6 ],
    0x203: [ 0, 0, 0, 0 ]
}


N_CAN_BYTES = 8
N_THRUSTERS = 8
ZERO_THROTTLE = 127
LIL_FORWARD = ZERO_THROTTLE + 13
HALT_BYTE_ARRAY = bytearray([ZERO_THROTTLE] * N_CAN_BYTES)

BASE_PACKET = {
    0x201: [ZERO_THROTTLE] * N_CAN_BYTES,
    0x202: [ZERO_THROTTLE] * N_CAN_BYTES,
    0x203: [ZERO_THROTTLE] * N_CAN_BYTES
}


def main(isMapped = False, channel='can0', bustype='socketcan'):
    can_bus = can.interface.Bus(channel=channel, bustype=bustype)
    signal.signal(signal.SIGINT, getSignal(can_bus))

    if(isMapped and 0):
        base_board = min(can_better_map.keys())
        max_board = max(can_better_map.keys())
        while True:
            for thrusterNum in range(1, N_THRUSTERS + 1):
                can_pow = [ZERO_THROTTLE] * N_THRUSTERS
                can_pow[thrusterNum - 1] = LIL_FORWARD

                for cid in range(base_board, max_board + 1):
                    data_list = 0
                    board = can_better_map[cid]

                    if(thrusterNum not in board):
                        continue;

                    for thruster in board:
                        if thruster:
                            data_list += can_pow[thruster - 1]
                        else:
                            data_list += ZERO_THROTTLE

                        data_list = data_list << 8
                    data_list = data_list >> 8
                    data_list_send = list()
                    shift = 64
                    for i in range(0, 8):
                        shift -= 8
                        data_list_send.append((data_list >> shift) % 256)
                    data = bytearray(data_list_send)

                    # print(f"To board {cid:x} writing {data}")
                    print(f"Thruster {thrusterNum} to board {cid:x} writing {data_list_send}")
                    writeToCan({cid: data})
                    time.sleep(2)
                    writeToCan({cid: HALT_BYTE_ARRAY})
            time.sleep(2)

    else:
        while True:
            for can_id in [0x201, 0x202, 0x203]:
                for motor_index in range(1, 4 + 1):
                    packet = deepcopy(BASE_PACKET)
                    packet[can_id][3 + motor_index] = LIL_FORWARD
                    writeToCan(packet)
                    print(f"Firing ESC {can_id:x} motor {motor_index}")
                    time.sleep(2)
            time.sleep(2)


if __name__ == "__main__":
    main(True)
