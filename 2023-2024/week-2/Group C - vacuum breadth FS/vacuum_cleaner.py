import time
import queue
import threading
from vacuum_board.vacuum import board, get_board, set_board, get_random_board, move_to, get_dirt_pos, get_vacuum_pos
import os


solution=False

set_board(get_random_board())
board_thread = threading.Thread(target=board)
board_thread.start()
time.sleep(2)  # give some time for GUI startup and initialization
maze=get_board()


def printMaze(maze, path=""):
    global solution
    solution= True
    for y, row in enumerate(maze):
        for x, pos in enumerate(row):
            if pos == 10:
                 start = x
                 end =y
    i = start
    j = end

    pos = set()
    for move in path:
        if move == "L":
            i -= 1
        elif move == "R":
            i += 1
        elif move == "U":
            j -= 1
        elif move == "D":
            j += 1
        pos.add((j, i))

    for j, row in enumerate(maze):
        for i, col in enumerate(row):
            if (j, i) in pos:
                print("+ ",end='')
            else:
                print(str(col) + " " ,end='')
                
        print()

def valid(maze, moves):
    for y, row in enumerate(maze):
        for x, pos in enumerate(row):
            if pos == 10:
                 start = x
                 end =y
    i = start
    j = end
    for move in moves:
        if move == "L":
            i -= 1
        elif move == "R":
            i += 1
        elif move == "U":
            j -= 1
        elif move == "D":
            j += 1
            
        if not (0 <= i < len(maze[0]) and 0 <= j < len(maze)):
            return False
        elif (maze[j][i] == 0):
            return False
    return True

def findEnd(maze, moves):
    for y, row in enumerate(maze):
        for x, pos in enumerate(row):
            if pos == 10:
                 start = x
                 end =y
    i = start
    j = end
    for move in moves:
        if move == "L":
            i -= 1
        elif move == "R":
            i += 1
        elif move == "U":
            j -= 1
        elif move == "D":
            j += 1
    if maze[j][i] == 5:
        print("Found: " + moves)
        printMaze(maze, moves)
        return True
    return False


nums = queue.Queue()
nums.put("")
add = ""



while not findEnd(maze, add):
    add = nums.get()
   
    if (len(add)>19):
        print("solution not found")
        break
    motion=''
    if(len(add)):
        lastmove=add[-1]
        
        if(lastmove=='U'):
            motion='D'
        elif(lastmove=='D'):
            motion='U'
        elif(lastmove=='R'):
            motion='L'
        elif(lastmove=='L'):
                motion='R'

    for j in ["L", "R", "U", "D"]:
        put = add + j
        if(motion!=j):
            if valid(maze, put):
                nums.put(put)

print(add)




cost =0
for j in add:
    if j == "U":
        cost += 2
    elif j == "D":
        continue
    else:
        cost += 1
print(cost)

add=add.replace("R", "0")
add=add.replace("U", "3")
add=add.replace("D", "1")
add=add.replace("L", "2")

moves = ['right', 'bottom', 'left', 'top']

time.sleep(0.5)
if not board_thread.is_alive():
    quit()
if(solution):    
     for j in add:
        move_to(moves[int(j)])
        time.sleep(1)

print(get_board())



# Specify the filename
filename = r"2023-2024\week-2\Group C - vacuum breadth FS\solution.txt"

# Get the absolute path of the current directory and concatenate with the filename
file_path = os.path.join(os.getcwd(), filename)


with open(file_path, 'w') as file:

    # Write new content to the file
    if(solution):
        for j in add:
            file.write("step " + (moves[int(j)]))
            file.write("\n")
        file.write("Total cost = "+ str(cost))
    else:
        file.write('there is no solution')

