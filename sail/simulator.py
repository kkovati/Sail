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
                 mutation_rate):
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
        """
        self.nn_architecture = [2] + nn_architecture + [1]
        self.generation_count = generation_count
        self.population_size = (population_size // 10) * 10
        self.mutation_rate = mutation_rate
        
        # init model and view
        self.model = Model(self.nn_architecture, self.population_size)
        self.view = View()
        
    def run(self, display=False):
        """
        Runs evolution for given numbers of generations and saves the results
        of the current configuration
        Parameters
        ----------
        display : boolean
            !!!
        """
        # test results of the generations
        self.test_results = np.zeros((self.generation_count), dtype ='int32')
        
        # run the generations
        for i in range(self.generation_count):          
            self.run_generation(i, display)
            
        self.plot_results()      
            
        self.model.save('best_ship.npz') 
        # self.view.mainloop()
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
        
        # normal generation simulation in random environment        
        for i in range(3):
            print('- {}. race'.format(i + 1))
            self.model.prepare_generation()
            self.view.prepare_generation(self.model, display, generation_index)
            self.run_simulation()
            print('')
            self.view.clear()
            self.evaluate()
            
        self.mutate(generation_index)
        
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
        
        self.test_results[generation_index] = distance
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
        self.model.evaluate()
        
    def mutate(self, generation_index):
        """
        As the evolution progress the mutation rate decays to prevent the
        osciallation in the performance of the best neural network in each
        generation
        """
        mr = self.mutation_rate * (1 - 0.5 * (generation_index / 
                                              self.generation_count))
        self.model.mutate(mr) 
        
    def plot_results(self):
        
        # plt.figure(dpi=300) # for high resolution graphs
        plt.title('Best ship travel distance of each generation')
        plt.xlabel('Generation')
        plt.ylabel('Distance')
        info_label = ('NN: ' + str(self.nn_architecture) + '\nGens: ' + 
                      str(self.generation_count) + '\nPop size: ' + 
                      str(self.population_size) + '\nMutation: ' + 
                      str(self.mutation_rate))
        plt.gca().set_ylim([200,2200])
        plt.figtext(0.65, 0.15, info_label)          
        y = range(self.generation_count)
        plt.plot(y, self.test_results)        
        
        # save figure
        filename = ('simulation_results/' + 
                    str(self.nn_architecture) + '_' + 
                    str(self.generation_count) + '_' + 
                    str(self.population_size) + '_' + 
                    str(self.mutation_rate))        
        plt.savefig(filename, dpi=300)
        
        plt.show() 
          
    