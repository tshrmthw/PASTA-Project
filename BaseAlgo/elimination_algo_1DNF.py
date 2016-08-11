import csv
from math import pow,log
from codecs import open


#####################################
# Initialization Variables
def varinit():
  global mu
  mu = 0.4
  global epsilon           # for 21656 use 0.027, 269 = 0.17
  epsilon = 0.017  # fraction of epsilon that we can classify as anomaly (0.06-0.1)
  global anomalythreshold
  anomalythreshold = 0.53
  global eta #0.2
  eta = 2
  global delta
  delta = 0.05
  # global mu = (1.00+epsilon)*0.04
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
    fin = []                    # Matrix that contains the positions of the attributes
    for z in range(rowlen-1):
        falsepos.append(0)
        C.append(1)

    for row in data:

        if float(row[rowlen]) < anothresh:      # To single out the non-anomalies
            for i in range(1, rowlen):          # In each row tagged as non-anomalous, find the atts that are positive
                if row[i] == '1':               # and increment the false positive count of that attribute
                    falsepos[i-1] +=1
            for i in range(len(C)):                         # Check if the false positive count of any of the attributes
                if falsepos[i-1] > mu * eps * numrow:       # exceeds our threshold and if it does, then remove it from
                    C[i-1] = 0                              # our final formula
    # print falsepos
    print  "the false pos bound is  : " + str(mu * eps * numrow)
    for pos in range(len(C)):
        if C[pos] == 1:
            fin.append(pos+1)
    return fin

#####################################
# funtion to create a list of lists 
# which contains the rows of the 
# attribute CSV along with the
# PCA value appended at the end
# May or may not need to pass the matrix
######################################
def create_matrix(filename, matrix = None):
    tmp=0
    header = []
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
            if tmp == 1:
                header = row

            # print rowlen
            # print rowcount
        else:
            if tmp == 1:
                rowcount += 1
                matrix.append(row)  # Make a 2D array of the boolean data and store it in the array matrix
            else:

                matrix[rowcount - 1].append(row[rowlen-1])  # Make a 2D array of the boolean data and store it in the array matrix
                rowcount += 1

    exampleFile.close()
    rowcount -= 1   # to eliminate the header row that was counted
    return matrix, rowcount, rowlen, header

###############################
# funtion to count the number
# images that we classify as
# anomalies based on the rule
# that has been created and found
# by the last iteration of the
# tolerant elimination algorithm
################################
def classifier_anocount( data, C):
    x = 0
    for row in data:
        tmp = 0
        for cnt in C:       # OR all the attributes in each row contained in the returned formula C
            tmp = bool(tmp) or bool(row[cnt] == '1')
        if tmp:
            x += 1

    return x

########################################
# Funtion to get the final error rate of 
# of the classifier that is passed into 
# it along with the attribute data matrix
########################################
def errorrate(matrix , classifier):
      total_anomalies = 0.00
      total_false_anomalies = 0.00
      for row in matrix:
          pca = len(row)-1
          tmp = 0
          for x in classifier:
              tmp = bool(tmp) or bool(row[x] == '1')
          if tmp:
              total_anomalies+=1.00
              # print row[pca]
              if float(row[pca]) < 0.53:
                  total_false_anomalies+=1.00
          # elif (not tmp) and float(row[pca]) > 0.53:  # test to print out the 
              # print str(row[pca])                     # anomaly scores of those 
                                                        # images that rule did not pick up
      return total_false_anomalies/total_anomalies 


# Main Method
if __name__ == '__main__':
    "This code runs when you invoke the script from the command line"
    # Get the data as matrices
    varinit()
    matrix, rowcount, rowlen, labels= create_matrix('269/binary-269.csv')
    matrix, elim1, elim2 , elim3= create_matrix('269/PCA-269.csv', matrix)

    # Run the first iteration of tolerant elimination and set the iternation number
    thetest = tolerantelim(mu, epsilon, anomalythreshold, rowlen, rowcount, matrix)
    iternum = 1
    deltai = delta

    # the major loop that executes in order to check if we have reached a favourable classification rule
    while ((float(classifier_anocount(matrix, thetest))/float(rowcount)) < (mu/(1+eta))):
        var1 = (3.0*pow(1.0+eta, 2+iternum)*log((2.0*iternum*(iternum+1.0))/delta))/(pow(eta, 2))
        var2 = (3.0*log(2.0*(rowlen-1)/deltai))/(mu*epsilon*(1.0+eta)*pow(eta, 2))
        print "The iteration number is : " + str(iternum)
        print "Variable 1 is : " + str(var1)
        print "Variable 2 is : " + str(var2)
        print "mu : " + str(mu)
        print "Quaifying condition of while loop : " + str(classifier_anocount(matrix, thetest)/float(rowcount)) +\
              " is less than " + str((mu/(1+eta)))
        # Boundarycheck conditions based on theoretical calculations for validity
        if rowcount > var1 and rowcount > var2:
            mu = (mu / (1.0 + eta))
            deltai = deltai/(iternum*(iternum+1))
            iternum += 1
            thetest = tolerantelim(mu, epsilon, anomalythreshold, rowlen, rowcount, matrix)
            print "The attributes remaining in the formula are : " + str(thetest)
        else:
            raise ValueError('An Optimal Classifier could not be found!!!!')
            break
    # Create a list which contains the labels that are a part of the rule that was found
    finalclassifier = []
    for count in thetest:
        finalclassifier.append(labels[count])
    
    
    # printing out the results
    print "\n--------------A RESULT HAS BEEN FOUND!!!!!!---------------"
    print "Out of " + str(len(labels)-1) + " attributes, " + str(len(finalclassifier)) + " attriutes are in the final" \
                                                                                         " classifier"
    print "Last known classifier is : " + str(finalclassifier)
    print "Algorithm went through " + str(iternum) + " iterations"
    print "The probability of striking an image as anomaly is : " + str(mu)
    print "The Error rate is : " + str(errorrate(matrix , thetest))
         

