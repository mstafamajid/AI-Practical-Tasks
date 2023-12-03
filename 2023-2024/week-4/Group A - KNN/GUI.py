import tkinter as tk
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class DataParticlesGUI:
    def __init__(self, master, x_test, y_test, y_pred):
        self.master = master
        self.master.title("Data Particles GUI")

        self.x_test = x_test
        self.y_test = y_test
        self.y_pred = y_pred

        # Create figures and axes for actual and predicted circles
        self.fig_actual = Figure(figsize=(5, 4), dpi=100)
        self.ax_actual = self.fig_actual.add_subplot(111)

        self.fig_predicted = Figure(figsize=(5, 4), dpi=100)
        self.ax_predicted = self.fig_predicted.add_subplot(111)

        self.create_widgets()

        # Initial plot for actual circles
        self.plot_actual_circles()
        self.plot_pred_circles()
        self.update_predicted_circles()

        # Initial plot for predicted circles
        # self.update_predicted_circles()

    def create_widgets(self):
        # Create a canvas to embed the Matplotlib figure for actual circles in the Tkinter GUI
        self.canvas_actual = FigureCanvasTkAgg(self.fig_actual, master=self.master)
        self.canvas_widget_actual = self.canvas_actual.get_tk_widget()
        self.canvas_widget_actual.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        # Create a canvas to embed the Matplotlib figure for predicted circles in the Tkinter GUI
        self.canvas_predicted = FigureCanvasTkAgg(self.fig_predicted, master=self.master)
        self.canvas_widget_predicted = self.canvas_predicted.get_tk_widget()
        self.canvas_widget_predicted.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)
        self.fig_actual.suptitle("actual data")
        self.fig_predicted.suptitle("predicted data")

    def plot_actual_circles(self):
        self.scatter_actual = self.ax_actual.scatter(self.x_test[:, 0], self.x_test[:, 1], c=self.y_test, cmap='viridis', label='Actual')
        self.scatter_actual.set_alpha(0.5)
        self.canvas_actual.draw()
        
    def plot_pred_circles(self):
        self.scatter_pred = self.ax_predicted.scatter(self.x_test[:, 0], self.x_test[:, 1], c=self.y_pred, cmap='viridis', label='Actual')
        self.scatter_pred.set_alpha(0.5)
        self.canvas_predicted.draw()

    def update_predicted_circles(self):


        # Highlight misclassified points with a circle and change their color to the predicted class
        for i, (actual_label, predicted_label) in enumerate(zip(self.y_test, self.y_pred)):
            if actual_label != predicted_label:
                circle = plt.Circle((self.x_test[i, 0], self.x_test[i, 1]), radius=0.1, color="red", fill=False)
                self.ax_predicted.add_patch(circle)

        self.canvas_predicted.draw()