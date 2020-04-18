import random as rand
import math as math
import numpy as np
import matplotlib.pyplot as plt

from point import Point
#
# class Clustering:
#     def __init__(self, geo_locs_, k_):
#         self.geo_locations = geo_locs_
#         self.k = k_
#         self.clusters = []  #clusters of nodes
#         self.means = []     #means of clusters
#         self.debug = False  #debug flag
#
#     #this method returns the next random node
#     def next_random(self, index, points, clusters):
#         #pick next node that has the maximum distance from other nodes
#         dist = {}
#         for point_1 in points:
#             if self.debug:
#                 print("point_1: {} {}".format(point_1.latit, point_1.longit))
#             #compute this node distance from all other points in cluster
#             for cluster in clusters.values():
#                 point_2 = cluster[0]
#                 if self.debug:
#                     print("point_2: {} {}".format(point_2.latit, point_2.longit))
#                 if point_1 not in dist:
#                     dist[point_1] = math.sqrt(math.pow(point_1.latit - point_2.latit,2.0) + math.pow(point_1.longit - point_2.longit,2.0))
#                 else:
#                     dist[point_1] += math.sqrt(math.pow(point_1.latit - point_2.latit,2.0) + math.pow(point_1.longit - point_2.longit,2.0))
#         if self.debug:
#             for key, value in dist.items():
#                 print("({}, {}) ==> {}".format(key.latit, key.longit, value))
#         #now let's return the point that has the maximum distance from previous nodes
#         count_ = 0
#         max_ = 0
#         for key, value in dist.items():
#             if count_ == 0:
#                 max_ = value
#                 max_point = key
#                 count_ += 1
#             else:
#                 if value > max_:
#                     max_ = value
#                     max_point = key
#         return max_point
#
#     #this method computes the initial means
#     def initial_means(self, points):
#         #pick the first node at random
#         point_ = rand.choice(points)
#         if self.debug:
#             print("point#0: {} {}".format(point_.latit, point_.longit))
#         clusters = dict()
#         clusters.setdefault(0, []).append(point_)
#         points.remove(point_)
#         #now let's pick k-1 more random points
#         for i in range(1, self.k):
#             point_ = self.next_random(i, points, clusters)
#             if self.debug:
#                 print("point#{}: {} {}".format(i, point_.latit, point_.longit))
#             #clusters.append([point_])
#             clusters.setdefault(i, []).append(point_)
#             points.remove(point_)
#         #compute mean of clusters
#         #self.print_clusters(clusters)
#         self.means = self.compute_mean(clusters)
#         if self.debug:
#             print("initial means:")
#             self.print_means(self.means)
#
#     def compute_mean(self, clusters):
#         means = []
#         for cluster in clusters.values():
#             mean_point = Point(0.0, 0.0)
#             cnt = 0.0
#             for point in cluster:
#                 #print "compute: point(%f,%f)" % (point.latit, point.longit)
#                 mean_point.latit += point.latit
#                 mean_point.longit += point.longit
#                 cnt += 1.0
#             mean_point.latit = mean_point.latit/cnt
#             mean_point.longit = mean_point.longit/cnt
#             means.append(mean_point)
#         return means
#
#     #this method assign nodes to the cluster with the smallest mean
#     def assign_points(self, points):
#         if self.debug:
#             print("assign points")
#         clusters = dict()
#         for point in points:
#             dist = []
#             if self.debug:
#                 print("point({},{})".format(point.latit, point.longit))
#             #find the best cluster for this node
#             for mean in self.means:
#                 dist.append(math.sqrt(math.pow(point.latit - mean.latit,2.0) + math.pow(point.longit - mean.longit,2.0)))
#             #let's find the smallest mean
#             if self.debug:
#                 print(dist)
#             cnt_ = 0
#             index = 0
#             min_ = dist[0]
#             for d in dist:
#                 if d < min_:
#                     min_ = d
#                     index = cnt_
#                 cnt_ += 1
#             if self.debug:
#                 print("index: {}".format(index))
#             clusters.setdefault(index, []).append(point)
#         return clusters
#
#     def update_means(self, means, threshold):
#         #check the current mean with the previous one to see if we should stop
#         for i in range(len(self.means)):
#             mean_1 = self.means[i]
#             mean_2 = means[i]
#             if self.debug:
#                 print("mean_1({},{})".format(mean_1.latit, mean_1.longit))
#                 print("mean_2({},{})".format(mean_2.latit, mean_2.longit))
#             if math.sqrt(math.pow(mean_1.latit - mean_2.latit,2.0) + math.pow(mean_1.longit - mean_2.longit,2.0)) > threshold:
#                 return False
#         return True
#
#     #debug function: print cluster points
#     def print_clusters(self, clusters):
#         cluster_cnt = 1
#         for cluster in clusters.values():
#             print("nodes in cluster #{}".format(cluster_cnt))
#             cluster_cnt += 1
#             for point in cluster:
#                 print("point({},{})".format(point.latit, point.longit))
#
#     #print means
#     def print_means(self, means):
#         for point in means:
#             print("{} {}".format(point.latit, point.longit))
#
#     #k_means algorithm
#     def k_means(self, plot_flag):
#         if len(self.geo_locations) < self.k:
#             return -1   #error
#         points_ = [point for point in self.geo_locations]
#         #compute the initial means
#         self.initial_means(points_)
#         stop = False
#         while not stop:
#             #assignment step: assign each node to the cluster with the closest mean
#             points_ = [point for point in self.geo_locations]
#             clusters = self.assign_points(points_)
#             if self.debug:
#                 self.print_clusters(clusters)
#             means = self.compute_mean(clusters)
#             if self.debug:
#                 print("means:")
#                 self.print_means(means)
#                 print("update mean:")
#             stop = self.update_means(means, 0.01)
#             if not stop:
#                 self.means = []
#                 self.means = means
#         self.clusters = clusters
#         #plot cluster for evluation
#         if plot_flag:
#             fig = plt.figure()
#             ax = fig.add_subplot(111)
#             markers = ['o', 'd', 'x', 'h', 'H', 7, 4, 5, 6, '8', 'p', ',', '+', '.', 's', '*', 3, 0, 1, 2]
#             colors = ['r', 'k', 'b', [0,0,0], [0,0,1], [0,1,0], [0,1,1], [1,0,0], [1,0,1], [1,1,0], [1,1,1]]
#             cnt = 0
#             for cluster in clusters.values():
#                 latits = []
#                 longits = []
#                 for point in cluster:
#                     latits.append(point.latit)
#                     longits.append(point.longit)
#                 ax.scatter(longits, latits, s=60, c=colors[cnt], marker=markers[cnt])
#                 cnt += 1
#             plt.show()
#         return 0

plotly = True
try:
    import plotly
    from plotly.graph_objs import Scatter, Scatter3d, Layout
except ImportError:
    print("INFO: Plotly is not installed, plots will not be generated.")

# Helper Methods
def getDistance(a, b):
    '''
    Squared Euclidean distance between two n-dimensional points.
    https://en.wikipedia.org/wiki/Euclidean_distance#n_dimensions
    Note: This can be very slow and does not scale well
    '''
    if a.n != b.n:
        raise Exception("ERROR: non comparable points")

    accumulatedDifference = 0.0
    for i in range(a.n):
        squareDifference = pow((a.coords[i] - b.coords[i]), 2)
        accumulatedDifference += squareDifference

    return accumulatedDifference

def makeRandomPoint(n, lower, upper):
        '''
        Returns a Point object with n dimensions and values between lower and
        upper in each of those dimensions
        '''
        p = Point([rand.uniform(lower, upper) for _ in range(n)])
        return p

def calculateError(clusters):
        '''
        Return the average squared distance between each point and its cluster
        centroid.
        This is also known as the "distortion cost."
        '''
        accumulatedDistances = 0
        num_points = 0
        for cluster in clusters:
            num_points += len(cluster.points)
            accumulatedDistances += cluster.getTotalDistance()

        error = accumulatedDistances / num_points
        return error

def plotClusters(data, dimensions):
        '''
        This uses the plotly offline mode to create a local HTML file.
        This should open your default web browser.
        '''
        if dimensions not in [2, 3]:
            raise Exception(
                "Plots are only available for 2 and 3 dimensional data")

        # Convert data into plotly format.
        traceList = []
        for i, c in enumerate(data):
            # Get a list of x,y coordinates for the points in this cluster.
            cluster_data = []
            for point in c.points:
                cluster_data.append(point.coords)

            trace = {}
            centroid = {}
            if dimensions == 2:
                # Convert our list of x,y's into an x list and a y list.
                trace['x'], trace['y'] = zip(*cluster_data)
                trace['mode'] = 'markers'
                trace['marker'] = {}
                trace['marker']['symbol'] = i
                trace['marker']['size'] = 12
                trace['name'] = "Cluster " + str(i)
                traceList.append(Scatter(**trace))
                # Centroid (A trace of length 1)
                centroid['x'] = [c.centroid.coords[0]]
                centroid['y'] = [c.centroid.coords[1]]
                centroid['mode'] = 'markers'
                centroid['marker'] = {}
                centroid['marker']['symbol'] = i
                centroid['marker']['color'] = 'rgb(200,10,10)'
                centroid['name'] = "Centroid " + str(i)
                traceList.append(Scatter(**centroid))
            else:
                symbols = [
                    "circle",
                    "square",
                    "diamond",
                    "circle-open",
                    "square-open",
                    "diamond-open",
                    "cross", "x"
                ]
                symbol_count = len(symbols)
                if i > symbol_count:
                    print("Warning: Not enough marker symbols to go around")
                # Convert our list of x,y,z's separate lists.
                trace['x'], trace['y'], trace['z'] = zip(*cluster_data)
                trace['mode'] = 'markers'
                trace['marker'] = {}
                trace['marker']['symbol'] = symbols[i]
                trace['marker']['size'] = 12
                trace['name'] = "Cluster " + str(i)
                traceList.append(Scatter3d(**trace))
                # Centroid (A trace of length 1)
                centroid['x'] = [c.centroid.coords[0]]
                centroid['y'] = [c.centroid.coords[1]]
                centroid['z'] = [c.centroid.coords[2]]
                centroid['mode'] = 'markers'
                centroid['marker'] = {}
                centroid['marker']['symbol'] = symbols[i]
                centroid['marker']['color'] = 'rgb(200,10,10)'
                centroid['name'] = "Centroid " + str(i)
                traceList.append(Scatter3d(**centroid))

        title = "K-means clustering with %s clusters" % str(len(data))
        plotly.offline.plot({
            "data": traceList,
            "layout": Layout(title=title)
        })

# K-means Methods
def iterative_kmeans(points, num_clusters, cutoff, iteration_count):
        """
        K-means isn't guaranteed to get the best answer the first time. It might
        get stuck in a "local minimum."
        Here we run kmeans() *iteration_count* times to increase the chance of
        getting a good answer.
        Returns the best set of clusters found.
        """
        print("Running K-means {} times to find best clusters ...".format(iteration_count))
        candidate_clusters = []
        errors = []
        for _ in range(iteration_count):
            clusters = kmeans(points, num_clusters, cutoff)
            error = calculateError(clusters)
            candidate_clusters.append(clusters)
            errors.append(error)

        highest_error = max(errors)
        lowest_error = min(errors)
        print("Lowest error found: {} (Highest: {})".format(
            lowest_error,
            highest_error
        ))
        ind_of_lowest_error = errors.index(lowest_error)
        best_clusters = candidate_clusters[ind_of_lowest_error]

        return best_clusters

def kmeans(points, k, cutoff):

        # Pick out k random points to use as our initial centroids
        initial_centroids = rand.sample(points, k)

        # Create k clusters using those centroids
        # Note: Cluster takes lists, so we wrap each point in a list here.
        clusters = [Clustering([p]) for p in initial_centroids]

        # Loop through the dataset until the clusters stabilize
        loopCounter = 0
        while True:
            # Create a list of lists to hold the points in each cluster
            lists = [[] for _ in clusters]
            clusterCount = len(clusters)

            # Start counting loops
            loopCounter += 1
            # For every point in the dataset ...
            for p in points:
                # Get the distance between that point and the centroid of the first
                # cluster.
                smallest_distance = getDistance(p, clusters[0].centroid)

                # Set the cluster this point belongs to
                clusterIndex = 0

                # For the remainder of the clusters ...
                for i in range(1, clusterCount):
                    # calculate the distance of that point to each other cluster's
                    # centroid.
                    distance = getDistance(p, clusters[i].centroid)
                    # If it's closer to that cluster's centroid update what we
                    # think the smallest distance is
                    if distance < smallest_distance:
                        smallest_distance = distance
                        clusterIndex = i
                # After finding the cluster the smallest distance away
                # set the point to belong to that cluster
                lists[clusterIndex].append(p)

            # Set our biggest_shift to zero for this iteration
            biggest_shift = 0.0

            # For each cluster ...
            for i in range(clusterCount):
                # Calculate how far the centroid moved in this iteration
                shift = clusters[i].update(lists[i])
                # Keep track of the largest move from all cluster centroid updates
                biggest_shift = max(biggest_shift, shift)

            # Remove empty clusters
            clusters = [c for c in clusters if len(c.points) != 0]

            # If the centroids have stopped moving much, say we're done!
            if biggest_shift < cutoff:
                print("Converged after {} iterations".format(loopCounter))
                break
        return clusters


class Clustering(object):
    '''
    A set of points and their centroid
    '''

    def __init__(self, points):
        '''
        points - A list of point objects
        '''

        if len(points) == 0:
            raise Exception("ERROR: empty cluster")

        # The points that belong to this cluster
        self.points = points

        # The dimensionality of the points in this cluster
        self.n = points[0].n

        # Assert that all points are of the same dimensionality
        for p in points:
            if p.n != self.n:
                raise Exception("ERROR: inconsistent dimensions")

        # Set up the initial centroid (this is usually based off one point)
        self.centroid = self.calculateCentroid()

    def __repr__(self):
        '''
        String representation of this object
        '''
        return str(self.points)

    def update(self, points):
        '''
        Returns the distance between the previous centroid and the new after
        recalculating and storing the new centroid.
        Note: Initially we expect centroids to shift around a lot and then
        gradually settle down.
        '''
        old_centroid = self.centroid
        self.points = points
        # Return early if we have no points, this cluster will get
        # cleaned up (removed) in the outer loop.
        if len(self.points) == 0:
            return 0

        self.centroid = self.calculateCentroid()
        shift = getDistance(old_centroid, self.centroid)
        return shift

    def calculateCentroid(self):
        '''
        Finds a virtual center point for a group of n-dimensional points
        '''
        numPoints = len(self.points)
        # Get a list of all coordinates in this cluster
        coords = [p.coords for p in self.points]
        # Reformat that so all x's are together, all y'z etc.
        unzipped = zip(*coords)
        # Calculate the mean for each dimension
        centroid_coords = [math.fsum(dList)/numPoints for dList in unzipped]

        return Point(centroid_coords)

    def getTotalDistance(self):
        '''
        Return the sum of all squared Euclidean distances between each point in
        the cluster and the cluster's centroid.
        '''
        sumOfDistances = 0.0
        for p in self.points:
            sumOfDistances += getDistance(p, self.centroid)

        return sumOfDistances


