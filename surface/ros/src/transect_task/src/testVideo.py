import cv2
import numpy as np
import helperFunctions as hp
from datetime import datetime

cam_feed_url = "http://192.168.1.3:8090/test.mjpg"
# Make this True to save the video
# On a side note, are preprocessor macros a thing in Python?
saving = False
# saving = True
debug = False
# debug = True

now = datetime.now()
date_time = now.strftime("%Y-%m-%d_%H:%M")
save_path = f'output_{date_time}.avi'

# cap = cv2.VideoCapture("transectLineExample.mp4")
cap = cv2.VideoCapture("http://192.168.1.3:8090/cam0.mjpg")
fps = 24
fourcc = cv2.VideoWriter_fourcc('M', 'P', 'E', 'G')

# Just for the purpose of seeing how many seconds into the video you are in OpenCV
losing_frames = 0
losses = 0
seconds = 0
paused = False
print("Running...\n")

if saving:
    out = cv2.VideoWriter(save_path, fourcc, fps, (480, 360))

while cap.isOpened():

    if not paused:
        ret, frame = cap.read()
        #print(frame.shape)
        # May need to alter fps depending on video

        if ret and not paused:
            seconds += int(1000 / fps)
            #print(seconds)
            # print(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            # print(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            # All video properties can be found on opencv website
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            hframe = frame.copy()
            # phframe = frame.copy()
            # phough not working
            #hboldframe = frame.copy()

            output = hp.apply_hough_transform(hframe, None, threshold=100, show_all=True, debug=False)
            if output is not None and len(output['big_lines']) is not 2:
                losing_frames += 1
                # print(f"{output['big_lines']}")
            else:
                losing_frames = 0
                if debug:
                    if output is not None and len(output['big_lines']):
                        print(f"Has 2: {output['big_lines']}")
                    else:
                        if output is None:
                            print("Output is None.")

            if losing_frames == 24:
                losses += 1

            if losses == 2:
                print(f"Task failed. Showing {len(output['big_lines'])} pipe(s) over {losing_frames} frames.")
                break

            # print(losing_frames)

            cv2.imshow('Current frame', hframe)
            # cv2.imshow('vales', hp.createValueEdges(frame))
            #hp.applyPHough(phframe, None, minLineLength=50, maxLineGap=40)
            #hp.applyHoughTransform(hframe, hp.boldImage(hp.createHueEdges(frame)), threshold=200)
            #cv2.imshow('Current frame probablistic', phframe)
            #cv2.imshow('Current frame hough with bold', hboldframe)
            # Hough transform test
            if saving:
                out.write(hframe)

        else:
            break

    user_input = cv2.waitKey(int(1000 / fps))
    if user_input is ord('q'):
        break
    if user_input is ord('p'):
        paused = True
    if user_input is ord('r'):
        paused = False

cap.release()
if saving:
    out.release()