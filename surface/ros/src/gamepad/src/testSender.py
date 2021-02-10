#!/usr/bin/env python3
import json
import rospy
from std_msgs.msg import String
from shared_msgs.msg import rov_velocity_command
from geometry_msgs.msg import Twist

cmd = rov_velocity_command(Twist(), 'something', False, False)

def pub_data(event):
    pub.publish(cmd)

def talker():
    rospy.Timer(rospy.Duration(0.1), pub_data)

    rospy.spin()

if __name__ == '__main__':
    global pub

    pub = rospy.Publisher('chatter', rov_velocity_command, queue_size=10)
    rospy.init_node('test_pub', anonymous=True)

    try:
        talker()
    except rospy.ROSInterruptException:
        pass
