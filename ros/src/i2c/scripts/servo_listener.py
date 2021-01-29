#! /usr/bin/env python3

import rospy
from std_msgs.msg import Float32
import RPi.GPIO as GPIO #imports the standard Raspberry Pi GPIO library
import time
from time import sleep #imports sleep (aka waiting or pause) into the program

#Setting a Pin Mode
GPIO.setmode(GPIO.BCM) #Chose Board pin number scheme
#Set up pin 11 for PWM
GPIO.setup(14, GPIO.OUT) #sets up pin 14 to an output
p = GPIO.PWM(14,50) #sets up pin 11 as a PWM pin(50 is the frequency)
p.start(0) #starts running PWM on the pin and sets it to 0. 0 is the middle, 
duty_prev = 7.5 #in the middle

def callback(requestedAngle):
    rate = rospy.Rate(100)  
    #change the angle to desired duty cycle
    duty = ((requestedAngle.data / 180) + 1 ) / 0.2 #((Angle you want / 180) + 1 for the period offset) / 2 for the total period))
    global duty_prev

    if (duty != duty_prev):
        try:
            print(f"Current Duty: {duty}")
            print(f"Prev Duty: {duty_prev} \n")
            it = [12.4, 12, 0.8, 1]   #OKAY so for some reason a duty cycle of 1-12 is used to get a full 180  degrees of rotation
            for i in it:
               print(f"Current Duty Cycle: {i}")
               p.ChangeDutyCycle(i)
               time.sleep(2.5)
            print("finished diognostic")
            time.sleep(2.5)
            duty_prev = duty
#            p.ChangeDutyCycle(duty)
        except:
            print("there has been some error of some type :/")
    rate.sleep() #waits 0.01 seconds

def listener():
    rospy.init_node('test_servo_listener_node', anonymous=True)
    rospy.Subscriber("test_servor_angle", Float32, callback)
    rospy.spin() #keeps python from exiting until this node is stopped 

if __name__ == '__main__':
    #subscribe to the can hardware transmitter
    listener()

