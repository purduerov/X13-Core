#! /usr/bin/python3
import rospy
import smbus
import math
import numpy as np
from BNO055 import BNO055
from shared_msgs.msg import imu_msg
from std_msgs.msg import Bool
from geometry_msgs.msg import Pose
import geometry_msgs.msg
from tf.transformations import euler_from_quaternion
import tf2_ros
from pyquaternion import Quaternion

IMU_PITCH_OFFSET = 0.0
IMU_ROLL_OFFSET = 0.0
IMU_YAW_OFFSET = 0.0

def reset_imu_offsets():
    global imu
    global IMU_PITCH_OFFSET
    global IMU_ROLL_OFFSET
    global IMU_YAW_OFFSET
    print ("message recieved")
    IMU_PITCH_OFFSET = imu.pitch()
    IMU_ROLL_OFFSET = imu.roll()
    IMU_YAW_OFFSET = imu.yaw()
    print ("imu_pitch offset" , IMU_PITCH_OFFSET)

#bind all angles to -180 to 180
def clamp_angle_neg180_to_180(angle):
    angle_0_to_360 = clamp_angle_0_to_360(angle)
    if angle_0_to_360 > 180:
        return angle_0_to_360 - 180 * -1.0
    return angle_0_to_360
#bind all angles to -180 to 180
def clamp_angle_0_to_360(angle):
    return (angle + 1 * 360) - math.floor((angle + 2 * 360)/360)*360

def quaternion_multiply(quaternion1, quaternion0):
    w0, x0, y0, z0 = quaternion0
    w1, x1, y1, z1 = quaternion1
    return np.array([-x1*x0 - y1*y0 - z1*z0 + w1*w0,
                     x1*w0 + y1*z0 - z1*y0 + w1*x0,
                    -x1*z0 + y1*w0 + z1*x0 + w1*y0,
                     x1*y0 - y1*x0 + z1*w0 + w1*z0])
def publishTF(self):
    br = tf2_ros.TransformBroadcaster()
    t = geometry_msgs.msg.TransformStamped()
   
    t.header.stamp = rospy.Time.now()
    t.child_frame_id = "imu"
    t.transform.translation.x = 0.0
    t.transform.translation.y = 0.0
    t.transform.translation.z = 0.0
    #q = tf_conversions.transformations.quaternion_from_euler(0, 0, msg.theta)
    t.transform.rotation.x = imu.quat_arr()[0]
    t.transform.rotation.y = imu.quat_arr()[1]
    t.transform.rotation.z = imu.quat_arr()[2]
    t.transform.rotation.w = imu.quat_arr()[3]
   
    br.sendTransform(t)
if __name__ == "__main__":
    global imu
    rospy.init_node('imu_proc')
    imu = BNO055()
    # Publish to the CAN hardware transmitter
    pub = rospy.Publisher('imu', imu_msg,
                          queue_size=1)
    pub2 = rospy.Publisher('imu_quat', Pose,
                          queue_size=1)
    
    tfBuffer = tf2_ros.Buffer()
    listener = tf2_ros.TransformListener(tfBuffer)
    rate = rospy.Rate(10)
    

    #sub = rospy.Subscriber('reset_imu', Bool,
    #                       _reset_imu_offsets)
    
    rate = rospy.Rate(50)  # 10hz
    while not rospy.is_shutdown():
        # try:
        #     trans = tfBuffer.lookup_transform('imu', 'base_link', rospy.Time())
        # except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
        #     rate.sleep()
        #     print("could not find it")
        #     continue
        if imu.update():
            out_message = imu_msg()
            pose_message = Pose()
            
            # br = tf2_ros.TransformBroadcaster()
            # t = geometry_msgs.msg.TransformStamped()
        
            # t.header.stamp = rospy.Time.now()
            # t.header.frame_id = "world"
            # t.child_frame_id = "imu"
            # t.transform.translation.x = 0.0
            # t.transform.translation.y = 0.0
            # t.transform.translation.z = 0.0
            # #q = tf_conversions.transformations.quaternion_from_euler(0, 0, msg.theta)
            # t.transform.rotation.x = imu.quat_arr()[0]
            # t.transform.rotation.y = imu.quat_arr()[1]
            # t.transform.rotation.z = imu.quat_arr()[2]
            # t.transform.rotation.w = imu.quat_arr()[3]
        
            # br.sendTransform(t)

            # convert everything to a 0 to 360 to apply a 1d rotation then convert back to -180 to 180
            ROV_Pitch = clamp_angle_0_to_360(imu.roll()) - IMU_ROLL_OFFSET
            ROV_Roll = clamp_angle_0_to_360(imu.yaw()) - IMU_YAW_OFFSET
            ROV_Yaw = clamp_angle_0_to_360(imu.pitch()) - IMU_PITCH_OFFSET
            # out_message.gyro = [ROV_Pitch, ROV_Roll, ROV_Yaw]
            pose_message.orientation.x = imu.quat_x()
            pose_message.orientation.y = imu.quat_y()
            pose_message.orientation.z = imu.quat_z()
            pose_message.orientation.w = imu.quat_w()
            pub2.publish(pose_message)
            transQ = np.array([0, 0.7068252, 0, 0.7073883])#[trans.transform.rotation.x,trans.transform.rotation.y,trans.transform.rotation.z,trans.transform.rotation.w])
            imuQ = np.array(imu.quat_arr())
            Q = Quaternion(imu.quat_arr())
            T1 = Quaternion(axis=[1, 0, 0], angle=(90 * 3.141592/180))
            T2 = Quaternion(axis=[0,0,1], angle=(-90 *3.141592/180.0))
            #T3 = Quaternion([ 0.7068252, 0, 0, 0.7073883 ])
            #resultQ = quaternion_multiply(transQ, imuQ)
            R = Q * T1
            rads = euler_from_quaternion(Q.elements)
            out_message.header.stamp = rospy.Time.now()
            out_message.gyro
            for i in range(0,3):
                out_message.gyro[i] = rads[i] * 180.0 / 3.1415
            # = euler_from_quaternion(imu.quat_arr())#[imu.quat_x(),imu.quat_y(),imu.quat_z()]
            # out_message.gyro = [imu.temp(),imu.temp(),imu.temp()]
            ROV_X_Accel = imu.acceleration_z()
            ROV_Y_Accel = imu.acceleration_x()
            ROV_Z_Accel = imu.acceleration_y()
            out_message.accel = [ROV_X_Accel, ROV_Y_Accel, ROV_Z_Accel]
            pub.publish(out_message)
        rate.sleep()

