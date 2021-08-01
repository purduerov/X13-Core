import matplotlib.pyplot as plt 
import math 
import numpy as np
from matplotlib import pyplot as plt
import cv2
import imutils

tolerance = .2

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
    
    bigli = [ [line3[0], line3[1], line2[0], line2[1]], [line3[0], line3[1], line2[2], line2[3]], [line3[2], line3[3], line2[0], line2[1]], [line3[2], line3[3], line2[2], line2[3]] ] 
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
    #case x1,y1 of orth lie on line3
    if( (orth[0] <= max(line3[0], line3[2])) and (orth[0] >= min(line3[0], line3[2])) and (orth[1] <= max(line3[1], line3[3])) and (orth[1] <= max(line3[1], line3[3])) ):
        return True
    #case x2,y2 of orth lie on line3
    if( (orth[2] <= max(line3[0], line3[2])) and (orth[2] >= min(line3[0], line3[2])) and (orth[3] <= max(line3[1], line3[3])) and (orth[3] <= max(line3[1], line3[3])) ):
        return True
    #case line3 is inside of orth, test with one point on line3
    if( (line3[0] <= max(orth[0], orth[2])) and (line3[2] >= min(orth[0], orth[2])) and (line3[3] <= max(orth[1], orth[3])) and (line3[3] <= max(orth[1], orth[3])) ):
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
    
    crop_picture = picture[coords[2]:coords[3], coords[0]:coords[1]]

    #plt.imshow(crop_picture,cmap = 'gray')
    
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
    
#19,21, want 23
def print_pairs(keep, lines, picture):
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

def operate(lines, picture):
    slopes = np.apply_along_axis( find_slope, 1, lines )
    keep = find_parallels(slopes, lines)

    print(keep)
    print(slopes[19])
    print(slopes[21])
    print(slopes[23])
    print_pairs(keep, lines, picture)
    '''
    #ortho: para para
    threes = find_orthos(keep, slopes, lines)

    done = set()
    for ortho in threes:
        if(ortho in keep):
            for para1, para2 in threes[ortho]:
                for testortho in keep[ortho]:
                    if( ortho_project(lines[para1], lines[para2], lines[testortho]) ):
                        done.add( frozenset([ortho, para1, para2, testortho]) )
    if(done):
        show_all_rects(lines, done, picture)
        #show_desired_rect(lines, done, picture)
    else:
        print('Oops')
    '''

def get_lines():
    #image = cv2.imread('../photos/box3crop.png', -1) #bad angle
    image = cv2.imread('../photos/box2crop.png', -1) #bad angle
    #image = cv2.imread('../photos/Capture.png', -1) #alright
    #image = cv2.imread('../photos/five.jpg', -1) #land image
    #image = cv2.imread('../photos/four.jpg', -1) #land image
    #image = cv2.imread('../photos/one.jpg', -1) #land image
    #image = cv2.imread('../photos/paper1.jpg', -1) #land image
    #image = cv2.imread('../photos/paper2.jpg', -1) #land image
    #image = cv2.imread('../photos/paper3.jpg', -1) #land image
    #image = cv2.imread('../photos/three.jpg', -1) #land image
    #image = cv2.imread('../photos/two.jpg', -1) #land image

    resized = imutils.resize(image, width=300)
    #ratio = image.shape[0] / float(resized.shape[0])
    new_image = resized.copy()
    edges = cv2.Canny(resized, 10, 100, 3, L2gradient=True)
    #Hough
    minLineLength = 250
    maxLineGap = 5
    #lines = np.squeeze(cv2.HoughLinesP(edges,3,np.pi/30,30,minLineLength,maxLineGap))
    lines = np.squeeze(cv2.HoughLinesP(edges, 1, np.pi/30, 30, minLineLength=25, maxLineGap=5))

    for li in lines:
        x1, y1, x2, y2 = li
        cv2.line(new_image,(x1,y1),(x2,y2),(0,255,0),1)
    cv2.line(new_image,(3,3),(53,3),(0,255,0),1)

    #cv2.line(new_image,(200,1),(201,101),(0,255,0),1)
    
    plt.subplot(131),plt.imshow(image,cmap = 'gray')
    plt.title('Original Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(132),plt.imshow(edges,cmap = 'gray')
    plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(133),plt.imshow(new_image,cmap = 'gray')
    plt.title('Hough Image'), plt.xticks([]), plt.yticks([])
    plt.show()
    
    return lines, resized 


if __name__ == "__main__":
    #line1 = [1, 0, 1, 3]
    #line2 = [3, 2, 3, 4]
    #line3 = [5, 3, 5, 5]
    #line4 = [1, 5, 2, 5]
    #line5 = [4, 5, 5, 5]
    #line6 = [3, 1, 5, 1]
    #lines = np.array([line1, line2, line3, line4, line5, line6])
    lines, resized = get_lines()
    operate(lines, resized)
