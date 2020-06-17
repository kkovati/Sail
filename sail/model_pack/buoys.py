import numpy as np


class Buoys:
    """
    Model of the list of target buoys
    """    
    def __init__(self, buoy_count):
        self.buoys = []
        
        for i in range(buoy_count):
            x = np.random.uniform(100, 1060)
            y = np.random.uniform(100, 650)
            self.buoys.append(_Buoy(x,y))
        
    def __getitem__(self, index):
        return self.buoys[index]
        
    def __iter__(self):
        return self.buoys.__iter__()
    
    def __len__(self):
        return len(self.buoys)

class _Buoy:
    """
    Model of single buoy
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y
