import cv2
from matplotlib import pyplot as plt
import os
import numpy as np


def color_diff(color0, color1):
    return abs(int(color0) - int(color1)) 


def color_down(image, thresh):           
    row = int(image.shape[0] / 2)   #start at center, move towards edge looking for colors
    col = int(image.shape[1] / 2)
    new_row = row + 1
    new_col = col #+ 1
    baseline = image[row][col]

    while(new_row < image.shape[0]):
        if( color_diff(baseline, image[new_row][new_col]) > thresh ):
            break
        new_row += 1

    if new_row == image.shape[0]: 
        return new_row - 1
    return new_row  


def color_left(image, thresh):
    row = int(image.shape[0] / 2)
    col = int(image.shape[1] / 2)
    new_row = row #- 1
    new_col = col - 1
    baseline = image[row][col]

    while(new_col >= 0):
        if( color_diff(baseline, image[new_row][new_col]) > thresh ):
            break 
        new_col -= 1 

    if new_col < 0:
        return 0
    return new_col 


def color_up(image, thresh):
    row = int(image.shape[0] / 2)
    col = int(image.shape[1] / 2)
    new_row = row - 1 
    new_col = col #+ 1
    baseline = image[row][col]

    while(new_row >= 0):
        if( color_diff(baseline, image[new_row][new_col]) > thresh ):
            break 
        new_row -= 1

    if new_row < 0:
        return 0
    return new_row 


def color_right(image, thresh):
    row = int(image.shape[0] / 2)
    col = int(image.shape[1] / 2)
    new_row = row #+ 1 
    new_col = col + 1
    baseline = image[row][col] 

    while(new_col < image.shape[1]):
        if( color_diff(baseline, image[new_row][new_col]) > thresh ):
            break 
        new_col += 1

    if new_col == image.shape[1]:
        return new_col - 1
    return new_col 


def crops_and_colors(brg, image, thresh, crop_delta, color_delta):
    down = color_down(image, thresh)
    left = color_left(image, thresh)
    up = color_up(image, thresh)
    right = color_right(image, thresh)

    new_image = image.copy()    #so I can draw on the picture in testing

    #grab better color pixel
    downc =  image.shape[0]-1 if down + color_delta >= image.shape[0] else down + color_delta
    leftc =  0 if left - color_delta < 0 else left - color_delta
    upc = 0 if up - color_delta < 0 else up - color_delta 
    rightc = image.shape[1]-1 if right + color_delta >= image.shape[1] else right + color_delta 

    #color extracting 
    row = int(new_image.shape[0] / 2)
    col = int(new_image.shape[1] / 2)

    image_struct = { 'down': image[downc][col], 
        'left': image[row][leftc], 
        'up': image[upc][col], 
        'right': image[row][rightc] }

    #print(image_struct)

    #color drawing 
    #cv2.line(new_image,(col,row),(col,down),(255,0,0),1) #down
    #cv2.line(new_image,(col,row),(left,row),(255,0,0),1) #left
    #cv2.line(new_image,(col,row),(col,up),(255,0,0),1) #up
    #cv2.line(new_image,(col,row),(right,row),(255,0,0),1) #right

    #expand beyond color start for cropping purposes
    downd =  image.shape[0] if down + crop_delta > image.shape[0] else down + crop_delta
    leftd =  0 if left - crop_delta < 0 else left - crop_delta
    upd = 0 if up - crop_delta < 0 else up - crop_delta 
    rightd = image.shape[1] if right + crop_delta > image.shape[1] else right + crop_delta 

    #crop delta drawing
    #cv2.line(new_image,(col,down),(col,downd),(0,0,255),1) #down
    #cv2.line(new_image,(left,row),(leftd,row),(0,0,255),1) #left
    #cv2.line(new_image,(col,up),(col,upd),(0,0,255),1) #up
    #cv2.line(new_image,(right,row),(rightd,row),(0,0,255),1) #right

    newer_image = brg[upd:downd, leftd:rightd, :]  #y:y+h, x:x+w, z

    #plt.subplot(131),plt.imshow(image)
    #plt.subplot(132),plt.imshow(new_image)
    #plt.subplot(133),plt.imshow(newer_image)
    #plt.show()

    return image_struct, newer_image


def compile_mosaic(mosaic):
    #push everything down and left
    tallest = max( 
        mosaic['left_square'].shape[0],
        mosaic['rect_bot'].shape[0],
        mosaic['right_square'].shape[0],
        mosaic['rect_right'].shape[0]
    )
    widest = mosaic['top'].shape[1] if mosaic['top'].shape[1] > mosaic['rect_bot'].shape[1] else mosaic['rect_bot'].shape[1]
    
    image_top = cv2.copyMakeBorder(mosaic['top'],
        0,
        tallest,
        mosaic['left_square'].shape[1],
        widest-mosaic['top'].shape[1] + mosaic['right_square'].shape[1] + mosaic['rect_right'].shape[1],
        0)
    image_rect_bot = cv2.copyMakeBorder(mosaic['rect_bot'],
        tallest-mosaic['rect_bot'].shape[0] + mosaic['top'].shape[0],
        0,
        mosaic['left_square'].shape[1],
        widest-mosaic['rect_bot'].shape[1] + mosaic['right_square'].shape[1] + mosaic['rect_right'].shape[1],
        0)
    image_right_square = cv2.copyMakeBorder(mosaic['right_square'],
        tallest-mosaic['right_square'].shape[0] + mosaic['top'].shape[0],
        0,
        mosaic['left_square'].shape[1] + widest,
        mosaic['rect_right'].shape[1],
        0)
    image_rect_right = cv2.copyMakeBorder(mosaic['rect_right'],
        tallest-mosaic['rect_right'].shape[0] + mosaic['top'].shape[0],
        0,
        mosaic['left_square'].shape[1] + widest + mosaic['right_square'].shape[1],
        0,
        0)
    image_left_square = cv2.copyMakeBorder(mosaic['left_square'],
        tallest-mosaic['left_square'].shape[0] + mosaic['top'].shape[0],
        0,
        0,
        widest + mosaic['right_square'].shape[1] + mosaic['rect_right'].shape[1],
        0)

    shape = (tallest + mosaic['top'].shape[0],
        mosaic['left_square'].shape[1] + widest + mosaic['right_square'].shape[1] + mosaic['rect_right'].shape[1],
        3)
    final = np.zeros(shape, np.uint8)
    return final + image_top + image_rect_bot + image_right_square + image_rect_right + image_left_square


def image_folder_read(path):
    images = [ cv2.imread(path+j) for j in sorted( [i for i in os.listdir(path)] ) ]
    #if not(len(images) == 5):
    #    print('Incorrect number of images, there should be exactly 5')
    #    exit()
    return images 


def square_right(mosaic, image_struct, new_image):
    mosaic['right_square'] = {'image_struct': image_struct, 'image': new_image}


if __name__ == "__main__":
    path = './testing/'
    thresh = 10                     #difference from baseline saturation
    crop_delta = 100               #color overflow to edge
    color_delta = 25

    images = image_folder_read(path)
    
    mosaic = {}

    for i, image in enumerate(images):
        
        if i == 0:
            mosaic['top'] = image
        if i == 1:
            mosaic['rect_bot'] = image
        if i == 2: 
            mosaic['right_square'] = image
        if i == 3: 
            mosaic['rect_right'] = image
        if i == 4:
            mosaic['left_square'] = image

    final = compile_mosaic(mosaic)
    #final = cv2.cvtColor(final, cv2.COLOR_BGR2RGB)
    #plt.imshow(final)
    #plt.show()
    cv2.imwrite('./testing/done.png', final)