import numpy as np
import cv2
import copy 
from scipy.signal import argrelextrema


#return specified number of unique hues of image sorted by descending frequency 
def get_palette_freq(image, num_colors):
    #np.unique will flatten input: this is good, but it's a ref not a deep copy, so it would mess up the image in the calling func
    temp = copy.deepcopy(image) 
    #unique values, their frequency
    image_palette, count = np.unique(temp, return_counts=True) 
    #above is sorted by value not freq; let's sort the freqs and then use those indices to sort the palette
    order = np.argsort(count)
    return image_palette[order[::-1]][:num_colors]


#return distinct unique hues of image 
def get_palette_distinct(image):
    #np.unique will flatten input: this is good, but it's a ref not a deep copy, so it would mess up the image in the calling func
    temp = copy.deepcopy(image) 
    #unique values, their frequency
    image_palette, count = np.unique(temp, return_counts=True) 
    #above is sorted by value not freq
    #to get distinct colors, we're going to find the local maxima in freq
    return image_palette[argrelextrema(count, np.greater)]
     

def modulo_diff(a, b):
    diff = abs(int(a) - int(b))
    if(diff < 180):
        return diff 
    return 360 - diff 


def quantize(hues, image_palette):
    mod = []
    for idx, row in enumerate(hues):
        print(mod)
        mod.append( [] )
        for hue in row:
            closest_color = image_palette[0]
            closest_dist = modulo_diff(hue, image_palette[0])
            for i in image_palette: #at the very least, this could be made into a binary search looking for the closest difference 
                diff = modulo_diff(hue, i)
                if(diff < closest_dist):
                    closest_dist = diff  
                    closest_color = i 
            mod[idx].append(closest_color)

    return np.array(mod)


if __name__ == "__main__":
    vcap = cv2.VideoCapture('http://127.0.0.1:8090/stream')

    while(True):
        # Capture frame-by-frame
        try:
            ret, frame = vcap.read()
        except:
            continue 

        #print cap.isOpened(), ret

        # Display the resulting frame if there is one 
        if frame is not None:
            img_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            hue = img_hsv[:, :, 0]
            cv2.imshow('frame', hue)
            image_palette = get_palette_distinct(hue)
            print(hue)
            print(image_palette)
            quant = quantize(hue, image_palette)
            cv2.imshow('frame', quant)

            # Press q to close the video windows before it ends if you want
            if cv2.waitKey(22) & 0xFF == ord('q'):
                break
        else:
            print("Frame is None; video is likely done")
            break

    # When everything is done, release the capture
    vcap.release()
    cv2.destroyAllWindows()
    print("Video stop")