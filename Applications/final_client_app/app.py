from flask import Flask, config, render_template, request
from flask_pymongo import PyMongo
import pandas as pd
import json
import plotly
import plotly.express as px
import plotly.figure_factory as ff
import numpy as np


# SETUP --------------------------------------------------------------

app = Flask(__name__, template_folder = 'templates')

app.config["MONGO_DBNAME"] = "TaxRecords"
app.config["MONGO_URI"] = "mongodb+srv://ak7ra:ds6013_ak7ra@onesharedstory.9pydghi.mongodb.net/TaxRecords?retryWrites=true&w=majority"

mongo = PyMongo(app)
columns = list(mongo.db["Tax_Record_1867"].find_one({}, {'_id':False}))

# SIMPLE SEARCH -------------------------------------------------------------

@app.route("/", methods=['POST', 'GET']) # without methods, this page on its own will not exist
def simple_search():
    """
    Renders the main page; no cards/people for now
    Takes inputs: text search bars (given_name, surname), 
                  text/date selection (two for list type date_range)
                  text search bar (location)
                  dropdown (source)
    """

    columns = list(mongo.db["Tax_Record_1867"].find_one({}, {'_id':False}))
    
    # Takes in input from HTML
    given_name = request.form.get("given_name") 
        # assumes <input type="text" name="given_name" id="given_name" minlength="3" class="validate">
    surname = request.form.get("surname")
        # assumes <input type="text" name="surname" id="surname" minlength="3" class="validate">
    date_range_0 = request.form.get("date_range_0")
    date_range_1 = request.form.get("date_range_1")
    location = request.form.get("location")
    chosen_col = request.form.getlist("chosen_col")

    if "" in chosen_col:
        chosen_col.remove("")
    if len(chosen_col)==0:
        chosen_col = ['EventLocJurisdictionCounty', 'PersonGivenNames', 'PersonSurname', 'EventImageLink']
    chosen_col_dict = {}
    for col in chosen_col:
        chosen_col_dict[col] = 1
    chosen_col_dict['_id'] = 0
    
    if date_range_0 == "":
        date_range_0 = None

    if date_range_1 == "":
        date_range_1 = None

    if date_range_0 != None and date_range_1 != None:
        date_range_0 = int(date_range_0)
        date_range_1 = int(date_range_1)
        date_range = [date_range_0, date_range_1]
    else:
        date_range = []

    # SEARCH FUNCTION
    #----------------------------------------------

    # get column names
    keys = mongo.db['Tax_Record_1867'].find_one()

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
        if given_name_query:
            query["$and"].append(given_name_query)

    if surname:
        surname_query = {"$or" : []}
        for key in key_for_surname:
            surname_query["$or"].append({ key: {"$regex" : surname, "$options" : "i"} })
        if surname_query:
            query["$and"].append(surname_query)

    if date_range:
        date_query = {"$or" : []}
        for key in key_with_date:
            date_query["$or"].append({ key: {'$gte' : date_range[0], '$lte' : date_range[1]} })
        if date_query:
            query["$and"].append(date_query)

    if location:
        location_query = {"$or" : []}
        for key in key_with_location:
            location_query["$or"].append({ key : {"$regex" : location, "$options" : "i"} })
        if location_query:
            query["$and"].append(location_query)

    # produce result
    if len(query['$and'])==0:
        output = pd.DataFrame(list(mongo.db["Tax_Record_1867"].find({}, chosen_col_dict).limit(5)))
    elif pd.DataFrame(list(mongo.db["Tax_Record_1867"].find(query))).empty:
        output = pd.DataFrame(columns=list(mongo.db['Tax_Record_1867'].find_one({}, chosen_col_dict).keys()))
    else:
        output = pd.DataFrame(list(mongo.db["Tax_Record_1867"].find(query, chosen_col_dict).limit(40)))

    #----------------------------------------------
    # END SEARCH FUNCTION
    
    search_fig = ff.create_table(output)

    searchJSON = search_fig.to_json()
    
    return render_template(
        "simple_search.html",
        columns=columns,
        searchJSON=searchJSON,
        selected_given_name = given_name,
        selected_surname = surname,
        selected_date_0 = date_range_0,
        selected_date_1 = date_range_1,
        selected_location = location,
        selected_chosen_col = chosen_col
    )

# DATADICT --------------------------------------------------------------
from starlette.templating import Jinja2Templates
templates = Jinja2Templates(directory='templates')

@app.route("/data_dictionary") # without methods, this page on its own will not exist
def data_dictionary():

    data_df = pd.DataFrame(list(mongo.db['Data_Dict']\
            .find({}, {'_id':False})))
    
    temp = data_df.to_dict('records')
    colNames = data_df.columns.values

    return render_template('datadict.html', records=temp, colnames=colNames)

# ERROR HANDLER ---------------------------------------------

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")


# RUN --------------------------------------------------------

if __name__ == "__main__":
    app.run(# host=os.environ.get("IP"),
            port=9001, # int(os.environ.get("PORT"))
            debug=True)
# TO DO:
# - add CSS styling to the HTML for visuals, adding descriptions, etc.
# - fix callback function, add functionality for exploration and changing other graphs