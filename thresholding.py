import matplotlib.pyplot as plt 
import math 
import numpy as np
from matplotlib import pyplot as plt
import cv2
import imutils
from skimage.morphology import closing, square 

def get_lines():
    #image = cv2.imread('../photos/Capture.png', -1) 
    image = cv2.imread('../photos/box3crop.png', -1)
    #image = cv2.imread('../photos/three.jpg', -1)
    resized = imutils.resize(image, width=300)
    ratio = image.shape[0] / float(resized.shape[0])
    new_image = resized.copy()
    edges = cv2.Canny(resized, 10, 100, 3, L2gradient=True)

    #Hough
    lines = np.squeeze(cv2.HoughLinesP(edges, 3, np.pi/90, 30, minLineLength=25, maxLineGap=5))

    for li in lines:
        x1, y1, x2, y2 = li
        cv2.line(new_image,(x1,y1),(x2,y2),(0,255,0),1)
    cv2.line(new_image,(3,3),(53,3),(0,255,0),1)
    
    plt.subplot(131),plt.imshow(image,cmap = 'gray')
    plt.title('Original Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(132),plt.imshow(edges,cmap = 'gray')
    plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(133),plt.imshow(new_image,cmap = 'gray')
    plt.title('Hough Image'), plt.xticks([]), plt.yticks([])
    plt.show()
    
    return lines, resized 


if __name__ == "__main__":
    #line1 = [1, 0, 1, 3]
    #line2 = [3, 2, 3, 4]    #example stuff
    #line3 = [5, 3, 5, 5]
    #line4 = [1, 5, 2, 5]
    #line5 = [4, 5, 5, 5]
    #line6 = [3, 1, 5, 1]
    #lines = np.array([line1, line2, line3, line4, line5, line6])
    lines, resized = get_lines()