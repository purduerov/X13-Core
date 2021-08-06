import cv2
from matplotlib import pyplot as plt
import numpy as np


if __name__ == '__main__':
    bgr = cv2.imread('./coral.png')
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    edge0 = cv2.Canny(rgb, 3, 30, 3, L2gradient=True)
    edge1 = cv2.Canny(rgb, 1, 30, 7, L2gradient=True)

    points = np.nonzero(edge0)
    #points = np.array( [points[0], points[1]] ).T
    #hull = ConvexHull(points)

    #li = []
    #for x, y in zip(points[0], points[1]):
    #    li.append( (x,y) )
    

    #get hsv, then throw out v and replace with 0s
    print(hsv.shape)
    shape = ( hsv.shape[0], hsv.shape[1])
    print(shape)
    vibe = np.zeros_like(None, shape=shape, dtype=np.float32)
    print(vibe.shape)

    hs = hsv[:,:,:2]
    print(hs.shape)
    
    print(hs.shape)
    #then plot, get pixel color data, set thresholds, binary threshold, contour up, skeletonize

    white_min, white_max = x,y 
    pink_min, pink_max = x,y 
    #binary threshold
    
    #contour
    contours, hierarchy = cv2.findContours(hs.copy() , cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
    #skeletonize
    skelly = skimage.skeletonize()


    plt.imshow(hsv)
    plt.title('HSV Image'), plt.xticks([]), plt.yticks([])

    plt.show()

    '''
    plt.subplot(131),plt.imshow(rgb)
    plt.title('Original Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(132),plt.imshow(edge0, cmap='gray')
    plt.title('Edge0 Image'), plt.xticks([]), plt.yticks([])
    #plt.subplot(133),plt.imshow(hull, cmap='gray')
    #plt.title('Hull Image'), plt.xticks([]), plt.yticks([])
    
    #hull 
    #plt.subplot(133)
    #for simplex in hull.simplices:
    #    plt.plot(points[simplex, 0], points[simplex, 1], 'k-')
    
    plt.show()
    '''

   

#plot it, get color data
#threshold down to white and pink, or get rid of blue background
#contour
#skeletonize 