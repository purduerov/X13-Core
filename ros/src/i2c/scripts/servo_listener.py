#! /usr/bin/env python3

import rospy
from std_msgs.msg import Float32
import RPi.GPIO as GPIO #imports the standard Raspberry Pi GPIO library
import time
from time import sleep #imports sleep (aka waiting or pause) into the program

#Setting a Pin Mode
GPIO.setmode(GPIO.BCM) #Chose Board pin number scheme
#Set up pin 11 for PWM
GPIO.setup(33, GPIO.OUT) #sets up pin 11 to an output
p = GPIO.PWM(33,50) #sets up pin 11 as a PWM pin(50 is the frequency)
p.start(0) #starts running PWM on the pin and sets it to 0. 0 is the middle, 
duty_prev = 7.5 #in the middle

def callback(requestedAngle):
    #change the angle to desired duty cycle
    duty = ((requestedAngle.data / 180) + 1 ) / 0.2 #((Angle you want / 180) + 1 for the period offset) / 2 for the total period))
    global duty_prev

    if (duty != duty_prev):
        try:
            print(f"Duty: {duty}")
            print(f"Duty Prev: {duty_prev}")
            duty_prev = duty
            p.ChangeDutyCycle(duty)
            time.sleep(1)
        except:
            print("there has been some error of some type :/")

def listener():
    rospy.init_node('test_servo_listener_node', anonymous=True)
    rospy.Subscriber("test_servor_angle", Float32, callback)
    rospy.spin() #keeps python from exiting until this node is stopped 

if __name__ == '__main__':
    #subscribe to the can hardware transmitter
    listener()

