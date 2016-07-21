from PIL import Image
import numpy as np
import imagehash
from scipy.misc import imsave
import os

folder = "/home/tushar/PycharmProjects/Test/Kmeans/Camview"
#create a black jpg and get hashcode
img = np.zeros([100,100,3],dtype=np.uint8)
img.fill(0) # or img[:] = 255
imsave("Camview/Black.jpg",img)
hashblack = imagehash.dhash(Image.open('Camview/Black.jpg'))
os.remove("Camview/Black.jpg")

#function to calculate the image hash and distance from "black"
def Imagehashdist(path):
    global hashblack
    hash = imagehash.dhash(Image.open(path))
    hashdist = hashblack - hash
    return hashdist

def rgbhashdist(path):
    img = Image.open(path).convert('RGBA')
    imgarr = np.array(img)
    rgbdist = np.linalg.norm(0 - imgarr)
    return rgbdist
list=[]
for filename in os.listdir(folder):
    innerlist = []
    #tup = ((int(Imagehashdist("Camview/" + filename))),int(rgbhashdist("Camview/" + filename)))
    innerlist.append(float(Imagehashdist("Camview/" + filename)))
    innerlist.append(float(rgbhashdist("Camview/" + filename)))
    list.append(innerlist)
    #print str(Imagehashdist("Camview/" + filename)) + ", " + str(rgbhashdist("Camview/" + filename))

print list







