import os
import time
import threading
from tkinter import messagebox
from vacuum_board.vacuum import *

# Just setting the board up
set_board(get_random_board())
board_thread = threading.Thread(target=board)
board_thread.start()
time.sleep(2)  # give some time for GUI startup and initialization

# Depth First Search Algorthim
# To be studied
def find_shortest_path(board):
    def is_in_board(x, y):
        return 0 <= x < len(board) and 0 <= y < len(board[0])

    def dfs(x, y, path):
        if not is_in_board(x, y) or board[x][y] == 0 or visited[x][y]:
            return

        path.append((x, y))
        visited[x][y] = True

        if board[x][y] == 5:  # Destination
            nonlocal shortest_path
            if shortest_path is None or len(path) < len(shortest_path):
                shortest_path = path.copy()

        # Try moving in all four directions: up, down, left, right
        dfs(x - 1, y, path)  # Top
        dfs(x + 1, y, path)  # Bottom
        dfs(x, y - 1, path)  # Left
        dfs(x, y + 1, path)  # Right

        # Backtrack
        path.pop()
        visited[x][y] = False

    visited = [[False for _ in range(len(board[0]))] for _ in range(len(board))]
    shortest_path = None

    vacuum_x, vacuum_y = get_vacuum_pos()
    dfs(vacuum_x, vacuum_y, [])
    return shortest_path


board = get_board()
shortest_path = find_shortest_path(board)

# Converting the path into movement (top, bottom, right, left)
if shortest_path:
    print('Vacuum Path found: ')
    print(shortest_path)
    global moves
    global cost
    moves = []
    cost = 0
    for i in range(1, len(shortest_path)):
        prev_x, prev_y = shortest_path[i - 1]
        curr_x, curr_y = shortest_path[i]
        if prev_x < curr_x:
            moves.append("bottom")
        elif prev_x > curr_x:
            moves.append("top")
            cost = cost + 2
        elif prev_y < curr_y:
            moves.append("right")
            cost = cost + 1
        elif prev_y > curr_y:
            moves.append("left")
            cost = cost + 1
    print("Vacuum Movement:")
    print(moves)
else:
    messagebox.showinfo("No Solution", "There is no solution because of the obstacles")
    quit()

# Performing the moves
for move in moves:
    time.sleep(0.5)
    if not board_thread.is_alive():
        quit()

    move_to(move)


# Writing result to solution.txt file
script_path = os.path.abspath(__file__)
script_directory = os.path.dirname(script_path)
file_path = os.path.join(script_directory, "solution.txt")

with open(file_path, "w") as file:
    file.write("Initial Board:\n")
    for row in board:
        for cell in row:
            file.write(f"{cell} ")
        file.write("\n")

    file.write(f"\nMovement Order:\n{moves}")

    board = get_board();
    file.write("\n\nFinal Board:\n")
    for row in board:
        for cell in row:
            file.write(f"{cell} ")
        file.write("\n")

    file.write(f"\nNumber of steps: {len(moves)}")
    file.write(f"\nOverall cost: {cost}")