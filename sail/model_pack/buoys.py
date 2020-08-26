import numpy as np
import pandas as pd


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
            '1' - standard race route no. 1
            '2' - standard race route no. 2
            '3' - standard race route no. 3
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
                
        elif mode in {'1', '2', '3'}:
            # pandas dataframe
            df = pd.read_json('sail/model_pack/buoy_coordinates.json')
            for buoy_coords in df[mode + '_race']:
                x = int(buoy_coords['x'])
                y = int(buoy_coords['y'])
                self.buoys.append(_Buoy(x,y))
                
        else:
            raise Exception('Invalid mode parameter')
        
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
