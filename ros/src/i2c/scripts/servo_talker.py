#! /usr/bin/env python3

import rospy
import time
from std_msgs.msg import Float32

def talker():
    rospy.init_node('test_servo_talker_node', anonymous=True)
    pub = rospy.Publisher('test_servor_angle', Float32, queue_size=10)
    rate = rospy.Rate(0.1)
    i = 0
    while not rospy.is_shutdown():
        if i%2 == 0:
            angle = 0.0
            print(angle)
            pub.publish(angle)
        else:
            angle = 180.0
            print(angle)
            pub.publish(angle)
        i += 1

        time.sleep(4)

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
