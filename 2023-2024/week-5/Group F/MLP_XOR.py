import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Sigmoid activation function
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

# Derivative of the sigmoid function
def sigmoid_derivative(x):
    return x * (1 - x)

# Initialize random weights and biases for the network
def initialize_weights_and_biases(input_size, hidden_size, output_size):
    weights_input_hidden = 2 * np.random.random((input_size, hidden_size)) - 1
    biases_hidden = np.zeros((1, hidden_size))
    weights_hidden_output = 2 * np.random.random((hidden_size, output_size)) - 1
    biases_output = np.zeros((1, output_size))
    return weights_input_hidden, biases_hidden, weights_hidden_output, biases_output

# Calculate accuracy
def calculate_accuracy(predictions, targets):
    predictions = (predictions >= 0.5).astype(int)  # Thresholding for binary classification
    correct = np.sum(predictions == targets)
    total = targets.size
    accuracy = correct / total
    return accuracy * 100  # Return percentage


# Forward pass through the network
def forward_pass(inputs, weights_input_hidden, biases_hidden, weights_hidden_output, biases_output):
    hidden_layer_input = np.dot(inputs, weights_input_hidden) + biases_hidden
    hidden_layer_output = sigmoid(hidden_layer_input)

    output_layer_input = np.dot(hidden_layer_output, weights_hidden_output) + biases_output
    output_layer_output = sigmoid(output_layer_input)

    return hidden_layer_output, output_layer_output

# Backpropagation to update weights and biases
def backpropagation(inputs, given_output, hidden_layer_output, output_layer_output, 
                    weights_input_hidden, biases_hidden, weights_hidden_output, biases_output, learning_rate):
    output_error = given_output - output_layer_output
    output_delta =  output_error * sigmoid_derivative(output_layer_output)
    hidden_error = output_delta.dot(weights_hidden_output.T)
    hidden_delta = hidden_error * sigmoid_derivative(hidden_layer_output)
    weights_hidden_output += hidden_layer_output.T.dot(output_delta) * learning_rate
    biases_output += np.sum(output_delta, axis=0, keepdims=True) * learning_rate
    weights_input_hidden += inputs.T.dot(hidden_delta) * learning_rate
    biases_hidden += np.sum(hidden_delta, axis=0, keepdims=True) * learning_rate

# Modified training function to include dynamic plotting of the decision boundary, 
# weight and bias saving, and final text file
class Plotter:
    def __init__(self, master, X, y, weights_input_hidden, biases_hidden, weights_hidden_output, biases_output, save_file):
        self.master = master
        self.X = X
        self.y = y
        self.weights_input_hidden = weights_input_hidden
        self.biases_hidden = biases_hidden
        self.weights_hidden_output = weights_hidden_output
        self.biases_output = biases_output

        self.figure, self.ax = plt.subplots(figsize=(6,4))
        self.canvas = FigureCanvasTkAgg(self.figure, master=master)
        self.canvas.get_tk_widget().pack()

        self.save_file = save_file
        self.weights_history = ""  # String to accumulate weights and biases at each epoch

    def plot_decision_boundary(self, epoch):
        self.ax.clear()

        # Plot input data points
        self.ax.scatter(self.X[:, 0], self.X[:, 1], c=self.y.flatten(), cmap=plt.cm.Spectral, marker='o', edgecolors='k')

        # Plot decision boundary
        h = 0.01
        x_min, x_max = self.X[:, 0].min() - 1, self.X[:, 0].max() + 1
        y_min, y_max = self.X[:, 1].min() - 1, self.X[:, 1].max() + 1
        xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
        Z = forward_pass(np.c_[xx.ravel(), yy.ravel()], self.weights_input_hidden, self.biases_hidden,
                        self.weights_hidden_output, self.biases_output)[1]
        Z = Z.reshape(xx.shape)
        self.ax.contour(xx, yy, Z, levels=[0.5], colors='black', linestyles='dashed')

        self.ax.set_title(f'Decision Boundary (Epoch {epoch})')
        self.ax.set_xlabel('F1')
        self.ax.set_ylabel('F2')
        self.canvas.draw()
        

        # Save weights and biases to history
        self.weights_history += f"Epoch {epoch}:\n"
        self.weights_history += f"Weights Input Hidden:\n{self.weights_input_hidden}\n\n"
        self.weights_history += f"Biases Hidden:\n{self.biases_hidden}\n\n"
        self.weights_history += f"Weights Hidden Output:\n{self.weights_hidden_output}\n\n"
        self.weights_history += f"Biases Output:\n{self.biases_output}\n\n"

# Modified training function to include dynamic plotting of decision boundary, 
# weight and bias saving to txt, and final text file
def train_with_gui_and_save_weights_to_txt(X, y, hidden_size, epochs, learning_rate, save_file):
    input_size = X.shape[1]
    output_size = y.shape[1]

    weights_input_hidden, biases_hidden, weights_hidden_output, biases_output = \
        initialize_weights_and_biases(input_size, hidden_size, output_size)

    # Create Tkinter GUI
    root = tk.Tk()
    root.title("Neural Network Decision Boundary")

    # Create Plotter instance
    plotter = Plotter(root, X, y, weights_input_hidden, biases_hidden,
                    weights_hidden_output, biases_output, save_file)

    for epoch in range(epochs):
        # Forward pass
        hidden_layer_output, output_layer_output = forward_pass(
            X, weights_input_hidden, biases_hidden, weights_hidden_output, biases_output
        )

        
        # Backpropagation
        backpropagation(
            X, y, hidden_layer_output, output_layer_output,
            weights_input_hidden, biases_hidden,
            weights_hidden_output, biases_output,
            learning_rate
        )
        predictions = forward_pass(X, weights_input_hidden, biases_hidden, weights_hidden_output, biases_output)[1]
        accuracy = calculate_accuracy(predictions, y)
        

        # Update the plot every 100 epochs
        if epoch % 100 == 0:
            plotter.plot_decision_boundary(epoch)
            root.update_idletasks()
            root.update()
            
            if accuracy >= 99.9:
                print(f"Training stopped at Epoch {epoch} as accuracy reached 100%.")
                break

    # Save weights and biases to a text file
    with open(f"{save_file}.txt", 'w') as f:
        f.write(plotter.weights_history)


    # Print final accuracy and weights
    print(f"Final Accuracy: {accuracy:.2f}%")
    print("Final Weights:")
    print(f"Weights Input Hidden:\n{weights_input_hidden}\n")
    print(f"Biases Hidden:\n{biases_hidden}\n")
    print(f"Weights Hidden Output:\n{weights_hidden_output}\n")
    print(f"Biases Output:\n{biases_output}\n")

    # Pause at the final result
    root.mainloop()

# XOR input and output
X = np.array([[0, 0],
              [0, 1],
              [1, 0],
              [1, 1]])

y = np.array([[0],
              [1],
              [1],
              [0]])

# Set hyperparameters
hidden_size = 2
epochs = 15000

learning_rate = 0.1
save_file = "weights_history_with_biases"

# Train the neural network with dynamic plot, decision boundary, 
# and weight and bias saving to one txt file
train_with_gui_and_save_weights_to_txt(X, y, hidden_size, epochs, learning_rate, save_file)
