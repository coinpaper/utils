from typing import List

import numpy as np

from .APIObject import APIObject


class LinearRegression(APIObject):
    """
    Finds the Least-Squares Linear approximator to fit any numerical input dataset
    """

    def __init__(self, y: List[int]):
        """
        Constructs a linear estimator based on the input data
        :param y: Numerical input data
        """
        x = np.linspace(0, len(y) - 1, len(y))
        coefficients = np.polyfit(np.array(x), np.array(y), 1)

        # Numpy sorts coefficients from high-to-low
        self.x0: float = float(coefficients[1])
        self.x1: float = float(coefficients[0])
