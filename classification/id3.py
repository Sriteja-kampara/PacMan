# ID3 by Alex and Kevin
# ---------------

import util
import math
import classificationMethod


class DecisionTreeClassifier(classificationMethod.ClassificationMethod):
    """
    The Decision Tree is implemented on a Python Dictionary. Each node is a dictionary
    with the following attributes: attr, val, children (list of 2).
    First children is accessible by 1, second by 0.
    If the children list is empty - the node is a leaf.
    Pruning is implemented recursively according to Mitchell's reduce-error pruning, page 69.
    """

    def __init__(self, legalLabels):
        self.guess = None
        self.type = "id3"
        self.tree = {}
        # For post-pruning on a validation set
        self.currentPerformance = 0

    def train(self, data, labels, validationData, validationLabels):
        '''
        # DEBUG DATA
        data = [{(0, 0): 0, (0, 1): 0, (0, 2): 0},
                {(0, 0): 1, (0, 1): 0, (0, 2): 0},
                {(0, 0): 0, (0, 1): 1, (0, 2): 1},
                {(0, 0): 1, (0, 1): 1, (0, 2): 0},
                {(0, 0): 0, (0, 1): 0, (0, 2): 1}]
        labels = [0, 1, 2, 2, 1]
        '''

        allTrainingFeatures = data[0].keys()

        # Labels can be not hardcoded
        t = self.buildDecisionTree(data, labels, allTrainingFeatures, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

        self.tree = t

        # The performance of the tree on the validation set before prunning
        guesses = self.classify(validationData)
        correct = [guesses[i] == validationLabels[i] for i in range(len(validationLabels))].count(True)
        self.currentPerformance = correct

        # DO PRUNE!!
        self.recPruneTheTree(self.tree, validationData, validationLabels)

        print self.tree

    def recPruneTheTree(self, t, validationData, validationLabels):
        # On a back way from DFS recursion we try to remove children
        # from the current node and check the correct guess rate on a validation set.
        # In case of no benefit we return children, otherwise update the
        # current performance of the tree.

        copyChildren = t['children']

        if len(copyChildren) == 0:
            return

        for d in copyChildren:
            self.recPruneTheTree(d, validationData, validationLabels)

        # Removing child nodes to check the benefit
        t['children'] = []

        guesses = self.classify(validationData)
        correct = [guesses[i] == validationLabels[i] for i in range(len(validationLabels))].count(True)

        if correct > self.currentPerformance:
            print "Prune: ", self.currentPerformance, " to ", correct
            self.currentPerformance = correct
        else:
            # Need to add children back
            t['children'] = copyChildren


    def chooseTheBestInformationGain(self, allData, allLabels, legalFeatures, legalLabels, priorCounts):
        # Straightforward to the slides from the correspondent lecture - calculating entropy,
        # and the total information gain (IG).

        priorH = 0
        for l in legalLabels:
            if l in priorCounts:
                p = priorCounts[l] / float(len(allData))
                if p > 0:
                    priorH += -p * math.log(p)

        maxIG = -1
        bestF = -1
        for f in legalFeatures:
            labelCountsTrue = {}
            labelCountsFalse = {}
            totalNumberTrue = 0
            totalNumberFalse = 0
            cnt = 0
            for row in allData:
                # Value of this feature in a one evidence
                v = row[f]
                if v == 1:
                    totalNumberTrue += 1
                    if allLabels[cnt] in labelCountsTrue:
                        labelCountsTrue[allLabels[cnt]] += 1
                    else:
                        labelCountsTrue[allLabels[cnt]] = 1
                else:
                    totalNumberFalse += 1
                    if allLabels[cnt] in labelCountsFalse:
                        labelCountsFalse[allLabels[cnt]] += 1
                    else:
                        labelCountsFalse[allLabels[cnt]] = 1
                cnt += 1
            hForTrue = 0
            for l in legalLabels:
                if l in labelCountsTrue:
                    p = labelCountsTrue[l] / float(totalNumberTrue)
                    if p > 0:
                        hForTrue += -p * math.log(p)
            hForFalse = 0
            for l in legalLabels:
                if l in labelCountsFalse:
                    p = labelCountsFalse[l] / float(totalNumberFalse)
                    if p > 0:
                        hForFalse += -p * math.log(p)
            IG = priorH - (totalNumberTrue / float(len(allData))) * hForTrue - (totalNumberFalse / float(len(allData))) * hForFalse
            if IG > maxIG:
                maxIG = IG
                bestF = f

        return bestF

    def buildDecisionTree(self, allData, allLabels, legalFeatures, legalLabels):

        # Preliminary, calculating of occurrences

        priorCounts = {}
        popularLabel = 0 # default
        maxPopularity = -1
        for l in allLabels:
            if l in priorCounts:
                priorCounts[l] += 1
            else:
                priorCounts[l] = 1
            if maxPopularity < priorCounts[l]:
                maxPopularity = priorCounts[l]
                popularLabel = l

        # First, base cases with leaf nodes

        if len(legalFeatures) == 0:
            # All decisions made, select what is most likely
            return {'val': popularLabel, 'children':[]}
        if len(allData) == 0:
            # No other train evidences
            return {'val': legalLabels[0], 'children':[]}
        if priorCounts[popularLabel] == len(allLabels):
            # Only one choice is left
            return {'val': popularLabel, 'children':[]}

        # Otherwise, choose next attribute-feature with the best IG
        nextFeature = self.chooseTheBestInformationGain(allData, allLabels, legalFeatures, legalLabels, priorCounts)

        # Saving popularLabel too for further pruning
        currentNode = {'attr': nextFeature, 'children':[], 'val': popularLabel}

        # A node can have only two children

        listFisTrue = []
        labelsFisTrue = []
        listFisFalse = []
        labelsFisFalse = []

        cnt = 0
        for row in allData:
            # Value of this feature in a one evidence
            v = row[nextFeature]
            if v == 1:
                listFisTrue.append(row)
                labelsFisTrue.append(allLabels[cnt])
            else:
                listFisFalse.append(row)
                labelsFisFalse.append(allLabels[cnt])
            cnt += 1

        # First child is by '1' value
        currentNode['children'].append(
            self.buildDecisionTree(listFisTrue, labelsFisTrue, [f for f in legalFeatures if f != nextFeature], legalLabels))
        # Second child is by '0' value
        currentNode['children'].append(
            self.buildDecisionTree(listFisFalse, labelsFisFalse, [f for f in legalFeatures if f != nextFeature], legalLabels))

        #print currentNode

        return currentNode

    def searchTheTree(self, oneSample):

        # Just going by children.
        # Remember: first children is accessible by 1, second by 0

        dict = self.tree
        while len(dict['children']) > 0:
            f = dict['attr']
            if oneSample[f] == 1:
                dict = dict['children'][0]
            else:
                dict = dict['children'][1]

        return dict['val']

    def classify(self, testData):
        '''
        # FOR DEBUG
        tmp = testData
        testData = [{(0,0): 1, (0,1): 0, (0,2): 1},
                    {(0,0): 1, (0,1): 0, (0,2): 0},
                    {(0,0): 1, (0,1): 1, (0,2): 1},
                    {(0,0): 0, (0,1): 0, (0,2): 0}]
        '''

        result = []

        for test in testData:
            result.append(self.searchTheTree(test))

        #print result

        return result
        #return [9 for i in tmp]
