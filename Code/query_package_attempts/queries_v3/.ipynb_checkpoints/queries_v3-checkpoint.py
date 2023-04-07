"""
Metadata

Title: queries_v3
Author: Ami Kano
Date: February 19, 2023


Comments:

This Python file contains the function query().

The inputs for the query() function are:
- given_name : string, "" by default
- surname : string, "" by default
- date_range : list of 2 integers, [1600, 1900] by default
- location : string, "" by default
- source : string, "any" by default
- wide : boolean, True by default

The output will be a list of pandas dataframes.

The MongoDB database is accessed with the author's credentials. 

To be run without error, this file requires the Python packages PyMongo, NumPy, and Pandas.

------------------------------------------
TO-DO: 
- make query less error-prone

"""

#-------------------------------------------------------------------------------------------------

from pymongo import MongoClient
import numpy as np
import pandas as pd

#-------------------------------------------------------------------------------------------------

def query(given_name="", surname="", date_range=[1600, 1900], location="", source="any", wide=True):
    
    # URI is specific to Ami's login credentials
    uri = "mongodb+srv://DS6013_Students_Ami:DS6013_Students_AK@countyrecords.4cdfgz2.mongodb.net/?retryWrites=true&w=majority"

    # connect to database
    client = MongoClient(uri)
    database = client['TaxRecords']

    # define output as list
    output = list()

    # if searching all documents in database
    if source=="any":
        
        # look at each table/document
        for collection in database.list_collection_names():
            
            # acquire column names
            keys = database[collection].find_one()

            # separate keys by type of information
            key_for_given_name = list()
            key_for_surname = list()
            key_with_date = list()
            key_with_location = list()

            # sort keys into categories
            for key in keys:
                
                # if column name is "EventTitle"
                if key=="EventTitle":
                    key_for_given_name.append(key)
                    key_for_surname.append(key)
                
                # if column name does not include "GivenNames" or "Surname" but includes "name"
                if (not "GivenNames" in key) and (not "Surname" in key) and ("name" in key.lower()):
                    key_for_given_name.append(key)
                    key_for_surname.append(key)
                
                # if column name includes "GivenNames"
                if ("GivenNames" in key):
                    key_for_given_name.append(key)
                    
                # if column name includes "Surname"
                if ("Surname" in key):
                    key_for_surname.append(key)
                
                # if column name includes "date"
                if ("date" in key.lower()):
                    key_with_date.append(key)
                
                # if column name includes "loc"
                if ("loc" in key.lower()):
                    key_with_location.append(key)

            # build query

            # wide search; "or"
            if wide==True:
                query = {'$or': []} 

                # add onto query with keys
                for key in key_for_surname:
                    query["$or"].append({key : {"$regex" : surname, "$options" : "i"}})
                for key in key_for_given_name:
                    query["$or"].append({key : {"$regex" : given_name, "$options" : "i"}})
                for key in key_with_date:
                    query["$or"].append({key : {'$gte' : date_range[0], '$lte' : date_range[1]}})
                for key in key_with_location:
                    query["$or"].append({key : {"$regex" : location, "$options" : "i"}})

                # add results in output list
                output.append(pd.DataFrame(list(database[collection].find(query))))

            # narrow search; "and"
            else:
                query = {} 
                query["$and"] = []

                # add onto query with keys
                given_name_query = {"$or" : []}
                for key in key_for_given_name:
                    given_name_query["$or"].append({ key: {"$regex" : given_name, "$options" : "i"} })
                query["$and"].append(given_name_query)
                
                surname_query = {"$or" : []}
                for key in key_for_surname:
                    surname_query["$or"].append({ key: {"$regex" : surname, "$options" : "i"} })
                query["$and"].append(surname_query)

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
        key_for_given_name = list()
        key_for_surname = list()
        key_with_date = list()
        key_with_location = list()

        for key in keys:
            
            # if column name is "EventTitle"
            if key=="EventTitle":
                key_for_given_name.append(key)
                key_for_surname.append(key)

            # if column name does not include "GivenNames" or "Surname" but includes "name"
            if (not "GivenNames" in key) and (not "Surname" in key) and ("name" in key.lower()):
                key_for_given_name.append(key)
                key_for_surname.append(key)

            # if column name includes "GivenNames"
            if ("GivenNames" in key):
                key_for_given_name.append(key)

            # if column name includes "Surname"
            if ("Surname" in key):
                key_for_surname.append(key)

            # if column name includes "date"
            if ("date" in key.lower()):
                key_with_date.append(key)

            # if column name includes "loc"
            if ("loc" in key.lower()):
                key_with_location.append(key)


        # build query
        # wide search; "or"
        if wide==True:
            query = {'$or': []} 

            # add onto query with keys
            for key in key_for_surname:
                query["$or"].append({key : {"$regex" : surname, "$options" : "i"}})
            for key in key_for_given_name:
                query["$or"].append({key : {"$regex" : given_name, "$options" : "i"}})
            for key in key_with_date:
                query["$or"].append({key : {'$gte' : date_range[0], '$lte' : date_range[1]}})
            for key in key_with_location:
                query["$or"].append({key : {"$regex" : location, "$options" : "i"}})
            
            # produce result
            output.append(pd.DataFrame(list(database[source].find(query))))

        # narrow search; "and"
        else:
            query = {} 
            query["$and"] = []

            # add onto query with keys
            given_name_query = {"$or" : []}
            for key in key_for_given_name:
                given_name_query["$or"].append({ key: {"$regex" : given_name, "$options" : "i"} })
            query["$and"].append(given_name_query)

            surname_query = {"$or" : []}
            for key in key_for_surname:
                surname_query["$or"].append({ key: {"$regex" : surname, "$options" : "i"} })
            query["$and"].append(surname_query)

            date_query = {"$or" : []}
            for key in key_with_date:
                date_query["$or"].append({ key: {'$gte' : date_range[0], '$lte' : date_range[1]} })
            query["$and"].append(date_query)

            location_query = {"$or" : []}
            for key in key_with_location:
                location_query["$or"].append({ key : {"$regex" : location, "$options" : "i"} })
            query["$and"].append(location_query)

            # produce result
            output.append(pd.DataFrame(list(database[source].find(query))))
    
    # close connection to database
    client.close()

    return output
