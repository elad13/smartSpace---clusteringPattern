import pandas as pd
import csv
from exportDB import read_mongo
from point import Point
from clustering import iterative_kmeans

# Export data from mongoDB
df_exportDB = read_mongo('course', 'ACTIONS', {}, host='smartspace-shard-00-01-zmxlk.azure.mongodb.net', port=27017, username='admin', password='Afeka2020', no_id=True)
df_exportDB.to_csv('data/ActionsFile.csv', index=False)

# Insert the user you want to analyze.
userEmail = 'eladm1991@gmail.com'#input("Enter the email of the user: ")

inputFile = 'data/smartSpace_' + userEmail + '_beforCluster.csv'
resultsFile = 'data/smartSpace_' + userEmail + '_afterCluster.csv'

# Load Data
df = pd.read_csv('data/ActionsFile.csv')

# ****************          Create new Data Frame - check if legal!!!             ********************
df_userActions = pd.DataFrame(columns=['elementId', 'Day', 'Hour', 'Action'])

for user in df['playerEmail']:
    # filter the data for each user email
    if (user == userEmail):
        df_userActions['elementId'] = df['elementId'].loc[df['playerEmail']==userEmail]

        dateFromTimeStamp = pd.to_datetime(df['creationTimestamp'].loc[df['playerEmail']==userEmail])
        df_userActions['Day'] = dateFromTimeStamp.dt.strftime("%w")
        df_userActions['Hour'] = dateFromTimeStamp.dt.strftime("%H%M")

        tg = df['moreAttributes'].loc[df['playerEmail']==userEmail]
        a_string = tg.to_string(index=False)
        escaped = a_string.translate(str.maketrans({"{": r"",
                                                    "}": r"",
                                                    "'": r"",
                                                    " ": r"",
                                                    "\n": r";",
                                                    ",": r"*"}))

        escaped2 = escaped.split(';')
        for line in escaped2:
            fg = line.split(':')
            print(fg)
            if(fg[1] == 'Off'):
                df_userActions['Action'] = 0
            elif (fg[1] == 'On'):
                df_userActions['Action'] = 1
            # for dv in fg:
            #     gt = dv.split('*')
            #     if(gt[1] == 'Off'):
            #         df_userActions['Action'] = 0
            #     elif (gt[1] == 'On'):
            #         df_userActions['Action'] = 1

            # *********************** need to insert the temp value ********************
            # *********************** need to filter the temp value to the last one *******************


print('***')

# save into csv file using filename: color_colour.csv
df_userActions.to_csv(inputFile, index=False)

print(df_userActions)

dataframe_collection = {}

dataframe_collection = [y for x , y in df_userActions.groupby(['elementId', 'Day'])]

dimensions = 3

# The K in k-means. How many clusters do we assume exist?
#   - Must be less than num_points
num_clusters = 2 #cluster to on and cluster to off - need to change in the future *************************************************

# When do we say the process has 'converged' and stop updating clusters?
cutoff = 0.2 #need to understand the number *************************************************

# Cluster those data!
iteration_count = 20 #need to understand the number *************************************************
with open(resultsFile, 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["elementId", "Day", "Hour", "Action"])

x = {}

best_clusters = []
df_centroidsTable = []
for i in range(0, len(dataframe_collection)):
    points = []
    x[i] = dataframe_collection[i].values
    elementNum = x[i][0][0]
    print(x[i])
    for row in x[i]:
        coor = []
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

        with open(resultsFile, 'a') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([elementNum, centroid['x'], centroid['y'], centroid['z']])