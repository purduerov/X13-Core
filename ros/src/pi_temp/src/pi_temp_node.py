#!/usr/bin/env python

# license removed for brevity
import rospy
from gpiozero import CPUTemperature
from std_msgs.msg import String
from std_msgs.msg import Float64

def talker():
    
    #get the cpu temperature of the pi
    cpu = CPUTemperature()
    pub = rospy.Publisher(cpu.temperature, Float64, queue_size=10)
    rospy.init_node('Pi_CPU_TEMP', anonymous=True)
    rate = rospy.Rate(1) # 10hz
    
    while not rospy.is_shutdown():
        hello_str = "hello world %s" % rospy.get_time()
        rospy.loginfo(hello_str)
        pub.publish(hello_str)
        rate.sleep()
   
if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
