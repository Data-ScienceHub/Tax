import os
# import math
from flask_pymongo import PyMongo
# from bson.objectid import ObjectId
# from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, flash, render_template, redirect, request, session, url_for
import pandas as pd
import numpy as np
    
#--------------------------------------------------------

import dotenv
dotenv.load_dotenv(dotenv_path="/Users/amikano/Documents/MSDS/Capstone/web_app/.env")

app = Flask(__name__, template_folder = 'template')

# print(os.getenv("MONGO_DBNAME")) # returns None

app.config["MONGO_DBNAME"] = "TaxRecords" # os.getenv("MONGO_DBNAME")
app.config["MONGO_URI"] = "mongodb+srv://DS6013_Students_Ami:DS6013_Students_AK@countyrecords.4cdfgz2.mongodb.net/TaxRecords?retryWrites=true&w=majority"
# os.getenv("MONGO_URI")

mongo = PyMongo(app)

#--------------------------------------------------------


@app.route("/")
@app.route("/records_list")
def records_list():
    """
    Renders the main page; no cards/people for now
    Takes inputs: text search bars (given_name, surname), 
                  text/date selection (two for list type date_range)
                  text search bar (location)
                  dropdown (source)
    """
    
    sources = mongo.db.list_collection_names()
    return render_template(
        "records_list.html",
        sources=sources
    )



@app.route("/search", methods=["GET", "POST"])
def search():
    """
    Function to use the searchbar in homepage.
    Events can be filtered by given_name, surname, date range, location, source
    """
    
    # Takes in input from HTML
    given_name = request.form.get("given_name") 
        # assumes <input type="text" name="given_name" id="given_name" minlength="3" class="validate">
    surname = request.form.get("surname")
        # assumes <input type="text" name="surname" id="surname" minlength="3" class="validate">
    date_range_0 = request.form.get("date_range_0")
    date_range_1 = request.form.get("date_range_1")
    location = request.form.get("location")
    source = request.form.get("source")
    
    date_range = [date_range_0, date_range_1]
    
    sources = mongo.db.list_collection_names()
    
    # SEARCH FUNCTION
    #----------------------------------------------
    
    # define output as empty list
    output = list()

    # if searching all documents in database
    if source=="":
        
        # look at each table/document
        for collection in mongo.db.list_collection_names():
            
            # acquire column names
            keys = mongo.db[collection].find_one()

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

            query = {} 
            query["$and"] = []

            # add onto query with keys
            if given_name:
                given_name_query = {"$or" : []}
                for key in key_for_given_name:
                    given_name_query["$or"].append({ key: {"$regex" : given_name, "$options" : "i"} })
                query["$and"].append(given_name_query)

            if surname:
                surname_query = {"$or" : []}
                for key in key_for_surname:
                    surname_query["$or"].append({ key: {"$regex" : surname, "$options" : "i"} })
                query["$and"].append(surname_query)

            if date_range:
                date_query = {"$or" : []}
                for key in key_with_date:
                    date_query["$or"].append({ key: {'$gte' : date_range[0], '$lte' : date_range[1]} })
                query["$and"].append(date_query)

            if location:
                location_query = {"$or" : []}
                for key in key_with_location:
                    location_query["$or"].append({ key : {"$regex" : location, "$options" : "i"} })
                query["$and"].append(location_query)

            # add results in output list
            output.append(pd.DataFrame(list(mongo.db[collection].find(query))))

    # if a specific source document is selected
    else:

        # acquire column names
        try:
            keys = mongo.db[source].find_one()
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
        
        query = {} 
        query["$and"] = []

        # add onto query with keys
        if given_name:
            given_name_query = {"$or" : []}
            for key in key_for_given_name:
                given_name_query["$or"].append({ key: {"$regex" : given_name, "$options" : "i"} })
            query["$and"].append(given_name_query)

        if surname:
            surname_query = {"$or" : []}
            for key in key_for_surname:
                surname_query["$or"].append({ key: {"$regex" : surname, "$options" : "i"} })
            query["$and"].append(surname_query)

        if date_range:
            date_query = {"$or" : []}
            for key in key_with_date:
                date_query["$or"].append({ key: {'$gte' : date_range[0], '$lte' : date_range[1]} })
            query["$and"].append(date_query)

        if location:
            location_query = {"$or" : []}
            for key in key_with_location:
                location_query["$or"].append({ key : {"$regex" : location, "$options" : "i"} })
            query["$and"].append(location_query)
        
        # produce result
        output.append(pd.DataFrame(list(mongo.db[source].find(query))))

    
    #----------------------------------------------
    # END SEARCH FUNCTION
    
    
    events = output # currently list of pandas dataframes
    return render_template(
        "get_records.html",
        sources=sources,
        events=events
    )


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")




#--------------------------------------------------------

if __name__ == "__main__":
    app.run(# host=os.environ.get("IP"),
            port=9000, # int(os.environ.get("PORT"))
            debug=False)