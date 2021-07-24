#! /usr/bin/python3
"""
This file prints out all incoming CAN messages. FUN!
"""


import sys
from copy import deepcopy

import can


def bus_message_received(can_rx: "can.Message") -> None:
    print(type(can_rx))
    print(f"data: {list(can_rx.data)}")
    print(f"id: {can_rx.arbitration_id:03X}")
    print(f"message {can_rx}\n\n")


def main(args: list) -> None:
    """"""
    channel = "can0"
    can_bus = can.interface.Bus(channel = channel, bustype = 'socketcan')

    for can_rx in can_bus:
        bus_message_received()
    


if(__name__ == "__main__"):
    main(sys.argv)
