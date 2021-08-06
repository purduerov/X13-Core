import numpy as np
import scipy.ndimage.morphology
from skimage import io, filters, measure, util, morphology, transform
from matplotlib import pyplot as plt
from PIL import Image 

path = "./output/land_nodes.png"
img = io.imread(path) # https://i.imgur.com/f8EBFd0.png

junctions = morphology.erosion(img, morphology.square(5))

#chop off under thresh


plt.subplot(121), plt.imshow(img)
plt.subplot(122), plt.imshow(junctions)
plt.show()