#!/usr/bin/env python3

import rospy
from std_msgs.msg import Float32, String
import socket, signal, sys
import threading

angle = 30.0

class SocketManager:
    def __init__(self, port):
        self.running = True
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('127.0.0.1', port))
        self.sock.listen(5)
        self.sock.settimeout(1)
        self.connected = False

        print('ready')

        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def shutdown(self):
        self.running = False
        self.sock.close()
        self.thread.join()

    def run(self):
        while not self.connected and self.running:
            try:
                conn, addr = self.sock.accept()
                self.connected = True
            except:
                pass
        while self.running:
            try:
                data = conn.recv(10)
            except:
                pass
            if data:
                global angle

                angle = float(data.decode())

def shutdown(sig, frame):
    global sock

    sock.shutdown() 
    rospy.signal_shutdown('interrupt')

if __name__ == '__main__':
    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    rospy.init_node('servo_sender')

    sock = SocketManager(int(sys.argv[1]))

    pub = rospy.Publisher('/rov/servo', Float32, queue_size=10)
    rate = rospy.Rate(100)

    while not rospy.is_shutdown():
        pub.publish(angle)
        rate.sleep()
