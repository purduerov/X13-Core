#! /usr/bin/python3
import rospy
import time
from std_msgs.msg import Float32
from shared_msgs.msg import servo_msg

def talker():
    rospy.init_node('other_talker', anonymous=True)
    pub = rospy.Publisher('ServoAngles', servo_msg, queue_size=10)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        servoCam = servo_msg()
        servoCam.angle = float(input("Insert desired angle: "))
        servoCam.servo_lock_status = False
        servoCam.header.stamp = rospy.Time.now()
        servoCam.header.frame_id = "/ServoTest"
        
        print(servoCam)
        rospy.loginfo(servoCam)
        pub.publish(servoCam)
        rate.sleep()   

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
