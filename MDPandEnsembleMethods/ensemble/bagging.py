import util
import numpy as np
import sys
import random

PRINT = True

###### DON'T CHANGE THE SEEDS ##########
random.seed(42)
np.random.seed(42)

class BaggingClassifier:
    """
    Bagging classifier.

    Note that the variable 'datum' in this code refers to a counter of features
    (not to a raw samples.Datum).
    
    """

    def __init__( self, legalLabels, max_iterations, weak_classifier, ratio, num_classifiers):

        self.ratio = ratio
        self.num_classifiers = num_classifiers
        self.classifiers = [weak_classifier(legalLabels, max_iterations) for _ in range(self.num_classifiers)]

    def train( self, trainingData, trainingLabels):
        """
        The training loop samples from the data "num_classifiers" time. Size of each sample is
        specified by "ratio". So len(sample)/len(trainingData) should equal ratio. 
        """
        self.features = trainingData[0].keys()
        "*** YOUR CODE HERE ***"
        for j in self.classifiers:
            index = np.random.randint(len(trainingData),size = int(len(trainingData)*self.ratio))
            sampleData = [trainingData[i] for i in index]
            sampleLabels = [trainingLabels[i] for i in index]
            # for i in range(int(self.ratio * len(trainingData))):
            #     index = random.randint(0, len(trainingData)-1)
            #     sampleData.append(trainingData[index])
            #     sampleLabels.append(trainingLabels[index])
            j.train(sampleData,sampleLabels)
        
        # util.raiseNotDefined()


    def classify( self, data):
        """
        Classifies each datum as the label that most closely matches the prototype vector
        for that label. This is done by taking a polling over the weak classifiers already trained.
        See the assignment description for details.

        Recall that a datum is a util.counter.

        The function should return a list of labels where each label should be one of legaLabels.
        """

        "*** YOUR CODE HERE ***"
        guesses = []
        for j in self.classifiers:
            guesses.append(j.classify(data))
        guesses = np.mean(guesses,axis = 0)
        guesses = np.sign(guesses)
        return guesses
        # util.raiseNotDefined()
