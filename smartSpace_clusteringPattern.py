# import matplotlib.pyplot as plt         # for plotting
# import numpy as np
# import pandas as pd
# from math import sqrt
# from random import uniform
# from collections import defaultdict
#
#
# def point_avg(points):
#     """
#     Accepts a list of points, each with the same number of dimensions.
#     NB. points can have more dimensions than 2
#
#     Returns a new point which is the center of all the points.
#     """
#     dimensions = len(points[0])
#
#     new_center = []
#
#     for dimension in range(dimensions):
#         dim_sum = 0  # dimension sum
#         for p in points:
#             dim_sum += p[dimension]
#
#         # average of each dimension
#         new_center.append(dim_sum / float(len(points)))
#
#     return new_center
#
#
# def update_centers(data_set, assignments):
#     """
#     Accepts a dataset and a list of assignments; the indexes
#     of both lists correspond to each other.
#     Compute the center for each of the assigned groups.
#     Return `k` centers where `k` is the number of unique assignments.
#     """
#     new_means = defaultdict(list)
#     centers = []
#     for assignment, point in zip(assignments, data_set):
#         new_means[assignment].append(point)
#
#     for points in new_means.itervalues():
#         centers.append(point_avg(points))
#
#     return centers
#
#
# def assign_points(data_points, centers):
#     """
#     Given a data set and a list of points betweeen other points,
#     assign each point to an index that corresponds to the index
#     of the center point on it's proximity to that point.
#     Return a an array of indexes of centers that correspond to
#     an index in the data set; that is, if there are N points
#     in `data_set` the list we return will have N elements. Also
#     If there are Y points in `centers` there will be Y unique
#     possible values within the returned list.
#     """
#     assignments = []
#     for point in data_points:
#         shortest = ()  # positive infinity
#         shortest_index = 0
#         for i in range(len(centers)):
#             val = distance(point, centers[i])
#             if val < shortest:
#                 shortest = val
#                 shortest_index = i
#         assignments.append(shortest_index)
#     return assignments
#
#
# def distance(a, b):
#     """
#     """
#     dimensions = len(a)
#
#     _sum = 0
#     for dimension in range(dimensions):
#         difference_sq = (a[dimension] - b[dimension]) ** 2
#         _sum += difference_sq
#     return sqrt(_sum)
#
#
# def generate_k(data_set, k):
#     """
#     Given `data_set`, which is an array of arrays,
#     find the minimum and maximum for each coordinate, a range.
#     Generate `k` random points between the ranges.
#     Return an array of the random points within the ranges.
#     """
#     centers = []
#     dimensions = len(data_set[0]) #len(data_set.axes[1])  = total days
#     min_max = defaultdict(int)
#
#     for point in data_set:
#         for i in range(dimensions):
#             val = point[i]
#             min_key = 'min_%d' % i
#             max_key = 'max_%d' % i
#             if min_key not in min_max or val < min_max[min_key]:
#                 min_max[min_key] = val
#             if max_key not in min_max or val > min_max[max_key]:
#                 min_max[max_key] = val
#
#     for _k in range(k):
#         rand_point = []
#         for i in range(dimensions):
#             min_val = min_max['min_%d' % i]
#             max_val = min_max['max_%d' % i]
#
#             rand_point.append(uniform(min_val, max_val))
#
#         centers.append(rand_point)
#
#     return centers
#
#
# def k_means(dataset, k):
#     k_points = generate_k(dataset, k)
#     assignments = assign_points(dataset, k_points)
#     old_assignments = None
#     while assignments != old_assignments:
#         new_centers = update_centers(dataset, assignments)
#         old_assignments = assignments
#         assignments = assign_points(dataset, new_centers)
#     return zip(assignments, dataset)
#
# # points = [
# #     [1, 2],
# #     [2, 1],
# #     [3, 1],
# #     [5, 4],
# #     [5, 5],
# #     [6, 5],
# #     [10, 8],
# #     [7, 9],
# #     [11, 5],
# #     [14, 9],
# #     [14, 14],
# #     ]
# #
# # print(k_means(points, 3))
# """
# """
# # Importing the dataset
# dataset = pd.read_csv('smartSapce1_lamp1.csv')        # read the data from the CSV file
# print("Input Data and Shape")
# print(dataset.shape)                       # number of columns and rows in the CSV
# dataset.head()
# #print(dataset) #print all data
#
# total_days = len(dataset.axes[1])           # Number of columns in the CSV file is the number of days (our K)
# print("Total days: " + str(total_days))     # Number of clusters
#
# # Getting the values and plotting it - ???
# f1 = dataset['0'].values
# print(type(f1))
# f2 = dataset['1'].values
# print(type(f2))
# X = np.array(list(zip(f1, f2)))
# print(type(X))
# plt.scatter(f1, f2, c='black', s=7)
#
# # Need to get the values from the CSV into array or to define variables as k amount
# for i in range(total_days):
#     actionsTimes = list(dataset[str(i)].values)
#     print(actionsTimes)
# """"
# X = data[["LoanAmount","ApplicantIncome"]]
# #Visualise data points
# plt.scatter(X["ApplicantIncome"],X["LoanAmount"],c='black')
# """
# # Plot the data (random)
#
# # Euclidean Distance Caculator
# def dist(a, b, ax=1):
#     return np.linalg.norm(a - b, axis=ax)
#
# # Number of clusters
# k = total_days
# # X coordinates of random centroids
# C_x = np.random.randint(0, np.max(X)-20, size=k)
# # Y coordinates of random centroids
# C_y = np.random.randint(0, np.max(X)-20, size=k)
# C = np.array(list(zip(C_x, C_y)), dtype=np.float32)
# print("Initial Centroids:")
# print(C)