import matplotlib.pyplot as plt 
import math 
import numpy as np
import sys
from matplotlib import pyplot as plt
import cv2
import imutils
from area import * 

if __name__ == "__main__":

    filename = './photos/okcolor1.mp4'

    cap = cv2.VideoCapture(filename)
    frame_count = 0
    if not(cap.isOpened()):
        print('Vid didn\'t open')
        sys.exit()

    print('To go to next frame press n')
    print('To quit press q')
    print('To activate the CV on a frame, press spacebar')
    
    while(cap.isOpened()):
        ret, frame = cap.read() 
        print(frame_count)

        if not ret:
            break

        frame_count += 1
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow('frame', gray)

        bits = cv2.waitKey(0) & 0xFF
        if(bits == ord('q')):
            break
        elif(bits == ord(' ')):
            lines, resized = get_lines(gray) #frame
            coords = operate(lines, resized)
            #if coords, save them
            if(coords):
                print('Press s to save, anything else to continue')
                if(cv2.waitKey(0) & 0xFF == ord('s')):
                    frame = imutils.resize(frame, width=300)    #refactor pls
                    crop_picture = frame[coords[2]:coords[3], coords[0]:coords[1]]
                    cv2.imwrite('./saved.jpg', crop_picture)
                    break
        elif(bits == ord('n')):
            pass 
        else:
            break

    cap.release()
    cv2.destroyAllWindows()