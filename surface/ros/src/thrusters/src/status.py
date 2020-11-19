#!/usr/bin/env python3

import json
import sys

#ROS
import rospy
from shared_msgs.msg import final_thrust_msg
from std_msgs.msg import String

thrust = [0, 0, 0, 0, 0, 0, 0, 0]

def _thuster(comm):
    global thrust
    thrust[0] = comm.hfl
    thrust[1] = comm.hfr
    thrust[2] = comm.hbr
    thrust[3] = comm.hbl
    thrust[4] = comm.vfl
    thrust[5] = comm.vfr
    thrust[6] = comm.vbr
    thrust[7] = comm.vbl

    print(json.dumps(thrust))
  
if __name__ == '__main__':
    rospy.init_node('thrusters_surface')
    stat = rospy.Subscriber('/rov/final_thrust', final_thrust_msg, _thuster)  
    
    while not rospy.is_shutdown():
        rospy.spin()