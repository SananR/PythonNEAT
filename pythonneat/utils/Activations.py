import numpy as np


def tanh(x):
    return np.tanh(x)


def sigmoid(x):
    return 1/(1 + np.power(np.e, -4.9 * x))

