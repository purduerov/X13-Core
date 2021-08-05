import cv2
import socket
import threading
import time
import sys
import signal
import os

capture = False
counter = 0

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
        global capture, counter
        while not self.connected and self.running:
            try:
                conn, addr = self.sock.accept()
                self.connected = True
            except:
                pass
            time.sleep(1)
        while self.running:
            try:
                data = conn.recv(1024)
            except:
                pass
            if data:
                capture = len(data.decode()) > 0
                counter = int(data.decode())
                print(capture)
                print(counter)
                
def shutdown(sig, frame):
    global input_socket
    print('shutting down')
    input_socket.shutdown()

if __name__ == '__main__':
    global input_socket

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    input_socket = SocketManager(int(sys.argv[1]))

    vcap = cv2.VideoCapture('http://192.168.1.3:8090/cam0')

    print('ready')

    while(input_socket.running):
        try:
            ret, frame = vcap.read()
        except:
            continue    

        if capture and ret:
            #Save image
            print(os.path.curdir)
            cv2.imwrite(f'cv/testing/im{counter + 1}.png', frame)
            capture = False

        time.sleep(0.5)

    input_socket.shutdown()