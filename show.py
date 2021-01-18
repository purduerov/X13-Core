from lxml import etree 
from io import StringIO
import os  
import cv2
from matplotlib import pyplot as plt

def findall():
    prefix = './labelled_images/'
    di = {}
    for xml in os.listdir(prefix):
        tree = etree.parse(prefix + xml)
        name = tree.findtext('./filename')
        xmin = tree.findtext('.//xmin')
        ymin = tree.findtext('.//ymin')
        xmax = tree.findtext('.//xmax')
        ymax = tree.findtext('.//ymax')
        di[name] = {'xmin': xmin, 'ymin': ymin, 'xmax': xmax, 'ymax': ymax}
    print(di)

def test():
    tree = etree.parse('./labelled_images/gray1.xml')
    name = tree.findtext('./filename')
    xmin = int(tree.findtext('.//xmin'))
    ymin = int(tree.findtext('.//ymin'))
    xmax = int(tree.findtext('.//xmax'))
    ymax = int(tree.findtext('.//ymax'))

    image = cv2.imread('./images/gray1.jpg')
    new_image = image.copy() 
    
    cv2.line(new_image, (xmin,ymin), (xmin, ymax), (0,255,0),1)
    cv2.line(new_image, (xmin,ymax), (xmax, ymax), (0,255,0),1)
    cv2.line(new_image, (xmin,ymin), (xmax, ymin), (0,255,0),1)
    cv2.line(new_image, (xmax,ymin), (xmax, ymax), (0,255,0),1)

    plt.subplot(121),plt.imshow(image,cmap='gray')
    plt.title('Original'), plt.xticks([]), plt.yticks([])
    plt.subplot(122),plt.imshow(new_image,cmap='gray')
    plt.title('Label'), plt.xticks([]), plt.yticks([])
    plt.show()

if __name__ == "__main__":
    test()