import numpy as np
import matplotlib.pyplot as plt
from .model_pack import Model
from .view_pack import View, LoadingBar


class Simulator():
    """
    Simulates the evolution of the ships learning to sail
    Acts as a controller between models and views
    """
    def __init__(self, nn_architecture, generation_count, population_size, 
                 mutation_rate, random_race=True, race_count=1):
        """
        Initalizes Model and View
        Parameters
        ----------
        nn_architecture : list of integers
            neuron number of each hidden layer in the neural network
        generation_count : int
            number of generations during the evolution
        population_size : int 
            number of instances (ships) in one generation
        mutation_rate : int
            change of the neural network parameters during mutation in 
            percentage
        random_race : boolean
            if True ships will compete on randomly generated race environment
            (buoys placement, start position, wind direction), else each
            generation will compete on the same 3 pre-defined races
        race_count : int
            number of random races of each generation
            (omitted if random_race == False)
        """
        self.nn_architecture = [2] + nn_architecture + [1]
        self.generation_count = generation_count
        self.population_size = (population_size // 10) * 10
        self.mutation_rate = mutation_rate
        self.random_race = random_race
        # there are 3 pre-defined race tracks
        self.race_count = race_count if random_race else 3
        
        # init Model and View
        self.model = Model(self.nn_architecture, self.population_size) 
        self.view = View()
        
    def run(self, display=False, disp_from_gen=0):
        """
        Runs evolution for given numbers of generations and saves the results
        of the current configuration
        Parameters
        ----------
        display : boolean
            !!!
        """
        # test results of each generations
        self.test_results = np.zeros((self.generation_count), dtype ='int32')
        
        # run the generations
        for i in range(self.generation_count):
            if display and i >= disp_from_gen:
                self.run_generation(i, display=True)
            else:
                self.run_generation(i, display=False)
            
        self.plot_results()      
           
        self.view.root.destroy()
  
    def run_generation(self, generation_index, display=False):
        """
        Runs a single generation's simulation
        Evaluates the neuaral network population by fitness
        Mutates the population
        Runs the 3 test cases for results with the best neural network        
        """
        print('------------------------------------------')
        print(generation_index, '.generation')
        
        # normal generation simulation in a standard or random environment        
        for race_number in range(1, self.race_count + 1):
            print('- {}. race'.format(race_number))
            self.model.prepare_generation(self.random_race, race_number)
            self.view.prepare_generation(self.model, display, generation_index,
                                         race_number)
            self.run_simulation()
            print('')
            self.view.clear()
            self.evaluate()
            
        self.evolve(generation_index)
        
        # test run of current generation's best ship
        print('\nTest of', generation_index, '.generation')
        self.model.prepare_test()            
        self.view.prepare_generation(self.model, display, 
                                     generation_index, test=True)
        self.run_simulation(test=True)        
        
        # calculate test results
        ship = self.model.population.ship_population[0]  
        if ship.curr_buoy_index == 4:
            distance = 2200
        else:
            distance = 550 * (ship.curr_buoy_index + 1) - ship.min_distance
        print('Distance sailed on test track:\n{}'.format(int(distance)))
        # save best ship's test distance into test_results
        self.test_results[generation_index] = distance
        # !!!
        if distance > 1800:
            print('DISTANCE OVER 1800')
            self.model.save(generation_index, distance)
        self.view.clear()  
        
    def run_simulation(self, test=False):
        """
        Runs simulation by calls model.update() and view.update() methods
        for 1000 time units at most
        """
        lb = LoadingBar(1000, 'Simulation')
        for t in range(1000):
            self.model.update(t)
            self.view.update(self.model, t)
            # stop simulation if all ships reached all the targets
            if self.model.population.finished:                
                return            
            if not test:
                lb()             
        
    def evaluate(self):
        # !!!
        self.model.evaluate()
        
    def evolve(self, generation_index):
        """
        As the evolution progress the mutation rate decays to prevent the
        oscillation in the performance of the best neural network in each
        generation
        """
        mr = self.mutation_rate * (1 - 0.1 * (generation_index / 
                                              self.generation_count))
        self.model.evolve(mr) 
        
    def plot_results(self):
        
        # plt.figure(dpi=300) # for high resolution graphs
        plt.title('Best ship travel distance of each generation')
        plt.xlabel('Generation')
        plt.ylabel('Distance')
        info_label = ('NN: ' + str(self.nn_architecture).replace(' ','') + 
                      '\nGens: ' + str(self.generation_count) + 
                      '\nPop size: ' + str(self.population_size) + 
                      '\nMutation: ' + str(self.mutation_rate))
        plt.gca().set_ylim([200,2200])
        plt.figtext(0.65, 0.15, info_label)          
        y = range(self.generation_count)
        plt.plot(y, self.test_results)        
        
        # save figure
        filename = ('simulation_results/' + 
                    str(self.nn_architecture).replace(' ','') + '_' + 
                    str(self.generation_count) + '_' + 
                    str(self.population_size) + '_' + 
                    str(self.mutation_rate))        
        plt.savefig(filename, dpi=300)
        
        plt.show() 
        
    @classmethod
    def load_and_test(cls, filename):
        # init Model and View
        model = Model([], 1) 
        view = View()
          
        # inject loaded ship
        model.load(filename) 
        
        # test run of current generation's best ship
        print('\nTest of', filename)
        model.prepare_test()            
        view.prepare_generation(model, display=True, generation_index=-1, 
                                test=True)
        
        # run test simulation
        for t in range(1000):
            model.update(t)
            view.update(model, t)
            # stop simulation if ship reached all the targets
            if model.population.finished:                
                break            
        
        view.root.destroy()
     
        
