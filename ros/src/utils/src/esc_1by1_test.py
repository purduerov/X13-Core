#! /usr/bin/python3
"""
This file is made for checking the functionality of each thruster. It goes over
every thruster of every ESC one by one.
"""
import argparse
import sys
import time
from copy import deepcopy

import can
import signal

from thrust_range_test import getSignal, writeToCan, N_CAN_BYTES, ZERO_THROTTLE
# from ...can_proc.scripts.thrust_proc import can_better_map

can_better_map = {
    0x201: [ 1, 5, 4, 8 ],
    0x202: [ 3, 7, 2, 6 ],
    0x203: [ 0, 0, 0, 0 ]
}

DELAY = 3
N_THRUSTERS = 8
LIL_FORWARD = ZERO_THROTTLE + 13
HALT_BYTE_ARRAY = bytearray([ZERO_THROTTLE] * N_CAN_BYTES)

BASE_PACKET = {
    0x201: [ZERO_THROTTLE] * N_CAN_BYTES,
    0x202: [ZERO_THROTTLE] * N_CAN_BYTES,
    0x203: [ZERO_THROTTLE] * N_CAN_BYTES
}


def main(args: list) -> None:
    """"""
    parser = argparse.ArgumentParser(description = __doc__)
    parser.add_argument("--isMapped", default = True, type = bool, help = "")
    parser.add_argument("--channel", default = "can0", help = "Which can channel to send messages on.")
    parser.add_argument("--bustype", default = "socketcan", help = "The bus type")
    parsed = parser.parse_args(args)

    can_bus = can.interface.Bus(channel=parsed.channel, bustype=parsed.bustype)
    signal.signal(signal.SIGINT, getSignal(can_bus))

    min_board = min(can_better_map.keys())
    max_board = max(can_better_map.keys())
    if(parsed.isMapped):
        while True:
            for thrusterNum in range(1, N_THRUSTERS + 1):
                can_pow = [ZERO_THROTTLE] * N_THRUSTERS
                can_pow[thrusterNum - 1] = LIL_FORWARD

                for cid in range(min_board, max_board + 1):
                    data_list = 0x7F_7F_7F_7F_00
                    board = can_better_map[cid]

                    if(thrusterNum not in board):
                        continue

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

                    print(f"Thruster {thrusterNum} to board 0x{cid:x} writing {data_list_send}")
                    writeToCan({cid: data})
                    time.sleep(2)
                    writeToCan({cid: HALT_BYTE_ARRAY})

    else:
        while True:
            for can_id in range(min_board, max_board + 1):
                for motor_index in range(1, 4 + 1):
                    packet = deepcopy(BASE_PACKET)
                    packet[can_id][3 + motor_index] = LIL_FORWARD
                    writeToCan(packet)
                    print(f"Firing ESC 0x{can_id:x} motor {motor_index}")
                    time.sleep(DELAY)


if __name__ == "__main__":
    main(sys.argv[1:])
