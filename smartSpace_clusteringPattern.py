import matplotlib.pyplot as plt         # for plotting
import numpy as np
import pandas as pd

# Importing the dataset
dataset = pd.read_csv('xclara_elad.csv')        # read the data from the CSV file
print("Input Data and Shape")
print(dataset.shape)                       # number of columns and rows in the CSV
dataset.head()

total_days = len(dataset.axes[1])           # Number of columns in the CSV file is the number of days (our K)
print("Total days: " + str(total_days))     # Number of clusters

# Getting the values and plotting it - ???
f1 = dataset['V1'].values
f2 = dataset['V2'].values
X = np.array(list(zip(f1, f2)))
plt.scatter(f1, f2, c='black', s=7)

# Euclidean Distance Caculator
def dist(a, b, ax=1):
    return np.linalg.norm(a - b, axis=ax)

# Number of clusters
k = total_days
# X coordinates of random centroids
C_x = np.random.randint(0, np.max(X)-20, size=k)
# Y coordinates of random centroids
C_y = np.random.randint(0, np.max(X)-20, size=k)
C = np.array(list(zip(C_x, C_y)), dtype=np.float32)
print("Initial Centroids:")
print(C)

"""
from sklearn.datasets import make_blobs #elad: generate the data set

# function: make_blobs
# intro: ???
# param: n_samples - the total number of points equally divided among clusters
# param: n_features - The number of features for each sample.
# param: centers - (default=None) The number of centers to generate, or the fixed center locations
# param: cluster_std - The standard deviation of the clusters.
# param: random_state - Determines random number generation for dataset creation.
# return: array of shape [n_samples, n_features] - The generated samples.
dataset = make_blobs(n_samples=200, centers=4, n_features=2, cluster_std=1.6, random_state=50)          # Generate our dataset

points = dataset[0]

# kmeans
from sklearn.cluster import KMeans

kmeans = KMeans(n_clusters=4)           # Create a kmeans objects - Number of clusters
kmeans.fit(points)                      # fit the kmeans object to the dataset - Fitting the input data

plt.scatter(dataset[0][:,0], dataset[0][:,1])   #elad: to see the graph points. Cant see in pycharm

clusters = kmeans.cluster_centers_              # Centroid values

#print out the clusters
print(clusters)

y_km = kmeans.fit_predict(points)
"""