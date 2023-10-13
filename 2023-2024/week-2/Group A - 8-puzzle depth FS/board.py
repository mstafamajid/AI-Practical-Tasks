import tkinter as tk
from tkinter import PhotoImage
import os



class EightPuzzleGUI:
    def __init__(self, root, solution_path):
        self.root = root
        self.root.title("8 Puzzle Game")
        self.solution = solution_path
        self.current_step = 0



        current_directory = os.path.dirname(os.path.abspath(__file__))

        image_paths = [
    os.path.join(os.path.dirname(current_directory),"puzzle_board", "assets", f"{i}.png")
    for i in range(1, 9)
]


        image_paths.append(os.path.join(current_directory, "0.png"))


        self.images = [PhotoImage(file=image_path) for image_path in image_paths]








        # Initialize the puzzle board
        self.puzzle_board = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 0],  # 0 represents the blank space
        ]

        # Create labels for each tile
        self.labels = [[None, None, None], [None, None, None], [None, None, None]]

        for i in range(3):
            for j in range(3):
                tile_number = self.puzzle_board[i][j]
                self.labels[i][j] = tk.Label(root, image=self.images[tile_number - 1])
                self.labels[i][j].grid(row=i, column=j)

        # Schedule the periodic update
        self.update_puzzle()

    def update_puzzle(self):
        if self.current_step < len(self.solution):
            step = self.solution[self.current_step]
            self.update_labels(step)
            self.current_step += 1
            self.root.after(
                200, self.update_puzzle
            )  # Schedule the next update in 1 second

    def update_labels(self, step):
        for i in range(3):
            for j in range(3):
                tile_number = step[i][j]
                self.labels[i][j].config(image=self.images[tile_number - 1])
