import math, cmath
from .neural_network import NeuralNetwork


class Ship:
   
    def __init__(self, neural_network, buoys, wind, start_position):
        """
        Initializes ship model by setting up the neural network for 
        controlling the ship, the target buoys and the wind
        """
        self.nn = neural_network
        
        self.buoys = buoys
        self.wind = wind
        
        self.x = start_position['x']
        self.y = start_position['y']
        self.orientation = start_position['orient'] # angle in radians
        self.prev_steer = 0
        
        self.speed = 0        
        
        self.curr_buoy_index = 0
        self.min_distance = self.calc_ship_buoy_dist()
        self.time = 0
        self.finished = False
                
    def update(self, time):
        """
        Calls the neural network to control the ship and calls the self.move
        method which updates the ship model
        """
        if self.finished:
            return
        # updates controls by inputs
        controls = self.nn.predict(self.calc_ship_buoy_angle(),
                                   self.calc_ship_wind_angle())
        # moves the ship
        self.move(controls)
        # analyze position
        self.analyze_position(time)                   
        
    def calc_ship_buoy_angle(self):
        """
        Calculates target buoy orientation relative to ship
        """
        buoy = self.buoys[self.curr_buoy_index]
        angle_buoy = cmath.phase(complex(buoy.x - self.x, buoy.y - self.y))
        return self.normalize_angle(angle_buoy - self.orientation)
    
    def calc_ship_wind_angle(self):
        """
        Calculates wind orientation relative to ship
        """
        return self.normalize_angle(self.wind.orientation - self.orientation) 
    
    def normalize_angle(self, angle):
        """
        Moves input angle into [-pi,pi] interval
        """
        if -math.pi < angle < math.pi:
            return angle
        else:
            return cmath.phase(cmath.exp(angle * 1j))                           
    
    def move(self, controls):
        """
        Updates ship speed, orientation and position due to current state, 
        wind and controls        
        Parameters:
        - controls: map - The predicted output from the neural network 
        Returns:
        - None
        Side effects:
        - self.speed, self.prev_steer, self.orientation, self.orientation,
          self.x, self.y
        """
        # Update ship speed relative to the wind
        wind_angle = self.calc_ship_wind_angle()
        if wind_angle >= 0:
            self.speed = 12 * (math.pi - wind_angle) / math.pi 
        else:
            self.speed = 12 * (wind_angle + math.pi) / math.pi
        self.speed += min(self.speed, 8) # speed maximum set to 8
        
        # Update orientation by steer
        steer = controls['steer']
        if abs(steer) > 0.1: # penalty for turning
            self.speed /= 2
            
        # A derviative member added to steer thus making a PD controller 
        # to prevent oscillation of orientation around the target angle
        D = -0.7
        steer += D * (steer - self.prev_steer)
        self.prev_steer = steer
        self.orientation += steer 
        
        # Update position by speed and orientation
        cangle = cmath.exp(self.orientation * 1j) # angle in radians
        cspeed = cangle * complex(self.speed, 0)
        x_speed = cspeed.real
        y_speed = cspeed.imag        
        self.x += x_speed
        self.y += y_speed
        
    def analyze_position(self, time):
        """
        Calculates distance to the target buoy
        Counts the reached buoys
        Records the time needed to reach all the buoys
        
        These results are the basis to specify fitness of the ship
        """
        self.min_distance = min(self.calc_ship_buoy_dist(), self.min_distance)
        if self.min_distance < 10: 
            self.curr_buoy_index += 1
            if self.curr_buoy_index >= len(self.buoys):
                self.finished = True
                self.min_distance = 0
                self.time = time
                return
            self.min_distance = self.calc_ship_buoy_dist() 
                
    def calc_ship_buoy_dist(self):
        """
        Calculates the target buoy distance from ship
        """
        buoy = self.buoys[self.curr_buoy_index]
        return math.sqrt(((buoy.x - self.x) ** 2) + ((buoy.y - self.y) ** 2))    
    

        