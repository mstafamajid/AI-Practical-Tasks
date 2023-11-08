
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

import os

# Parameters
POPULATION_SIZE = 200
MUTATION_RATE = 0.01
CROSSOVER_RATE = 0.5
GENERATIONS = 500


script_path = os.path.abspath(__file__)
# Extract the directory containing the script
script_directory = os.path.dirname(script_path)

image_path = os.path.join(script_directory, "binary.png")

# Convert to grayscale
image = Image.open(image_path).convert('L')

# Convert image to numpy array and threshold to binary
threshold = 128  # This value can be adjusted based on your needs
target_image = np.array(image) > threshold

# Target image: 20x20 binary image
# target_image = np.random.choice([0, 1], (20, 20))


# Fitness function


def fitness(chromosome):
    reshaped = chromosome.reshape(20, 20)
    return np.sum(target_image == reshaped)
    

# Mutation function


def mutate(chromosome):
    for idx in range(len(chromosome)):
        if np.random.rand() < MUTATION_RATE:
            chromosome[idx] = 1 - chromosome[idx]
    return chromosome

# Crossover function


def crossover(parent1, parent2):
    child1, child2 = parent1.copy(), parent2.copy()
    if np.random.rand() < CROSSOVER_RATE:
        point = np.random.randint(len(parent1))
        child1[:point], child2[:point] = parent2[:point], parent1[:point]
    return child1, child2


def on_close(event):
    plt.close('all')
    os._exit(0)


# Genetic Algorithm


def genetic_algorithm():
    plt.ion()
    fig, ax = plt.subplots(1, 2)
    fig.canvas.mpl_connect('close_event', on_close)
    
    ax[0].set_title("Target Image")
    
    # Initialize population
    pop = np.array([np.random.choice([0, 1], 400)
                for _ in range(POPULATION_SIZE)])
    print(pop.shape)

    for generation in range(GENERATIONS):
        fit = np.array([fitness(chromosome) for chromosome in pop])
        # Display best solution
        best_index = np.argmax(fit)
        best_fitness = fit[best_index]
        best_solution = pop[best_index].reshape(20, 20)

        
        ax[0].imshow(target_image, cmap='gray')
        ax[1].imshow(best_solution, cmap='gray')
        ax[1].set_xlabel(f"Gen: {generation}, Fitness: {fit[best_index]}")
        plt.pause(0.1)

        if best_fitness == 400:
            print("Perfect match found at generation:", generation)
            break
        ax[1].cla()

        # Selection
        parents = pop[np.argsort(fit)[-2:]]

        # Creating the next generation
        next_gen = []
        for _ in range(POPULATION_SIZE // 2):
            child1, child2 = crossover(*parents)
            next_gen.append(mutate(child1))
            next_gen.append(mutate(child2))

        pop = np.array(next_gen)

    plt.ioff()
    plt.show()


genetic_algorithm()
