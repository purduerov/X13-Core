import matplotlib.pyplot as plt 
import math

def linelen(x):
    return math.sqrt( pow(x[3]-x[1], 2) + pow(x[2]-x[0], 2) )


#x1, y1, x2, y2
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
        return True, line3
    return False, line3


    '''
    #case x1,y1 of orth lie on line3
    if( (orth[0] <= max(line3[0], line3[2])) and (orth[0] >= min(line3[0], line3[2])) and (orth[1] <= max(line3[1], line3[3])) and (orth[1] <= max(line3[1], line3[3])) ):
        return True, line3
    #case x2,y2 of orth lie on line3
    if( (orth[2] <= max(line3[0], line3[2])) and (orth[2] >= min(line3[0], line3[2])) and (orth[3] <= max(line3[1], line3[3])) and (orth[3] <= max(line3[1], line3[3])) ):
        return True, line3
    #case line3 is inside of orth, test with one point on line3
    if( (line3[0] <= max(orth[0], orth[2])) and (line3[2] >= min(orth[0], orth[2])) and (line3[3] <= max(orth[1], orth[3])) and (line3[3] <= max(orth[1], orth[3])) ):
        return True, line3
    return False, line3
    '''





getx = lambda x: [x[0], x[2]]
gety = lambda y: [y[1], y[3]]

line0 = [1, 1, 5, 1]
line1 = [3, 2, 5, 2]
line2 = [4, 4, 4, 6]
line3 = [6, 4, 6, 6]
#line2 = para_project(line0, line1)

l0x = getx(line0)
l0y = gety(line0)
l1x = getx(line1)
l1y = gety(line1)
l2x = getx(line2)
l2y = gety(line2)
l3x = getx(line3)
l3y = gety(line3)


plt.plot(l0x, l0y, '--')
plt.plot(l1x, l1y, '--')
plt.plot(l2x, l2y, '--')
plt.plot(l3x, l3y, '--')
#plt.plot(line2[0], line2[1], marker='o', color='red')
#plt.plot(line2[2], line2[3], marker='o', color='red')
#stat, newline = ortho_project(line0, line1, line2)
#stat, newline = ortho_project(line0, line1, line3)
#stat, newline = ortho_project(line2, line3, line0)
stat, newline = ortho_project(line2, line3, line1)
newx = getx(newline)
newy = gety(newline)
print(stat)
plt.plot(newx, newy, '--')

plt.show()