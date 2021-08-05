import cv2
import socket
import threading
import time

capture = False
counter = 0

class SocketManager:
    def __init__(self):
        self.running = True
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('127.0.0.1', 11005))
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
            time.sleep(1)
        while self.running:
            try:
                data = conn.recv(1024)
            except:
                pass
            if data:
                capture = len(data.decode()) > 0
                
sock_thread = SocketManager()

vcap = cv2.VideoCapture('http://192.168.1.3:8090/cam0')

while(True):
  try:
      ret, frame = vcap.read()
  except:
      continue 

  if capture:
    #Save image
    cv2.imwrite(f'./testing/im{counter + 1}.png', frame)
    counter += 1
    capture = False

  time.sleep(0.5)

sock_thread.shutdown()
