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

    def prepare_generation(self, random_race=True, race_number=0):
        """
        Randomly initializes ship start postitions, wind direction 
        and buoy positions at start of each generation
        """
        if random_race:
            self.buoys = Buoys(mode='random')        
            self.wind = Wind(random=True)        
            start_position = {'x': np.random.uniform(100, 1060), 
                              'y': np.random.uniform(100, 650), 
                              'orient': np.random.uniform(0, 2 * math.pi)}
        else:
            self.buoys = Buoys(mode=str(race_number))
            wind_orients = {1 : 0, 2 : math.pi / 4, 3: math.pi / 2}
            self.wind = Wind(random=False, 
                             orientation=wind_orients[race_number])
            ship_orient = np.random.uniform(0, 0.2) * math.pi
            start_position = {'x': 275, 'y': 100, 'orient': ship_orient}
            # start_position = {'x': 275, 'y': 100, 'orient': 0.18}
            
        self.population.prepare_generation(self.buoys, self.wind, 
                                           start_position) 
        
    def prepare_test(self):
        """
        Initializes ship start postition, wind direction and buoy positions 
        for testing
        """        
        self.buoys = Buoys(mode='test')
        
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
        
    

