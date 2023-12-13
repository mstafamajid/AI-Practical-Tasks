import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics.cluster import contingency_matrix
from sklearn import datasets
from pyclustering.cluster.kmeans import kmeans
from pyclustering.cluster.center_initializer import random_center_initializer
from pyclustering.cluster.encoder import cluster_encoder
from pyclustering.utils.metric import type_metric, distance_metric
from sklearn.decomposition import PCA


# Load the iris dataset
iris = datasets.load_iris()
X = iris.data
y = iris.target

# Function to compute purity score using contingency matrix
def purity_score(y_true, y_pred):
    confusion_matrix = contingency_matrix(y_true, y_pred)
    print(confusion_matrix)
    return np.sum(np.amax(confusion_matrix, axis=0)) / np.sum(confusion_matrix)

# Function to plot the clusters with cluster centers
def plot_clusters_with_centers(X, y_pred, centers, title, n_components=2):
    # Apply PCA for dimensionality reduction
    pca = PCA(n_components=n_components)
    X_pca = pca.fit_transform(X)

    # Create subplots
    fig, axs = plt.subplots(1, 2, figsize=(15, 5))

    # Plot real iris dataset on the left
    axs[0].scatter(X_pca[:, 0], X_pca[:, 1], c=y, cmap='viridis', edgecolor='k')
    axs[0].set_title('Real Iris Dataset')

    # Plot clustered data with centers on the right
    axs[1].scatter(X_pca[:, 0], X_pca[:, 1], c=y_pred, cmap='viridis', edgecolor='k')
    for center in centers:
        center_pca = pca.transform([center])[0]
        axs[1].scatter(center_pca[0], center_pca[1], marker='x', s=200, linewidths=3, color='red', label='Cluster Centers')
    axs[1].set_title(title)

    plt.show()
# Define the cosine metric class
class CosineMetric:
    @staticmethod
    def calculate(first, second):
        dot_product = np.dot(first, second)
        magnitude_first = np.linalg.norm(first)
        magnitude_second = np.linalg.norm(second)
        cosine_similarity = dot_product / (magnitude_first * magnitude_second)
        cosine_distance = 1 - cosine_similarity
        return cosine_distance

# Dictionary for distance measures
distance_measures = {'euclidean': 0, 'squared euclidean': 1, 'manhattan': 2, 'chebyshev': 3, 
                    'canberra': 5, 'chi-square': 6, 'cosine': 7}

# Function to compute purity score using pyclustering for various distance measures
# Function to compute purity score using pyclustering for various distance measures
def pyPurity(dist_measure, title, plot_function=None, n_components=2):
    # Initialize random centers
    initial_centers = random_center_initializer(X, 3, random_state=5).initialize()
    
    # Create kmeans instance with the specified distance metric
    if dist_measure == 7:
        # Use user-defined cosine metric
        metric = distance_metric(type_metric.USER_DEFINED, func=CosineMetric.calculate)
    else:
        # Use built-in distance metric
        metric = distance_metric(dist_measure)
    
    instanceKm = kmeans(X, initial_centers=initial_centers, metric=metric)
    
    # Perform cluster analysis
    instanceKm.process()
    
    # Get cluster analysis results - clusters and centers
    pyClusters = instanceKm.get_clusters()
    pyCenters = instanceKm.get_centers()
    
    # Get cluster labels using encoding
    pyEncoding = instanceKm.get_cluster_encoding()
    pyEncoder = cluster_encoder(pyEncoding, pyClusters, X)
    pyLabels = pyEncoder.set_encoding(0).get_clusters()
    
    # Plot the clusters with centers using the specified plot function
    if plot_function:
        plot_function(X, pyLabels, pyCenters, title, n_components)
    
    # Compute and return purity score
    return purity_score(y, pyLabels)

# Example usage with dimensionality reduction to 2 components
for measure, value in distance_measures.items():
    print(f"The purity score for {measure} distance is {round(pyPurity(value, measure, n_components=2) * 100, 2)}%")
    pyPurity(value, measure, plot_function=plot_clusters_with_centers, n_components=2)
