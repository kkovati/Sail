import numpy as np
from sail import Simulator


if __name__ == '__main__':

    
    np.random.seed(0)
    
    nn_architectures = [[6,4], [8,6], [6,4,2]]
    
    for nna in nn_architectures:
        s = Simulator(nn_architecture=nna, 
                      generation_count=5,
                      population_size=80,
                      mutation_rate=30)    
        s.run(display=False)                 
  

