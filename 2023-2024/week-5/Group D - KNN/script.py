import numpy as np
from sklearn.datasets import make_blobs
import matplotlib.pyplot as plt
from matplotlib import colormaps
import tkinter as tk


def calculate_euclidean_distance(x1, x2):
    """
    Calculates the Euclidean distance between two points x1 and x2.
    """
    return np.sqrt(np.sum((x1 - x2) ** 2))


def calculate_manhattan_distance(x1, x2):
    """
    Calculates the Manhattan distance between two points x1 and x2.
    """
    return np.sum(np.abs(x1 - x2))


def calculate_chebyshev_distance(x1, x2):
    """
    Calculates the Chebyshev distance between two points x1 and x2.
    """
    return np.max(np.abs(x1 - x2))


def predict_class(distances, classes, k):
    """
    Predicts the class for a given test sample using KNN based on average distances.
    """
    
    #   [3,4,1,5,2]
    #  0,1,2,3,4 index 
#      2,4,0,1,3 index 
    sorted_indices = np.argsort(distances)
    k_nearest_classes = classes[sorted_indices[:k]]
    k_nearest_distances = distances[sorted_indices[:k]]

    unique_classes = np.unique(k_nearest_classes)
    class_avg_distances = []
    print(
        f"k_nearest_classes: {k_nearest_classes}, k_nearest_distances: {k_nearest_distances}"
    )
    for cls in unique_classes:
        # Calculate the average distance for each class
        avg_distance = np.mean(k_nearest_distances[k_nearest_classes == cls])
        class_avg_distances.append(avg_distance)
    print(
        f"unique_classes: {unique_classes}, class_avg_distances: {class_avg_distances}"
    )
    # Find the class with the minimum average distance
    closest_class_idx = np.argmin(class_avg_distances)
    predicted_class = unique_classes[closest_class_idx]

    return predicted_class


def knn(features, classes, k, x_test, metric):
    """
    Performs KNN classification on a test sample x_test.
    """
    distances = [metric(x_test, x) for x in features]
    distances = np.array(distances)
    return predict_class(distances, classes, k)


# GUI function to perform KNN based on user inputs
def perform_knn():
    # Get user inputs from the Entrclasseswidgets
    k_value = int(entry_k.get())
    num_classes = int(entry_num_classes.get())
    selected_metric_str = metrics.get()

    # Convert selected metric string to the corresponding function
    if selected_metric_str == "Euclidean Distance":
        selected_metric = calculate_euclidean_distance
    elif selected_metric_str == "Manhattan Distance":
        selected_metric = calculate_manhattan_distance
    elif selected_metric_str == "Chebyshev Distance":
        selected_metric = calculate_chebyshev_distance

    # Get user input for test sample coordinates (x_test)
    x_test_input = entry_x_test.get().split(",")
    x_test = np.array([float(coord.strip()) for coord in x_test_input])

    # Generate synthetic classification data based on user input for number of classes
    features, classes= make_blobs(
        n_samples=2000, centers=num_classes, n_features=2, cluster_std=1
    )

    # Predict the class for the user-input test sample using the selected metric and KNN
    predicted_class = knn(features, classes, k_value, x_test, selected_metric)
    print(f"Predicted class for x_test: {predicted_class}")

    # Plot the scatter plot with the test sample and predicted class
    cmap = colormaps["Set1"]
    for class_idx in range(num_classes):
        plt.scatter(
            features[classes== class_idx, 0],
            features[classes== class_idx, 1],
            color=cmap(class_idx),
            label=f"Class {class_idx}",
            marker="o",
        )
    plt.scatter(
        x_test[0],
        x_test[1],
        color=cmap(predicted_class),
        label="Test Sample",
        marker="x",
        s=100,
    )
    plt.title("Blob Data Scatter Plot")
    plt.xlabel("Feature 1")
    plt.ylabel("Feature 2")
    plt.legend()
    plt.show()


# Create the GUI
root = tk.Tk()
root.title("KNN Classifier")
root.geometry("400x300")  # Set initial window size

# Entrclasseswidgets for k value, number of classes, distance metric, and x_test coordinates
label_k = tk.Label(root, text="Enter value of 'k':")
label_k.pack()
entry_k = tk.Entry(root)
entry_k.pack()

label_num_classes = tk.Label(root, text="Enter number of classes:")
label_num_classes.pack()
entry_num_classes = tk.Entry(root)
entry_num_classes.pack()

label_metric = tk.Label(root, text="Select distance metric:")
label_metric.pack()
metrics = tk.StringVar(root)
metrics.set("Euclidean Distance")
dropdown_metric = tk.OptionMenu(
    root,
    metrics,
    "Euclidean Distance",
    "Manhattan Distance",
    "Chebyshev Distance",
)
dropdown_metric.pack()

label_x_test = tk.Label(root, text="Enter x_test (comma-separated coordinates):")
label_x_test.pack()
entry_x_test = tk.Entry(root)
entry_x_test.pack()

btn_run_knn = tk.Button(root, text="Run KNN", command=perform_knn)
btn_run_knn.pack()

root.mainloop()
