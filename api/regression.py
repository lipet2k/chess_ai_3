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

        self.features_set = pd.read_excel("10_games_features.xlsx", "Sheet1")
        df_winner = pd.read_excel("10_games_winner.xlsx", "Sheet1")
        self.df_game_num = pd.read_excel("10_games_game_num.xlsx", "Sheet1")
        self.y_results = df_winner.to_numpy()[0]
        self.y_results = self.y_results[1:]


        self.df_write = pd.DataFrame()

        # tuple = file_to_arrays("first10kwhitewins.txt", "first10kblackwins.txt", 25)
        # one item = an array of feature values corresponding to one position

        # results = self.df.iloc[2]
        # self.y_results = results[1:]
        # self.y_results = self.y_results.to_numpy()
        # print(self.y_results)
        # self.y_results = np.array(results.to_numpy())
        # self.y_results = self.y_results[1:]

        # self.total_y = self.df["results"]

        self.iterations = 2

        # one set of weights
        self.weights = np.array([1] * (768 + 4 + 1 + 2))

        self.bias_weight = 1
        print("regression obj initialized")

    def regression(self):
        for iteration in range(self.iterations):
            self.update_weights()
            if iteration % 10 == 0:
                print("iteration " + str(iteration) + "\nbias term: " + str(self.bias_weight) + str(self.weights))
                self.df_write[iteration] = self.weights
        self.df_write.to_excel("final_weights.xlsx", sheet_name="Sheet1")
    # update all weights (not bias term) for data input
    def update_weights(self):
        new_weights = np.array([0] * 775)
        # for each weight
        self.bias_weight = self.bias_weight + self.learning_rate * self.derivative_loss()


        for j in range(len(self.weights)):
            # new weight = old weight + learning rate * derivative of loss func
            new_weights[j] = self.weights[j] + self.learning_rate * self.derivative_loss_second(j)
            # TODO: add x_j
        self.weights = new_weights

    # y = set of results
    # features is set of collections of features
    # y[n] is the result of the position represented by features[n]
    def derivative_loss(self):

        total = 0
        for i in range(len(self.y_results)):
            corresponding_features = self.features_set[i]
            total += self.y_results[i] - self.total_sum(self.bias_weight, corresponding_features, self.weights)
        return total

    def derivative_loss_second(self, j):
        total = 0
        for i in range(len(self.y_results)):
            corresponding_features = self.features_set[i]
            total += (self.y_results[i] - self.total_sum(self.bias_weight, corresponding_features, self.weights))*self.features_set[i][j]
        return total

    def total_sum(self, bias, features, weights):
        # print(type(features))
        # print(weights)
        # features = np.fromstring(features, dtype=int, sep=",")
        # print(features)
        return self.sigmoid(bias + np.dot(features, weights))

    def sigmoid(self, z):
        return 1 / (1 + math.exp(-z))


tester = logistic_regression()
tester.regression()
