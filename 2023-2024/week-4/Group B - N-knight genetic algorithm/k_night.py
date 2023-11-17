import random
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk


def initialize_population(population_size, board_size):
    population = []
    for _ in range(population_size):
        board = np.random.randint(2, size=(board_size, board_size))
        population.append(board)
    return population

root = tk.Tk()
root.title("Knight's Tour Genetic Algorithm")

board_label = tk.Label(root, text="", font=("Courier", 12))

board_canvas = tk.Canvas(root, width=400, height=400)
board_canvas.pack()

def load_knight_image():
    # Load your knight image here (replace 'knight.png' with your file)
    knight_image = Image.open('knight.jpg')
    knight_image = knight_image.resize((40, 40))  # Adjust size as needed
    return ImageTk.PhotoImage(knight_image)

knight_image = load_knight_image()

def display_board(board):
    cell_size = 40  # Adjust size as needed

    # Create a chessboard grid with lines
    for x in range(len(board)):
        for y in range(len(board[x])):
            x0, y0 = x * cell_size, y * cell_size
            x1, y1 = (x + 1) * cell_size, (y + 1) * cell_size
            if (x + y) % 2 == 0:
                board_canvas.create_rectangle(x0, y0, x1, y1, fill='white', outline='black')
            else:
                board_canvas.create_rectangle(x0, y0, x1, y1, fill='black', outline='black')

            if board[x, y] == 1:
                knight_x, knight_y = x0, y0
                board_canvas.create_image(knight_x, knight_y, anchor='nw', image=knight_image)

    # Add labels for numbers and letters on the sides
    for i, letter in enumerate('abcdefgh'):
        x0, y0 = i * cell_size, 8 * cell_size
        board_canvas.create_text(x0 + cell_size // 2, y0 + cell_size // 2, text=letter, font=("Helvetica", 12))

    for i, number in enumerate('87654321'):
        x0, y0 = 8 * cell_size, i * cell_size
        board_canvas.create_text(x0 + cell_size // 2, y0 + cell_size // 2, text=number, font=("Helvetica", 12))


# Function to display boards
def display_boards(generation, population):
    board_canvas.delete("all")
    for i, board in enumerate(population):
        display_board(board)
        root.update_idletasks()
        root.after(1000)  # Pause for 1 second

def is_valid_position(x, y, board_size):
    return 0 <= x < board_size and 0 <= y < board_size

def count_attacks(board, x, y, board_size):
    attack_positions = [(-1, -2), (-1, 2), (-2, -1), (-2, 1),
                       (1, -2), (1, 2), (2, -1), (2, 1)]

    attacks = 0

    for dx, dy in attack_positions:
        new_x, new_y = x + dx, y + dy
        if is_valid_position(new_x, new_y, board_size) and np.any(board[new_x * board_size + new_y] == 1):
            attacks += 1

    return attacks

def fitness(board):
    board_size = int(len(board) ** 0.5)  # Assuming a square chessboard
    total_knights = 0
    total_attacks = 0

    for i in range(len(board)):
        if np.any(board[i] == 1):
            x, y = i // board_size, i % board_size  # Convert 1D index to 2D coordinates
            total_knights += 1
            total_attacks += count_attacks(board, x, y, board_size)

    return total_knights - total_attacks


def crossover(parent1, parent2):
    # Copy the parents to create children
    child1 = parent1.copy()
    child2 = parent2.copy()

    # Randomly select two positions for crossover
    board_size = parent1.shape[0]
    row1, col1 = random.randint(0, board_size-1), random.randint(0, board_size-1)
    row2, col2 = random.randint(0, board_size-1), random.randint(0, board_size-1)

    # Swap the values at the selected positions
    child1[row1, col1], child2[row2, col2] = child2[row2, col2], child1[row1, col1]

    return child1, child2


def mutate(board, mutation_rate):
    if random.random() < mutation_rate:
        # Randomly select a knight to mutate
        board_size = int(len(board) ** 0.5)
        position = random.randint(0, len(board) - 1)
        x, y = position // board_size, position % board_size

        # Clear the potential attack positions for the selected knight
        attack_positions = [(-1, -2), (-1, 2), (-2, -1), (-2, 1),
                           (1, -2), (1, 2), (2, -1), (2, 1)]

        for dx, dy in attack_positions:
            new_x, new_y = x + dx, y + dy
            if is_valid_position(new_x, new_y, board_size):
                position = new_x * board_size + new_y
                board[position] = 0

    return board

def select_parents(population, num_parents, best_parents_ratio=0.5):
    # Sort the population based on fitness (lower fitness is better)
    population.sort(key=lambda board: fitness(board))

    # Select the two best parents
    best_parents = population[:2]

    # Calculate the number of parents to be selected using random selection
    num_random_parents = num_parents - 2

    # Ensure there are enough random parents to select
    if num_random_parents > 0:
        # Select random parents with a higher probability for the better parent
        parents = best_parents * int(num_random_parents * best_parents_ratio)

        # Add random parents with the remaining slots
        parents += random.choices(population, k=num_random_parents - len(parents))
    else:
        # If num_parents is 2, just return the best parents
        parents = best_parents

    return parents

def genetic_algorithm(board_size, population_size, generations, mutation_rate):
    population = initialize_population(population_size, board_size)

    for generation in range(generations):
        new_population = []

        for _ in range(population_size):
            parent1, parent2 = random.choices(population, k=2)
            child1, child2 = crossover(parent1, parent2)  # Pass board_size to crossover
            child1 = mutate(child1, mutation_rate)
            child2 = mutate(child2, mutation_rate)
            new_population.extend([child1, child2])

        population = new_population

        # Print all the boards in the current generation
        print(f"Generation {generation + 1} Boards:")
        for i, board in enumerate(population):
            print(f"Board {i + 1}:")
            print(board)

            # Display boards for each generation
        # display_boards(generation, population)

    best_board = max(population, key=fitness)
    return best_board

if __name__ == "__main__":
    board_size = 8  # Change this to your desired board size
    population_size = 100
    generations = 100
    mutation_rate = 0.1

    best_solution = genetic_algorithm(board_size, population_size, generations, mutation_rate)

     # Create a final window to display the best solution
    display_board(best_solution)
    root.mainloop()

    # Return the best board from the final population
    print("Best Solution: \n", best_solution)
