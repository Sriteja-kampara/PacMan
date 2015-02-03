# naiveBayes.py
# -------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

import util
import classificationMethod
import math

class NaiveBayesClassifier(classificationMethod.ClassificationMethod):
  """
  See the project description for the specifications of the Naive Bayes classifier.

  Note that the variable 'datum' in this code refers to a counter of features
  (not to a raw samples.Datum).
  """
  def __init__(self, legalLabels):
    self.legalLabels = legalLabels
    self.type = "naivebayes"
    self.k = 1 # this is the smoothing parameter, ** use it in your train method **
    self.automaticTuning = False # Look at this flag to decide whether to choose k automatically ** use this in your train method **

  def setSmoothing(self, k):
    """
    This is used by the main method to change the smoothing parameter before training.
    Do not modify this method.
    """
    self.k = k

  def train(self, trainingData, trainingLabels, validationData, validationLabels):
    """
    Outside shell to call your method. Do not modify this method.
    """

    # might be useful in your code later...
    # this is a list of all features in the training set.

    self.features = list(set([ f for datum in trainingData for f in datum.keys() ]));

    if (self.automaticTuning):
        kgrid = [0.001, 0.01, 0.05, 0.1, 0.5, 1, 5, 10, 20, 50]
        #kgrid = [5]
    else:
        kgrid = [self.k]

    self.trainAndTune(trainingData, trainingLabels, validationData, validationLabels, kgrid)

  def trainAndTune(self, trainingData, trainingLabels, validationData, validationLabels, kgrid):
    """
    Trains the classifier by collecting counts over the training data, and
    stores the Laplace smoothed estimates so that they can be used to classify.
    Evaluate each value of k in kgrid to choose the smoothing parameter
    that gives the best accuracy on the held-out validationData.

    trainingData and validationData are lists of feature Counters.  The corresponding
    label lists contain the correct label for each datum.

    To get the list of all possible features or labels, use self.features and
    self.legalLabels.
    """
    "*** YOUR CODE HERE ***"

    '''
    # FOR MANUAL ANALYSIS
    The result is based upon the number of 1s in a data set.
    allTrainingFeatures = [ (0,0), (0,1), (0,2)]
    allLabels = [0,1,2]
    trainingData = [{(0, 0): 0, (0, 1): 0, (0, 2): 0},
                    {(0, 0): 1, (0, 1): 0, (0, 2): 0},
                    {(0, 0): 0, (0, 1): 1, (0, 2): 1},
                    {(0, 0): 1, (0, 1): 1, (0, 2): 0},
                    {(0, 0): 0, (0, 1): 0, (0, 2): 1}]
    trainingLabels = [0, 1, 2, 2, 1]
    '''

    allLabels = self.legalLabels
    allTrainingFeatures = [ f for datum in trainingData for f in datum.values() ];
    numOfAllLabels = len(allLabels)
    numOfTrainingData = len(trainingLabels)
    squareLength = int(math.sqrt(len(allTrainingFeatures)/len(trainingLabels)))

    # c(y): the number of training instances with label y
    # Set Prior Distribution from Training Data
    self.priorDistribution = {}
    self.setPriorDistribution(allLabels, trainingLabels)
    print "Prior Distribution: " + str(self.priorDistribution)

    # Choose the best k value from kgrid when setting "autotune"
    maxCorrect = -1
    correctK = -1
    self.condProbOfFeaturesList = {}
    for k in kgrid:
        self.condProbOfFeatures = {}
        self.setCondProbOfFeatures(numOfAllLabels, squareLength,numOfTrainingData, trainingData, trainingLabels, k)
        guesses = self.classify(validationData)
        correct = [guesses[i] == validationLabels[i] for i in range(len(validationLabels))].count(True)
        self.condProbOfFeaturesList[k] = dict(self.condProbOfFeatures)
        if maxCorrect < correct:
            maxCorrect = correct
            correctK = k
        print "Current k: {}, Rate of Correctness: {}%".format(k, correct)

    print "Final Selected k: {}, Maximum Rate of Correctness: {}%".format(correctK, maxCorrect)

    self.condProbOfFeatures = dict(self.condProbOfFeaturesList[correctK])

    # print self.condProbOfFeaturesList

  # Helper method to set the prior distributions for Y
  # Using training data,count all features
  def setPriorDistribution (self, allLabels, trainingLabels):
    for label in allLabels :
        dataCtr = 0
        for tLabel in trainingLabels :
            if tLabel == label :
                dataCtr = dataCtr + 1
        estimateProb = float(dataCtr) / float(len(trainingLabels))
        self.priorDistribution[label] = estimateProb

  # Helper method to compute the conditional probability of all features
  def setCondProbOfFeatures(self, numOfAllLabels, squareLength, numOfTrainingData, trainingData, trainingLabels, k):
    for y in range(0, numOfAllLabels) :
        for i in range(0, squareLength):
            for j in range(0, squareLength):
                dataCtr = 0
                for index in range(0,numOfTrainingData):
                    if y==trainingLabels[index] and trainingData[index][(i,j)]==1 :
                        dataCtr = dataCtr + 1
                        # Given y, the number of times pixel Fi, took value fi = 1
                    self.condProbOfFeatures[(y,i,j)] = float(format((dataCtr + k)/(self.priorDistribution[y]*numOfTrainingData + k),'.8f'))

  def classify(self, testData):
    """
    Classify the data based on the posterior distribution over labels.

    You shouldn't modify this method.
    """
    guesses = []
    self.posteriors = [] # Log posteriors are stored for later data analysis (autograder).
    for datum in testData:
      posterior = self.calculateLogJointProbabilities(datum)
      guesses.append(posterior.argMax())
      self.posteriors.append(posterior)
    return guesses

  def calculateLogJointProbabilities(self, datum):
    """
    Returns the log-joint distribution over legal labels and the datum.
    Each log-probability should be stored in the log-joint counter, e.g.
    logJoint[3] = <Estimate of log( P(Label = 3, datum) )>

    To get the list of all possible features or labels, use self.features and
    self.legalLabels.
    """
    logJoint = util.Counter()

    "*** YOUR CODE HERE ***"

    # FOR MANUAL ANALYSIS
    # datum = {(0, 0): 1, (0, 1): 0, (0, 2): 1}

    for label in self.legalLabels:
        logProbabilities = 0
        py = self.priorDistribution[label]
        for key in datum.keys():
            (i,j) = key
            if datum[(i,j)] == 1:
                value = self.condProbOfFeatures[(label,i,j)]
            else:
                value = 1 - self.condProbOfFeatures[(label,i,j)]
            if value > 0 :
               logProbabilities = logProbabilities + math.log(value)
        logProbabilities = math.log(py) + logProbabilities
        logJoint[label] = logProbabilities

    return logJoint

  def findHighOddsFeatures(self, label1, label2):
    """
    Returns the 100 best features for the odds ratio:
            P(feature=1 | label1)/P(feature=1 | label2)

    Note: you may find 'self.features' a useful way to loop through all possible features
    """
    featuresOdds = []

    "*** YOUR CODE HERE ***"

    allOdds = []
    for (i,j) in self.features:
        odds = self.condProbOfFeatures[(label1, i, j)] / self.condProbOfFeatures[(label2, i, j)]
        # Will be sorted by odds first
        allOdds.append((odds, i, j))

    allOdds.sort()
    #print allOdds

    for x in range(len(allOdds)-1, max(0, len(allOdds)-100), -1):
        (odds, i, j) = allOdds[x]
        featuresOdds.append((i,j))
    #print featuresOdds

    return featuresOdds




