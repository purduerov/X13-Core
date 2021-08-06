#! /usr/bin/env python3

#Notes:
#This scripts takes an input of 0-180 degrees from the test servo publisher node
# It uses a math equation to translate this value into a number with a range of 1-12
#The servo specifications indicate a duty cycle of 1-2ms with a total period of 20ms. This would indicate a duty cycle from 5-10 percentage wise.
#However for some reason testing hardcoded values found that it takes 1-12 percent for a full range of 180 degree motion for some reason
#that's not mathmatically correct but it works so eh
#duty cycle(6) for in the middle. duty cycle(0) is off
#for this inclosure the input can be 12 to 120 degrees. the code will automatically make these the max values

import rospy
from std_msgs.msg import Float32
import RPi.GPIO as GPIO #imports the standard Raspberry Pi GPIO library
import time
from time import sleep #imports sleep (aka waiting or pause) into the program

#Setting a Pin Mode
GPIO.setmode(GPIO.BCM) #Chose Board pin number scheme
#Set up pin 14 for PWM
GPIO.setup(13, GPIO.OUT) #sets up pin 13 to an output
p = GPIO.PWM(13,50) #sets up pin 13 as a PWM pin(50 is the frequency)
p.start(0) #starts running PWM on the pin and sets it to 0. 0 is the middle
duty_prev = 5.8 #sets to middle duty cycle this is the "middle"
p.ChangeDutyCycle(duty_prev)
sleep(0.04) #max time delay
p.ChangeDutyCycle(0)

def callback(requestedAngle):
    global duty_prev
    rate = rospy.Rate(100)  
    #change the angle to desired duty cycle
    duty = requestedAngle # Just make sure on frontend the requested angle is a number from 2 to 8
    #((requestedAngle.data /180) * 11) + 1 #the range of the servo is dutycycle of 1-12 for some reason. So this formula should take in angle of 0-180 and transfer the value from 1-12
    #caps the duty cycle to the max angle values
    if duty > 8.02:
       duty = 8.02
    elif duty < 2.02:
       duty = 2.02
    

    dutyDiff = abs(duty_prev - duty)
    timeToWait = (12.5*(dutyDiff**0.515)+10)/1000

    #only run if new number
    if (duty != duty_prev):
        try:
            print(f"Current Duty: {duty:.4f}")
            print(f"Prev Duty: {duty_prev:.4f}")
            print(f"Duty Diff = {dutyDiff:.6f} and timeToWait = {timeToWait:.6f}\n")
            #Debug code for testing a varity of values to test full range of motion
            #it = [8.02, 2.02, 8.02, 6.5, 7.5, 6.5, 6.6, 6.5, 2.02]  #OKAY so for some reason a duty cycle of 1-12 is used to get a full 180 degrees of rotation. even tho that data sheet indicats 5-10
            #for i in it:
            #   print(f"Current Duty Cycle: {i}")
            #   p.ChangeDutyCycle(i)
            #   time.sleep(2.0)
            #print("finished diognostic")
            p.ChangeDutyCycle(duty)
            duty_prev = duty
        except:
            print("there has been some error of some type :/")
    sleep(timeToWait) #this is so the servo pauses before turning off the power
    # p.ChangeDutyCycle(0) #if the servo jitters a lot uncomment this it should stop all movement in between calls
    

def listener():
    rospy.init_node('servo_listener_node', anonymous=True)
    rospy.Subscriber("servo", Float32, callback)
    #rospy.Subscriber("test_servor_angle", Float32, callback)
    rospy.spin() #keeps python from exiting until this node is stopped 

if __name__ == '__main__':
    #subscribe to the can hardware transmitter
    listener()

