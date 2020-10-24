#!/usr/bin/env python3

from inputs import get_gamepad
import json
import sys

#ROS
import rospy
from std_msgs.msg import String

from config import *

def correct_raw(raw, abbv):
    sign = (raw >= 0) * 2 - 1
    raw = abs(raw)

    if abbv[1] == 'T':
        dead_zone = TRIGGER_DEAD_ZONE
        value_range = TRIGGER_RANGE
    else:
        dead_zone = STICK_DEAD_ZONE
        value_range = STICK_RANGE

    if raw < dead_zone:
        return 0.0

    raw -= dead_zone
    raw *= value_range / (value_range - dead_zone)
    raw = 1.0 if raw > value_range else raw / value_range
    corrected = round(raw, 3)
    corrected *= sign
    return corrected

def process_event(event):
    
    if event.ev_type in ignore_events:
        return

    if event.ev_type == EVENT_KEY:
        gamepad_state[EVENTS[event.code]] = event.state
    elif event.ev_type == EVENT_ABSOLUTE:
        gamepad_state[EVENTS[event.code]] = correct_raw(event.state, EVENTS[event.code])
    else:
        gamepad_state[EVENTS[event.code]] = event.state

def pub_data(event):
    #rospy.loginfo(gamepad_state)
    print(json.dumps(gamepad_state)) #Proper formatting for stdout
    pub.publish(json.dumps(gamepad_state))

def update_gamepad(event):
    try:
        event = get_gamepad()[0]
        process_event(event)
    except:
        rospy.signal_shutdown('no gamepad')

def talker():
    rospy.init_node('gp_pub', anonymous=True)

    rospy.Timer(rospy.Duration(0.1), pub_data)
    rospy.Timer(rospy.Duration(0.001), update_gamepad)

    rospy.spin()
  
if __name__ == '__main__':
    global pub

    try:
        get_gamepad()
    except:
        sys.exit(json.dumps({'gamepad': False}))

    pub = rospy.Publisher('chatter', String, queue_size=10)
    try:
        talker()
    except rospy.ROSInterruptException:
        pass