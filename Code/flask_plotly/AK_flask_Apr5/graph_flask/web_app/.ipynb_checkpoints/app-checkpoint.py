import os
# import math
from flask_pymongo import PyMongo
# from bson.objectid import ObjectId
# from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, flash, render_template, redirect, request, session, url_for
import pandas as pd
import numpy as np
import json
import plotly
import plotly.express as px
import plotly.figure_factory as ff
    
#--------------------------------------------------------

# import dotenv
# dotenv.load_dotenv(dotenv_path="/Users/amikano/Documents/MSDS/Capstone/web_app/.env")

app = Flask(__name__, template_folder = 'template')

# print(os.getenv("MONGO_DBNAME")) # returns None

app.config["MONGO_DBNAME"] = "TaxRecords" # os.getenv("MONGO_DBNAME")
app.config["MONGO_URI"] = "mongodb+srv://DS6013_Students_Ami:DS6013_Students_AK@countyrecords.4cdfgz2.mongodb.net/TaxRecords?retryWrites=true&w=majority"
# os.getenv("MONGO_URI")

mongo = PyMongo(app)
columns = list(mongo.db["Tax_Record_1867"].find_one())

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
    columns = list(mongo.db["Tax_Record_1867"].find_one())
    
    return render_template(
        "records_list.html",
        columns=columns
    )

@app.route("/graph", methods=["GET", "POST"])
def graph():

    var1 = request.form.get("x_col")
    var2 = request.form.get("y_col")

    new_data = pd.DataFrame(list(mongo.db["Tax_Record_1867"].find()))[[var1, var2]]

    graph_fig = px.scatter(new_data, x=var1, y=var2,
                     hover_data=[var1, var2],
                     height=600, width=1000)

    graphJSON = json.dumps(graph_fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template(
        "records_list.html",
        columns=columns,
        graphJSON=graphJSON
    )    


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")




#--------------------------------------------------------

if __name__ == "__main__":
    app.run(# host=os.environ.get("IP"),
            port=9001, # int(os.environ.get("PORT"))
            debug=False)