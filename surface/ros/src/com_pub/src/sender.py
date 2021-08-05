#!/usr/bin/env python3

import rospy
from std_msgs.msg import Float32, String
from shared_msgs.msg import com_msg
import socket, signal, sys
import threading

com_x = 0.0
com_y = 0.0
com_z = 0.0

class SocketManager:
    def __init__(self, port):
        self.running = True
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('127.0.0.1', port))
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
        while not self.connected and self.running:
            try:
                conn, addr = self.sock.accept()
                self.connected = True
            except:
                pass
        while self.running:
            try:
                data = conn.recv(25)
            except:
                pass
            if data:
                global com_x, com_y, com_z, pub

                arr = [float(d) for d in data.decode().split(';')[0].split(',')]

                if len(arr) == 3:
                    com_x = arr[0]
                    com_y = arr[1]
                    com_z = arr[2]

                    msg = com_msg()
                    msg.com[0] = com_x
                    msg.com[1] = com_y
                    msg.com[2] = com_z
                    pub.publish(msg)

def shutdown(sig, frame):
    global sock

    print('please')
    sock.shutdown()
    rospy.signal_shutdown('now')

if __name__ == '__main__':
    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    sock = SocketManager(int(sys.argv[1]))

    rospy.init_node('com_sender', disable_signals=True)

    pub = rospy.Publisher('/rov/com_tweak', com_msg, queue_size=10)
    rate = rospy.Rate(10)

    print('ready')

    rospy.spin()
