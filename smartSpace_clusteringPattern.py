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