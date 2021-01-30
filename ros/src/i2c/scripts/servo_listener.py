#! /usr/bin/env python3

import rospy
from std_msgs.msg import Float32
import RPi.GPIO as GPIO #imports the standard Raspberry Pi GPIO library
import time
from time import sleep #imports sleep (aka waiting or pause) into the program

#Setting a Pin Mode
GPIO.setmode(GPIO.BCM) #Chose Board pin number scheme
#Set up pin 14 for PWM
GPIO.setup(14, GPIO.OUT) #sets up pin 14 to an output
p = GPIO.PWM(14,50) #sets up pin 11 as a PWM pin(50 is the frequency)
p.start(0) #starts running PWM on the pin and sets it to 0. 0 is the middle, 
duty_prev = 7 #duty cycle for in the middle duty cycle of 0 is off effectivly

def callback(requestedAngle):
    rate = rospy.Rate(100)  
    #change the angle to desired duty cycle
    duty = ((requestedAngle.data /180) * 10) + 2 #the range of the servo is dutycycle of 2-12 for some reason. So this formula should take in angle of 0-180 and transfer the value from 2-12
    global duty_prev
    if (duty != duty_prev):
        try:
            
            print(f"Current Duty: {duty}")
            print(f"Prev Duty: {duty_prev} \n")
            #Debug code for testing a varity of values to test full range of motion
            #it = [12.4, 12, 1.8, 2]   #OKAY so for some reason a duty cycle of 2-12 is used to get a full 180  degrees of rotation. even tho that data sheet says 5-10
            #for i in it:
            #   print(f"Current Duty Cycle: {i}")
            #   p.ChangeDutyCycle(i)
            #   time.sleep(2.5)
            #print("finished diognostic")

            p.ChangeDutyCycle(duty)
            duty_prev = duty
        except:
            print("there has been some error of some type :/")
    #p.ChangeDutyCycle(0) #if the servo jitters a lot uncomment this it should stop all movement in between calls
    rate.sleep() #waits 0.01 seconds

def listener():
    rospy.init_node('test_servo_listener_node', anonymous=True)
    rospy.Subscriber("test_servor_angle", Float32, callback)
    rospy.spin() #keeps python from exiting until this node is stopped 

if __name__ == '__main__':
    #subscribe to the can hardware transmitter
    listener()

