import argparse
import pandas as pd
from point import Point
from clustering import Clustering, iterative_kmeans, plotClusters, plotly

parser = argparse.ArgumentParser(description="Run k-means for location data",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--input', type=str, default='‏‏lamp1_fullDays.csv',
                        dest='inputfile', help='input location file name')
parser.add_argument('--clusters', type=int, default=8, dest='clusters', help='number of clusters')
args = parser.parse_args()
fn = args.inputfile #fn = "data/" + args.inputfile

#main(fn, args.clusters)

#def main(fn, clusters_no):
#read location data from csv file and store each location as a Point(latit,longit) object
df = pd.read_csv(fn)
#total_days = len(df.axes[0])
#print("total_days: ", total_days)
df.drop(['Id'], axis=1, inplace=True)
x = df.values
print("x: ", x)

# df_days1 = []
# df_days2 = []
# df_days3 = []
# df_days4 = []
# df_days5 = []
# df_days6 = []
# df_days7 = []
#
# for row in x:
#     if (row[0] == 1):
#         df_days1.append(row)
#     if (row[0] == 2):
#         df_days2.append(row)
#     if (row[0] == 3):
#         df_days3.append(row)
#     if (row[0] == 4):
#         df_days4.append(row)
#     if (row[0] == 5):
#         df_days5.append(row)
#     if (row[0] == 6):
#         df_days6.append(row)
#     if (row[0] == 7):
#         df_days7.append(row)
#
# for row in df_days1:
#     print("day 1: ", row)

df_days = []
for row in x:
    for day in row[0]:
        df_days[day].append(row)

for row in df_days[1]:
    print("day 1: ", row)

# create the points (x, y, z)
points = []
for row in x:
    coor = []
    print("point:", row)
    coor.append(float(row[0]))
    coor.append(float(row[1]))
    coor.append(float(row[2]))
    point = Point(coor)
    points.append(point)

dimensions = 3

# The K in k-means. How many clusters do we assume exist?
#   - Must be less than num_points
num_clusters = 8

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

# #run k_means clustering
# #print("clusters no: " + str(clusters_no))
# #cluster = Clustering(geo_locs, clusters_no)
# cluster = Clustering(points, 8)
# flag = cluster.k_means(False)
# if flag == -1:
#     print("Error in arguments!")
# else:
#     #clustering results is a list of lists where each list represents one cluster
#     print("Clustering results:")
#     cluster.print_clusters(cluster.clusters)