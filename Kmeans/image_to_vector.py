import numpy as np
import Image

imgA = Image.open('camview1.jpg').convert('RGBA')
imgB = Image.open('camview2.jpg').convert('RGBA')
arrA = np.array(imgA)
arrB = np.array(imgB)
distA = np.linalg.norm(0-arrA)
distB = np.linalg.norm(0-arrB)

print dist


# record the original shape
shape = arrA.shape

# make a 1-dimensional view of arr
flat_arr = arrA.ravel()

# convert it to a matrix
vector = np.matrix(flat_arr)

# do something to the vector
vector[:,::10] = 128

# reform a numpy array of the original shape
arr2 = np.asarray(vector).reshape(shape)

# calculate the distance
# dist = numpy.linalg.norm(a-b)

# make a PIL image
img2 = Image.fromarray(arrB, 'RGBA')
img2.show()
# print arr2