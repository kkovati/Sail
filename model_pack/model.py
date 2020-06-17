import math
import numpy as np
from .population import Population
from .buoys import Buoys
from .wind import Wind


class Model:
    """
    Model handles all objects in the simulation
    """
    def __init__(self, nn_architecture, population_size):
        self.population = Population(nn_architecture, population_size)

    def prepare_generation(self):
        """
        Randomly initializes ship start postitions, wind direction 
        and buoy positions at start of each generation
        """
        buoy_count = np.random.randint(4,9)
        print('Buoy count:', buoy_count)
        self.buoys = Buoys(buoy_count)
        self.wind = Wind()
        start_position = {'x': np.random.uniform(100, 1060), 
                          'y': np.random.uniform(100, 650), 
                          'orient': np.random.uniform(0, 2 * math.pi)}
        self.population.prepare_generation(self.buoys, self.wind, 
                                           start_position) 
        
    def prepare_test(self, test_id):
        """
        Initializes ship start postitions, wind direction and buoy positions 
        for testing
        """
        self.wind = Wind()
        self.buoys = Buoys(1)
        self.buoys[0].x = 1000
        self.buoys[0].y = 380
        start_position = {'x': 100, 'y': 380, 'orient': 0.18}        
        if test_id == 0: 
            # downwind
            self.wind.orientation = 0
            self.wind.x = 1
            self.wind.y = 0           
        elif test_id == 1:  
            # upwind
            self.wind.orientation = math.pi
            self.wind.x = -1
            self.wind.y = 0        
        elif test_id == 2:
            # cross-wind
            self.wind.orientation = math.pi / 2
            self.wind.x = 0
            self.wind.y = 1 
        else:
            raise NotImplementedError('Test case no. ' + 
                                      '{} is not implemented'.format(test_id))
        self.population.prepare_test(self.buoys, self.wind, start_position)
        
    def update(self, time):
        self.population.update(time)
        
    def evaluate(self):
        self.population.evaluate()
        
    def mutate(self, mutation_rate):
        self.population.mutate(mutation_rate)
        
    def save(self, filename):
        self.population.save(filename)
        
    def load(self, filename, number):
        self.population.load(filename, number)
        
    

