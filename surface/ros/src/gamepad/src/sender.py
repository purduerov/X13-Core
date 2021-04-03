#!/usr/bin/env python3

from inputs import get_gamepad
import json
import sys

#ROS
import rospy
from std_msgs.msg import String
from std_msgs.msg import Bool
from shared_msgs.msg import rov_velocity_command
from geometry_msgs.msg import Twist

from config import *

pm_toggle = False
gh_toggle = False

def getMessage():
    global gamepad_state

    t = Twist()

    t.linear.x = gamepad_state['LSY'] * SCALE_TRANSLATIONAL
    t.linear.y = gamepad_state['LSX'] * SCALE_TRANSLATIONAL * SCALE_TRANSLATIONAL_MAGIC
    t.linear.z = (gamepad_state['RT'] - gamepad_state['LT']) * SCALE_TRANSLATIONAL

    if gamepad_state['LB'] == 1:
        x = 1 * SCALE_ROTATIONAL
    elif gamepad_state['RB'] == 1:
        x = -1 * SCALE_ROTATIONAL
    else:
        x = 0.0

    t.angular.x = x
    t.angular.y = gamepad_state['RSY'] * SCALE_ROTATIONAL
    t.angular.z = -gamepad_state['RSX'] * SCALE_ROTATIONAL

    return rov_velocity_command(t, 'gamepad', False, False)

def getPMState():
    global pm_toggle

    return Bool(pm_toggle)

def getGHState():
    global gh_toggle

    return Bool(gh_toggle)

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
    global pm_toggle, gh_toggle

    if event.ev_type in ignore_events:
        return

    if event.ev_type == EVENT_KEY:
        gamepad_state[EVENTS[event.code]] = event.state
        if event.code == 'BTN_SOUTH' and event.state:
            pm_toggle = not pm_toggle

        if event.code == 'BTN_EAST' and event.state:
            gh_toggle = not gh_toggle

    elif event.ev_type == EVENT_ABSOLUTE:
        gamepad_state[EVENTS[event.code]] = correct_raw(event.state, EVENTS[event.code])
    else:
        gamepad_state[EVENTS[event.code]] = event.state

def pub_data(event):

    pub.publish(getMessage())
    pub_pm.publish(getPMState())
    pub_gh.publish(getGHState())

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
    global pub, pub_pm, pub_gh

    try:
        get_gamepad()
    except:
        sys.exit(json.dumps({'gamepad': False}))

    pub = rospy.Publisher('rov_velocity', rov_velocity_command, queue_size=10)
    pub_pm = rospy.Publisher('pm_cmd', Bool, queue_size=10)
    pub_gh = rospy.Publisher('gh_cmd', Bool, queue_size=10)

    try:
        talker()
    except rospy.ROSInterruptException:
        pass
