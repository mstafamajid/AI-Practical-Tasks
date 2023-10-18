import sys
sys.path.append('..')  # Add the parent directory to the Python path

import time
import threading
from vacuum_board.vacuum import board, get_board, set_board, get_random_board, move_to, get_dirt_pos, get_vacuum_pos
import queue
import os
from tkinter import messagebox

class Project2:
    def __init__(self):
        self.moves = ['top', 'left', 'right', 'bottom']
        self.cost = 0
        self.element_list = []  # to keep track of elements
        self.check = True
        self.priority_queue = queue.PriorityQueue()
        set_board(get_random_board())
        # set_board( [1,30, [7,13,19,25,24]] )


        self.priority_heuristic = queue.PriorityQueue()
        script_path = os.path.abspath(__name__)
        script_directory = os.path.dirname(script_path)
        self.file_path = os.path.join(script_directory, "solution.txt")
        time.sleep(2)

    def run_app(self):
        time.sleep(1.5)

        self.element_list.append(get_vacuum_pos())

        self.grid = get_board()

        #adding the initial position of the board
        with open(self.file_path, "w") as file:
                file.write("Initial Board:\n")
                for row in self.grid:
                    for cell in row:
                        file.write(f"{cell} ")
                    file.write("\n")

        while True:
            time.sleep(0.5)
            if not self.board_thread.is_alive():
                quit()

            if get_vacuum_pos() == get_dirt_pos():
                with open(self.file_path, "a") as file:
                    file.write('final board\n')
                    file.write('\nThe goal is reached')
                    file.write(f'\nCost: {self.cost}')
                messagebox.showinfo("Search Ended",  "You Have Reached The Final Position")
                exit()

            self.position(get_vacuum_pos())
            cell_to_go = self.priority_heuristic.get()[1]
            next_cell = self.moves[cell_to_go]

            if self.check:
                self.priority_queue.put((self.cost, self.convert(cell_to_go)))
                self.check = True

            move_to(next_cell)

            if next_cell == "top":
                self.cost +=2
            elif next_cell == "left" :
                self.cost +=1
            elif next_cell == "right":
                self.cost +=1

            self.add_to_solution()


            while not self.priority_heuristic.empty():
                self.priority_heuristic.get()[1]

            self.element_list.append(get_vacuum_pos())


    def convert(self, cell_to_go):
        conversion_map = {0: 3, 1: 2, 2: 1, 3: 0}
        
        if cell_to_go == 0:
            self.cost -=2
        elif cell_to_go == 1 or cell_to_go == 2:
            self.cost -=1
        
        return conversion_map.get(cell_to_go)
    

    #add it to the file
    def add_to_solution(self):
        
        with open(self.file_path, "a") as file:
            file.write("\n")
            board = get_board()
            for row in board:
                for cell in row:
                    file.write(f"{cell} ")
                file.write("\n")

    def position(self, vac):
        moves = [(-1, 0), (0, -1), (0, 1), (1, 0)]

        #get top, left, bottom, right cells
        for move_index, (row_change, col_change) in enumerate(moves):
            new_row, new_col = vac[0] + row_change, vac[1] + col_change

            #the cell must be on the board
            if 0 <= new_row < 6 and 0 <= new_col < 6:
                cell_value = get_board()[new_row][new_col]

                 #the part we already were on.
                if cell_value != 0 and [new_row, new_col] not in self.element_list:
                    hr = self.calculate([new_row, new_col])
                    self.priority_heuristic.put((hr, move_index))



        if self.priority_heuristic.empty():
            if self.priority_queue.empty():
                with open(self.file_path, "a") as file:
                    file.write('\nThe goal can\'t be reached')
                    file.write(f'\nCost: {self.cost}')
                    messagebox.showinfo("Search Interrupted",  "No Path Forward")
                exit()
            else:
                last_move = self.priority_queue.get()[1]
                self.priority_heuristic.put((1, last_move))
                self.check = False

    def calculate(self, cell):
        x1, y1 = cell
        x2, y2 = get_dirt_pos()
        return abs(x1 - x2) + abs(y1 - y2)

    def run(self):
        self.board_thread = threading.Thread(target=board)
        self.run_app_thread = threading.Thread(target=self.run_app)

        self.board_thread.start()
        self.run_app_thread.start()

obj = Project2()
obj.run()