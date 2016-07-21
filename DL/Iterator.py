# load the different libraries
import numpy as np
import caffe
import os.path
import csv

# Set the computation mode CPU
caffe.set_mode_cpu()

# Load the net
net = caffe.Net('models/googlenet_places205/deploy_places205.protxt',
                'models/googlenet_places205/googlelet_places205_train_iter_2400000.caffemodel',
                caffe.TEST)

# load input and configure preprocessing
transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})

transformer.set_mean('data', np.load('models/placesCNN/places205CNN_mean.npy').mean(1).mean(1))

transformer.set_transpose('data', (2,0,1))

transformer.set_channel_swap('data', (2,1,0))

transformer.set_raw_scale('data', 255.0)

folder = "/home/tushar/PycharmProjects/Test/images/Scenes"
with open('outputfile_googlenet.csv', 'wb') as myfile:
    wr = csv.writer(myfile,  delimiter=',', quoting=csv.QUOTE_ALL)
    for filename in os.listdir(folder):
        #Load image
        im = caffe.io.load_image("images/Scenes/"+filename)
        net.blobs['data'].data[...] = transformer.preprocess('data', im)

        #compute through the net
        out = net.forward()

        labels = np.loadtxt("models/placesCNN/categoryIndex_places205.csv", str, delimiter='\t')
        # print labels
        top_k = net.blobs['prob'].data[0].flatten().argsort()[-1:-6:-1]
        wr.writerow([filename, str(labels[top_k])])		#write the filename and the labels
        #print filename + ":\t"
        #print str(labels[top_k])
