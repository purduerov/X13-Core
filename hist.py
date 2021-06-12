from PIL import Image 
import cv2
import numpy as np
from matplotlib import pyplot as plt


def palette(img):
    arr = np.asarray(img)
    palette, index = np.unique(asvoid(arr).ravel(), return_inverse=True)
    palette = palette.view(arr.dtype).reshape(-1, arr.shape[-1])
    count = np.bincount(index)
    order = np.argsort(count)
    return palette[order[::-1]]


def asvoid(arr):
    arr = np.ascontiguousarray(arr)
    return arr.view(np.dtype((np.void, arr.dtype.itemsize * arr.shape[-1])))


if __name__ == "__main__":
    num_colors = 20
    #image = './photos/Capture.png'
    image = './photos/ss.jpg'
    image = Image.open(image)
    print(image.mode)
    pal = palette(image)[:num_colors]
    pal_image = Image.new('P', (16, 16))
    pal_image.putpalette(pal * 32) 
    quant = image.quantize(colors=len(pal), palette=pal_image, dither=0)
    image.show()
    quant.show()
    '''
    #print(type(quant))
    cv2image = cv2.cvtColor(np.array(quant), cv2.COLOR_RGB2BGR)
    print(type(cv2image))
    edges = cv2.Canny(cv2image, 10, 100, 3, L2gradient=True)
    print(type(edges))

    #plt.subplot(121),plt.imshow(cv2image)
    #plt.title('Original Image'), plt.xticks([]), plt.yticks([])
    #plt.subplot(122),plt.imshow(edges)
    #plt.title('Edge Image'), plt.xticks([]), plt.yticks([])


    contours, hierarchy = cv2.findContours(edges.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
    print(len(contours))
    squares = []
    for cnt in contours:
        perim = cv2.arcLength(cnt, True)
        shape = cv2.approxPolyDP(cnt, .015 * perim, True)
        if(len(shape == 4) and cv2.contourArea(shape) > 100):
            squares.append(shape)
        
    for square in squares:
        print(cv2.contourArea(square))
        cv2.drawContours(cv2image, [square], -1, (0,255,0), 1)
        cv2.imshow('fuck', cv2image)
        cv2.waitKey(0)
    
    plt.subplot(121),plt.imshow(cv2image)
    plt.subplot(122),plt.imshow(edges)
    plt.show()

    plt.show()

    #get edges 
    #findContours with one inversion, then the other and compare 
    '''