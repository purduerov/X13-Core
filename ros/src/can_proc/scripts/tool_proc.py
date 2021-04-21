#! /usr/bin/python3
import rospy
from shared_msgs.msg import can_msg, tools_command_msg

TOOLS_BOARD_ID = 0x204

#PM_BIT = 0b00001000
#GHOST_BIT = 0b11110111

#Easier swapping if we plug solenoids in differently
sol0 = 1 << 1
sol1 = 1 << 3 
sol2 = 1 << 4

SECONDARY_BIT = sol0
PM_BIT = sol1
GHOST_BIT = sol2

#8'bdd654321
# ^^^ wtf is this, if no one can tell me it's getting deleted

pub = None
sub = None


def message_received(msg):
    cmd = (msg.pm * PM_BIT)
    cmd |= (msg.ghost * GHOST_BIT)
    cmd |= (msg.secondary * SECONDARY_BIT)
    
    cmsg = can_msg()
    cmsg.id = TOOLS_BOARD_ID
    cmsg.data = cmd
    pub.publish(cmsg)


if __name__ == "__main__":
    rospy.init_node('tool_proc', anonymous=True)

    # Publish to the CAN hardware transmitter
    pub = rospy.Publisher('can_tx', can_msg,
                          queue_size=10)

    sub = rospy.Subscriber('/tools_proc', tools_command_msg,
                           message_received)

    # rate = rospy.Rate(5) # 5hz

    while not rospy.is_shutdown():
        # rate.sleep()
        rospy.spin()
