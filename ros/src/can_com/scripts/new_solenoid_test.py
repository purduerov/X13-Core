#! /usr/bin/python3
import rospy
from shared_msgs.msg import can_msg

sol0 = 1 << 1
sol1 = 1 << 3 
sol2 = 1 << 5

BS_BIT = sol0
PM_BIT = sol1
GHOST_BIT = sol2

pub = None
sub = None

def test_sender(count):
    if(count & 1):
        pm = PM_BIT
    if(count & 2):
        gt = GHOST_BIT
    if(count & 4):
        bs = BS_BIT
    cmd = pm | gt | bs

    cmsg = can_msg()
    cmsg.id = TOOLS_BOARD_ID
    cmsg.data = cmd
    pub.publish(cmsg)

if __name__ == "__main__":
    rospy.init_node('tool_proc', anonymous=True)

    # Publish to the CAN hardware transmitter
    pub = rospy.Publisher('can_tx', can_msg,
                          queue_size=10)

    rate = rospy.Rate(1) # 5hz

    count = 1
    while not rospy.is_shutdown():
        rate.sleep()
        test_sender()
        count = (count << 1)
        if(count == 8):
            count = 1
