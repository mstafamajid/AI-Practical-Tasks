import tkinter
import sklearn.datasets as sk
import numpy as np
from GUI import DataParticlesGUI


class Custom_KNN:
    
    def __init__(self, k=3):
        self.k = k
        
    def fit(self, X_train, y_train):
        self.X_train = X_train
        self.y_train = y_train
        
    def euclidean_distance(self,x_train, x_test):
        distances = np.sqrt(np.sum((x_train - x_test)**2, axis=1))
        return distances
        
    def predict(self, X_test,):
        y_pred = np.zeros(X_test.shape[0])

        for i, x_test in enumerate(X_test):
            distances = self.euclidean_distance(self.X_train,x_test)
      
            k_nearest_indices = np.argsort(distances)[:self.k]
           
            k_nearest_labels = self.y_train[k_nearest_indices]
 
            unique_labels, counts = np.unique(k_nearest_labels, return_counts=True)
            y_pred[i] = unique_labels[np.argmax(counts)]

        return y_pred
    
    def predict_subset(self, X_test, subset_ratio=0.5, random_seed=None):
        if random_seed is not None:
            np.random.seed(random_seed)

        # Randomly choose a subset of the training data
        subset_indices = np.random.choice(len(self.X_train), int(len(self.X_train) * subset_ratio), replace=False)
        subset_X_train = self.X_train[subset_indices]
        subset_y_train = self.y_train[subset_indices]

        y_pred = np.zeros(X_test.shape[0])

        for i, x_test in enumerate(X_test):
            distances = self.euclidean_distance(subset_X_train, x_test)
            k_nearest_indices = np.argsort(distances)[:self.k]
            k_nearest_labels = subset_y_train[k_nearest_indices]
            unique_labels, counts = np.unique(k_nearest_labels, return_counts=True)
            y_pred[i] = unique_labels[np.argmax(counts)]

        return y_pred
          




def split(dataset, train_ratio=0.7, random_seed=None):

    if random_seed is not None:
        np.random.seed(random_seed)

    # Shuffle the dataset
    np.random.shuffle(dataset)

    # Calculate the split index
    split_index = int(len(dataset) * train_ratio)
    

    # Split the dataset
    train_data, test_data = dataset[:split_index], dataset[split_index:]

    x_train, y_train = train_data[:, :-1], train_data[:, -1]
    x_test, y_test = test_data[:, :-1], test_data[:, -1]
    
    return x_train, x_test, y_train, y_test


dataset = sk.load_iris()
iris_data = np.column_stack((dataset.data, dataset.target))  # Combine features and labels

x_train, x_test, y_train, y_test = split(iris_data)

custom_knn_full_dataset = Custom_KNN(k=3)
custom_knn_full_dataset.fit(x_train, y_train)
y_pred_custom_full_dataset = custom_knn_full_dataset.predict(x_test)




accuracy = np.mean(y_pred_custom_full_dataset == y_test)
print("All Predictions:", y_pred_custom_full_dataset)
print("All data Test Accuracy:", accuracy)


y_pred_custom_subset = custom_knn_full_dataset.predict_subset(x_test, subset_ratio=.9)

accuracy_subset = np.mean(y_pred_custom_subset == y_test)
print("Subset Predictions:", y_pred_custom_subset)
print("Subset Test Accuracy:", accuracy_subset)

root = tkinter.Tk()

# Create an instance of the DataParticlesGUI class
data_particles_gui = DataParticlesGUI(root, x_test, y_test, y_pred_custom_subset)

# Run the Tkinter main loop
root.mainloop()



