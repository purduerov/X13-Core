import matplotlib.pyplot as plt 
import math

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

    return line3 

getx = lambda x: [x[0], x[2]]
gety = lambda y: [y[1], y[3]]

line0 = [1, 2, 4, 4]
line1 = [2, 6, 5, 8]
line2 = para_project(line0, line1)

l0x = getx(line0)
l1x = getx(line1)
l0y = gety(line0)
l1y = gety(line1)

plt.plot(l0x, l0y, '--')
plt.plot(l1x, l1y, '--')
plt.plot(line2[0], line2[1], marker='o', color='red')
plt.plot(line2[2], line2[3], marker='o', color='red')
plt.show()