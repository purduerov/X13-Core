#!/usr/bin/env python3 

import rospy 
from std_msgs.msg import Float32, String
import json

angle = 30.0

def servo_sender(): 
    rospy.init_node('servo_sender')
    pub = rospy.Publisher('servo', Float32, queue_size=10)
    rate = rospy.Rate(1)

    while not rospy.is_shutdown():
        newVal = float(input('val').rstrip())
        angle = newVal
        pub.publish(json.dumps(angle))
        print(angle)
        rate.sleep()

if __name__ == '__main__':
    try:
        servo_sender()
    except rospy.ROSInterruptException:
        pass