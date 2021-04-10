#!/usr/bin/env python3

import json
import sys

#ROS
import rospy
from std_msgs.msg import String

thrust_ramp = {'ramp': 0.001}

def pub_data(event):
    #rospy.loginfo(gamepad_state)
    print(json.dumps(gamepad_state)) #Proper formatting for stdout
    pub.publish(json.dumps(gamepad_state))

def talker():
    print("Waiting")
    newVal = float(input('val').rstrip())

    thrust_ramp['ramp'] = newVal

    pub.publish(json.dumps(thrust_ramp))
    print(thrust_ramp)

if __name__ == '__main__':
    global pub

    rospy.init_node('ramp_pub', anonymous=True)
    pub = rospy.Publisher('ramp', String, queue_size=10)

    r = rospy.Rate(50)
    while not rospy.is_shutdown():
        talker()
        r.sleep()
