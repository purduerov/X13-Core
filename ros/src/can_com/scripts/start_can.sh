#!/bin/bash
sudo ip link set can0 down
sudo ip link set can0 up type can bitrate 125000 restart-ms 1 
# sudo ip link set can0 type can restart-ms 100
