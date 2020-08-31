import copy
import numpy as np
from .ship import Ship
from .neural_network import NeuralNetwork


class Population:
    """
    Population contains all neural networks through the evolution process
    During simulation Population contains all ship models
    """    
    def __init__(self, nn_architecture, population_size):
        self.nn_population = []  
        self.population_size = population_size
        for i in range(population_size):
            self.nn_population.append(NeuralNetwork(nn_architecture))
            
    def __iter__(self):
        return self.ship_population.__iter__()  
    
    def __getitem__(self, index):
        return self.ship_population[index]
    
    def __len__(self):
        return len(self.ship_population)
    
    def prepare_generation(self, buoys, wind, start_position):
        self.finished = False
        self.ship_population = []
        for nn in self.nn_population:
            self.ship_population.append(Ship(nn, buoys, wind, start_position))
            
    def prepare_test(self, buoys, wind, start_position):
        self.finished = False
        self.ship_population = [Ship(self.nn_population[0], buoys, wind, 
                                     start_position)]
        
    def update(self, time):
        for ship in self.ship_population:
             ship.update(time)                 
        self.finished = all([ship.finished for ship in self.ship_population])
            
    def evaluate(self):
        """
        Orders the list of ships by fitness and updates each ship's rank 
        accordingly
        Fitness is based on the number of buoys reached, the minimum distance
        to the next target buoy and the time neeeded to reach all the buoys
        """
        ordered_ship_population = sorted(self.ship_population, 
                   key=lambda x: (-x.curr_buoy_index, x.min_distance, x.time))
        # update rank (the lower the rank the higher the fitness)
        for rank, ship in enumerate(ordered_ship_population):
            ship.nn.rank += rank        
        print('Best results:')
        print('{:<6s} {:<10s} {:<10s}'.format('Buoys', 'Distance', 'Time'))
        for ship in ordered_ship_population[0:5]:
            print('{:<6s} {:<10s} {:<10s}'.format(
                                            str(ship.curr_buoy_index), 
                                            str(int(ship.min_distance)), 
                                            str(ship.time)))
            
    def evolve(self, mutation_rate):
        """
        Creates the new generation based on the results of the former
        generation's simulation results, using the most fit instances
        Elitism: the best 20% of the instances goes directly to the next 
                 generation
        Mutation: the best 20% of the instances copied 3 times and it's 
                parameters randomly changed using mutation_rare
                (makes up 60% of next generation's population)
        Crossover: averaging the parameters of randomly chosen pairs from 
                the best 20% of the instances
                (makes up 20% of the next generation's population)
        """
        # sort neural network population
        self.nn_population = sorted(self.nn_population, 
                                    key=lambda nn: nn.rank)    
        # choose the fittest 20%
        fit_list = self.nn_population[0:int(self.population_size * 0.2)]
        
        new_nn_population = []     
        
        # elitism (20%)
        for nn in fit_list:
            new_nn_population.append(nn) 
            
        # mutation (60%)
        for nn in fit_list:
            for i in range(3):
                temp_nn = copy.deepcopy(nn)
                temp_nn.mutate(mutation_rate) 
                new_nn_population.append(temp_nn)
                
        # crossover (20%)
        for nn in fit_list:
            temp_nn = copy.deepcopy(nn)                
            temp_nn.crossover(np.random.choice(fit_list)) 
            new_nn_population.append(temp_nn)
                
        # population size of each generation must remain constant
        assert len(self.nn_population) == len(new_nn_population)
        self.nn_population = new_nn_population 
        
        # reset neural networks' rank
        for nn in self.nn_population:
            nn.rank = 0
            
    def save(self, generation, distance):
        """
        Save best neural network of current generation into .npz file
        """
        self.nn_population[0].save(generation, distance)
        
    def load(self, filename):
        """
        Load neural network from appropriate .npz file 
        """
        nn = NeuralNetwork([])
        nn.load(filename)
        self.nn_population = [nn]

        
        