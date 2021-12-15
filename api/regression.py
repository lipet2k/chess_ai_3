import numpy as np
# import matplotlib.pyplot as plt
import math
import pandas as pd

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
        self.learning_rate = 0.1

        self.df = pd.read_excel("10_games.xlsx", "Sheet1")
        make_rows = ['game', 'move#', 'features']
        self.df_write = pd.DataFrame(index=make_rows)

        # tuple = file_to_arrays("first10kwhitewins.txt", "first10kblackwins.txt", 25)
        # one item = an array of feature values corresponding to one position

        features = self.df.iloc[1]
        self.features_set = np.array(features.to_numpy())
        print(type(self.features_set))

        results = self.df.iloc[2]
        self.y_results = np.array(results.to_numpy())

        # self.total_y = self.df["results"]

        self.iterations = len(self.y_results)

        # one set of weights
        self.weights = np.array([0] * (768 + 4 + 1 + 2))

        self.bias_weight = 1
        print("regression obj initialized")

    def regression(self):
        for iteration in range(self.iterations):
            self.update_weights()
            if iteration % 10 == 0:
                print("iteration " + str(iteration) + "\nbias term: " + str(self.bias_weight) + str(self.weights))
                self.df_write[iteration] = [iteration, 0, pd.Series(self.weights)]
        self.df_write.to_excel("final_weights", sheet_name="Sheet1")
    # update all weights (not bias term) for data input
    def update_weights(self):
        new_weights = np.array([0] * 775)
        # for each weight
        self.bias_weight = self.bias_weight + self.learning_rate * self.derivative_loss(self.y_results, self.features_set)


        for j in range(len(self.weights)):
            # new weight = old weight + learning rate * derivative of loss func
            new_weights[j] = self.weights[j] + self.learning_rate * self.derivative_loss(self.y_results, self.features_set)*self.features_set
            # add x_j
        self.weights = new_weights

    # y = set of results
    # features is set of collections of features
    # y[n] is the result of the position represented by features[n]
    def derivative_loss(self, y, features):

        total = 0
        for i in range(len(y)):
            corresponding_features = features[i]
            total += y[i] - self.total_sum(self.bias_weight, corresponding_features, self.weights)
        return total

    def total_sum(self, bias, features, weights):
        return self.sigmoid(bias + np.dot(features, weights))

    def sigmoid(self, z):
        return 1 / (1 + math.exp(-z))


tester = logistic_regression()
tester.regression()
