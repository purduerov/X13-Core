#!/usr/bin/env python3

import json
#ROS
import rospy
from shared_msgs.msg import final_thrust_msg

thrust = [0, 0, 0, 0, 0, 0, 0, 0]

def _thuster(comm):
    global thrust
    thrust[0] = int(comm.thrusters[0])
    thrust[1] = int(comm.thrusters[1])
    thrust[2] = int(comm.thrusters[2])
    thrust[3] = int(comm.thrusters[3])
    thrust[4] = int(comm.thrusters[4])
    thrust[5] = int(comm.thrusters[5])
    thrust[6] = int(comm.thrusters[6])
    thrust[7] = int(comm.thrusters[7])

    print(json.dumps(thrust))

if __name__ == '__main__':
    rospy.init_node('thrusters_surface')
    stat = rospy.Subscriber('/rov/final_thrust', final_thrust_msg, _thuster)

    while not rospy.is_shutdown():
        rospy.spin()
