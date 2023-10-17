import os
import time
import threading
import heapq
from vacuum_board.vacuum import *

# Just setting the board up
set_board(get_random_board())
board_thread = threading.Thread(target=board)
board_thread.start()
time.sleep(2)  # give some time for GUI startup and initialization

def find_shortest_path(grid):
    def is_valid(x, y):
        return 0 <= x < len(grid) and 0 <= y < len(grid[0])

    visited = [[False for _ in range(len(grid[0]))] for _ in range(len(grid))]
    start_x, start_y = get_vacuum_pos()
    dest_x, dest_y = get_dirt_pos()

    if start_x is None or not is_valid(dest_x, dest_y):
        return None

    priority_queue = [(0, start_x, start_y, [])]  # (estimated cost, x, y, path)
    heapq.heapify(priority_queue)

    while priority_queue:
        est_cost, x, y, path = heapq.heappop(priority_queue)

        if visited[x][y]:
            continue

        visited[x][y] = True
        path.append((x, y))

        if (x, y) == (dest_x, dest_y):
            return path

        # Generate all possible next moves
        moves = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        for new_x, new_y in moves:
            if is_valid(new_x, new_y) and not visited[new_x][new_y] and grid[new_x][new_y] != 0:
                new_est_cost = abs(new_x - dest_x) + abs(new_y - dest_y)  # Manhattan distance
                heapq.heappush(priority_queue, (new_est_cost, new_x, new_y, path[:]))

    return None

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