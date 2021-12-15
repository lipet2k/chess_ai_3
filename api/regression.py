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

        self.batch_size = 5

        features_data = pd.read_excel("10_games_features.xlsx", "Sheet1")
        df_winner_data = pd.read_excel("10_games_winner.xlsx", "Sheet1")
        # self.df_game_num_data = pd.read_excel("10_games_game_num.xlsx", "Sheet1")
        y_results_data = df_winner_data
        # .to_numpy()[0]


        something = y_results_data.columns.tolist()[1:]


        random.Random(1234).shuffle(something)


        self.new_list = something[:self.batch_size]
        # print(self.new_list) 

        self.features_set = features_data[self.new_list]
        # print(type(self.features_set))
        self.y_results = y_results_data[self.new_list]
        # print(type(self.y_results))




        self.df_write = pd.DataFrame()

        # self.total_y = self.df["results"]

        self.iterations = 10

        # one set of weights
        self.weights = np.array([1.0] * (768 + 4 + 1 + 2))

        self.bias_weight = 1

    def regression(self):
        for iteration in range(self.iterations):
            self.update_weights()
            if iteration % 4 == 0:
                print(self.weights)
                self.df_write[iteration] = self.weights
        self.df_write.to_excel("final_weights.xlsx", sheet_name="Sheet1")
    # update all weights (not bias term) for data input
    def update_weights(self):
        new_weights = np.array([0.0] * 775)
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


tester = logistic_regression()
tester.regression()
print(tester.weights)
