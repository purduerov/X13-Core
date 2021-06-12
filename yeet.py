import cv2 
import numpy as np 
from matplotlib import pyplot as plt
import imutils
from skimage.filters import unsharp_mask

if __name__ == "__main__":
    filename = './photos/gray183.jpg'

    image = cv2.imread(filename, cv2.COLOR_BGR2GRAY)  
    new_image = image.copy() 


    
    edges = cv2.Canny(new_image, 10, 100, 3, L2gradient=True)
    
    contours, hierarchy = cv2.findContours(edges.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
    print(len(contours))
    squares = []
    for cnt in contours:
        #print(cnt)
        perim = cv2.arcLength(cnt, True)
        shape = cv2.approxPolyDP(cnt, .005 * perim, True)
        if(len(shape == 4) and cv2.contourArea(shape) > 100):
            squares.append(shape)
        
    for square in squares:
        print(cv2.contourArea(square))
        cv2.drawContours(new_image, [square], -1, (0,255,0), 1)
        cv2.imshow('fuck', new_image)
        cv2.waitKey(0)
    
    plt.subplot(121),plt.imshow(new_image,cmap='gray')
    plt.subplot(122),plt.imshow(edges,cmap='gray')
    plt.show()
    