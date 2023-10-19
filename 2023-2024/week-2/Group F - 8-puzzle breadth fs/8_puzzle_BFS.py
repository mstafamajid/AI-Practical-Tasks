import queue
import random
import tkinter as tk
from tkinter import messagebox

import os
# Get the absolute path of the script being executed
script_path = os.path.abspath(__file__)
# Extract the directory containing the script
script_directory = os.path.dirname (script_path)

solution_path = os.path.join(script_directory,"solution.txt")

# Create the main GUI window
root = tk.Tk()
root.title("8-Puzzle Solver by BFS")

# Define the goal state
goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]

# Function to check if two puzzle states are equal
def is_goal_state(state):
    return state == goal_state

# Function to get valid neighbor states for a given state
def get_neighbors(state):
    neighbors = []

    empty_index = state.index(0)
    row, col = divmod(empty_index, 3)

    # Possible moves: left, right, up, down
    moves = [(0, -1), (0, 1), (-1, 0), (1, 0)]

    for dr, dc in moves:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            neighbor_state = state[:]
            # Calculate the index of the tile to swap with the empty tile
            neighbor_index = new_row * 3 + new_col
            neighbor_state[empty_index], neighbor_state[neighbor_index] = (  # Swapping process with empty tile with the neighbor
                neighbor_state[neighbor_index],
                neighbor_state[empty_index],
            )
            neighbors.append(neighbor_state)

    return neighbors

# Function to perform breadth-first search
def bfs(initial_state):
    frontier = queue.Queue()
    visited = set()
    parent = {}
    cost = {}

    frontier.put(initial_state)
    visited.add(tuple(initial_state))
    cost[tuple(initial_state)] = 0

    while not frontier.empty():
        current_state = frontier.get()

        if is_goal_state(current_state):
            path = []
            while current_state != initial_state:
                path.append(current_state)
                current_state = parent[tuple(current_state)]
            path.append(initial_state)
            path.reverse()
            return path

        for neighbor_state in get_neighbors(current_state):
            if tuple(neighbor_state) not in visited:
                frontier.put(neighbor_state)
                visited.add(tuple(neighbor_state))
                parent[tuple(neighbor_state)] = current_state
                cost[tuple(neighbor_state)] = cost[tuple(current_state)] + 1

    return None

# Generate a random initial state
def generate_random_puzzle():
    puzzle = list(range(9))
    random.shuffle(puzzle)
    return puzzle

def save_solution_to_file(initial_state, path_solution):
    
    with open(solution_path, "w") as file:
        file.write("Initial Puzzle Board:\n")
        for i in range(0, 9, 3):
            file.write(" ".join(map(str, initial_state[i: i + 3])) + "\n")

        if path_solution:
            file.write("\nSteps to Solution:\n")
            for step, state in enumerate(path_solution):
                file.write(f"Step {step + 1}:\n")
                for i in range(0, 9, 3):
                    file.write(" ".join(map(str, state[i: i + 3])) + "\n")
            file.write("\nOverall Cost of Solution: {}\n".format(
                len(path_solution) - 1))
        else:
            file.write("\nNot Solvable!")
            messagebox.showerror("No Solution", "The puzzle is not solvable!")

# Create labels for the puzzle grid
labels = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
for i in range(3):
    for j in range(3):
        labels[i][j] = tk.Label(root, width=5, height=2, font=("Arial", 30))
        labels[i][j].grid(row=i, column=j)

# Function to update the GUI with the current state
def update_gui():
    for i in range(3):
        for j in range(3):
            cell_value = initial_state[i * 3 + j]
            labels[i][j].config(text=str(cell_value)
                                if cell_value != 0 else "", state=tk.DISABLED)

# Function to automatically solve the puzzle
def solve_puzzle():
    solution_path = bfs(initial_state)
    if solution_path:
        for step, state in enumerate(solution_path):
            # Update GUI every 500ms
            root.after(
                step * 500, lambda state=state: update_initial_state(state))
        root.after((len(solution_path)) * 500, show_success_message)
    else:
        print("Not Solvable !")

# Function to update the puzzle state and GUI
def update_initial_state(new_state):
    global initial_state
    initial_state = new_state
    update_gui()


def show_nosolution_message():
    messagebox.showerror("Error", "No solution found.")

def show_success_message():
    messagebox.showinfo("Success", "Puzzle Solved!")

def start_puzzle_solving():
    root.after(2000, solve_puzzle)

# Generate a random initial solvable state
initial_state = generate_random_puzzle()

# Solve the puzzle using BFS
path_solution= bfs(initial_state)

# save to file and do solution
save_solution_to_file(initial_state, path_solution)
# Update the GUI with the initial puzzle state
update_gui()


# Automatically solve the puzzle after the GUI is initialized
start_puzzle_solving()

# Run the main loop
root.mainloop()
