#!/usr/bin/env python3

import json
import sys

#ROS
import rospy
from shared_msgs.msg import imu_msg
from std_msgs.msg import String

imu = [0, 0, 0]

def _imu(comm):
    global imu
    imu[0] = comm.gyro[0] / 90
    imu[1] = (abs(comm.gyro[1]) - 180) / 180
    imu[2] = comm.gyro[2] / 90

    print(json.dumps(imu))

if __name__ == '__main__':
    rospy.init_node('imu_surface')
    stat = rospy.Subscriber('/rov/imu', imu_msg, _imu)

    while not rospy.is_shutdown():
        rospy.spin()
