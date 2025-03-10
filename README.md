# ⛵ Sail

Neural network learns to control sailing ship with genetic algorithm.

[![Demo](https://github.com/kkovati/Sail/blob/master/docs/demo.gif)](https://youtu.be/wNEWmePgh4I)

### 🧬 Simulation with genetic algorithm
 
The objective of the ships (controlled by neural networks) is to reach all target buoys 
one after another in the shortest possible time. 
A neural network's inputs are the direction of the next target buoy 
and the direction of the wind relative to the ship and its output is the steering angle of the ship.

At the beginning of the simulation the neural networks do not know what is their objective but as the simulation
progresses they start to 'understand' it and become better with each generation.

The implementation of the neural networks and genetic operations done using only **NumPy**.<br/>
The GUI is made with **Tkinter**, visualized with its graphical drawing tools.
 
### 🌱 Generations
 
The simulation is divided into generations. Each generation has a population of different instances (neural networks)
who are competing against each other. Each generation competes on a randomly generated map 
where the number and position of the buoys, the wind direction and the start position are random.
The new generations evolves from the previous ones. 
 
### 🏆 Selection based on fitness
 
The new generation is created using the best instances and the selection is based on their fitness.
The fitness is calculated by the performance of the ships (~neural networks) according to how many 
bouys they reached, how close they approached the next buoy and how much time needed to reach all buoys.
 
### 🎲 Genetic operators
 
The genetic algorithm uses the following strategies during the optimization:
 
- **Elitism**: the best selected instances goes directly to the next generation
- **Mutation**: the best selected instances' parameters randomly modified
- **Crossover**: averaging the parameters of randomly chosen pairs from the best selected instances 

### 🦋 Evolve

The new generation is built up with instances created by the genetic operators.

### 🌊 Physics

The ships sail fastest downwind (in the direction of the wind) and become slower as they turn into
upwind (opposite of wind). Also the ships get speed penalty if they steer too rapidly. 

### ⚙️ Simulation settings

For optimization the following settings can be customized:

- Neural network architecture (number of neurons in each hidden layer)
- Population size (no. of instances in a generation)
- Mutation rate (maximum rate of random NN parameter modification)
- Number of generations
- Number of races before evolving (more races result more accurate selection of the fittest NN)
- Random or pre-fixed races (each generation races on random or on the same map)

---
## 🎥 Demo video of a simulation and analysis

[Simulation video on YouTube](https://youtu.be/wNEWmePgh4I)

This linked video shows an evolution progress with the following settings:
- a simple NN architecture with only one hidden layer of 5 neurons, 
- population size is 100,
- mutation rate is 30%,
- there are two random races before evolving a generation

It can be seen that the first generations do not know what is their goal and just sailing pointless.
As the simulation advances the ships start to steer better and better towards their target buoy.
There is a huge jump in performance started from the 14th generation.<br/>

This video is edited to show only the relevant parts. (Poor upload resolution) 

## 🚀 Run the simulation

Requires Python 3.7+ and dependencies from requirements.txt (```pip install -r requirements.txt```).<br>
[The code](https://github.com/kkovati/Sail/blob/master/main.py) for the above simulation:
 
```python
from sail import Simulator

sim = Simulator(
    nn_architecture=[5],
    generation_count=50,
    population_size=100,
    mutation_rate=30,
    random_race=True,
    race_count=2)    

sim.run(display=True, disp_from_gen=0)
```

## ⚡ Plans for improvement 

The neural networks could not learn how to efficiently sail upwind by the end
of the simulation. The expected strategy is turning away from wind thus reaching greater velocity,
but seemingly they always approach the target buoy directly, not paying attention to the wind direction.
