import cv2
import numpy as np
import os
import random
from matplotlib import pyplot as plt

white_thresh = 20
square_tolerance = .25

def color_diff(color0, color1):
    return abs(int(color0) - int(color1)) 
    diff = 0                        #from before I only used H in HSV
    for i,j in zip(color0, color1):
        diff += abs(int(i)-int(j))  #prevent uint8 overflow
    return diff

'''
def color_down(image):
    new_image = image.copy()            #so I can draw on the picture in testing 
    row = int(new_image.shape[0] / 2)   #start at center, move towards edge looking for colors
    col = int(new_image.shape[1] / 2)
    new_row = row + 1
    new_col = col #+ 1
    white_baseline = image[row][col]
    flag = 0
    confirmed = 0
    edge = None

    while(new_row < new_image.shape[0]):
        diff = color_diff(white_baseline, image[new_row][new_col])
        if not flag:    #no new color detected yet
            if(diff > white_thresh):
                new_color = image[new_row][new_col]
                flag = 1
                edge = new_row
        else:   #new color detected, back to white or off the edge of the target?
            if(color_diff(image[edge][new_col], image[new_row][new_col]) < white_thresh):
                confirmed = 1
                break #new color confirmed 

        new_row += 1

    cv2.line(new_image,(col,row),(new_col,new_row),(255,0,0),1)
    #cv2.imshow("fuck", new_image)
    #cv2.waitKey(0)
    plt.subplot(111),plt.imshow(new_image)
    plt.show()

    if(confirmed):
        return new_color, new_row - row
    if(edge is not None):
        return None, edge - row
    return None, new_row - row
'''

def color_down(image):
    new_image = image.copy()            #so I can draw on the picture in testing 
    row = int(new_image.shape[0] / 2)   #start at center, move towards edge looking for colors
    col = int(new_image.shape[1] / 2)
    new_row = row + 1
    new_col = col #+ 1
    white_baseline = image[row][col]
    flag = 0
    confirmed = 0
    edge = None

    while(new_row < new_image.shape[0]):
        diff = color_diff(white_baseline, image[new_row][new_col])
        if not flag:    #no new color detected yet
            if(diff > white_thresh):
                new_color = image[new_row][new_col]
                flag = 1
                edge = new_row
        else:   #new color detected, back to white or off the edge of the target?
            if(color_diff(image[edge][new_col], image[new_row][new_col]) < white_thresh):
                confirmed = 1
                break #new color confirmed 

        new_row += 1

    cv2.line(new_image,(col,row),(new_col,new_row),(255,0,0),1)
    #cv2.imshow("fuck", new_image)
    #cv2.waitKey(0)
    plt.subplot(111),plt.imshow(new_image)
    plt.show()

    if(confirmed):
        return new_color, new_row - row
    if(edge is not None):
        return None, edge - row
    return None, new_row - row

def color_right(image):
    new_image = image.copy()
    row = int(new_image.shape[0] / 2)
    col = int(new_image.shape[1] / 2)
    new_row = row #+ 1
    new_col = col + 1
    white_baseline = image[row][col]
    flag = 0
    confirmed = 0
    edge = None

    while(new_col < new_image.shape[1]):
        diff = color_diff(white_baseline, image[new_row][new_col])
        if not flag:    #no new color detected yet
            if(diff > white_thresh):
                new_color = image[new_row][new_col]
                flag = 1
                edge = new_col
        else:   #new color detected, back to white or off the edge of the target?
            if(color_diff(image[new_row][edge], image[new_row][new_col]) < white_thresh):
            #if(diff < white_thresh):
                confirmed = 1
                break #new color confirmed 

        new_col += 1

    cv2.line(new_image,(col,row),(new_col,new_row),(255,0,0),1)
    #cv2.imshow("fuck", new_image)
    #cv2.waitKey(0)
    plt.subplot(111),plt.imshow(new_image)
    plt.show()

    if(confirmed):
        return new_color, new_col - col
    if(edge is not None):
        return None, edge - col
    return None, new_col - col


def color_up(image):
    new_image = image.copy()
    row = int(new_image.shape[0] / 2)
    col = int(new_image.shape[1] / 2)
    new_row = row - 1
    new_col = col #+ 1
    white_baseline = image[row][col]
    flag = 0
    confirmed = 0
    edge = None

    while(new_row >= 0):
        diff = color_diff(white_baseline, image[new_row][new_col])
        if not flag:    #no new color detected yet
            if(diff > white_thresh):
                new_color = image[new_row][new_col]
                flag = 1
                edge = new_row
        else:   #new color detected, back to white or off the edge of the target?
            if(color_diff(image[edge][new_col], image[new_row][new_col]) < white_thresh):
            #if(diff < white_thresh):
                confirmed = 1
                break #new color confirmed 

        new_row -= 1

    cv2.line(new_image,(col,row),(new_col,new_row),(255,0,0),1)
    #cv2.imshow("fuck", new_image)
    #cv2.waitKey(0)
    plt.subplot(111),plt.imshow(new_image)
    plt.show()

    if(confirmed):
        return new_color, row - new_row 
    if(edge is not None):
        return None, row - edge
    return None, row - new_row


def color_left(image):
    new_image = image.copy()
    row = int(new_image.shape[0] / 2)
    col = int(new_image.shape[1] / 2)
    new_row = row #- 1
    new_col = col - 1
    white_baseline = image[row][col]
    flag = 0
    confirmed = 0
    edge = None

    while(new_col >= 0):
        diff = color_diff(white_baseline, image[new_row][new_col])
        if not flag:    #no new color detected yet
            if(diff > white_thresh):
                new_color = image[new_row][new_col]
                flag = 1
                edge = new_col
        else:   #new color detected, back to white or off the edge of the target?
            if(color_diff(image[new_row][edge], image[new_row][new_col]) < white_thresh):
            #if(diff < white_thresh):
                confirmed = 1
                break #new color confirmed 

        new_col -= 1

    cv2.line(new_image,(col,row),(new_col,new_row),(255,0,0),1)
    #cv2.imshow("fuck", new_image)
    #cv2.waitKey(0)
    plt.subplot(111),plt.imshow(new_image)
    plt.show()

    if(confirmed):
        return new_color, col - new_col 
    if(edge is not None):
        return None, col - edge
    return None, col - new_col 


def is_square(image):
    ret = {"is_square": 0}

    down, down_dist = color_down(image)
    right, right_dist = color_right(image)
    up, up_dist = color_up(image)
    left, left_dist = color_left(image)

    if(left is None):
        #rotate ccw 
        image = np.rot90(image, k=1)
        ret["down"] = left 
        ret["right"] = down 
        ret["up"] = right 
        ret["left"] = up 
    elif(up is None):
        #rotate upside down 
        image = np.rot90(image, k=2)
        ret["down"] = up 
        ret["right"] = left 
        ret["up"] = down 
        ret["left"] = right 
    elif(right is None):
        #rotate cw 
        image = np.rot90(image, k=3)
        ret["down"] = right 
        ret["right"] = up 
        ret["up"] = left 
        ret["left"] = down 
    else:
        #load colors no rotate 
        ret["down"] = down 
        ret["right"] = right 
        ret["up"] = up 
        ret["left"] = left 
    
    square = abs(1 - (down_dist + up_dist) / (right_dist + left_dist)) 
    print(square)
    if( square < square_tolerance):
        ret["is_square"] = 1

    print(ret)

    plt.subplot(111),plt.imshow(image)
    plt.show()
    #cv2.imshow("fuck", image)
    #cv2.waitKey(0)
    

def image_folder_read(path):
    images = [cv2.imread(path+i) for i in os.listdir(path)]
    #if not(len(images) == 5):
    #    print('Incorrect number of images, there should be exactly 5')
    #    exit()
    return images 


def image_folder_write(new_path, test_images):
    """Write test_images to a new folder.

    Creates a folder of images in a form that can be read by image_folder_read.
    Can be used to create new test sets of modified images to test the order_sides function.
    """
    if not os.path.exists(new_path):
        os.makedirs(new_path)
    cv2.imwrite(new_path + 'Subway_Back.png', test_images[0])
    cv2.imwrite(new_path + 'Subway_Front.png', test_images[1])
    cv2.imwrite(new_path + 'Subway_Left.png', test_images[2])
    cv2.imwrite(new_path + 'Subway_Right.png', test_images[3])
    cv2.imwrite(new_path + 'Subway_Top.png', test_images[4])


def shuffle_images(images):
    """Shuffles a list of images.

    Is used to test the order_sides method, which determines which image corresponds to each face.
    """
    shuffled = []
    for i in range(0,len(images)):
        rand = random.randint(0, len(images) - 1)
        shuffled.append(images[rand])
        del images[rand]

    return shuffled


def rand_shade(image, range = 40):
    """Adds a random degree of shading to an image.

    Used to test how the order_sides method responds to differences in lighting.
    TODO: Change this to HSV to allow for a wider range.
    """
    new_image = ((256 - 2 * range) / 256) * image
    new_image = new_image + range
    new_image = new_image.astype('uint8')
    change = random.randint(-range, range)
    new_image = new_image + change
    new_image = new_image.astype('uint8')
    return new_image


def noise_add(image, range = 20):
    """Adds noise to an image.

    Used to test how the order_sides method responds to noise.
    Range indicates the intensity of the noise.
    Using this method can lead to overflow errors, which will cause some pixels to have great differences in color.
    The range is divided by 2 to minimize this.
    """
    noise = np.random.normal(0, range / 2, image.shape)
    new_image = ((256 - 4 * range) / 256) * image
    new_image = new_image + 2 * range
    new_image = new_image.astype('uint8')

    noisy_image = new_image + noise
    noisy_image = noisy_image.astype('uint8')

    return noisy_image


def mosaic_compile_ordered(sides):
    """Creates a mosaic of sides given in the right order."""
    # used when sides is an array with sides in the correct order
    return mosaic_compile(sides[0], sides[1], sides[2], sides[3], sides[4])


def mosaic_compile_unordered(sides):
    """Creates a mosaic of sides given in any order."""
    return mosaic_compile_ordered(order_sides(sides))


def mosaic_compile(back, front, left, right, top, print_shape = False):
    """Creates a mosaic of sides."""
    # Images list should contain images in this order:
    total_shape = [0, 0, 3]
    all_bottom_imgs = [back, front, left, right]
    # sort faces by height
    all_bottom_imgs = sorted(all_bottom_imgs, key=lambda face: face.shape[0])
    # Find the bottom face with the greatest height
    max_height = all_bottom_imgs[3].shape[0]
    total_shape[0] = max_height + top.shape[0]
    total_shape[1] = left.shape[1] + front.shape[1] + right.shape[1] + back.shape[1]

    image_front = cv2.copyMakeBorder(front,
                                     top.shape[0],
                                     total_shape[0] - top.shape[0] - front.shape[0],
                                     left.shape[1],
                                     right.shape[1] + back.shape[1],
                                     0)
    image_left = cv2.copyMakeBorder(left,
                                    top.shape[0],
                                    total_shape[0] - top.shape[0] - left.shape[0],
                                    0,
                                    total_shape[1] - left.shape[1],
                                    0)
    image_right = cv2.copyMakeBorder(right,
                                     top.shape[0],
                                     total_shape[0] - top.shape[0] - right.shape[0],
                                     left.shape[1] + front.shape[1],
                                     back.shape[1],
                                     0)
    image_top = cv2.copyMakeBorder(top,
                                   0,
                                   total_shape[0] - top.shape[0],
                                   left.shape[1],
                                   total_shape[1] - left.shape[1] - top.shape[1],
                                   0)
    image_back = cv2.copyMakeBorder(back,
                                    top.shape[0],
                                    total_shape[0] - top.shape[0] - back.shape[0],
                                    total_shape[1] - back.shape[1],
                                    0,
                                    0)

    if print_shape:
        print("img_top" + str(image_top.shape))
        print("img_left" + str(image_left.shape))
        print("img_right" + str(image_right.shape))
        print("img_back" + str(image_back.shape))
        print("img_front" + str(image_front.shape))

    mosaic = np.zeros(total_shape, np.uint8)
    mosaic = mosaic + image_front + image_left + image_right + image_back + image_top
    return mosaic


def order_sides(sides, show_samples = False, show_faces = False):
    """Returns an array of sides in the correct order.

    Determines which image corresponds to which side. Returns an array of images in the order
    that mosaic_compile_ordered requires.

    If show_samples is true, samples for each direction will be shown.
    If show_faces is true, the image found for each face will be shown.
    """
    # sample_locs determines how many samples and where they are taken from
    directions = {'top', 'bottom', 'left', 'right'}
    box_lengths = {'short', 'long'}

    length = 10
    # sample_locs represents where the samples should be obtained from to compare.
    # As of now, the second sample is always used in comparisons.
    # The other locations will also be displayed to the user if show_samples is true.
    sample_locs = [0.4, 0.5, 0.6]

    # There will be a top, bottom, left and right.
    short_sides = []
    long_sides = []
    # all_sides contains short and long sides.
    all_sides = []
    ordered_sides = {}
    list_ordered_sides = []
    ratios = []
    # Take "samples" of each image- column from left
    # Will produce 20 different samples.
    # 4 will be the base and will not contain any colors.

    for side in sides:

        side = cv2.cvtColor(side, cv2.COLOR_BGR2HSV)
        ratio = side.shape[1] / side.shape[0]
        ratios.append(ratio)

        top_samples = []
        bottom_samples = []
        left_samples = []
        right_samples = []

        for loc in sample_locs:
            top_samples.append(middle_out_sample(side, 'top', distance=loc))
            bottom_samples.append(middle_out_sample(side, 'bottom', distance=loc))
            left_samples.append(middle_out_sample(side, 'left', distance=loc))
            right_samples.append(middle_out_sample(side, 'right', distance=loc))
        all_sides.append({'top': top_samples, 'bottom': bottom_samples, 'left': left_samples, 'right': right_samples,
         'image': side, 'ratio': ratio})

    by_ratios = sorted(all_sides, key=lambda side_dict: side_dict.get('ratio'))
    short_sides.append(by_ratios[0])
    short_sides.append(by_ratios[1])
    long_sides.append(by_ratios[2])
    long_sides.append(by_ratios[3])
    long_sides.append(by_ratios[4])
    sides_dict = {'short': short_sides, 'long': long_sides}

    # View samples:
    # NOTE: Only works when NOT using middle_out samples
    if show_samples:
        for direction in directions:
            all_side_samples = []

            for box_length in box_lengths:
                for side in sides_dict.get(box_length):
                    one_side_samples = np.concatenate(tuple(side.get(direction)), axis=1)
                    all_side_samples.append(one_side_samples)
            img = np.concatenate(tuple(all_side_samples), axis=1)
            cv2.imshow("All " + direction + " slices", cv2.cvtColor(img, cv2.COLOR_HSV2BGR))

    # First, find the long rectangle with color on the bottom.
    # We can do this by sorting the long rectangles by their saturation values.
    by_saturations = sorted(sides_dict['long'], key=lambda side_current: pixel_from_sample(side_current['bottom'][1])[0])

    ordered_sides['top'] = by_saturations[2]

    # Now, find all the other faces from the top face.
    # Compare the hue values
    # SHORT SIDES:
    hue_differences = []
    top_left_hue = pixel_from_sample(ordered_sides['top']['left'][1])[0]
    hues = []

    hues.append(pixel_from_sample(sides_dict['short'][0]['top'][1])[0])
    hues.append(pixel_from_sample(sides_dict['short'][1]['top'][1])[0])

    for hue in hues:
        # check the difference between each of the sides
        # and the left edge of the top side
        hue_differences.append(abs(int(top_left_hue) - int(hue)))

    if hue_differences[0] > hue_differences[1]:
        ordered_sides['right'] = sides_dict['short'][0]
        ordered_sides['left'] = sides_dict['short'][1]
    else:
        ordered_sides['right'] = sides_dict['short'][1]
        ordered_sides['left'] = sides_dict['short'][0]

    hue_total_differences = np.array([0, 0])
    # Now do the same thing for the long sides.
    # First, remove the top from the by_saturations array, where it is the last element.
    new_long_sides = [by_saturations[0], by_saturations[1]]
    top_bottom_hue = pixel_from_sample(ordered_sides['top']['bottom'][1])[0]
    left_right_hue = pixel_from_sample(ordered_sides['left']['right'][1])[0]
    right_left_hue = pixel_from_sample(ordered_sides['right']['left'][1])[0]
    edge_hues = [top_bottom_hue, left_right_hue, right_left_hue]
    first_hues = []
    second_hues = []
    edge_hues = []
    first_hues.append(pixel_from_sample(new_long_sides[0]['top'][1])[0])
    second_hues.append(pixel_from_sample(new_long_sides[1]['top'][1])[0])
    first_hues.append(pixel_from_sample(new_long_sides[0]['left'][1])[0])
    second_hues.append(pixel_from_sample(new_long_sides[1]['left'][1])[0])
    first_hues.append(pixel_from_sample(new_long_sides[0]['right'][1])[0])
    second_hues.append(pixel_from_sample(new_long_sides[1]['right'][1])[0])
    edge_hues.append(top_bottom_hue)
    edge_hues.append(left_right_hue)
    edge_hues.append(right_left_hue)
    hue_differences[0] = 0
    hue_differences[1] = 0
    first_hues = np.array(first_hues)
    second_hues = np.array(second_hues)
    edge_hues = np.array(edge_hues)
    hue_differences[0] = sum(abs(first_hues - edge_hues))
    hue_differences[1] = sum(abs(second_hues - edge_hues))

    if hue_differences[0] > hue_differences[1]:
        # Indicates that the first of the new long sides is more different from the top edge than the other.
        ordered_sides['back'] = new_long_sides[0]
        ordered_sides['front'] = new_long_sides[1]
    else:
        ordered_sides['back'] = new_long_sides[1]
        ordered_sides['front'] = new_long_sides[0]

    if show_faces:
        cv2.imshow("Top face:", cv2.cvtColor(ordered_sides['top']['image'], cv2.COLOR_HSV2BGR))
        cv2.imshow("Left face:", cv2.cvtColor(ordered_sides['left']['image'], cv2.COLOR_HSV2BGR))
        cv2.imshow("Right face:", cv2.cvtColor(ordered_sides['right']['image'], cv2.COLOR_HSV2BGR))
        cv2.imshow("Front face:", cv2.cvtColor(ordered_sides['front']['image'], cv2.COLOR_HSV2BGR))
        cv2.imshow("Back face:", cv2.cvtColor(ordered_sides['back']['image'], cv2.COLOR_HSV2BGR))

    side_indices = ['back', 'front', 'left', 'right', 'top']
    for side_name in side_indices:
        list_ordered_sides.append(cv2.cvtColor(ordered_sides[side_name]['image'], cv2.COLOR_HSV2BGR))
    return list_ordered_sides


def pixel_from_sample(sample, threshold = 50, min_band = 4):
    """Returns the HSV of the first colored band in a sample.

    Iterates through a sample until it finds a band of pixel with a saturation greater than the threshold,
    and a length greater than the min_band. Returns the average HSV of the band."""
    # Note: It is assumed that the sample provided is hsv.
    band_width = 0
    band_avg = np.array([0, 0, 0])
    band_sum = np.array([0, 0, 0])

    for i in range(0, sample.shape[0]):
        saturation = sample[i, 0, 1]
        # print(saturation)
        if saturation > threshold:
            # print("Returning pixel with " + str(saturation))
            band_sum = band_sum + sample[i, 0, :]
            band_width += 1
        elif band_width != 0 and band_width < min_band and saturation <= threshold:
            # must have been one or two random points.
            band_sum = band_sum * 0
            band_width = 0
        elif band_width != 0 and saturation <= 50:
            break
        # Pythonic ternary checks if band_width is 0
    band_avg = band_sum / (band_width or not band_width)
    # If it returns 0, it means it found no points with high saturation.
    # This means it probably is the bottom edge of one of the sides.
    return band_avg


def middle_out_sample(side, edge, distance = 0.5):
    """Creates a ."""
    if (edge == 'top'):
        index = int(distance * side.shape[1])
        start_y = int(0.5 * side.shape[0])
        plane = side[:, index:index + 1, :]
        slice = plane[0:start_y, :]
        slice = np.flip(slice, axis=0)
        # Creates cut that goes from top to start_y
        return slice
    elif (edge == 'bottom'):
        index = int(distance * side.shape[1])
        plane = side[:, index:index + 1, :]
        slice = plane[int(0.5 * side.shape[0]):side.shape[0], :]
        return slice
    elif (edge == 'left'):
        index = int(distance * side.shape[0])
        plane = side[index:index + 1, :]
        slice = plane[:, 0:int(0.5*side.shape[1]), :]
        slice = slice.transpose((1, 0, 2))
        slice = np.flip(slice, axis=0)
        return slice
    elif (edge == 'right'):
        index = int(distance * side.shape[0])
        plane = side[index:index + 1, :, :]
        slice = plane[:, int(0.5 * side.shape[1]):side.shape[1], :]
        slice = slice.transpose((1, 0, 2))
        return slice
    print("Edge name \"" + edge + "\" not recognized.")


def side_sample(side, edge, length = 10, distance = 0.5):
    """Return a sample of a side.

    Obtains a sample from the edge of a face called "side".
    Returns a sample as a (length, 1, 3) array, representing a line of BGR values.
    """
    if (edge == 'top'):
        index = int(distance * side.shape[1])
        plane = side[:, index:index + 1, :]
        slice = plane[0:length, :]

        return slice
    elif (edge == 'bottom'):
        index = int(distance * side.shape[1])
        plane = side[:, index:index + 1, :]
        slice = plane[(side.shape[0]-length):side.shape[0], :]
        slice = np.flip(slice, axis=0)
        return slice
    elif (edge == 'left'):
        index = int(distance * side.shape[0])
        plane = side[index:index + 1, :]
        slice = plane[:, 0:length, :]
        slice = slice.transpose((1, 0, 2))
        return slice
    elif (edge == 'right'):
        index = int(distance * side.shape[0])
        plane = side[index:index + 1, :, :]
        slice = plane[:, (side.shape[1]-length):side.shape[1], :]
        slice = slice.transpose((1, 0, 2))
        slice = np.flip(slice, axis=0)
        return slice
    print("Edge name \"" + edge + "\" not recognized.")