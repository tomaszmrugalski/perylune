import numpy as np

def close_enough(a, b, epsilon):
    assert np.abs(a - b) <= epsilon
