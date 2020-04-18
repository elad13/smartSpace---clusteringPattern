from itertools import groupby
import pandas as pd
import numpy as np
import csv

from point import Point
from clustering import Clustering, iterative_kmeans, plotClusters, plotly

# Load Data
df = pd.read_csv('data/smartSpace1_fullSpace.csv')
df.drop(['Id'], axis=1, inplace=True)

df_userActions = pd.DataFrame(np.array(df), columns=['elementId', 'Day', 'Hour', 'Action'])
#print(df_userActions.head())
#print(df_userActions)


# df_elements = []
# for row in df_userActions.groupby('elementId'):
#     df_elements.append(row)

dataframe_collection = {}

# d1 = df_elements.copy()
# print(d1)
# print(type(df_elements))
# de_ele1 = pd.DataFrame(df_elements[0])
# print(de_ele1)

dataframe_collection = [y for x , y in df_userActions.groupby(['elementId', 'Day'])]

# df_elementAndDay = []
# for row in df_userActions.groupby(['elementId', 'Day']):
#     df_elementAndDay.append(row)
#     #print(row)
# #print(df_elementAndDay[7])

# for i in range(0, len(df_elementAndDay)):
#     #print("i: ", i, " ", df_elementAndDay[i])
#     dataframe_collection[i] = pd.DataFrame(np.array(df_elementAndDay[i]))
#     print(dataframe_collection[i])

# df_elements = []
# for row in df_userActions.groupby('elementId'):
#     df_elements.append(row)
# #print(df_elements[0])

dimensions = 3

# The K in k-means. How many clusters do we assume exist?
#   - Must be less than num_points
num_clusters = 2 #cluster to on and cluster to off - need to change in the future

# When do we say the process has 'converged' and stop updating clusters?
cutoff = 0.2 #need to understand the number

# Cluster those data!
iteration_count = 20 #need to understand the number

with open('data/smartSpace1_fullSpace_afterCluster.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["elementId", "Day", "Hour", "Action"])



x = {}

best_clusters = []
df_centroidsTable = []
for i in range(0, len(dataframe_collection)):
    points = []
    x[i] = dataframe_collection[i].values
    elementNum = x[i][0][0]
    #print(elementNum)
    print(x[i])
    #print("!!!!!!!!!!")
    for row in x[i]:
        coor = []
        #print("index: ", i)
        #print("point:", row)
        #coor.append(row[0])         #element ID
        coor.append(float(row[1]))  #Day = x
        coor.append(float(row[2]))  #Hour = y
        coor.append(float(row[3]))  #Action = z
        point = Point(coor)
        points.append(point)
        #print(points)

    best_clusters.append(iterative_kmeans(
        points,
        num_clusters,
        cutoff,
        iteration_count
    ))

    print("best clusters: ", best_clusters[i])
    #print("@@@@@@@@@@@")

    centroid = {}
    df_centroidTemp = {}
    # Print our best clusters
    for j, c in enumerate(best_clusters[i]):
        for p in c.points:
            print(" Cluster: {} \t Point : {}".format(i, p))


        #the centroid of element in one day
        centroid['x'] = c.centroid.coords[0]
        centroid['y'] = c.centroid.coords[1]
        centroid['z'] = c.centroid.coords[2]
        print("iter: ", i, ", cluster number: ", j, ", centroid: ")
        print("element id: ", elementNum, ", ", centroid)
        #df_centroidsTable.append(centroid)
        #print(df_centroidsTable)
        with open('data/smartSpace1_fullSpace_afterCluster.csv', 'a') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([elementNum, centroid['x'], centroid['y'], centroid['z']])
    #print("&&&&&&&&&&&")

        #df_centroidTemp[j] = centroid.values()
        #print(df_centroidTemp[j])
        #df_centroidsTable.append(elementNum)
    #print(df_centroidsTable)

    #df_centroidsTable[index] = df_centroidTemp[0].values()
    #df_centroidsTable[index+1] = df_centroidTemp[1].values()
    #index = index+1
    #print("^^^^^^^^^^^^^^^")
#print(df_centroidsTable)

    # # Display clusters using plotly for 2d data
    # if dimensions in [2, 3] and plotly:
    #     print("Plotting points, launching browser ...")
    #     plotClusters(best_clusters, dimensions)



#plotClusters(best_clusters[7], dimensions)
#print(x[0])
#print(len(x))
#print("############")
#print("$$$$$$$$$$$$$$$$$$$")



#dataframe_collectionCentroids = [y for x , y in df_userActions.groupby(['elementId'])]

#create the points (x, y, z)
# points = []
# for i in range(0, len(dataframe_collection)):
#     #print(dataframe_collection[i])
#     #print(i)
#     for row in x[i]:
#         coor = []
#         #print("index: ", i)
#         #print("point:", row)
#         coor.append(float(row[1]))
#         coor.append(float(row[2]))
#         coor.append(float(row[3]))
#         point = Point(coor)
#         points.append(point)
#
# dimensions = 3
#
# # The K in k-means. How many clusters do we assume exist?
# #   - Must be less than num_points
# num_clusters = 8
#
# # When do we say the process has 'converged' and stop updating clusters?
# cutoff = 0.2
#
#
# # Cluster those data!
# iteration_count = 20
# best_clusters = iterative_kmeans(
#     points,
#     num_clusters,
#     cutoff,
#     iteration_count
# )
#
# # Print our best clusters
# for i, c in enumerate(best_clusters):
#     for p in c.points:
#         print(" Cluster: {} \t Point : {}".format(i, p))
#
# # Display clusters using plotly for 2d data
# if dimensions in [2, 3] and plotly:
#     print("Plotting points, launching browser ...")
#     plotClusters(best_clusters, dimensions)