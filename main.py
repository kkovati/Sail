import numpy as np
from controller_pack import Controller


if __name__ == '__main__':
    """
    Main function
    """
    np.random.seed(0)
    c = Controller()
    c.run()                 
  
    c.view.mainloop()
