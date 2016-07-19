import csv
from math import pow,log

#####################################
# Initialization Variables
mu = 1.00
epsilon = 0.2
anomalythreshold = 75.00
eta = 0.2
delta = 0.01
#####################################

########################################################
# Function to return the k-DNF that still holds
# Pass into the tolerant elimination algorithm the following parameters:
# mu - probability to find the anomaly
# epsilon - the error that we can tolerate (how man false positives vs how many tagged anomalies)
# anothresh - the threshold that we choose based on the anomaly score
# rowlen - the number of boolean attributes under consideration
# numrow - the number of images we are iterating through
# data - the 2D matrix which consists of the data
# Returns an array where the attribute number in the K-DNF will be 1
########################################################
def tolerantelim(mu, eps, anothresh, rowlen, numrow, data):
    falsepos = []               # Matrix that will store the false positive count
    C = []                      # Matrix that will store the attributes to be returned
    fin = []
    for z in range(rowlen-1):
        falsepos.append(0)
        C.append(1)

    for row in data:
        if float(row[rowlen]) < anothresh:
            for i in range(1, rowlen):
                if row[i] == '1':
                    falsepos[i-1] +=1
            for i in range(len(C)):
                if falsepos[i-1] > mu * eps * numrow:
                    C[i-1] = 0
    for pos in range(len(C)):
        if C[pos] == 1:
            fin.append(pos+1)
    return fin



def create_matrix(filename, matrix = None):
    tmp=0
    if matrix is None:
        matrix = []
        tmp = 1
    exampleFile = open(filename)
    exampleReader = csv.reader(exampleFile)
    rowcount = 0
    for row in exampleReader:
        if rowcount == 0:  # make sure that the header row is not appended to the matrix
            rowcount += 1
            rowlen = len(row)  # Get the length of the row to asses the number of attributes
        else:
            if tmp == 1:
                rowcount += 1
                matrix.append(row)  # Make a 2D array of the boolean data and store it in the array matrix
            else:
                matrix[rowcount - 1].append(row[1])  # Make a 2D array of the boolean data and store it in the array matrix
                rowcount += 1

    exampleFile.close()
    rowcount -= 1   # to eliminate the header row that was counted
    return matrix, rowcount, rowlen



def classifier_anocount( data, C):
    x = 0
    for row in data:
        tmp = 1
        for cnt in range(len(C)):
            tmp = tmp and row[C[cnt]]
        if tmp:
            x += 1
    return x




matrix, rowcount, rowlen = create_matrix('Synthetic_Data_Creation/Output/syntheticdata_attributes.csv')
matrix , elim1, elim2 = create_matrix('Synthetic_Data_Creation/Output/syntheticdata_anomalyscore.csv', matrix)

thetest = tolerantelim(mu, epsilon, anomalythreshold, rowlen, rowcount, matrix)


iternum = 1
deltai = delta
while ((classifier_anocount( matrix, thetest)/rowcount) < (mu/(1+eta))):
    var1 = (3.0*pow(1.0+eta, 2+iternum)*log((2.0*iternum*(iternum+1.0))/delta))/(pow(eta, 2))
    var2 = (3.0*log(2.0*(rowlen-1)/deltai))/(mu*epsilon*(1.0+eta)*pow(eta, 2))
    print "The iteration number is : " + str(iternum)
    print "Variable 1 is : " + str(var1)
    print "Variable 2 is : " + str(var2)
    print "mu : " + str(mu)
    print "Quaifying condition is : " + str(classifier_anocount(matrix, thetest)/float(rowcount)) +\
          " is less than " + str((mu/(1+eta)))

    if rowcount > var1 and rowcount > var2:
        mu = (mu / (1.0 + eta))
        deltai = deltai/(iternum*(iternum+1))
        iternum += 1
        thetest = tolerantelim(mu, epsilon, anomalythreshold, rowlen, rowcount, matrix)
        print "The attributes remaining in the formula are : " + str(thetest)
    else:
        print "An Optimal Classifier could not be found!!!!"
        break


# print classifier_anocount( matrix, thetest)
print "Last known classifier is : " + str(thetest)
print "Algorithm went through " + str(iternum) + " iterations"
print "The probability of strinking an image as anomaly is : " + str(mu)




