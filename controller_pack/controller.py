import sys
import numpy as np
import matplotlib.pyplot as plt
from model_pack import Model
from view_pack import View


class Simulator():
    """
    Simulator is responsible for handling the simulation
    Acts as a controller
    """
    def __init__(self, nn_architecture, generation_count, population_size, 
                 mutation_rate):
        self.generation_count = generation_count
        self.mutation_rate = mutation_rate
        self.model = Model(nn_architecture, population_size)
        self.view = View()
        
    def run(self):
        """
        Runs evolution for given numbers of generations
        """
        # test results of all generations of 3 test cases
        self.test_results = np.zeros((3, self.generation_count), dtype ='int32')
        for i in range(self.generation_count):
            display = i > 3           
            self.run_generation(i, display)
        # create graph of results
        t = range(self.generation_count)
        plt.plot(t, self.test_results[0], 'r')
        plt.plot(t, self.test_results[1], 'g')
        plt.plot(t, self.test_results[2], 'b')        
        plt.show()       
            
        self.model.save('best_ship.npz')
        self.view.mainloop() #!!!!
  
    def run_generation(self, generation_index, display=False):
        """
        Runs a single generation simulation
        Evaluates the neuaral network population by fitness
        Mutates the population
        Runs the 3 test cases for results with the best neural network
        """
        print('------------------------------------------')
        # normal generation simulation in random environment
        print(generation_index, '.generation')
        self.model.prepare_generation()
        self.view.prepare_generation(self.model, display, generation_index)
        self.run_simulation()
        print('')
        self.view.clear()
        self.evaluate()
        self.mutate(generation_index)
        # testing with the 3 test cases
        for test_id in range(3):            
            print('Test case no.', test_id, 'of', generation_index, 
                  '.generation')
            self.model.prepare_test(test_id)            
            self.view.prepare_generation(self.model, display, 
                                         generation_index, test=True)
            time = self.run_simulation(test=True)
            print('Result:', time)
            self.test_results[test_id][generation_index] = time
            self.view.clear()  
        
    def run_simulation(self, test=False):
        """
        Runs simulation by calls model.update() and view.update() methods
        for 1000 time units at most
        """
        for t in range(1000):
            self.model.update(t)
            self.view.update(self.model, t)
            # stop simulation if all ships reached all the targets
            if self.model.population.finished:                
                return t
            if not test:
                message = (str(t + 1) + "/1000 Simulation time |" + 
                           "|" * int(30 * t / 1000) + 
                           "." * int(30 * (1 - (t / 1000))) + "|  ")                
                sys.stdout.write('\r' + message) 
        return 1000
        
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
          
    