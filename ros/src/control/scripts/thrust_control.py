#! /usr/bin/python3
import rospy
from shared_msgs.msg import auto_control_msg, final_thrust_msg, thrust_status_msg, thrust_command_msg, controller_msg, com_msg
from sensor_msgs.msg import Imu
from std_msgs.msg import Float32, String
import numpy as np
import Complex_1
from thrust_mapping_dev import ThrustMapper
import json
from dynamic_reconfigure.server import Server
from control.cfg import ROV_COMConfig

desired_p = [0.0,0.0,0.0,0.0,0.0,0.0]
desired_thrusters = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0,0.0,0.0]
desired_p_unramped = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
locked_dims_list = [False, False, False, False, False, False]
disabled_list = [False, False, False, False, False, False, False, False]
inverted_list = [0, 0, 0, 0, 0, 0, 0, 0]
desired_thrust_final = [0, 0, 0, 0, 0, 0]
MAX_CHANGE = .15
mode_fine = True
fine_multiplier = 1.041
tm = ThrustMapper()
# watch dog stuff
last_packet_time = 0.0
is_timed_out = False
# timout in ms
WATCHDOG_TIMEOUT = 10


def _pilot_command(comm):
    global desired_p  # desired thrust from pilot
    global disabled_list  # disabled thrusters
    global inverted_list  # inverted thrusters
    global desired_p_unramped
    global tm
    #print (comm.desired_thrust)
    desired_p = comm.desired_thrust
    tm.set_multiplier(comm.multiplier)
    tm.set_fine(comm.isFine)
    # disabled_list = comm.disable_thrusters
    # inverted_list = comm.inverted
    on_loop()


def ramp(index):
    if (abs(desired_p_unramped[index] - desired_thrusters[index]) > MAX_CHANGE):
        if (desired_p_unramped[index] - desired_thrusters[index] > 0):
            desired_thrusters[index] += MAX_CHANGE
            #print(index, "ramping", desired_thrusters[index])
        else:
            desired_thrusters[index] -= MAX_CHANGE
        return
    else:
        desired_thrusters[index] = desired_p_unramped[index]
def _updateRamp(msg):
    stuff = json.loads(msg.data)
    MAX_CHANGE = stuff['ramp']
    print(MAX_CHANGE)

def on_loop():
    global new_auto_data
    global is_timed_out
    global last_packet_time
    global desired_thrusters
    global desired_p_unramped
    for i in range(0, 6):
        desired_thrust_final[i] = desired_p[i]

    # calculate thrust
    #pwm_values = c.calculate(desired_thrust_final, disabled_list, False)
    desired_p_unramped = [tm.thrust_to_pwm(val) for val in tm.thruster_output(desired_p)]
    # invert relevant values
    #for i in range(8):
    #    if inverted_list[i] == 1:
    #        pwm_values[i] = pwm_values[i] * (-1)
    for i in range(0,8):
        ramp(i)
    pwm_values = desired_thrusters
    
    # assign values to publisher messages for thurst control and status
    tcm = final_thrust_msg()
    # val = float of range(-1, 1)
    # if int8: (val * 127.5) - 0.5 will give range -128 to 127
    # if uint8: (val + 1) * 127.5 will give 0 to 255
    thrusters = [127,127,127,127,127,127,127,127]
    for i in range(0,8):
        thrusters[i] = int((pwm_values[i] + 1) * 127.5)
    tcm.thrusters = thrusters

    tsm = thrust_status_msg()
    tsm.status = pwm_values
    
    # publish data
    thrust_pub.publish(tcm)
    status_pub.publish(tsm)
def updateCOM(config, level):
    rospy.loginfo("""Reconfigure Request: {ROV_X}, {ROV_Y}, {ROV_Z}""".format(**config))
    return config
def _comUpdate(msg):
    tm.location = tm.change_origin(msg.com[0],msg.com[1],msg.com[2])
    tm.torque = tm.torque_values()
    tm.thruster_force_map = tm.thruster_force_map_values()
    rospy.loginfo("changed" + str(msg.com[0]) + ":" + str(msg.com[1]) + ":" + str(msg.com[2]))

if __name__ == "__main__":
    '''
    Note that this file is only set up for using 8 thrusters.
    '''

    # initialize node and rate
    rospy.init_node('thrust_control')
    srv = Server(ROV_COMConfig, updateCOM)
    rate = rospy.Rate(25)  # 20 hz

    # initialize subscribers
    comm_sub = rospy.Subscriber('/thrust_command', thrust_command_msg, _pilot_command)
    com_sub = rospy.Subscriber('com_tweak', com_msg, _comUpdate)

    # initialize publishers
    thrust_pub = rospy.Publisher('final_thrust', final_thrust_msg, queue_size=10)
    status_pub = rospy.Publisher('thrust_status', thrust_status_msg, queue_size=10)

    # define variable for class Complex to allow calculation of thruster pwm values
    c = Complex_1.Complex()
   
    

    while not rospy.is_shutdown():
        rospy.spin()

