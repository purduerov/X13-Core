import numpy as np
import scipy.ndimage.morphology
from skimage import io, filters, measure, util, morphology, transform
from matplotlib import pyplot as plt

img = io.imread("./input/capture.png") # https://i.imgur.com/f8EBFd0.png
segment_img = img[:, :, 0]

coral = segment_img > filters.threshold_otsu(segment_img)

print(coral.shape)

regions = measure.regionprops(measure.label(coral), cache=False)
sort_regions = sorted(regions, key=lambda l: l.perimeter, reverse=True)

coral_mask = np.pad(sort_regions[0].image, (20, 20), 'constant')

print(coral_mask.shape)

coral_mask_c = filters.gaussian(coral_mask, 5)
coral_mask_c = transform.rescale(coral_mask_c, 1/4) > .1

coral_reduce = morphology.skeletonize(coral_mask_c)
coral_reduce = morphology.dilation(coral_reduce, morphology.square(1))

coral_ends = np.zeros_like(coral_reduce)

plt.subplot(131),plt.imshow(img)
plt.subplot(132),plt.imshow(segment_img)
plt.subplot(133),plt.imshow(coral_reduce)
plt.show()

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

io.imsave('./output/output.png', (coral_reduce + ends + junctions) * 255)
