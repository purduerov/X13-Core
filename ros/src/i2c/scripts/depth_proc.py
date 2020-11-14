#! /usr/bin/python3
import rospy
# import ms5837
import ms5837
from std_msgs.msg import Float32


def message_received(msg):
    # This runs on a seperate thread from the pub
    pass


if __name__ == "__main__":
    rospy.init_node('depth_proc')

    depth_sensor = None
    try:
        depth_sensor = ms5837.MS5837(1) # Initialize sensor on i2c bus 1
        intializationValue = depth_sensor.init()  # Initializes with density of freshwater
        print("was the intialization of sensor successful: %d" % intializationValue) #right now the init is returning false. prob cuase no sensor. still need to figure out why it just runs blank instead of messages tho since X12 outputed messages still
    except:
        print("It big broke :( cannot initialize the sensor")
        pass

    pub = rospy.Publisher('depth',
                          Float32, queue_size=10)
   
   
   
    rate = rospy.Rate(10)  # 10hz
    # TODO: I2C related activities
    while not rospy.is_shutdown():
        try:
            depth_sensor.read() #allows the sensor to read new data     -> maybe need to add this at the begining of each call to pull new data
            depth = depth_sensor.depth()
            print(("P: %0.1f mbar  %0.3f psi\tT: %0.2f C  %0.2f F %0.2f Depth") % (
                    depth_sensor.pressure(), # Default is mbar (no arguments)
                    depth_sensor.pressure(ms5837.UNITS_psi), # Request psi
                    depth_sensor.temperature(), # Default is degrees C (no arguments)
                    depth_sensor.temperature(ms5837.UNITS_Farenheit),
                    depth_sensor.depth())) # Request Farenheit
        except:
            depth = 0
        pub.publish(Float32(depth))
        rate.sleep()
