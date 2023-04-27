"""
Metadata

Title: queries_v1.0
Author: Ami Kano
Date: January 28, 2023

Comments:
This Python file contains four functions: query(), name_query(), location_query(), and date_query().
Each function queries from the OneShardStory MongoDB database, with differing focus. The input for these queries is the same:
a single string. The MongoDB database with accessed with the author's credentials. 

To be run without error, this file requires the Python packages PyMongo, NumPy, and Pandas.
"""

#-------------------------------------------------------------------------------------------------

from pymongo import MongoClient
import numpy as np
import pandas as pd

#-------------------------------------------------------------------------------------------------

def query(input_string):
    
    # URI is specific to Ami's login credentials
    uri = "mongodb+srv://DS6013_Students_Ami:DS6013_Students_AK@countyrecords.4cdfgz2.mongodb.net/?retryWrites=true&w=majority"
    
    # connect to database
    client = MongoClient(uri)
    database = client['CountyRecords']
    
    # check if input is a string; if not, convert
    if type(input_string) is not str:
        input_string = str(input_string)
    
    # the query:
    query = {'$text': {'$search':input_string, '$caseSensitive': False}}

    # initialize return value
    output_list = list()

    # iterate through entire database with query
    for collection in database.list_collection_names():
        
        query_result = pd.DataFrame(list(database[collection].find(query)))
        
        if not query_result.empty:
            output_list.append(query_result)
    
    # close connection to database
    client.close()
    
    return output_list

#-------------------------------------------------------------------------------------------------

def name_query(input_string):
    
    # URI is specific to Ami's login credentials
    uri = "mongodb+srv://DS6013_Students_Ami:DS6013_Students_AK@countyrecords.4cdfgz2.mongodb.net/?retryWrites=true&w=majority"
    
    # connect to database
    client = MongoClient(uri)
    database = client['CountyRecords']
    
    # check if input is a string; if not, convert
    if type(input_string) is not str:
        input_string = str(input_string)
            
    # initialize return value
    output_list = list()
    
    # look into all column/field names in database, query fields with names that have "name" in it
    for collection in database.list_collection_names():
        
        keys = database[collection].find_one()
        key_with_name = list()
        
        for key in keys:
            if ("name" in key.lower()) or ("person" in key.lower()):
                key_with_name.append(key)
        
        query = {'$or': []} 
        
        for key in key_with_name:
            query["$or"].append({key : {"$regex" : input_string}})
        
        if len(query["$or"]) != 0:
            output_list.append(pd.DataFrame(list(database[collection].find(query))))
    
    # close connection to database
    client.close()
    
    return output_list

#-------------------------------------------------------------------------------------------------

def location_query(input_string):
    
    # URI is specific to Ami's login credentials
    uri = "mongodb+srv://DS6013_Students_Ami:DS6013_Students_AK@countyrecords.4cdfgz2.mongodb.net/?retryWrites=true&w=majority"
    
    # connect to database
    client = MongoClient(uri)
    database = client['CountyRecords']
    
    # check if input is a string; if not, convert
    if type(input_string) is not str:
        input_string = str(input_string)
            
    # initialize return value
    output_list = list()
    
    # look into all column/field names in database, query fields with names that have location-related terms in it
    for collection in database.list_collection_names():
        
        keys = database[collection].find_one()
        key_with_location = list()
        
        for key in keys:
            if ("county" in key.lower()) or ("district" in key.lower()) or ("place" in key.lower()) \
                or ("residence" in key.lower()) or ("location" in key.lower()):
                key_with_location.append(key)
        
        query = {'$or': []} 
        
        for key in key_with_location:
            query["$or"].append({key : {"$regex" : input_string}})

        if len(query["$or"]) != 0:
            output_list.append(pd.DataFrame(list(database[collection].find(query))))
    
    # close connection to database
    client.close()
    
    return output_list

#-------------------------------------------------------------------------------------------------

def date_query(input_string):
    
    # URI is specific to Ami's login credentials
    uri = "mongodb+srv://DS6013_Students_Ami:DS6013_Students_AK@countyrecords.4cdfgz2.mongodb.net/?retryWrites=true&w=majority"
    
    # connect to database
    client = MongoClient(uri)
    database = client['CountyRecords']
    
    # check if input is a string; if not, convert
    if type(input_string) is not str:
        input_string = str(input_string)
            
    # initialize return value
    output_list = list()
    
    # look into all column/field names in database, query fields with names that have date-related terms in it
    for collection in database.list_collection_names():
        
        keys = database[collection].find_one()
        key_with_date = list()
        
        for key in keys:
            if ("date" in key.lower()) or ("dob" in key.lower()) or ("month" in key.lower()) \
                or ("day" in key.lower()) or ("year" in key.lower()):
                key_with_date.append(key)
        
        query = {'$or': []} 
        
        for key in key_with_date:
            query["$or"].append({key : {"$regex" : input_string}})

        if len(query["$or"]) != 0:
            output_list.append(pd.DataFrame(list(database[collection].find(query))))
    
    # close connection to database
    client.close()
    
    return output_list
