import util
import numpy as np
import sys
import random

PRINT = True

###### DON'T CHANGE THE SEEDS ##########
random.seed(42)
np.random.seed(42)

def small_classify(y):
    classifier, data = y
    return classifier.classify(data)

class AdaBoostClassifier:
    """
    AdaBoost classifier.

    Note that the variable 'datum' in this code refers to a counter of features
    (not to a raw samples.Datum).
    
    """

    def __init__( self, legalLabels, max_iterations, weak_classifier, boosting_iterations):
        self.legalLabels = legalLabels
        self.boosting_iterations = boosting_iterations
        self.classifiers = [weak_classifier(legalLabels, max_iterations) for _ in range(self.boosting_iterations)]
        self.alphas = [0]*self.boosting_iterations

    def train( self, trainingData, trainingLabels):
        """
        The training loop trains weak learners with weights sequentially. 
        The self.classifiers are updated in each iteration and also the self.alphas 
        """
        
        self.features = trainingData[0].keys()
        "*** YOUR CODE HERE ***"
        weights = []
        for i in range(len(trainingData)):
            weights.append(1.0/len(trainingData))
        for k in range(self.boosting_iterations):
            self.classifiers[k].train(trainingData, trainingLabels, weights)
            guesses = self.classifiers[k].classify(trainingData)
            err = 0
            for i in range(len(trainingData)):
                err += weights[i] * (abs(guesses[i] - trainingLabels[i])/2)
            err /= np.sum(weights)
            self.alphas[k] = (1/2)*np.log((1 - err)/err)
            for i in range(len(trainingData)):
                weights[i] = weights[i] * np.exp(self.alphas[k] * (abs(guesses[i] - trainingLabels[i])/2))

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
        guesses = np.mean(guesses, axis=0)
        guesses = np.sign(guesses)
        return guesses
