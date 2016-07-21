import math
import random
from PIL import Image
import numpy as np
import imagehash
from scipy.misc import imsave
import os
import matplotlib.pyplot as plt


"""
https://gist.github.com/iandanforth/5862470

"""

folder = "/home/tushar/PycharmProjects/Test/Kmeans/Camview"
#create a black jpg and get hashcode
img = np.zeros([100,100,3],dtype=np.uint8)
img.fill(0) # or img[:] = 255
imsave("Camview/Black.jpg",img)
hashblack = imagehash.average_hash(Image.open('Camview/Black.jpg'))
os.remove("Camview/Black.jpg")

#function to calculate the image hash and distance from "black"
def Imagehashdist(path):
    global hashblack
    hash = imagehash.average_hash((Image.open(path)))
    hashdist = hashblack - hash
    return pow(hashdist,2)

def rgbhashdist(path):
    img = Image.open(path).convert('RGBA')
    imgarr = np.array(img)
    rgbdist = np.linalg.norm(0 - imgarr)
    return rgbdist


def main():
    list = []
    dict = {}
    for filename in os.listdir(folder):
        innerlist = []
        # tup = ((int(Imagehashdist("Camview/" + filename))),int(rgbhashdist("Camview/" + filename)))
        innerlist.append(float(Imagehashdist("Camview/" + filename)))
        innerlist.append(float(rgbhashdist("Camview/" + filename)))
        list.append(innerlist)
        dict.update({str(filename):innerlist})
        #print str(filename) +"\t:" + str(innerlist)
        #print str(filename)
    #print dict.keys()[dict.values().index(list[2])]

    # point dimension
    dimensions = 2

    # How many clusters do we need
    num_clusters = 4

    # convergence point
    opt_cutoff = 6

    pointstest = [makeRandomPoint(dimensions, value) for key,value  in dict.iteritems()]

    # Cluster those data!
    clusters = kmeans(pointstest, num_clusters, opt_cutoff)

    # print the centroids
    for i, c in enumerate(clusters):
        print c.centroid
    # Print our clusters
    colors = {0:"red" , 1:"green", 2:"blue", 3:"yellow"}
    for i, c in enumerate(clusters):
        x=[]
        y=[]
        for p in c.points:
            x.append(p.coords[0])
            y.append(p.coords[1])
            name = dict.keys()[dict.values().index(p.coords)]
            print " Cluster: ", i, "\t", str(name) ,  "\t Point :", p
        plt.scatter(x, y, c=colors[i])
    plt.show()

#create class point based on dimension
class Point:

    def __init__(self, coords):

        #coords - A list of values, one per dimension

        self.coords = coords
        self.n = len(coords)

    def __repr__(self):
        return str(self.coords)


# this class will define a set of points and their centroid
class Cluster:


    def __init__(self, points):
        # point ibjects
        if len(points) == 0: raise Exception("ILLEGAL: empty cluster")
        # The points that belong to this cluster
        self.points = points
        self.centroid = self.calculateCentroid()

    def __repr__(self):
        #string rep of points
        return str(self.points)

    def update(self, points):

        #Returns the distance between the previous centroid and the new after
        #recalculating and storing the new centroid.

        old_centroid = self.centroid
        self.points = points
        self.centroid = self.calculateCentroid()
        shift = getDistance(old_centroid, self.centroid)
        return shift

    def calculateCentroid(self):

        #Finds a virtual center point for a group of n-dimensional points

        numPoints = len(self.points)
        # Get a list of all coordinates in this cluster
        coords = [p.coords for p in self.points]
        # Reformat that so all x's are together, all y'z etc.
        unzipped = zip(*coords)
        # Calculate the mean for each dimension
        centroid_coords = [math.fsum(dList) / numPoints for dList in unzipped]

        return Point(centroid_coords)


def kmeans(points, k, cutoff):
    # Pick out k random points to use as our initial centroids
    initial = random.sample(points, k)

    # Create k clusters using those centroids
    clusters = [Cluster([p]) for p in initial]

    # Loop through the dataset until the clusters stabilize
    loopCounter = 0
    while True:
        # Create a list of lists to hold the points in each cluster
        lists = [[] for c in clusters]
        clusterCount = len(clusters)

        # Start counting loops
        loopCounter += 1
        # For every point in the dataset ...
        for p in points:
            # Get the distance between that point and the centroid of the first
            # cluster.
            smallest_distance = getDistance(p, clusters[0].centroid)

            # Set the cluster this point belongs to
            clusterIndex = 0

            # For the remainder of the clusters ...
            for i in range(clusterCount - 1):
                # calculate the distance of that point to each other cluster's
                # centroid.
                distance = getDistance(p, clusters[i + 1].centroid)
                # If it's closer to that cluster's centroid update what we
                # think the smallest distance is, and set the point to belong
                # to that cluster
                if distance < smallest_distance:
                    smallest_distance = distance
                    clusterIndex = i + 1
            lists[clusterIndex].append(p)

        # Set our biggest_shift to zero for this iteration
        biggest_shift = 0.0

        # As many times as there are clusters ...
        for i in range(clusterCount):
            # Calculate how far the centroid moved in this iteration
            shift = clusters[i].update(lists[i])
            # Keep track of the largest move from all cluster centroid updates
            biggest_shift = max(biggest_shift, shift)

        # If the centroids have stopped moving much, say we're done!
        if biggest_shift < cutoff:
            print "Converged after %s iterations" % loopCounter
            break
    return clusters


def getDistance(a, b):

    #Euclidean distance between two n-dimensional points.

    if a.n != b.n:
        raise Exception("ILLEGAL: non comparable points")

    #ret = reduce(lambda x, y: x + pow((a.coords[y] - b.coords[y]), 2), range(a.n), 0.0)
    #for two points
    ret = pow((a.coords[0]-b.coords[0]),2) + pow((a.coords[1]-b.coords[1]),2)
    #print math.sqrt(ret)
    return math.sqrt(ret)


def makeRandomPoint(n, thepoint):#n is number of dimensions

    # Returns a Point object with n dimensions and values
    p = Point(thepoint)
    #print list
    return p


if __name__ == "__main__":
    main()