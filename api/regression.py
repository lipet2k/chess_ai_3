import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from moves import pos_moves
import math

# MIRA
#Input: Board
#Output: Moves

# train it on only wins and losses
# test it on only wins and loss - assess our success

# train it on win/loss/draw
# test it
# output 0.4-0.6 = draw

class logistic_regression:

    def __init__(self):
        self.iterations = 100
        self.learning_rate = 0.01

        # one item = an array of feature values corresponding to one position
        self.features_set = np.array([])
        # one item corresponds to one item in feature set
        self.y_results = np.array([])

        # one set of weights
        self.weights = np.array([])
        self.bias_weight = 1

    def regression(self):
        for iteration in range(self.iterations):
            self.update_weights()
        print(self.weights)

    # update all weights (not bias term) for data input
    def update_weights(self):
        new_weights = np.array([])
        # for each weight
        for j in range(self.weights.size):
            # new weight = old weight + learning rate * derivative of loss func
            new_weights[j] = self.weights[j] + self.learning_rate * self.gradient(self.y_results, self.features_set)
        self.weights = new_weights

    # y = set of results
    # features is set of collections of features
    # y[n] is the result of the position represented by features[n]
    def gradient(self, y, features, j):
        total = 0
        for i in range(y.size):
            corresponding_features = features[i]
            total += y[i] - self.total_sum(self.bias_weight, corresponding_features, self.weights) \
                     * corresponding_features[j]
        return total

    def total_sum(self, bias, features, weights):
        return self.sigmoid(bias + np.dot(features, weights))

    def sigmoid(self, z):
        return 1 / (1 + math.exp(-z))