from flask import Flask, request, render_template
import random

app = Flask(__name__)
# Constants
N = 9  # Size of the Sudoku grid (9x9)


# Function to initialize the Sudoku board with some given values
def initialize_board():
    board = [[0] * N for _ in range(N)]

    # Define the initial values for predetermined cells
    board = [
        [3, 4, 0, 0, 5, 0, 0, 0, 0],
        [0, 7, 1, 0, 2, 9, 0, 0, 5],
        [2, 5, 0, 0, 0, 0, 9, 8, 0],
        [7, 6, 0, 9, 0, 0, 0, 0, 8],
        [5, 0, 0, 4, 0, 7, 0, 0, 2],
        [0, 3, 0, 0, 0, 6, 0, 4, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 4, 3, 0, 6, 0],
        [0, 0, 0, 0, 0, 0, 5, 2, 4],
    ]

    return board


# Function to fill predetermined cells with unique digits
def fill_predetermined_cells(board):
    for row in range(N):
        for col in range(N):
            if board[row][col] == 0:
                possible_values = set(range(1, N + 1))

                # Remove values already in the same row
                possible_values -= set(board[row])

                # Remove values already in the same column
                possible_values -= set(board[i][col] for i in range(N))

                # Remove values already in the same subgrid
                subgrid_values = get_subgrid_values(board, row, col)
                possible_values -= set(subgrid_values)

                # If there's only one possible value, assign it to the cell
                if len(possible_values) == 1:
                    board[row][col] = possible_values.pop()

    return board


# Helper function to get the values in the subgrid of a cell
def get_subgrid_values(board, row, col):
    subgrid_row, subgrid_col = row // 3, col // 3
    subgrid_values = []

    for i in range(3):
        for j in range(3):
            subgrid_values.append(board[subgrid_row * 3 + i][subgrid_col * 3 + j])

    return subgrid_values


# Function to evaluate the fitness of a Sudoku board
def fitness(board):
    fitness_score = 0

    # Check rows
    for row in board:
        fitness_score += 9 - len(set(row))

    # Check columns
    for col in range(N):
        column = [board[row][col] for row in range(N)]
        fitness_score += 9 - len(set(column))

    # Check sub-grids (3x3 grids)
    for start_row in range(0, N, 3):
        for start_col in range(0, N, 3):
            subgrid_values = get_subgrid_values(board, start_row, start_col)
            fitness_score += 9 - len(set(subgrid_values))

    # Count the number of zeros (empty cells) in the board
    zeros_count = sum(row.count(0) for row in board)

    # Add a penalty for each zero
    fitness_score += zeros_count

    return fitness_score


# Function for tournament selection
def tournament_selection(population, tournament_size):
    # Randomly select a subset of individuals for the tournament
    tournament = random.sample(population, tournament_size)
    # Return the individual with the lowest fitness score from the selected ones
    return min(tournament, key=lambda x: x[1])


# Function for single-point crossover with constraints
def crossover(parent1, parent2):
    # Create two new boards
    child1 = [[0] * N for _ in range(N)]
    child2 = [[0] * N for _ in range(N)]

    # Randomly select a range of rows and columns to perform crossover
    crossover_start_row = random.randint(0, N - 1)
    crossover_end_row = random.randint(crossover_start_row, N - 1)
    crossover_start_col = random.randint(0, N - 1)
    crossover_end_col = random.randint(crossover_start_col, N - 1)

    # Copy the selected range from parent1 to child1 and from parent2 to child2
    for row in range(N):
        for col in range(N):
            if (crossover_start_row <= row <= crossover_end_row) and (
                crossover_start_col <= col <= crossover_end_col
            ):
                child1[row][col] = parent1[row][col]
                child2[row][col] = parent2[row][col]
            else:
                child1[row][col] = parent2[row][col]
                child2[row][col] = parent1[row][col]

    # Ensure that each number appears only once in each row, column, and subgrid
    for i in range(N):
        for j in range(N):
            row = child1[i]
            col = [child1[k][j] for k in range(N)]

            if row.count(child1[i][j]) > 1 or col.count(child1[i][j]) > 1:
                # If a number appears more than once in the row or column, swap it with the corresponding number in the other child
                for x in range(N):
                    if row.count(child2[i][x]) == 0:
                        child1[i][j], child2[i][x] = child2[i][x], child1[i][j]
                        break

    return child1, child2


# Function for mutation with constraints
def mutate(board, mutation_rate):
    for row in range(N):
        for col in range(N):
            if random.random() < mutation_rate:
                # Check if the element is not fixed or predetermined
                if board[row][col] == 0:
                    # Get the available values for the cell
                    available_values = [
                        value
                        for value in range(1, N + 1)
                        if is_value_available(board, row, col, value)
                    ]

                    if available_values:
                        # Shuffle the available values for randomness
                        random.shuffle(available_values)
                        new_value = available_values[0]
                        board[row][col] = new_value

    return board


# Helper function to check if a value is available for a cell
def is_value_available(board, row, col, value):
    # Check if the value is not in the same row, column, or subgrid
    row_values = board[row]
    col_values = [board[i][col] for i in range(N)]
    subgrid_row, subgrid_col = row // 3, col // 3
    subgrid_values = []

    for i in range(3):
        for j in range(3):
            subgrid_values.append(board[subgrid_row * 3 + i][subgrid_col * 3 + j])

    return (
        value not in row_values
        and value not in col_values
        and value not in subgrid_values
    )


@app.route("/", methods=["GET"])
def home():
    initial_board = initialize_board()
    return render_template("index.html", board=initial_board)


@app.route("/solve", methods=["POST"])
def solve_sudoku():
    # Retrieve the initial Sudoku board from the form or another source
    initial_board = initialize_board()

    population_size = 250  # You can adjust this number based on your preferences
    tournament_size = 10  # Adjust this value as needed
    mutation_rate = 0.5  # Adjust this value as needed
    max_generations = 500  # Set your termination condition (e.g., maximum generations)

    # Initialize a population with random Sudoku boards
    population = [
        fill_predetermined_cells(initialize_board()) for _ in range(population_size)
    ]

    best_fitness = float(
        "inf"
    )  # Initialize the best fitness score to positive infinity
    best_board = None  # Initialize the best board

    generations_stuck = (
        0  # Counter to keep track of generations with no fitness improvement
    )
    max_generations_stuck = 50  # Maximum allowed generations with no improvement

    for generation in range(max_generations):
        # Evaluate fitness for each board in the population
        fitness_scores = [fitness(board) for board in population]

        # Find the best fitness score and board in this generation
        current_best_fitness = min(fitness_scores)
        current_best_board = population[fitness_scores.index(current_best_fitness)]

        # If the current best fitness score hasn't improved, increase the stuck counter
        if current_best_fitness >= best_fitness:
            generations_stuck += 1
        else:
            # Reset the stuck counter and update the best fitness and board
            generations_stuck = 0
            best_fitness = current_best_fitness
            best_board = current_best_board

        # Print the best fitness score in this generation
        print(f"Generation {generation}: Best Fitness Score = {best_fitness}")

        # Check if it's a multiple of 10 and print the Sudoku board
        if generation % 100 == 0:
            print("Sudoku Board:")
            for row in best_board:
                print(row)

        # If stuck for too many generations, introduce more random variation
        if generations_stuck >= max_generations_stuck:
            # Regenerate the entire population with some random boards
            print("Regenerate the entire population...")
            population = [
                fill_predetermined_cells(initialize_board())
                for _ in range(population_size)
            ]
            generations_stuck = 0
            # Reinitialize the best fitness and best board
            best_fitness = float("inf")
            best_board = None
        # Perform selection (you can use tournament_selection)
        selected_boards = [
            tournament_selection(list(zip(population, fitness_scores)), tournament_size)
            for _ in range(population_size)
        ]

        # Perform crossover (you can use crossover function)
        children = []
        for i in range(0, len(selected_boards), 2):
            parent1, _ = selected_boards[i]
            parent2, _ = selected_boards[i + 1]
            child1, child2 = crossover(parent1, parent2)
            children.extend([child1, child2])

        # Perform mutation (you can use mutate function)
        for i in range(len(children)):
            if random.random() < mutation_rate:
                children[i] = mutate(children[i], mutation_rate)

        # Replace the old population with the new generation
        population = children

        # Check if a solution has been found (fitness_score == 0 for a complete Sudoku)
        if best_fitness == 0:
            print("Solution Found!")
            print(f"Best Solution:")
            for row in best_board:
                print(row)
            return render_template(
                "index.html", board=initial_board, solved_board=best_board
            )

        # Optionally, print or log the best solution in this generation

    # At the end of the loop, you can retrieve the best solution found in the population
    best_solution, fitness_score = min(
        list(zip(population, fitness_scores)), key=lambda x: x[1]
    )
    print("No solutions found!")
    print(f"fitness score: {fitness_score}")
    print(f"Best Solution:")
    for row in best_solution:
        print(row)

    # Once solved, return the solved board
    solved_board = best_solution  # Replace this with the actual solved board

    return render_template("index.html", board=initial_board, solved_board=solved_board)


if __name__ == "__main__":
    app.run(debug=True)
