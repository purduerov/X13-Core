# ROS Imports

import rospy
from std_msgs.msg import String
from std_msgs.msg import Bool
# fix shared msgs problem by doing catkin make
from shared_msgs.msg import rov_velocity_command
from geometry_msgs.msg import Twist

# CV Imports

import cv2
import numpy as np
import helperFunctions as hp
from datetime import datetime


class TransectStream:
    def __init__(self, camera_feed, max_consecutive_losing_frames = 24):
        self.camfeed = camera_feed
        self.cap = cv2.VideoCapture(self.camfeed)
        self.losing_frames = 0
        self.losses = 0
        self.max_losing_frames = max_consecutive_losing_frames
        # Keep last twist just in case one cannot be obtained from new frames.
        self.last_good_twist = None

    def update(self, test=False):
        """ Updates the feed.

        Updates the camera feed. Set test to true
        """
        ret, frame = self.cap.read()
        if ret:
            hframe = frame.copy()
            output = hp.apply_hough_transform(hframe, None, threshold=100, show_all=True, debug=False)
            if (test):

                cv2.imshow("Frame", frame)
                cv2.imshow("Analysis Frame", hframe)
                cv2.waitKey()

            if output is not None and len(output['big_lines']) is not 2:
                self.losing_frames += 1
            else:
                self.losing_frames = 0
                twist = Twist()
                twist_info = output['twist_info']
                twist.linear.x = twist_info['translation']['x']
                twist.linear.y = twist_info['translation']['y']
                twist.linear.z = twist_info['translation']['z']

                twist.angular.x = twist_info['rotation']['pitch']
                twist.angular.y = twist_info['rotation']['yaw']
                twist.angular.z = twist_info['rotation']['roll']
                self.last_good_twist = twist
            if self.losing_frames == self.max_losing_frames:
                self.losses += 1

            if self.losses == 1:
                print(f"Task failed. Showing {len(output['big_lines'])} pipe(s) over {self.losing_frames} frames.")
            return
        return

    def get_message(self):
        return self.last_good_twist
        # return rov_velocity_command(self.last_good_twist, 'transect', False, False)

def print_twist(twist):
    print(f"Linear: ({twist.linear.x}, {twist.linear.y}, {twist.linear.z}), " +
          f"Angular: ({twist.angular.x}, {twist.angular.y}, {twist.angular.z})")


def test():
    print("Running...")
    print("Press p to pause. Press q to exit.")

    stream = TransectStream("http://192.168.1.4:8090/cam0")

    while True:
        stream.update()
        if (stream.get_message() is not None):
            print_twist(stream.get_message())