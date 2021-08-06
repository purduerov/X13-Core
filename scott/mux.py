import numpy as np
import scipy.ndimage.morphology
from skimage import io, filters, measure, morphology, transform
from matplotlib import pyplot as plt



#take in both images
#np.nonzero of both
#for all the pixels in one image
    #if no pixels in the other image that are within threshold distance?
        #unique, flag it 


img = io.imread("./output/output.png")

eroded = morphology.erosion(img,  morphology.square(3))


plt.subplot(121),plt.imshow(img)
plt.subplot(122),plt.imshow(eroded)
plt.show()