# 1. KNN distance based method
Create an app where it uses KNN distance based method, meaning every point will be clustered based on the average distance comparing to the class members.

the app will have a GUI where it show the points and their class, it will have 3 methods that user can select from, and user can set how many points (k) are taken for calculation also .


## Requirements:
- data particle dots are placed on the board
- each data particle has a color according toi the cluster it belongs to
- feel free to use any language/library for UI or Actual code
- no library should be used for implementing KNN formula, you can use any language you want like ( php, node, c# ..etc )
- minimum 3 distance methods should be used
- user should be able t enter the number of samples (k) and select any method they want
- app should be able to calculate 3 clusters and more
- don't use libraries for the KNN methods and calculations
- feel free to use any language/framework

# 2. Dynamic Bayesian Classifier
The app will accept a Excel file or any other file format which is table, after that the app can take a examples via some form and predict the outcome using Bayesian Classifier.

the app shows the calculated table and also can download it.

## Requirements:
- the data input is a Excel file or any other table based file
- the last column in the file is the labels
- each column is a feature with non-binary value ( means the value can be any thing ) 
- after calculation show and make the user be able to download the calculated table in Excel or any other table file format
- after the calculation (training), user can enter their own data
- make all the fields that user enters data a dropdown
- don't let user enter the last column because it is the result and app should predict it
- don't use libraries for the bayesian classifier methods and calculations
- feel free to use any language/framework

# 3. Multi Layer perceptron for XOR (in the lecture)
create a app where it shows the Multi Layer perceptron for XOR learning algorithm line movement it justifies itself to satisfy all the points.

the app is a white board ( or app or any thing )

use 4 data samples of two classes where each class include 2 samples.
the app will draw two separating line between the two classes

then the line starts adjusting toward the better position in a 1fps speed so that the movement be clear 

the app will save each iteration table in a file

## Requirements:
- animation speed ( iteration speed ) should be 1fps
- open another windows to show the live table or save each table in a file
- feel free to use any language/library for UI or Actual code 
- no library should be used for implementing PSO formula, you can use any language you want like ( php, node, c# ..etc )

# 4 SVM Model
train SVM model on iris dataset, the app will train the model 3 times showing the difference kernel works in each model ( RBF, Linear, Polynomial) kernels

at the GUI for each kernel show support vectors and separation line and margin lines

show the model accuracy

## requirements
- train svm with 3 different kernels ( RBF, Linear, Polynomial) and know their difference
- use iris dataset in Sklearn 
- use 2 dimensions for each data (for simplicity)
- show support vector
- show separation lines
- show margin lines
- use Sklearn in Python for SVM
- show the model accuracy


# 5 Regression model
In the iris dataset use the Sepal length feature to predict the Sepal Width using a regression model. 

Then use the Sepal Length and Width to predict the Petal Length and Petal width.

show the model accuracy

## requirements
- use iris dataset in Sklearn
- use Sklearn in Python for regression
- show the model accuracy


# 6 KMeans clustering
Cluster the Iris dataset using KMeans clustering.

Cluster the data 3 times using three different metrics ( Euclidean distance, cosine distance and manhattan distance).

plot each KMeans result to a scatter plot GUI, give each cluster a different color.

show the model accuracy

## requirements
- use iris dataset in Sklearn
- use Sklearn in Python for KMeans
- use three different metrics ( Euclidean distance, cosine distance and manhattan distance)
- show scatter plot for each method with coloring each cluster in a different color
- show the model accuracy
