import pandas as pd
import csv
from exportDB import read_mongo
from point import Point
from clustering import iterative_kmeans
from element import Element
import pymongo

# Export data from mongoDB
# mongo_uri = 'mongodb://admin:Afeka2020@smartspace-shard-00-00-zmxlk.azure.mongodb.net:27017,smartspace-shard-00-01-zmxlk.azure.mongodb.net:27017,smartspace-shard-00-02-zmxlk.azure.mongodb.net:27017/test?ssl=true&replicaSet=SmartSpace-shard-0&authSource=admin&retryWrites=true'
# myclient = pymongo.MongoClient(mongo_uri)
# mydb = myclient['course']
# mycol = mydb['ACTIONS']
# # for x in mycol.find({},{'_id': 0, 'actionSmartspace': 0, 'actionId': 0, 'elementSmartspace': 0,  'playerSmartspace': 0, '_class': 0}):
# #   #print(x)
# #   df_exportDB = x
# #   with open('data/ActionsFile.csv', 'w') as outfile:
# #       fields = ['elementId', 'playerEmail', 'actionType', 'creationTimestamp', 'moreAttributes']
# #       write = csv.DictWriter(outfile, fieldnames=fields)
# #       write.writeheader()
# #       for answers_record in x:  # Here we are using 'cursor' as an iterator
# #           #print(answers_record)
# #           #print('!!!')
# #           print(answers_record['elementId'])
# #
# #           answers_record_id = answers_record['elementId']
# #           #for answer_record in answers_record['answers']:
# #           flattened_record = {
# #               'elementId': answers_record_id,
# #               'playerEmail': answers_record['playerEmail'],
# #               'actionType': answers_record['actionType'],
# #               'creationTimestamp': answers_record['creationTimestamp'],
# #               'moreAttributes': answers_record['moreAttributes']
# #           }
# #           write.writerow(flattened_record)
#
# fields = ['elementId', 'playerEmail', 'actionType', 'creationTimestamp', 'moreAttributes']
# #data_py = mycol.find({},{'_id': 0, 'elementId': 1,'playerEmail': 1,'actionType': 1,'creationTimestamp': 1,'moreAttributes': 1})
# data_py = mycol.find({},{'_id': 0, 'actionSmartspace': 0, 'actionId': 0, 'elementSmartspace': 0,  'playerSmartspace': 0, '_class': 0})
# with open('data/ActionsFile.csv', 'w', newline='') as outfile:
#     csv_output = csv.writer(outfile)
#     csv_output.writerow(fields)
#
#     for data in data_py:
#         csv_output.writerow(
#             [
#                 data['elementId'],
#                 data['playerEmail'],
#                 data['actionType'],
#                 data['creationTimestamp'],
#                 data['moreAttributes']
#             ])
#
#
#     print(csv_output)
#
#     #outfile.write(x)
# #df_exportDB.to_csv('data/ActionsFile.csv', index=False)
# print(csv_output)
# print('#######')
df_exportDB = read_mongo('course', 'ACTIONS', {}, host='smartspace-shard-00-01-zmxlk.azure.mongodb.net', port=27017, username='admin', password='Afeka2020', no_id=True)
df_exportDB.drop(['actionSmartspace', 'actionId', 'elementSmartspace',  'playerSmartspace', '_class'], axis=1, inplace=True)

df_exportDB.to_csv('data/ActionsFile.csv', index=False)

# Insert the user you want to analyze.
userEmail = input("Enter the email of the user: ")

inputFile = 'data/smartSpace_' + userEmail + '_beforCluster.csv'
resultsFile = 'data/smartSpace_' + userEmail + '_afterCluster.csv'


# Load Data
elements = []
#fields = ['elementId', 'actionType', 'creationTimestamp', 'moreAttributes']
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
                    #elements[el].actionType, **************************
                    day,
                    hour,
                    state
                ])

print('***')
# df = pd.read_csv('data/ActionsFile.csv')
#
# # ****************          Create new Data Frame - check if legal!!!             ********************
# df_userActions = pd.DataFrame(columns=['elementId', 'Day', 'Hour', 'Action'])
#
# for user in df['playerEmail']:
#     # filter the data for each user email
#     if (user == userEmail):
#         df_userActions['elementId'] = df['elementId'].loc[df['playerEmail']==userEmail]
#
#         dateFromTimeStamp = pd.to_datetime(df['creationTimestamp'].loc[df['playerEmail']==userEmail])
#         df_userActions['Day'] = dateFromTimeStamp.dt.strftime("%w")
#         df_userActions['Hour'] = dateFromTimeStamp.dt.strftime("%H%M")
#
#         tg = df['moreAttributes'].loc[df['playerEmail']==userEmail]
#         a_string = tg.to_string(index=False)
#         escaped = a_string.translate(str.maketrans({"{": r"",
#                                                     "}": r"",
#                                                     "'": r"",
#                                                     " ": r"",
#                                                     "\n": r";",
#                                                     ",": r"*"}))
#
#         escaped2 = escaped.split(';')
#         for line in escaped2:
#             fg = line.split(':')
#             print(fg)
#             if(fg[1] == 'Off'):
#                 df_userActions['Action'].loc[df['playerEmail']==userEmail] = 0
#             elif (fg[1] == 'On'):
#                 df_userActions['Action'].loc[df['playerEmail']==userEmail] = 1
#             # for dv in fg:
#             #     gt = dv.split('*')
#             #     if(gt[1] == 'Off'):
#             #         df_userActions['Action'] = 0
#             #     elif (gt[1] == 'On'):
#             #         df_userActions['Action'] = 1
#
#             # *********************** need to insert the temp value ********************
#             # *********************** need to filter the temp value to the last one *******************
#
#
# save into csv file using filename: color_colour.csv
#df_userActions.to_csv(inputFile, index=False)
#
#print(df_userActions)
print('***')

df_userActions = pd.read_csv(inputFile)

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
    print(len(points))
    clusterNum = ((len(points))/4)/2
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

        with open(resultsFile, 'a') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([elementNum, centroid['x'], centroid['y'], centroid['z']])