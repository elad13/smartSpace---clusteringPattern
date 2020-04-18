import argparse
import csv
import numpy as np
from matplotlib import pyplot as plt

import pandas as pd
from mpl_toolkits.mplot3d import Axes3D

from point import Point
from clustering import Clustering
from sklearn import datasets
import plotly


# # Load the DATASET
# #df = datasets.load_data("C:\Users\User\Desktop\Afeka\Final Project\Algorithm\lamp1.csv", "lamp1.csv")
# df = pd.read_csv("‏‏lamp1.csv")
# #totalDays = len(df.axes[1])
# x = df._data
# print(x)
#
# # Return a new matrix, filled with zeros.
# min_of_features=np.zeros((1,3))
# max_of_features=np.zeros((1,3))
# # Find the min and max value of the features
# for i in range(3):
#     min_of_features[0,i]=min(x[:,i])
#     max_of_features[0,i]=max(x[:,i])
#
# print("min:", min_of_features)
# print("max: ", max_of_features)
#
#
# fig=plt.figure()
# ax=Axes3D(fig)
# ax.scatter(x[:50,0],x[:50,1],x[:50,2],color='red')
# ax.scatter(x[50:100,0],x[50:100,1],x[50:100,2],color='green')
# ax.scatter(x[100:150,0],x[100:150,1],x[100:150,2],color='blue')
# plt.show()


def main(fn, clusters_no):

    geo_locs = []
    #read location data from csv file and store each location as a Point(latit,longit) object
    df = pd.read_csv(fn)
    total_days = len(df.axes[1])


    points = []
    with open('d:/temp/seeds_dataset.txt', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='\t', quotechar=',')
        for row in spamreader:
            coor = []
            # print(row)
            coor.append(float(row[2]))
            coor.append(float(row[3]))
            coor.append(float(row[4]))
            point = Point(coor)
            points.append(point)
            # print(', '.join(r))

    for index_x in range(total_days):
        total_hours = len(df[str(index_x)].values)
        for index_y in range(total_hours):
            loc_ = Point(float(index_x), float(df.loc[int(index_y)].at[str(index_x)]))
            geo_locs.append(loc_)


    dimensions = 3

    # The K in k-means. How many clusters do we assume exist?
    #   - Must be less than num_points
    num_clusters = total_hours

    # When do we say the process has 'converged' and stop updating clusters?
    cutoff = 0.2






    # Cluster those data!
    iteration_count = 20
    best_clusters = iterative_kmeans(
        points,
        num_clusters,
        cutoff,
        iteration_count
    )

    # Print our best clusters
    for i, c in enumerate(best_clusters):
        for p in c.points:
            print(" Cluster: {} \t Point : {}".format(i, p))

    # Display clusters using plotly for 2d data
    if dimensions in [2, 3] and plotly:
        print("Plotting points, launching browser ...")
        plotClusters(best_clusters, dimensions)

# def main(fn, clusters_no):
#     geo_locs = []
#     #read location data from csv file and store each location as a Point(latit,longit) object
#     df = pd.read_csv(fn)
#     total_days = len(df.axes[1])
#
#     for index_x in range(total_days):
#         total_hours = len(df[str(index_x)].values)
#         #print("total days: " + str(total_days) + " total hours: " + str(total_hours))
#         for index_y in range(total_hours):
#             #loc_ = Point(float(index_x), float(index_y))
#             loc_ = Point(float(index_x), float(df.loc[int(index_y)].at[str(index_x)]))
#             #loc_ = Point(float(df.loc[int(index_y)].at[str(index_x)]), float(index_x))
#             #print(str(df.loc[int(index_y)].at[str(index_x)]))
#             #print("day: " + str(index_x) + " y: " + str(index_y))
#             geo_locs.append(loc_)
#
#     # for index, row in df.iterrows():
#     #     loc_ = Point(float(row['LAT']), float(row['LON']))   #tuples for location
#     #     geo_locs.append(loc_)
#
#     #run k_means clustering
#     #print("clusters no: " + str(clusters_no))
#     #cluster = Clustering(geo_locs, clusters_no)
#     cluster = Clustering(geo_locs, total_hours)
#     flag = cluster.k_means(False)
#     if flag == -1:
#         print("Error in arguments!")
#     else:
#         #clustering results is a list of lists where each list represents one cluster
#         print("Clustering results:")
#         cluster.print_clusters(cluster.clusters)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run k-means for location data",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    #parser.add_argument('--input', type=str, default='NYC_Free_Public_WiFi_03292017.csv',
    parser.add_argument('--input', type=str, default='‏‏lamp1.csv',
                        dest='inputfile', help='input location file name')
    parser.add_argument('--clusters', type=int, default=8, dest='clusters', help='number of clusters')
    args = parser.parse_args()
    fn = args.inputfile #fn = "data/" + args.inputfile
    main(fn, args.clusters)