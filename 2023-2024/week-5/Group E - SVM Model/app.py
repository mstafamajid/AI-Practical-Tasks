# Import necessary libraries
import matplotlib.pyplot as plt
from sklearn import datasets, svm
from sklearn.inspection import DecisionBoundaryDisplay
from sklearn.metrics import accuracy_score

# Import the Iris dataset from scikit-learn
iris = datasets.load_iris() # 2D Array (table)

# Extract the first two features for simplicity
X = iris.data[:, :2] # length, Width
y = iris.target # Setosa, Versicolor, Virginica

# Create three SVM models with different kernels: linear, RBF, and polynomial
models = (
    svm.SVC(kernel="linear", gamma=1.0),
    svm.SVC(kernel="rbf", gamma=1.0),
    svm.SVC(kernel="poly", gamma=1.0),
)

# Fit each model to the data (train the models)
# clf.fit(X, y) is the training method
models = (clf.fit(X, y) for clf in models)

# Titles for the subplots
titles = (
    "SVC with linear kernel",
    "SVC with RBF kernel",
    "SVC with polynomial kernel",
)

# Set up a 2x2 grid for subplots
fig, sub = plt.subplots(2, 2)
plt.subplots_adjust(wspace=0.4, hspace=0.4)

# Extract the first and second feature datas for clarity in plotting
# (y,x) Widths, Lengths
X0, X1 = X[:, 0], X[:, 1]

# Loop through each model, title, and subplot
for clf, title, subplot in zip(models, titles, sub.flatten()):
    # Create a decision boundary display for the current model (classify)
    DecisionBoundaryDisplay.from_estimator(
        clf,
        X,
        cmap=plt.cm.coolwarm, # color map
        alpha=0.8, # transparency of the regions
        ax=subplot,
        xlabel=iris.feature_names[0],
        ylabel=iris.feature_names[1],
    )

    # Get model predictions
    y_pred = clf.predict(X)
    # Compute accuracy
    accuracy = accuracy_score(y, y_pred)
    
    # Scatter plot the data points with colors based on the true labels
    subplot.scatter(X0, X1, c=y, cmap=plt.cm.coolwarm, s=20, edgecolors="k")
    
    # Remove x and y ticks for clarity
    subplot.set_xticks(())
    subplot.set_yticks(())
    
    # Include accuracy in the title of each subplot
    subplot.set_title(f"{title}\nAccuracy: {accuracy:.2f}")

# Show the plot
plt.show()
