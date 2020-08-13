import numpy as np


class Buoys:
    """
    Model of the list of target buoys
    """    
    def __init__(self, mode):
        """
        Parameters
        mode : str
            'random' - random number of buoys on random coordinate
            'test' - test race in a square shaped route
            else - standard race route
        """
        self.buoys = []
        
        if mode == 'test':
            coords = [(825,100),(825,650),(275,650),(275,100)]
            for x, y in coords:
                self.buoys.append(_Buoy(x,y))  
                
        elif mode == 'random':
            buoy_count = np.random.randint(4,9)
            print('Random race, buoy count:', buoy_count)            
            for i in range(buoy_count):
                x = np.random.uniform(100, 1060)
                y = np.random.uniform(100, 650)
                self.buoys.append(_Buoy(x,y))
                
        else:
            coords = [(600,100),(825,200),(700,300),(870,470),(550,500),(550,650),(100,620),(530,290),(120,200)]
            for x, y in coords:
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
