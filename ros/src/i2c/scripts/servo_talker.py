#! /usr/bin/env python3

import rospy
import time
from std_msgs.msg import Float32
#from shared_msgs.msg import servo_msg

def talker():
    rospy.init_node('servo_debug_talker_node', anonymous=True)
    pub = rospy.Publisher('servo', Float32, queue_size=10)
    rate = rospy.Rate(10) #10Hz
    i = 0
        
    while not rospy.is_shutdown():
        
        #servoCam = servo_msg()
        servoCam = float(input("Insert desired angle: "))
        #servoCam.servo_lock_status = False #might have to be false
        #servoCam.header.stamp = rospy.Time.now() #also might have to include
        #servoCam.header.frame_id = "/ServoTest" #might have to include

        pub.publish(servoCam)        

        #if i%2 == 0:
        #    angle = 0.0
        #    print(angle)
        #    pub.publish(angle)
        #else:
        #    angle = 180.0
        #    print(angle)
        #    pub.publish(angle)
        #i += 1

        #time.sleep(4)

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
