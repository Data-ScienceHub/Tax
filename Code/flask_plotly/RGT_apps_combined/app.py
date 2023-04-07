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
app.config["MONGO_URI"] = "mongodb+srv://DS6013_Students_Ami:DS6013_Students_AK@countyrecords.4cdfgz2.mongodb.net/TaxRecords?retryWrites=true&w=majority"

mongo = PyMongo(app)
columns = list(mongo.db["Tax_Record_1867"].find_one())

# HOMEPAGE --------------------------------------------------------------

@app.route('/callback', methods=['POST', 'GET'])
def cb():
    return gm(request.args.get('data'))
   
@app.route('/')
def index():
    return render_template('chartsajax.html',  graphJSON=gm())

def gm(EventLocJurisdictionCounty='Fluvanna'):
#def gm():
    #df = pd.read_csv('Tax_1867_Cleaned.csv')

    # find is a pymongo function to select the entire collection; list makes it iterable; then make a pandas df
    df = pd.DataFrame(list(mongo.db["Tax_Record_1867"].find()))

    # add condition for whether employer and person have same last name
    conditions = [
        (df['PersonRoleLocSurnameEmployer']==df['PersonSurname']),
        (df['PersonRoleLocSurnameEmployer']!=df['PersonSurname'])
        ]

    values = ['Confirmed', 'Unconfirmed']

    df['FormerlyEnslaved'] = np.select(conditions, values)

    # if trying to use callback function:
    #fig1 = px.histogram(df[df['EventLocJurisdictionCounty']==EventLocJurisdictionCounty], x="PersonEventRole", y="PersonTaxStateAll",
    
    # if not:
    fig1 = px.histogram(df, x="PersonEventRole", y="PersonTaxStateAll",
             color="SourceLocCreatedCounty", barmode='group',
             #barmode='group',
             width=600, height=400)
    
    fig2 = px.histogram(df, x='EventLocJurisdictionCounty', y='PersonsTaxedCountNMalesover21',
             color="PersonEventRole", barmode='group',
             width=600, height=400)
    
    fig3 = px.histogram(df, x='EventLocJurisdictionCounty', y='PersonsTaxedCountWMalesover21',
             color="PersonEventRole", barmode='group',
             width=600, height=400)
    
    fig4 = px.histogram(df, x="PersonEventRole", y="PersonTaxStateAll",
             color="FormerlyEnslaved",
             barmode="group",
             width=600, height=400)


    graphJSON = [None, None, None, None]
    graphJSON[0] = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON[1] = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON[2] = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON[3] = json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)
    
    print(fig1.data[0])
    print(fig2.data[0])
    print(fig3.data[0])
    print(fig4.data[0])
    
    #fig.data[0]['staticPlot']=True
    
    return graphJSON

# SIMPLE SEARCH -------------------------------------------------------------

@app.route("/records_list") # without methods, this page on its own will not exist
def records_list():
    """
    Renders the main page; no cards/people for now
    Takes inputs: text search bars (given_name, surname), 
                  text/date selection (two for list type date_range)
                  text search bar (location)
                  dropdown (source)
    """
    columns = list(mongo.db["Tax_Record_1867"].find_one())
    
    return render_template(
        "records_list_search.html",
        columns=columns
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
    chosen_col = request.form.getlist("chosen_col")

    if "" in chosen_col:
        chosen_col.remove("")
    
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
        output = pd.DataFrame(list(mongo.db["Tax_Record_1867"].find().limit(5)))[chosen_col]
    elif pd.DataFrame(list(mongo.db["Tax_Record_1867"].find(query))).empty:
        output = pd.DataFrame(columns=list(mongo.db['Tax_Record_1867'].find_one().keys()))[chosen_col]
    else:
        output = pd.DataFrame(list(mongo.db["Tax_Record_1867"].find(query).limit(20)))[chosen_col]

    #----------------------------------------------
    # END SEARCH FUNCTION
    
    search_fig = ff.create_table(output)

    searchJSON = json.dumps(search_fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return render_template(
        "records_list_search.html",
        columns=columns,
        searchJSON=searchJSON
    ) 

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")

# INTERACTIVE VISUALIZATION ----------------------------------------------

@app.route("/records_list_graph") # without methods, this page on its own will not exist
def records_list_graph():
    """
    Renders the main page; no cards/people for now
    Takes inputs: text search bars (given_name, surname), 
                  text/date selection (two for list type date_range)
                  text search bar (location)
                  dropdown (source)
    """

    agg_func_list = ["mean", "median", "count"]
    fig_type=["tab", "bar", "scatter"]

    return render_template(
        "records_list.html",
        columns=columns,
        agg_func_list=agg_func_list,
        fig_type=fig_type
    )

@app.route("/graph", methods=["GET", "POST"])
def graph():

    var1 = request.form.get("x_col")
    var2 = request.form.get("y_col")
    var_3 = request.form.get("group_col")
    agg_func = request.form.get("agg_func")
    fig_type = request.form.get("fig_type")

    data = pd.DataFrame(list(mongo.db["Tax_Record_1867"].find()))

    if var1 == None or var2 == None or var1=="" or var2=="":
        fig=ff.create_table(data)

    else:
        if agg_func != "":
            new_data = data.groupby(var1)\
                    .agg({var2:agg_func})\
                    .reset_index()
            if var_3 != "":
                new_data = data.groupby([var1, var_3])\
                        .agg({var2:agg_func})\
                        .reset_index()
        else:
            if var_3 != "":
                new_data = data[[var1, var2, var_3]]
            else:
                new_data = data[[var1, var2]]
        
        if fig_type=="tab":
            fig=ff.create_table(new_data)
        elif fig_type=="bar":
            if var_3 != "":
                fig = px.bar(new_data, x=var1, y=var2, color=var_3,
                            hover_name=var2,
                            height=600, width=1000)
            else:
                fig = px.bar(new_data, x=var1, y=var2, 
                            hover_name=var2,
                            height=600, width=1000)
        elif fig_type=="scatter":
            if var_3 != "":
                fig = px.scatter(new_data, x=var1, y=var2, color=var_3,
                        hover_data=[var1, var2, var_3],
                        height=600, width=1000)
            else:
                fig = px.scatter(new_data, x=var1, y=var2, 
                        hover_data=[var1, var2],
                        height=600, width=1000)
        else:
            fig=ff.create_table(new_data)

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    agg_func_list = ["mean", "median", "count"]
    fig_type=["tab", "bar", "scatter"]

    return render_template(
        "records_list.html",
        columns=columns,
        graphJSON=graphJSON,
        agg_func_list=agg_func_list,
        fig_type=fig_type
    )




# RUN --------------------------------------------------------

if __name__ == "__main__":
    app.run(# host=os.environ.get("IP"),
            port=9001, # int(os.environ.get("PORT"))
            debug=False)
# TO DO:
# - add CSS styling to the HTML for visuals, adding descriptions, etc.
# - fix callback function, add functionality for exploration and changing other graphs