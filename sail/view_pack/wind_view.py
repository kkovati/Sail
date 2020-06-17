from itertools import product
import tkinter as tk

class WindView:
    """
    Displays arrow representation of wind
    """    
    def __init__(self, canvas, wind):
        self.grid = 40
        self.wind_views = []
        for x, y in product(range(60), range(60)):
            wv = canvas.create_line(x * self.grid, y * self.grid, 
                                    x * self.grid + wind.x * 30, 
                                    y * self.grid + wind.y * 30, 
                                    arrow=tk.LAST, fill='gray')
            self.wind_views.append(wv)
     
    def clear(self, canvas):
        for wv in self.wind_views:
            canvas.delete(wv) 
        self.wind_views = None  
                
                