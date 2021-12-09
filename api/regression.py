import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from moves import pos_moves
import math

# MIRA
#Input: Board
#Output: Moves



class logisti_regression:

    def __init__(self):
        self.iteration = 100
        self.learning_rate = 0.01

        self.features = np.array([])
        self.weights = np.array([])
        self.bias_weight = 1
        self.y_results = np.array([])


    def loss_function(self, y_i):
        total = 0
        for i in range(y_i.size):
            total += y_i[i] - total_sum(bias_weight)

    def total_sum(self, bias, features, weights):
        return sigmoid(bias + np.dot(features, weights))

    def sigmoid(self, z):
        return 1 / (1 + math.exp(-z))