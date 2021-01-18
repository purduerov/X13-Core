import matplotlib.pyplot as plt 
import math 
import numpy as np
from matplotlib import pyplot as plt
import cv2
import imutils

tolerance = .2
perimeter_percentage = .5
resolution = 300
edge_tolerance = 10

def linelen(x):
    return math.sqrt( pow(x[3]-x[1], 2) + pow(x[2]-x[0], 2) )

#x1, y1, x2, y2
def para_project(line1, line2):
    A = line1[0] - line2[0]
    B = line1[1] - line2[1]
    C = line2[2] - line2[0]
    D = line2[3] - line2[1]
    dot = A * C + B * D
    len_sq = C * C + D * D 
    param = dot / len_sq 
    newx = line2[0] + param * C
    newy = line2[1] + param * D 
    deltax = newx - line1[0]
    deltay = newy - line1[1]
    line3 = [line1[0]+deltax, line1[1]+deltay, line1[2]+deltax, line1[3]+deltay]
    
    bigli = [ [line3[0], line3[1], line2[0], line2[1]], [line3[0], line3[1], line2[2], line2[3]], [line3[2], line3[3], line2[0], line2[1]], [line3[2], line3[3], line2[2], line2[3]], line3, line2 ] 
    maxlen = 0
    for trycoords in bigli:  
        templen = linelen(trycoords)
        if(templen > maxlen): 
            maxlen = templen 
            coords = trycoords
    line4 = coords

    if( (linelen(line3) + linelen(line2)) >= linelen(line4) ):
        return True
    return False
        

def find_slope(x):
    if(x[2] == x[0]):
        return np.nan 
    return (x[3]-x[1])/(x[2]-x[0])


def find_parallels(slopes, lines):
    di = {}
    for idx, slope in enumerate(slopes):
        for jdx, pair in enumerate(slopes):
            #if (jdx > idx): #no symmetry
            if not (jdx == idx): 
                if( (np.isnan(slope) and np.isnan(pair)) or (abs(slope - pair) <= tolerance) ):  #is parallel
                    if( para_project(lines[idx], lines[jdx]) ):
                        di_li_add(di, idx, jdx)
    return di


def di_li_add(di, i, j):
    if(i in di.keys()):
        if(j not in di[i]):
            di[i].append(j)
    else:
        di[i] = [j]


def find_orthos(keep, slopes, lines):
    stuff = {}
    for line in keep:
        for idx, slope in enumerate(slopes):
            #if(idx > line): #no symmetry
            if(np.isnan(slopes[line])):
                if(slope == 0):

                    for i in keep[line]:
                        if( ortho_project( lines[line], lines[i], lines[idx] ) ):
                            if not(idx in stuff):
                                stuff[idx] = set()
                                stuff[idx].add( frozenset([line, i]) )
                            else: 
                                stuff[idx].add( frozenset([line, i]) )
                    
            elif(slopes[line] == 0):
                if(np.isnan(slope)):
                    
                    for i in keep[line]:
                        if( ortho_project( lines[line], lines[i], lines[idx] ) ):
                            if not(idx in stuff):
                                stuff[idx] = set()
                                stuff[idx].add( frozenset([line, i]) )
                            else: 
                                stuff[idx].add( frozenset([line, i]) )

            elif( abs(slopes[line] * slope + 1) <= tolerance ):   #orthogonal

                for i in keep[line]:
                    if( ortho_project( lines[line], lines[i], lines[idx] ) ):
                        if not(idx in stuff):
                            stuff[idx] = set()
                            stuff[idx].add( frozenset([line, i]) )
                        else: 
                            stuff[idx].add( frozenset([line, i]) )

    return stuff


def ortho_project(para1, para2, orth):
    A = para1[0] - orth[0]
    B = para1[1] - orth[1]
    C = orth[2] - orth[0]
    D = orth[3] - orth[1]
    dot = A * C + B * D
    len_sq = C * C + D * D 
    param = dot / len_sq 
    newx1 = orth[0] + param * C
    newy1 = orth[1] + param * D 

    A = para2[0] - orth[0]
    B = para2[1] - orth[1]
    C = orth[2] - orth[0]
    D = orth[3] - orth[1]
    dot = A * C + B * D
    len_sq = C * C + D * D 
    param = dot / len_sq 
    newx2 = orth[0] + param * C
    newy2 = orth[1] + param * D 

    line3 = [newx1, newy1, newx2, newy2]
    bigli = [ [line3[0], line3[1], orth[0], orth[1]], [line3[0], line3[1], orth[2], orth[3]], [line3[2], line3[3], orth[0], orth[1]], [line3[2], line3[3], orth[2], orth[3]], orth, line3 ] 
    maxlen = 0
    for trycoords in bigli:  
        templen = linelen(trycoords)
        if(templen > maxlen): 
            maxlen = templen 
            coords = trycoords
    line4 = coords

    if( (linelen(line3) + linelen(orth)) >= linelen(line4) ):
        return True
    return False


def show_desired_rect(lines, done, picture):
    max_perim = 0
    biggest = []
    coords = []
    for i,j,k,l in done:
        minx = min( lines[i][0], lines[i][2], lines[j][0], lines[j][2], lines[k][0], lines[k][2], lines[l][0], lines[l][2] )
        maxx = max( lines[i][0], lines[i][2], lines[j][0], lines[j][2], lines[k][0], lines[k][2], lines[l][0], lines[l][2] )
        miny = min( lines[i][1], lines[i][3], lines[j][1], lines[j][3], lines[k][1], lines[k][3], lines[l][1], lines[l][3] )
        maxy = max( lines[i][1], lines[i][3], lines[j][1], lines[j][3], lines[k][1], lines[k][3], lines[l][1], lines[l][3] )
        perimeter = (maxx - minx) * 2 + (maxy - miny) * 2
        tot = linelen(lines[i]) + linelen(lines[j]) + linelen(lines[k]) + linelen(lines[l]) 
        if( tot / perimeter > max_perim ):
            max_perim = tot / perimeter 
            biggest = [i,j,k,l]
            coords = [minx, maxx, miny, maxy]
    if(max_perim < perimeter_percentage):
        print('No confidence in any rectangles')
        return
    expand = 10
    topx = 300
    topy = 205
    coords = [max(coords[0]-expand,0), min(coords[1]+expand,topx), max(coords[2]-expand,0), min(coords[3]+expand,topy)]
    crop_picture = picture[coords[2]:coords[3], coords[0]:coords[1]]
    print('perimeter ratio: ' + str(max_perim))
    plt.imshow(crop_picture,cmap = 'gray')


    plt.imshow(picture,cmap = 'gray')
    
    l1x = [ lines[biggest[0]][0], lines[biggest[0]][2] ]
    l1y = [ lines[biggest[0]][1], lines[biggest[0]][3] ]
    l2x = [ lines[biggest[1]][0], lines[biggest[1]][2] ]
    l2y = [ lines[biggest[1]][1], lines[biggest[1]][3] ]
    l3x = [ lines[biggest[2]][0], lines[biggest[2]][2] ]
    l3y = [ lines[biggest[2]][1], lines[biggest[2]][3] ]
    l4x = [ lines[biggest[3]][0], lines[biggest[3]][2] ]
    l4y = [ lines[biggest[3]][1], lines[biggest[3]][3] ]
    plt.plot(l1x, l1y, '--')
    plt.plot(l2x, l2y, '--')
    plt.plot(l3x, l3y, '--')
    plt.plot(l4x, l4y, '--')
    
    plt.show()
    return coords


def show_all_rects(lines, done, picture):
    #count = 0
    plt.imshow(picture, cmap='gray')
    for i,j,k,l in done:
        #if(count == 30):
        #    break
        #count += 1
        l1x = [ lines[i][0], lines[i][2] ]
        l1y = [ lines[i][1], lines[i][3] ]
        l2x = [ lines[j][0], lines[j][2] ]
        l2y = [ lines[j][1], lines[j][3] ]
        l3x = [ lines[k][0], lines[k][2] ]
        l3y = [ lines[k][1], lines[k][3] ]
        l4x = [ lines[l][0], lines[l][2] ]
        l4y = [ lines[l][1], lines[l][3] ]
        plt.plot(l1x, l1y, '--')
        plt.plot(l2x, l2y, '--')
        plt.plot(l3x, l3y, '--')
        plt.plot(l4x, l4y, '--')

    plt.show()
    

def print_pairs(keep, lines, picture):  #unused helper func
    for key in keep:
        print(key)
        for val in keep[key]:
            plt.imshow(picture, cmap='gray')
            l1x = [ lines[key][0], lines[key][2] ]
            l1y = [ lines[key][1], lines[key][3] ]
            l2x = [ lines[val][0], lines[val][2] ]
            l2y = [ lines[val][1], lines[val][3] ]
            plt.plot(l1x, l1y, '--')
            plt.plot(l2x, l2y, '--')
            plt.show()


def merge_dicts(keep, maybekeep):
    for key in maybekeep:
        for val in maybekeep[key]:
            di_li_add(keep, key, val)


def invert(slope):
    if(np.isnan(slope)):
        return 0
    elif(slope == 0):
        return np.nan
    else:
        return 1 / slope


def operate(lines, picture):
    slopes = np.apply_along_axis( find_slope, 1, lines )
    flag = False
    if(np.isnan(slopes[0])):      #vectorize doesn't work when first element is nan, numpy is broken 
        slopes[0] = 1
        flag = True
    inverter = np.vectorize(invert)
    inv_slopes = inverter(slopes)
    if(flag):
        slopes[0] = np.nan 
        inv_slopes[0] = 0

    #para: [para1,para2...]
    keep = find_parallels(slopes, lines)
    maybekeep = find_parallels(inv_slopes, lines)   #necessary to get parallels for nan and toleranced to nan
    merge_dicts(keep, maybekeep)
    
    #print_pairs(keep, lines, picture)
    
    #ortho: para para
    threes = find_orthos(keep, slopes, lines)

    done = set()
    for ortho in threes:
        if(ortho in keep):  #if ortho has a parallel
            for para1, para2 in threes[ortho]:
                for testortho in keep[ortho]:
                    if( ortho_project(lines[para1], lines[para2], lines[testortho]) and ortho_project(lines[testortho], lines[ortho], lines[para1]) and ortho_project(lines[testortho], lines[ortho], lines[para2]) ):
                        done.add( frozenset([ortho, para1, para2, testortho]) )
    if(done):
        show_all_rects(lines, done, picture)
        coords = show_desired_rect(lines, done, picture)
        return coords
    else:
        print('Oops')
        return None
    

def get_lines(maybe):
    image = cv2.imread('./photos/gray183.jpg', -1) 
    
    if maybe is not None:
        image = maybe
    
    resized = imutils.resize(image, width=resolution)
    #ratio = image.shape[0] / float(resized.shape[0])
    new_image = resized.copy()

    edges = cv2.Canny(resized, 10, 100, 3, L2gradient=True)

    #Hough
    #lines = np.squeeze(cv2.HoughLinesP(edges, 1, np.pi/30, 30, minLineLength=25, maxLineGap=5))
    lines = np.squeeze(cv2.HoughLinesP(edges, 1, np.pi/30, 20, minLineLength=25, maxLineGap=10))
   
    #this gets rid of lines drawn on the edges of the image
    toremove = []
    for idx, nums in enumerate(lines):
        for jdx, num in enumerate(nums):
            if(jdx & 1): #ys
                if(num < edge_tolerance or num > resized.shape[0]-edge_tolerance):
                    toremove.append(idx)
                    break
            else: #xs
                if(num < edge_tolerance or num > resolution-edge_tolerance):
                    toremove.append(idx)
                    break
    lines = np.delete(lines, (toremove), 0)
    
    #this is to show edges + hough lines 
    for li in lines:
        x1, y1, x2, y2 = li
        cv2.line(new_image,(x1,y1),(x2,y2),(0,255,0),1)
    
    plt.subplot(131),plt.imshow(image,cmap = 'gray')
    plt.title('Original Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(132),plt.imshow(edges,cmap = 'gray')
    plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(133),plt.imshow(new_image,cmap = 'gray')
    plt.title('Hough Image'), plt.xticks([]), plt.yticks([])
    plt.show()
    

    return lines, resized 


if __name__ == "__main__":
    lines, resized = get_lines(None)
    operate(lines, resized)
