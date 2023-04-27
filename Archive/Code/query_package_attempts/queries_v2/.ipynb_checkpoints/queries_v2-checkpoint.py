"""
Metadata

Title: queries_v2
Author: Ami Kano
Date: February 12, 2023


Comments:

This Python file contains the function query().

The inputs for the query() function are:
- first_name : string, "" by default
- last_name : string, "" by default
- date_range : list of 2 integers, [1600, 1900] by default
- location : string, "" by default
- source : string, "any" by default
- include : string, "all" by default

The MongoDB database is accessed with the author's credentials. 

To be run without error, this file requires the Python packages PyMongo, NumPy, and Pandas.
"""

#-------------------------------------------------------------------------------------------------

from pymongo import MongoClient
import numpy as np
import pandas as pd

#-------------------------------------------------------------------------------------------------

def query(first_name="", last_name="", date_range=[1600, 1900], location="", source="any", include="all"):
    
    # URI is specific to Ami's login credentials
    uri = "mongodb+srv://DS6013_Students_Ami:DS6013_Students_AK@countyrecords.4cdfgz2.mongodb.net/?retryWrites=true&w=majority"

     # connect to database
    client = MongoClient(uri)
    database = client['Tax_Records']

    # output is null/none now
    output = None 

    # if searching all documents in database
    if source=="any":
        
        # define output as list
        output = list()
        
        # acquire column names
        for collection in database.list_collection_names():
            keys = database[collection].find_one()

            # separate keys by type of information
            key_with_name = list()
            key_with_date = list()
            key_with_location = list()

            for key in keys:
                if ("name" in key.lower()) or ("person" in key.lower()):
                    key_with_name.append(key)
                if ("date" in key.lower()):
                    key_with_date.append(key)
                if ("loc" in key.lower()):
                    key_with_location.append(key)

            # build query

            # wide search; "or"
            if include=="all":
                query = {'$or': []} 

                # add onto query with keys
                for key in key_with_name:
                    query["$or"].append({key : {"$regex" : first_name, "$options" : "i"}})
                    query["$or"].append({key : {"$regex" : last_name, "$options" : "i"}})
                for key in key_with_date:
                    query["$or"].append({key : {'$gte' : date_range[0], '$lte' : date_range[1]}})
                for key in key_with_location:
                    query["$or"].append({key : {"$regex" : location, "$options" : "i"}})

                # add results in output list
                output.append(pd.DataFrame(list(database[collection].find(query))))

            # narrow search; "and"
            # elif include=="only":
            else:
                query = {} 
                query["$and"] = []

                # add onto query with keys
                name_query = {"$or" : []}
                for key in key_with_name:
                    name_query["$or"].append({ key: {"$regex" : first_name, "$options" : "i"} })
                    name_query["$or"].append({ key: {"$regex" : last_name, "$options" : "i"} })
                query["$and"].append(name_query)

                date_query = {"$or" : []}
                for key in key_with_date:
                    date_query["$or"].append({ key: {'$gte' : date_range[0], '$lte' : date_range[1]} })
                query["$and"].append(date_query)

                location_query = {"$or" : []}
                for key in key_with_location:
                    location_query["$or"].append({ key : {"$regex" : location, "$options" : "i"} })
                query["$and"].append(location_query)
                    
                # add results in output list
                output.append(pd.DataFrame(list(database[collection].find(query))))



    # if a specific source document is selected
    else:

        # acquire column names
        try:
            keys = database[source].find_one()
        except:
            return "source document not in database"

        # separate keys by type of information
        key_with_name = list()
        key_with_date = list()
        key_with_location = list()

        for key in keys:
            if ("name" in key.lower()) or ("person" in key.lower()):
                key_with_name.append(key)
            if ("date" in key.lower()):
                key_with_date.append(key)
            if ("loc" in key.lower()):
                key_with_location.append(key)

        # build query
        # wide search; "or"
        if include=="all":
            query = {'$or': []} 

            # add onto query with keys
            for key in key_with_name:
                query["$or"].append({key : {"$regex" : first_name, "$options" : "i"}})
                query["$or"].append({key : {"$regex" : last_name, "$options" : "i"}})
            for key in key_with_date:
                query["$or"].append({key : {'$gte' : date_range[0], '$lte' : date_range[1]}})
            for key in key_with_location:
                query["$or"].append({key : {"$regex" : location, "$options" : "i"}})

            # produce result
            output = pd.DataFrame(list(database[source].find(query)))

        # narrow search; "and"
        # elif include=="only":
        else:
            query = {} 
            query["$and"] = []
            
            # add onto query with keys
            name_query = {"$or" : []}
            for key in key_with_name:
                name_query["$or"].append({ "$or" : [{ key: {"$regex" : first_name, "$options" : "i"} }, 
                                                    { key: {"$regex" : last_name, "$options" : "i"} }]})
            query["$and"].append(name_query)
            
            date_query = {"$or" : []}
            for key in key_with_date:
                date_query["$or"].append({ key: {'$gte' : date_range[0], '$lte' : date_range[1]} })
            query["$and"].append(date_query)
            
            location_query = {"$or" : []}
            for key in key_with_location:
                location_query["$or"].append({ key : {"$regex" : location, "$options" : "i"}})
            query["$and"].append(location_query)

            # produce result
            output = pd.DataFrame(list(database[source].find(query)))
    
    # close connection to database
    client.close()

    return output

