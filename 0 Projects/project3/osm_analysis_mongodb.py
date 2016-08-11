# -*- coding: utf-8 -*-
"""
Created on Fri Aug 05 15:23:36 2016

@author: X.Pang
"""

from pymongo import MongoClient
from ggplot import *
import pandas as pd

# %% set db parameters
MONGO_CLIENT = "localhost:27017"
DB_NAME= 'osm'
COLLECTION = 'antwerp'
client = MongoClient(MONGO_CLIENT)
db = client[DB_NAME]

# %% look at basic stats
# Number of documents
num_docs = db[COLLECTION].find().count()
print "{}:{}".format("Number of documents", num_docs)

# Number of nodes
num_nodes = db[COLLECTION].find({"type":"node"}).count()
print "{}:{}".format("Number of nodes", num_nodes)

# Number of ways
num_ways = db[COLLECTION].find({"type":"way"}).count()
print "{}:{}".format("Number of ways", num_ways)

# Number of unique users contributed to the map
num_users = len(db[COLLECTION].distinct("created.user"))
print "{}:{}".format("Number of users", num_users)

# %% List of all cities
city_list = db[COLLECTION].aggregate([{"$match":{"address.city": {"$exists":True}}},
                                      {"$group":{"_id":"$address.city",
                                                 "count":{"$sum":1} } },
                                      {"$sort":{"count":-1} } ])
city_list = list(city_list)
print len(city_list)

# %% Number of documents contributed by each user
documents_by_user = db[COLLECTION].aggregate([{"$group":{"_id":"$created.user",
                                                         "count": {"$sum": 1} } },
                                              {"$sort" :{"count": -1} },
                                              {"$group":{"_id":"$count",
                                                         "count_of_users": {"$sum": 1} } }
                                            ])
documents_by_user = list(documents_by_user)                          
print "{}:{}".format("Number of users", len(documents_by_user))

# %% convert the result to a dataframe and visualize it
documents_by_user = pd.DataFrame(documents_by_user)

# Plot the number of users vs. frequence of contribution
plot_basic = ggplot(aes(x='_id', y='count_of_users'), data=documents_by_user)
plot = plot_basic + geom_point() \
                  + geom_line() \
                  + scale_x_log() \
                  + scale_y_continuous(limits=(0,250)) \
                  + xlab('Number of documents uploaded to OSM') \
                  + ylab('Number of users') 
print plot
