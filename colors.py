import matplotlib.pyplot as plt 
import math 
import numpy as np
from matplotlib import pyplot as plt
import cv2
import imutils

white_high = []
white_low = []

if __name__ == "__main__":
    image = cv2.imread('./saved.jpg', -1) 
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    ypos = int(image.shape[0] / 2)
    xpos = int(image.shape[1] / 2)
    print(image.shape)
    print(image[0][ypos])
    print(image[ypos][xpos])
    print()

    for x in range(hsv.shape[1]):
        print(hsv[ypos][x])



    plt.subplot(121),plt.imshow(image)
    plt.subplot(122),plt.imshow(hsv)
    plt.show()