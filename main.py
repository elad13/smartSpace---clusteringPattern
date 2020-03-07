import argparse
import pandas as pd

from point import Point
from clustering import Clustering



def main(fn, clusters_no):
    geo_locs = []
    #read location data from csv file and store each location as a Point(latit,longit) object
    df = pd.read_csv(fn)
    total_days = len(df.axes[1])

    for index_x in range(total_days):
        total_hours = len(df[str(index_x)].values)
        #print("total days: " + str(total_days) + " total hours: " + str(total_hours))
        for index_y in range(total_hours):
            #loc_ = Point(float(index_x), float(index_y))
            loc_ = Point(float(index_x), float(df.loc[int(index_y)].at[str(index_x)]))
            #loc_ = Point(float(df.loc[int(index_y)].at[str(index_x)]), float(index_x))
            #print(str(df.loc[int(index_y)].at[str(index_x)]))
            #print("day: " + str(index_x) + " y: " + str(index_y))
            geo_locs.append(loc_)

    # for index, row in df.iterrows():
    #     loc_ = Point(float(row['LAT']), float(row['LON']))   #tuples for location
    #     geo_locs.append(loc_)

    #run k_means clustering
    #print("clusters no: " + str(clusters_no))
    #cluster = Clustering(geo_locs, clusters_no)
    cluster = Clustering(geo_locs, total_days)
    flag = cluster.k_means(False)
    if flag == -1:
        print("Error in arguments!")
    else:
        #clustering results is a list of lists where each list represents one cluster
        print("Clustering results:")
        cluster.print_clusters(cluster.clusters)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run k-means for location data",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    #parser.add_argument('--input', type=str, default='NYC_Free_Public_WiFi_03292017.csv',
    parser.add_argument('--input', type=str, default='smartSapce1_lamp1.csv',
                        dest='inputfile', help='input location file name')
    parser.add_argument('--clusters', type=int, default=8, dest='clusters', help='number of clusters')
    args = parser.parse_args()
    fn = args.inputfile #fn = "data/" + args.inputfile
    main(fn, args.clusters)