#! /usr/bin/python3
import rospy
from shared_msgs.msg import can_msg, tools_command_msg

TOOLS_BOARD_ID = 0x204

PM_BIT = 0b00001000
#MANIPULATOR_CLOSE_BIT = 0b0000000
GHOST_BIT = 0b00100000
BS_BIT = 0b00000010

changed = False
pseudo_lock = False
#8'bdd654321

pub = None
sub = None


def message_received(msg):
    # data_list = [0] * 8
    pm = (msg.pm * PM_BIT)
    gt = (msg.ghost * GHOST_BIT)
    bs = (msg.bs * BS_BIT)
    cmd = pm | gt | bs
    # If we're doing this, we're getting rid of the rate
    # Pilots likely have a hard time beating 5 to 10 Hz...
    # We'll deal with spamming later
    cmsg = can_msg()
    cmsg.id = TOOLS_BOARD_ID
    cmsg.data = cmd
    pub.publish(cmsg)
    # if cmsg_pm.data != pm:
    #     cmsg_pm.data = pm
    #     pub.publish(cmsg_pm)

    # if cmsg_gt.data != gt:
    #     cmsg_gt.data = gt
    #     pub.publish(cmsg_gt)

    # if cmsg_lb.data != lb:
    #     cmsg_lb.data = lb
    #     pub.publish(cmsg_lb)

    # if cmsg_mk.data != mk:
    #     cmsg_mk.data = mk
    #     pub.publish(cmsg_mk)

    # data_list[-1] = data_list[-1] | (msg.manipulator * PM_BIT)
    # data_list[-1] = data_list[-1] | ((not msg.manipulator) * MANIPULATOR_CLOSE_BIT)
    # data_list[-1] = data_list[-1] | (msg.groutTrout * GHOST_BIT)
    # data_list[-1] = data_list[-1] | ((not msg.groutTrout) * GROUT_TROUT_CLOSE_BIT)
    # data_list[-1] = data_list[-1] | (msg.liftBag * LIFT_BAG_OPEN_BIT)
    # data_list[-1] = data_list[-1] | ((not msg.liftBag) * LIFT_BAG_CLOSE_BIT)
    # data_list[-1] = data_list[-1] | (msg.marker * MARKER_OPEN_BIT)
    # data_list[-1] = data_list[-1] | ((not msg.marker) * MARKER_CLOSE_BIT)
    # data = bytearray(data_list)

    # print data_list

    # cmsg.data = data_list[-1]


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
