import numpy as np
from sail import Simulator


def main():
    np.random.seed(2)

    sim = Simulator(nn_architecture=[5],
                    generation_count=50,
                    population_size=100,
                    mutation_rate=30,
                    random_race=True,
                    race_count=2)

    sim.run(display=True, disp_from_gen=0)


if __name__ == '__main__':
    main()
