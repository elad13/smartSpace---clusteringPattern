import pandas as pd
from pymongo import MongoClient


def _connect_mongo(host, port, username, password, db):
    """ A util for making a connection to mongo """

    if username and password:
        mongo_uri = 'mongodb://admin:Afeka2020@smartspace-shard-00-00-zmxlk.azure.mongodb.net:27017,smartspace-shard-00-01-zmxlk.azure.mongodb.net:27017,smartspace-shard-00-02-zmxlk.azure.mongodb.net:27017/test?ssl=true&replicaSet=SmartSpace-shard-0&authSource=admin&retryWrites=true'
        conn = MongoClient(mongo_uri)
    else:
        conn = MongoClient(host, port)
    return conn[db]


def read_mongo(db, collection, query={}, host='localhost', port=27017, username=None, password=None, no_id=True, no_elementId=True):
    """ Read from Mongo and Store into DataFrame """

    # Connect to MongoDB
    db = _connect_mongo(host=host, port=port, username=username, password=password, db=db)

    # Make a query to the specific DB and Collection
    cursor = db[collection].find(query)

    # Expand the cursor and construct the DataFrame
    df =  pd.DataFrame(list(cursor))

    # Delete the _id
    if no_id and '_id' in df:
        del df['_id']

    return df
