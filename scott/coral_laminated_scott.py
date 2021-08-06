import numpy as np
import scipy.ndimage.morphology
from skimage import io, filters, measure, util, morphology, transform
from matplotlib import pyplot as plt
from PIL import Image 

#path = "./input/test_land.jpg"
path = "./input/land_capture.png"

#img = io.imread("./input/test_land.png") # https://i.imgur.com/f8EBFd0.png
#gray = img[:, :, 0]

gray = np.array(Image.open(path).convert('L'))

coral = gray > filters.threshold_otsu(gray)

#coral = morphology.binary_dilation(coral)

#regions = measure.regionprops(measure.label(coral), cache=False)
#sort_regions = sorted(regions, key=lambda l: l.perimeter, reverse=True)

#for region in regions: #no longer same coords
#    plt.imshow(region.image)
#    plt.show()

coral_mask = np.pad(coral, (20, 20), 'constant')

coral_mask_c = filters.gaussian(coral_mask, 2)
coral_mask_c = transform.rescale(coral_mask_c, 1/4) > .1

coral_reduce = morphology.skeletonize(coral_mask_c)
#coral_reduce = morphology.dilation(coral_reduce, morphology.square(1))

coral_ends = np.zeros_like(coral_reduce)

end_kernels = [
    np.array([[0, 0, 0],
              [0, 0, 0],
              [0, 1, 0]]),
    np.array([[0, 0, 0],
              [1, 0, 0],
              [0, 0, 0]]),
    np.array([[0, 0, 0],
              [0, 0, 1],
              [0, 0, 0]]),
]

for kernel in end_kernels:
    coral_ends |= scipy.ndimage.morphology.binary_hit_or_miss(coral_reduce, kernel)

ends = morphology.dilation(coral_ends, morphology.square(5))

coral_junc = np.zeros_like(coral_reduce)

center = np.array([[0, 0, 0],
                   [0, 1, 0],
                   [0, 0, 0]])

junc_kernels = [
    np.array([[0, 1, 0],
              [1, 0, 1],
              [0, 1, 0]]),

    np.array([[0, 1, 0],
              [0, 0, 1],
              [0, 1, 0]]),

    np.array([[0, 1, 0],
              [0, 0, 1],
              [0, 0, 0]]),

    np.array([[0, 1, 0],
              [0, 0, 1],
              [1, 0, 0]]),
]

for kernel in junc_kernels:
    for rot in range(3):
        coral_junc |= scipy.ndimage.morphology.binary_hit_or_miss(coral_reduce, np.rot90(kernel, rot))
        coral_junc |= scipy.ndimage.morphology.binary_hit_or_miss(coral_reduce, np.rot90(kernel, rot) + center)

junctions = morphology.dilation(coral_junc, morphology.square(5))

plt.subplot(131),plt.imshow(gray)
plt.subplot(132),plt.imshow(coral)
plt.subplot(133),plt.imshow(junctions+ends)
plt.show()

io.imsave('./output/output.png', (coral_reduce + ends + junctions) * 255)


#be prepared to flip a mirror image
#remove below base 
#correlate colors