#!/usr/bin/python3

import time
import board
import busio
import adafruit_bno055
 
# Use these lines for I2C
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_bno055.BNO055_I2C(i2c)

while True:
    #print("Accelerometer (m/s^2): {}".format(sensor.acceleration))
    #print("Gyroscope (rad/sec): {}".format(sensor.gyro))
    #print("Euler angle: {}".format(sensor.euler))
    #print("Quaternion: {}\n".format(sensor.quaternion))
    while not sensor.euler[0]:
        pass
    print(sensor.euler)
    time.sleep(0.5)