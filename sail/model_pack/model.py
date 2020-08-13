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

    def prepare_generation(self, random_race=True):
        """
        Randomly initializes ship start postitions, wind direction 
        and buoy positions at start of each generation
        """
# =============================================================================
#         buoy_count = np.random.randint(4,9)
#         print('Buoy count:', buoy_count)
# =============================================================================
        if random_race:
            self.buoys = Buoys(mode='random')        
            self.wind = Wind(random=True)        
            start_position = {'x': np.random.uniform(100, 1060), 
                              'y': np.random.uniform(100, 650), 
                              'orient': np.random.uniform(0, 2 * math.pi)}
        else:
            self.buoys = Buoys(mode='standard')        
            self.wind = Wind(random=False, orientation=0)        
            start_position = {'x': 275, 'y': 100, 'orient': 0.18}
            
        self.population.prepare_generation(self.buoys, self.wind, 
                                           start_position) 
        
    def prepare_test(self):
        """
        Initializes ship start postition, wind direction and buoy positions 
        for testing
        """        
        self.buoys = Buoys(mode='test')
# =============================================================================
#         self.buoys[0].x = 825
#         self.buoys[0].y = 100
#         self.buoys[1].x = 825
#         self.buoys[1].y = 650
#         self.buoys[2].x = 275
#         self.buoys[2].y = 650
#         self.buoys[3].x = 275
#         self.buoys[3].y = 100
# =============================================================================
        
        self.wind = Wind(random=False, orientation=0)       
        
        start_position = {'x': 275, 'y': 100, 'orient': 0.18}    
        self.population.prepare_test(self.buoys, self.wind, start_position)
        
    def update(self, time):
        self.population.update(time)
        
    def evaluate(self):
        self.population.evaluate()
        
    def evolve(self, mutation_rate):
        self.population.evolve(mutation_rate)
        
    def save(self, generation, distance):
        self.population.save(generation, distance)
        
    def load(self, filename):
        self.population.load(filename)
        
    

