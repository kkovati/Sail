import copy
from .ship import Ship
from .neural_network import NeuralNetwork


class Population:
    """
    Population contains all neural networks through the evolution process
    During simulation Population contains all ship models
    """    
    def __init__(self, nn_architecture, population_size):
        self.nn_population = []        
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
        Orders the list of ship by fitness
        Fitness is based on the number of buoys reached, the minimum distance
        to the next target buoy and the time neeeded to reach all the buoys
        """
        ordered_ship_population = sorted(self.ship_population, 
                   key=lambda x: (-x.curr_buoy_index, x.min_distance, x.time))
        ordered_nn_population = []
        for ship in ordered_ship_population:
            ordered_nn_population.append(ship.nn)            
        self.nn_population = ordered_nn_population
        print('Best results:')
        print('{:<6s} {:<10s} {:<10s}'.format('Buoys', 'Distance', 'Time'))
        # print('Buoys\tDistance\tTime')
        for i in range(5):
            ship = ordered_ship_population[i]
            print('{:<6s} {:<10s} {:<10s}'.format(
                                            str(ship.curr_buoy_index), 
                                            str(int(ship.min_distance)), 
                                            str(ship.time)))
            
    def mutate(self, mutation_rate):
        """
        Creates the new generation based on the results of the simulation
        Elitism: the best 5 instances goes directly to the next generation
        The other 45 instances created by mutating the best 5
        """
        new_nn_population = []        
        # elitism
        for nn in self.nn_population[0:10]:
            new_nn_population.append(nn) 
        # mutation
        for nn in self.nn_population[0:10]:
            for i in range(4):
                temp_nn = copy.deepcopy(nn)
                temp_nn.mutate(mutation_rate) 
                new_nn_population.append(temp_nn)
        self.nn_population = new_nn_population 
        print('pop_size:', len(self.nn_population))           
            
    def save(self, filename):
        self.nn_population[0].save(filename)
        
    def load(self, filename, number):
        self.nn_population = []
        for i in range(number):
            nn = NeuralNetwork()
            nn.load(filename)
            self.nn_population.append(nn)
        self.mutate()
        
        