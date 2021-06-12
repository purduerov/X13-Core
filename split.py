import matplotlib.pyplot as plt 
import numpy as np
import sys
import os
from matplotlib import pyplot as plt
import cv2
import imutils

if __name__ == "__main__":

    filename = './photos/2021-02-26 13-19-01.mp4'
    directory = './images/'

    cap = cv2.VideoCapture(filename)

    if not(cap.isOpened()):
        print('nope')
        sys.exit()
    os.chdir(directory)
    
    count = 0
    while(cap.isOpened()):
        ret, frame = cap.read() 

        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow('frame', gray)
        cv2.imwrite('gray' + str(count) + '.jpg', gray)
        count += 1

        bits = cv2.waitKey(1) & 0xFF
        if(bits == ord('q')):
            break

    cap.release()
    cv2.destroyAllWindows()