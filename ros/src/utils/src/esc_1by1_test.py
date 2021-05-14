#! /usr/bin/python3
"""
This file is made for checking the functionality of each thruster. It goes over
every thruster of every ESC one by one.
"""

import sys
import can
import time
import signal

from .thrust_range_test import getSignal, writeToCan
from ...can_proc.scripts.thrust_proc import can_better_map

N_CAN_BYTES = 8
N_THRUSTERS = 8
ZERO_THROTTLE = 127
LIL_FORWARD = ZERO_THROTTLE + 13

BASE_PACKET = {
    0x201: [ZERO_THROTTLE] * N_CAN_BYTES,
    0x202: [ZERO_THROTTLE] * N_CAN_BYTES,
    0x203: [ZERO_THROTTLE] * N_CAN_BYTES
}


def main(isMapped = False, channel='can0', bustype='socketcan'):
    can_bus = can.interface.Bus(channel=channel, bustype=bustype)
    signal.signal(signal.SIGINT, getSignal(can_bus))

    if(isMapped):
        thrusterToCanId = {}
        thrusterToEscId = {}
        for (canId, thrusters) in can_better_map.items():
            for (i, thruster_num_i) in enumerate(thrusters):
                if(i != 0):
                    thrusterToCanId[thruster_num_i] = canId
                    thrusterToEscId[thruster_num_i] = i
        while True:
            for thrusterNum in range(1, N_THRUSTERS + 1):
                packet = BASE_PACKET.copy()
                canId = thrusterToCanId[thrusterNum]
                motorNumber = thrusterToEscId[thrusterNum]
                packet[canId][motorNumber] = LIL_FORWARD
                writeToCan(packet)
                print(f"Firing thruster {thrusterNum} on ESC {canId:x} motor {motorNumber}")
                time.sleep(1)
        while True:
            for can_id in [0x201, 0x202, 0x203]:
                for motor_index in range(1, 4 + 1):
                    packet = BASE_PACKET.copy()
                    packet[can_id][4 + motor_index] = LIL_FORWARD
                    writeToCan(packet)
                    print(f"Firing ESC {can_id:x} motor {motor_index}")
                    time.sleep(1)


if __name__ == "__main__":
    main()
