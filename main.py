import numpy as np
from sail import Simulator


if __name__ == '__main__':
    """
    Main function
    """
    np.random.seed(0)
    s = Simulator(nn_architecture=[2,6,4,1], 
                  generation_count=200,
                  population_size=50,
                  mutation_rate=30)
    
    s.run()                 
  
    s.view.mainloop() #!!!!
