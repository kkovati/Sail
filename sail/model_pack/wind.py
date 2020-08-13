import math, cmath
import numpy as np

class Wind:

    def __init__(self, random=True, orientation=0):
        """
        Initializes wind orientation and calculates x and y vectors
        Vectors will be used by View for display wind as arrow grid
        Parameters
        random : boolean 
            orientation initialization mode 
            (if True orientation parameter is omitted)
        orientation : float 
            wind orientation
        """
        if random:
            self.orientation = np.random.uniform(-math.pi, math.pi)
        else:
            self.orientation = orientation
        self.x = cmath.exp(self.orientation * 1j).real
        self.y = cmath.exp(self.orientation * 1j).imag
    
