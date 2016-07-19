import random
import csv
import os

# Only these variables need to be modified
##################################################################
# number of lines in CSV file which corresponds to number of images
numlines = 100000
# number of boolean attributes we want per 'image'
numatt = 20
# our formula  (here for eg 2 V 5 V 7)
formula = [2, 5, 7, 13, 15]
# what error rate
epsilon = 0.05
###################################################################
# Only these variables need to be modified ^^^^^^



# a tuple of weight and corresponding value are passed into this fn
def weighted_random(pairs):
    total = sum(pair[0] for pair in pairs)
    r = random.randint(1, total)
    for (weight, value) in pairs:
        r -= weight
        if r <= 0:
            return value

# Create the Output folder
try:
    os.mkdir("Output")
except Exception:
    pass


# To make sure we have a sane formula
for x in formula:
    if x > numatt:
        raise Exception('The formula contains an attribute number that is greater than the number of attributes')

anoscorelist = []
header=[]

# Create the header for attributes csv
for len in range(numatt+1):
    if len == 0:
        header.append('')
    else:
        header.append("att" + str(len))



# Write the attributes CSV
with open('Output/syntheticdata_attributes.csv', 'wb') as myfile:
    wr = csv.writer(myfile, delimiter=',', quoting=csv.QUOTE_ALL)
    for i in range(numlines+1):
        if i == 0:
            wr.writerow(header)
        else:
            anoscore = random.uniform(1, 100)                # generate a random anomaly score
            imageatt = []                                    # initialize an array for the row
            imageatt.append("Image" + str(i))
            if anoscore < 75:                                # get a weighted boolean in case of non-anomaly
                probchoice = weighted_random([(1-epsilon, 0), (epsilon, 1)])
            for col in range(1,numatt+1):
                if (col in formula) and (anoscore < 75):
                    imageatt.append(probchoice)
                else:
                    att = random.randint(0, 1)
                    imageatt.append(att)
            anoscorelist.append(anoscore)
            wr.writerow(imageatt)
myfile.close()

# Write the anomaly score CSV
with open('Output/syntheticdata_anomalyscore.csv', 'wb') as myfile:
    wr = csv.writer(myfile, delimiter=',', quoting=csv.QUOTE_ALL)
    for i in range(numlines + 1):
        if i == 0:
            wr.writerow(['', "Anomaly Score"])
        else:
            wr.writerow(["Image" + str(i), anoscorelist[i-1]])
myfile.close()
