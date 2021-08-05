#!/usr/bin/env python3

from inputs import get_gamepad
import json
import sys

#ROS
import rospy
from std_msgs.msg import String, Bool, Empty
from shared_msgs.msg import rov_velocity_command
from geometry_msgs.msg import Twist
import socket, threading
import signal, os

from config import *

pm_toggle = False
gh_toggle = False
bs_toggle = False

SCALE_TRANSLATIONAL_X = 1.0
SCALE_TRANSLATIONAL_Y = 1.0
SCALE_TRANSLATIONAL_Z = 1.0

SCALE_ROTATIONAL_X = 1.0
SCALE_ROTATIONAL_Y = 1.0
SCALE_ROTATIONAL_Z = 1.0

TRIM_X = 0.0
TRIM_Y = 0.0
TRIM_Z = 0.0

class SocketManager:
    def __init__(self):
        self.running = True
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('127.0.0.1', 11001))
        self.sock.listen(5)
        self.sock.settimeout(1)
        self.connected = False

        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def shutdown(self):
        self.running = False
        self.sock.close()
        self.thread.join()

    def run(self):
        global SCALE_ROTATIONAL_X, SCALE_ROTATIONAL_Y, SCALE_ROTATIONAL_Z, SCALE_TRANSLATIONAL_X, SCALE_TRANSLATIONAL_Y, SCALE_TRANSLATIONAL_Z
        global TRIM_X, TRIM_Y, TRIM_Z

        while not self.connected and self.running:
            try:
                conn, addr = self.sock.accept()
                self.connected = True
            except:
                pass
        while self.running:
            try:
                data = conn.recv(1024)
            except:
                pass
            if data:
                decoded = data.decode()
                mode = decoded.split(':')[0]
                arr = [float(d) for d in decoded.split(':')[1].split(',')]

                if mode == 'scale':
                    SCALE_TRANSLATIONAL_X = arr[0]
                    SCALE_TRANSLATIONAL_Y = arr[1]
                    SCALE_TRANSLATIONAL_Z = arr[2]

                    SCALE_ROTATIONAL_X = arr[3]
                    SCALE_ROTATIONAL_Y = arr[4]
                    SCALE_ROTATIONAL_Z = arr[5]
                elif mode == 'trim':
                    TRIM_X = arr[0]
                    TRIM_Y = arr[1]
                    TRIM_Z = arr[2]

def getMessage():
    global gamepad_state

    t = Twist()

    t.linear.x = gamepad_state['LSY'] * SCALE_TRANSLATIONAL_X + TRIM_X
    t.linear.y = gamepad_state['LSX'] * SCALE_TRANSLATIONAL_Y + TRIM_Y
    t.linear.z = (gamepad_state['RT'] - gamepad_state['LT']) * SCALE_TRANSLATIONAL_Z + TRIM_Z

    if gamepad_state['LB'] == 1:
        x = 1 * SCALE_ROTATIONAL_X
    elif gamepad_state['RB'] == 1:
        x = -1 * SCALE_ROTATIONAL_X
    else:
        x = 0.0

    t.angular.x = x
    t.angular.y = gamepad_state['RSY'] * SCALE_ROTATIONAL_Y
    t.angular.z = -gamepad_state['RSX'] * SCALE_ROTATIONAL_Z

    return rov_velocity_command(t, 'gamepad', False, False)

def getPMState():
    global pm_toggle

    return Bool(pm_toggle)

def getBSState():
    global bs_toggle

    return Bool(bs_toggle)

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
    global pm_toggle, gh_toggle, bs_toggle

    if event.ev_type in ignore_events:
        return

    if event.ev_type == EVENT_KEY:
        gamepad_state[EVENTS[event.code]] = event.state
        if event.code == 'BTN_SOUTH' and event.state:
            pm_toggle = not pm_toggle

        if event.code == 'BTN_EAST' and event.state:
            gh_toggle = not gh_toggle

        if event.code == 'BTN_WEST' and event.state:
            bs_toggle = not bs_toggle

    elif event.ev_type == EVENT_ABSOLUTE:
        gamepad_state[EVENTS[event.code]] = correct_raw(event.state, EVENTS[event.code])
    else:
        gamepad_state[EVENTS[event.code]] = event.state

def pub_data(event):
    pub.publish(getMessage())
    pub_pm.publish(getPMState())
    pub_gh.publish(getGHState())
    pub_bs.publish(getBSState())

def update_gamepad(event):
    try:
        event = get_gamepad()[0]
        process_event(event)
    except Exception:
        rospy.signal_shutdown('no gamepad')

def shutdown(sig, frame):
    global data_thread, gamepad_thread, sock_thread
    print('shutting down')
    data_thread.shutdown()
    gamepad_thread.shutdown()
    sock_thread.shutdown()
    rospy.signal_shutdown('now')

if __name__ == '__main__':
    global pub, pub_pm, pub_gh, data_thread, gamepad_thread, sock_thread

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    try:
        get_gamepad()
    except:
        sys.exit(0)

    sock_thread = SocketManager()
    
    rospy.init_node('gp_pub', anonymous=True, disable_signals=True)

    pub = rospy.Publisher('rov_velocity', rov_velocity_command, queue_size=10)
    pub_pm = rospy.Publisher('pm_cmd', Bool, queue_size=10)
    pub_gh = rospy.Publisher('gh_cmd', Bool, queue_size=10)
    pub_bs = rospy.Publisher('bs_cmd', Bool, queue_size=10)


    data_thread = rospy.Timer(rospy.Duration(0.1), pub_data)
    gamepad_thread = rospy.Timer(rospy.Duration(0.001), update_gamepad)

    print('ready')

    rospy.spin()

    data_thread.shutdown()
    gamepad_thread.shutdown()
    sock_thread.shutdown()