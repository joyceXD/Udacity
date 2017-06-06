# -*- coding: utf-8 -*-
"""
Created on Mon Jul 18 15:43:48 2016

@author: X.Pang
"""

"""
Complete the insert_data function to insert the data into MongoDB.
"""

import json

def insert_data(data, db):

    # Your code here. Insert the data into a collection 'arachnid'
    db.arachnid.insert_many(data)
    result = db.arachnid.count()
    print result


if __name__ == "__main__":
    
    from pymongo import MongoClient
    client = MongoClient("mongodb://localhost:27017")
    db = client.examples
    

    with open('arachnid.json') as f:
        data = json.loads(f.read())
        insert_data(data, db)
        print db.arachnid.find_one()