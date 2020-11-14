#!/usr/bin/env python3

import json
import sys

#ROS
import rospy
from shared_msgs.msg import thrust_status_msg
from std_msgs.msg import String

thrust = []

def _thuster(comm):
    global thrust

    thrust = comm.status
  
if __name__ == '__main__':
    rospy.init_node('thrusters_surface')
    rate = rospy.Rate(50)

    stat = rospy.Subscriber('/thrust_status', thrust_status_msg, _thuster)
    
    while not rospy.is_shutdown():   
        print(json.dumps(thrust))
        rate.sleep()