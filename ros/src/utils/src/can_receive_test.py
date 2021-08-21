#! /usr/bin/python3
"""
This file prints out all incoming CAN messages. FUN!
"""


import sys

import can

lastEsc = [0] * 3


def bus_message_received(can_rx: "can.Message") -> None:
    can_id = can_rx.arbitration_id
    if(0x301 <= can_id <= 0x303):
        lastEsc_ = lastEsc[can_id - 0x301]
        lastEsc[can_id - 0x301] = (lastEsc_ + 1) % 4
        data = list(can_rx.data)
        print(f"ESC # {lastEsc_}")
        print(f"Temperature {data[0]} C.")
        print(f"Voltage {data[1] / 255 + 10} V.")
        print(f"Current {(data[2] << 8 + data[3]) / 100} A.")
        print(f"Energy {(data[4] << 8 + data[5])} mAHr.")
        print(f"Speed {(data[6] << 8 + data[7]) * 100} erpm.\n")
    else:
        print(type(can_rx))
        print(f"data: {list(can_rx.data)}")
        print(f"id: {can_id:03X}")
        print(f"message {can_rx}\n\n")


def main(args: list) -> None:
    """"""
    channel = "can0"
    can_bus = can.interface.Bus(channel = channel, bustype = 'socketcan')

    for can_rx in can_bus:
        bus_message_received(can_rx)


if(__name__ == "__main__"):
    main(sys.argv)
