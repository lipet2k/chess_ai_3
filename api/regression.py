import numpy as np
# import matplotlib.pyplot as plt
import math
import pandas as pd
import random

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

        # pick minibatch size
        self.batch_size = 10

        # get the data on the features for all the positions from the features fiel
        self.features_data = pd.read_excel("10_games_features.xlsx", "Sheet1")
        # get the data on the results for all the corresponding positions
        self.y_results_data = pd.read_excel("10_games_winner.xlsx", "Sheet1")
        # all indices is all indices of positions
        self.all_indices = self.y_results_data.columns.tolist()[1:]
        # shuffle all the indices for our batches
        random.Random(1234).shuffle(self.all_indices)

        # new list is the indices of the first batch
        self.new_list = self.all_indices[:self.batch_size]
        # we remove these first X indices from all_indices
        self.all_indices = self.all_indices[self.batch_size:]
        # features set is
        self.features_set = self.features_data[self.new_list]
        self.y_results = self.y_results_data[self.new_list]

        self.df_write = pd.DataFrame()

        # self.iterations = len(self.all_results)
        self.iterations = len(self.all_indices)


        # one set of weights
        self.weights = np.array([0.0] * (768 + 4 + 1 + 2))

        self.bias_weight = 1.0

    def update_batch(self):
        # check there is enough elements
        self.batch_size = min(self.batch_size, len(self.all_indices))

        self.new_list = self.all_indices[:self.batch_size]
        self.all_indices = self.all_indices[self.batch_size:]

        self.features_set = self.features_data[self.new_list]
        self.y_results = self.y_results_data[self.new_list]

    def regression(self):
        for iteration in range(self.iterations):
            self.update_weights()
            self.update_batch()

            if iteration % 1 == 0:
                self.df_write[iteration] = self.weights

        # print(self.bias_weight, self.weights)
        self.df_write.to_excel("final_weights.xlsx", sheet_name="Sheet1")

    # update all weights (not bias term) for data input
    def update_weights(self):
        new_weights = np.array([0.0] * 775)
        # for each weight
        self.bias_weight = self.bias_weight + self.learning_rate * self.derivative_loss()

        for j in range(len(self.weights)):
            # new weight = old weight + learning rate * derivative of loss func
            new_weights[j] = self.weights[j] + self.learning_rate * self.derivative_loss_second(j)
        self.weights = new_weights

    # y = set of results
    # features is set of collections of features
    # y[n] is the result of the position represented by features[n]
    def derivative_loss(self):

        total = 0
        for i in self.new_list:
            corresponding_features = self.features_set[i].to_numpy()
            total += self.y_results[i] - self.total_sum(corresponding_features)
        return total

    def derivative_loss_second(self, j):
        total = 0
        for i in self.new_list:
            corresponding_features = self.features_set[i].to_numpy()
            total += (self.y_results[i] - self.total_sum(corresponding_features))*corresponding_features[j]
        return total

    def total_sum(self, features):
        return self.sigmoid(self.bias_weight + np.dot(features, self.weights))

    def sigmoid(self, z):
        return 1.0 / (1.0 + math.exp(-z))

    def test_against(self):
        tester = tester_data()
        count = len(tester.all_indices)
        errorvals = [0]*count
        for i in tester.all_indices:
            current = tester.features_set[i].to_numpy()
            true = tester.y_results_data[i]
            errorvals[i] = self.test_helper(current, true)


    def test_helper(self, features, true_value):
        error = true_value - self.total_sum(features)
        return error



class tester_data:

    def __init__(self):
        # get the data on the features for all the positions from the features fiel
        self.features_data = pd.read_excel("test_games_features.xlsx", "Sheet1")
        # get the data on the results for all the corresponding positions
        self.y_results_data = pd.read_excel("test_games_winner.xlsx", "Sheet1")
        # all indices is all indices of positions
        self.all_indices = self.y_results_data.columns.tolist()[1:]

        # features set is
        self.features_set = self.features_data[self.all_indices]
        self.y_results = self.y_results_data[self.all_indices]



main = logistic_regression()
main.regression()
