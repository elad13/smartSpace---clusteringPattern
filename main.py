import pandas as pd
import csv
from exportDB import read_mongo
from point import Point
from clustering import iterative_kmeans, plotClusters, plotly
from element import Element
import pymongo

df_exportDB = read_mongo('course', 'ACTIONS', {}, host='smartspace-shard-00-01-zmxlk.azure.mongodb.net', port=27017, username='admin', password='Afeka2020', no_id=True)
df_exportDB.drop(['actionSmartspace', 'actionId', 'elementSmartspace',  'playerSmartspace', '_class'], axis=1, inplace=True)

df_exportDB.to_csv('data/ActionsFile.csv', index=False)

# Insert the user you want to analyze.
userEmail = input("Enter the email of the user: ")

inputFile = 'data/smartSpace_' + userEmail + '_beforCluster.csv'
resultsFile = 'data/smartSpace_' + userEmail + '_afterCluster.csv'


# Load Data
elements = []
userFileFields = ['elementId', 'actionType', 'Day', 'Hour', 'moreAttributes']

with open('data/ActionsFile.csv', newline='') as mongoFile:
    reader = csv.reader(mongoFile)
    next(reader, None)  # Skip the header.
    for elementId, playerEmail, actionType, creationTimestamp, moreAttributes in reader:
        element = Element(elementId, playerEmail, actionType, creationTimestamp, moreAttributes)
        elements.append(element)

with open(inputFile, 'w', newline='') as userFile:
    userInput = csv.writer(userFile)
    userInput.writerow(userFileFields)

    for idx in range(0,len(elements)):

        if (elements[idx].playerEmail == userEmail):

            dateFromTimeStamp = pd.to_datetime(elements[idx].creationTimestamp)
            day = dateFromTimeStamp.strftime("%w")
            hour = dateFromTimeStamp.strftime("%H%M")

            attributesField = elements[idx].moreAttributes
            attributeTranslate = attributesField.translate(str.maketrans({"{": r"",
                                                               "}": r"",
                                                               "'": r"",
                                                               " ": r"",
                                                               "\n": r";",
                                                               ",": r"*"}))

            attributeSplited = attributeTranslate.split(';')
            for line in attributeSplited:
                attribute = line.split(':')
                if (attribute[0] == 'state'):
                    if(attribute[1] == 'Off'):
                        state = 0
                    elif (attribute[1] == 'On'):
                        state = 1
                elif (attribute[0] == 'temperature'):
                    asd = attribute[1].split('*')
                    state = asd[0]
                elif (attribute[0] == None):
                    state = 10

            userInput.writerow(
                [
                    elements[idx].elementId,
                    elements[idx].actionType,
                    day,
                    hour,
                    state
                ])

df_userActions = pd.read_csv(inputFile)

dataframe_collection = {}

dataframe_collection = [y for x , y in df_userActions.groupby(['elementId', 'Day'])]

dimensions = 3

# The K in k-means. How many clusters do we assume exist?
#   - Must be less than num_points
num_clusters = 2

# When do we say the process has 'converged' and stop updating clusters?
cutoff = 0.2

# Cluster those data!
iteration_count = 20
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
        coor.append(float(row[2]))  #Day = x
        coor.append(float(row[3]))  #Hour = y
        coor.append(float(row[4]))  #Action = z
        point = Point(coor)
        points.append(point)
    print(len(points))
    clusterNum = int(((len(points))/4))
    best_clusters.append(iterative_kmeans(
        points,
        clusterNum,
        #num_clusters,
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

        with open(resultsFile, 'a') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([elementNum, centroid['x'], centroid['y'], centroid['z']])

    # # Display clusters using plotly for 3d data
    # if dimensions in [2, 3] and plotly:
    #     print("Plotting points, launching browser ...")
    #     plotClusters(best_clusters, dimensions)