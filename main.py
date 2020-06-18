import numpy as np
from sail import Simulator


if __name__ == '__main__':
    """
    Main function
    """    
     
# =============================================================================
#     import matplotlib.pyplot as plt
# 
#     a = [1,2,5,4,7]
#     b = range(5)
#     
#     plt.title('Measurements')
#     plt.xlabel('time [usec]')
#     plt.ylabel('voltage [V]')
# =============================================================================
    
    np.random.seed(0)
    
    s = Simulator(nn_architecture=[2,6,4,1], 
                  generation_count=3,
                  population_size=45,
                  mutation_rate=30)
    
    s.run()                 
  

