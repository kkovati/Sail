import cmath


class ShipView:
    """
    Displays ship model
    """ 
    def __init__(self):
        SIZE = 2 # common size factor of ship elements
        # hull polygon coordinates (ship center is in origo)
        hull = [[-7,-4],[3,-4],[8,0],[3,4],[-7,4]]
        # rescale by SIZE
        self.hull = [[SIZE * j for j in i] for i in hull]
        self.hull_view = None
        # sail polygon coordinates (ship center is in origo)
        sail = [[-0.5,-3],[-1.5,-6],[-1.4,-6.1],[0.5,-3],[0.5,3],[-1.4,6.1],
                [-1.5,6],[-0.5,3]]
        # rescale by SIZE
        self.sail = [[SIZE * j for j in i] for i in sail]
        self.sail_view = None
        
    def update(self, canvas, ship):   
        """
        Rotates hull and sail coordinates with ship orientation,
        Offsets hull and sail coordinates with ship center coordinates,
        Updates canvas with new coordinates
        """
        ccenter = complex(ship.x, ship.y)        
        cangle = cmath.exp(ship.orientation * 1j)
        hull = []
        for x, y in self.hull:
            cc = cangle * complex(x, y) + ccenter
            hull.append([cc.real, cc.imag])

        if self.hull_view is not None:
            canvas.delete(self.hull_view)        
        
        self.hull_view = canvas.create_polygon(hull, outline='red', 
                                               fill='brown')
        
        sail = []
        for x, y in self.sail:
            cc = cangle * complex(x, y) + ccenter
            sail.append([cc.real, cc.imag])

        if self.sail_view is not None:
            canvas.delete(self.sail_view)        
        
        self.sail_view = canvas.create_polygon(sail, fill='white')

    def clear(self, canvas):
        canvas.delete(self.hull_view)
        self.hull_view = None
        canvas.delete(self.sail_view)
        self.sail_view = None
        
        