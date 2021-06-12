from photomosaics import *
import cv2
from matplotlib import pyplot as plt

def test_1():
    """A test to see if noisy images can be generated and an ordered mosaic can be made."""
    test_images_original_path = "./SubwayImagesOriginal/"
    test_images_original = image_folder_read(test_images_original_path)

    test_mosaic = mosaic_compile(test_images_original[0],
                                 test_images_original[1],
                                 test_images_original[2],
                                 test_images_original[3],
                                 test_images_original[4])

    cv2.imshow("Test Mosaic", test_mosaic)
    noise_test = noise_add(test_mosaic)
    cv2.imshow("Plus Noise", noise_test)

    noisy_images = []
    for side in test_images_original:
        noisy_images.append(rand_shade(noise_add(side)))

    image_folder_write("./SubwayImagesNoise/", noisy_images)
    noise_mosaic = mosaic_compile_ordered(noisy_images)
    cv2.imshow("Noisy Mosaic", noise_mosaic)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def test_2():
    """A test for the unordered mosaic function.

    Also an example of how to produce a mosaic from shuffled and cropped images.
    Reads a folder of ordered images, then shuffles them, then produces the ordered mosaic from shuffled images.
    """
    #path = "./shite/"
    path = "./underwater/"
    images = image_folder_read(path)
    for image in images:
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        hue, sat = hsv[:,:,0], hsv[:,:,1]
        plt.subplot(131),plt.imshow(hsv)
        plt.title('hsv'), plt.xticks([]), plt.yticks([])
        plt.subplot(132),plt.imshow(hue)
        plt.title('hue'), plt.xticks([]), plt.yticks([])
        plt.subplot(133),plt.imshow(sat)
        plt.title('sat'), plt.xticks([]), plt.yticks([])
        plt.show()
        
        is_square(sat)

    #mess = mosaic_compile_ordered(shuffled)
    #nice = mosaic_compile_unordered(images)
    #cv2.imshow("Mess: ", mess)
    #cv2.imshow("Nice: ", nice)

    


def test_3():
    """The final test, with realistic images."""
    new_path = "./Subway_Realistic_Images/"
    shuffled = image_folder_read(new_path)
    mess = mosaic_compile_ordered(shuffled)
    nice = mosaic_compile_unordered(shuffled)
    cv2.imshow("Mess: ", cv2.resize(mess, (1000,400), interpolation = cv2.INTER_AREA))
    cv2.imshow("Nice: ", cv2.resize(nice, (1000,400), interpolation = cv2.INTER_AREA))

    cv2.waitKey(0)
    cv2.destroyAllWindows()


test_2()
