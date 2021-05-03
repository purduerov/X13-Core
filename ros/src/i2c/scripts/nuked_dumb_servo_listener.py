#! /usr/bin/env python3

#Mom use this

#set servo angle to certain value and test to see if imu works with moving angle
#then test without imu to see if actual servo has basic functionality
#then test with imu enabled to see servo will actually move with it
#then hook up to front end and see what clicking lock and unlock mid difference does


#Notes:
#This scripts takes an input of 0-180 degrees from the test servo publisher node
# It uses a math equation to translate this value into a number with a range of 1-12
#The servo specifications indicate a duty cycle of 1-2ms with a total period of 20ms. This would indicate a duty cycle from 5-10 percentage wise.
#However for some reason testing hardcoded values found that it takes 1-12 value for a full range of 180 degree motion for some reason
#that's not mathmatically correct but it works so eh
#duty cycle(6) for in the middle. duty cycle(0) is off
#for this inclosure the input can be 12 to 120 degrees. the code will automatically make these the max values


#import statements
import RPi.GPIO as GPIO #imports the standard Raspberry Pi GPIO library
import rospy
from time import sleep #imports sleep (aka waiting or pause) into the program
from shared_msgs.msg import servo_msg

MAX_ANGLE = 98
MIN_ANGLE = 20

#Coverts angle to duty cycle, need to update values here
def angleToDuty(angle): 
    duty = ((angle /180) * 11) + 1 #converts to duty cycle
    return duty

#initialization
GPIO.setmode(GPIO.BCM) #Setting a Pin Mode aka Chose Board pin number scheme
#Set up pin 14 for PWM
GPIO.setup(13, GPIO.OUT) #sets up pin 13 to an output
p = GPIO.PWM(13,50) #sets up pin 13 as a PWM pin(50 is the frequency)
p.start(0) #starts running PWM on the pin and sets it to 0. 0 is the middle
angle_prev = 45 #sets to middle angle
duty_prev = angleToDuty(angle_prev)
p.ChangeDutyCycle(duty_prev)
sleep(0.04) #max time delay
p.ChangeDutyCycle(0)

def callback(servoStuff):    
    #print(imuStuff)
    global angle_prev
    global duty_prev

    adjustedAngle = servoStuff.angle
    if adjustedAngle > MAX_ANGLE:
        adjustedAngle = MAX_ANGLE
    elif adjustedAngle < MIN_ANGLE:
        adjustedAngle = MIN_ANGLE
    
    if (adjustedAngle != angle_prev):
        adjustedDuty = angleToDuty(adjustedAngle)

        dutyDiff = abs(duty_prev - adjustedDuty)
        timeToWait = (12.5*(dutyDiff**0.515)+10)/1000
      
        
        print(f'Old Adjusted angle: {angle_prev}')
        print(f'Old Adjusted duty: {duty_prev}') 
        print(f'Adjusted angle: {adjustedAngle}')
        print(f'Adjusted duty: {adjustedDuty}')
        print("\n") 
        p.ChangeDutyCycle(adjustedDuty)
        duty_prev = adjustedDuty
        angle_prev = adjustedAngle  
        sleep(timeToWait) #this is so the servo pauses before turning off the power
        p.ChangeDutyCycle(0) #if the servo jitters a lot uncomment this it should stop all movement in between calls

def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    print("starting")  

    rospy.Subscriber('ServoAngles', servo_msg, callback)
    rospy.spin() # spin() simply keeps python from exiting until this node is stopped
    
    print("shutting down servo node")


if __name__ == '__main__':
    rospy.init_node('listener', anonymous=True)
    listener()
    
