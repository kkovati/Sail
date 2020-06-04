import math, cmath
import numpy as np

class Wind:

    def __init__(self):
        """
        Randomly initializes wind orientation and calculates x and y vectors
        Vectors will be used by View for display
        """
        self.orientation = np.random.uniform(-math.pi, math.pi)
        self.x = cmath.exp(self.orientation * 1j).real
        self.y = cmath.exp(self.orientation * 1j).imag
    
