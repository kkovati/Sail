import numpy as np
from sail import Simulator


if __name__ == '__main__':
    
    np.random.seed(2)
    
# =============================================================================
#     nn_architectures = [[4,2],
#                         [6,4], 
#                         [8,6],
#                         [10,6],
#                         [4,4,2],
#                         [6,4,2],
#                         [8,4,2],
#                         [10,6,4]]
#     
#     for nna in nn_architectures:
#         s = Simulator(nn_architecture=nna, 
#                       generation_count=50,
#                       population_size=80,
#                       mutation_rate=30)    
#         s.run(display=False)                 
# =============================================================================
  


    s = Simulator(nn_architecture=[8,6],
                  generation_count=100,
                  population_size=100,
                  mutation_rate=30,
                  random_race=True,
                  race_count=3)    
    s.run(display=True, disp_from_gen=30) 

    
# =============================================================================
#     Simulator.load_and_test('simulation_results/[2,10,6,1]_21_2200.npz')
# =============================================================================

