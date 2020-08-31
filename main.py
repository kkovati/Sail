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
# =============================================================================

# =============================================================================
#     nn_architectures = [[1],[2],[3],[4],[5],[6],[7],[8],[9],[10],[11],[12],
#                         [13],[14],[15]]
#     
#     for nna in nn_architectures:
#         s = Simulator(nn_architecture=nna, 
#                       generation_count=20,
#                       population_size=100,
#                       mutation_rate=30,
#                       random_race=False,
#                       race_count=3)    
#         s.run(display=False, disp_from_gen=15)                 
# =============================================================================
      

    s = Simulator(nn_architecture=[5],
                  generation_count=50,
                  population_size=100,
                  mutation_rate=30,
                  random_race=True,
                  race_count=2)    

    s.run(display=True, disp_from_gen=0) 

    
# =============================================================================
#     Simulator.load_and_test('simulation_results/[2,11,1]_6_2181.npz')
# =============================================================================

