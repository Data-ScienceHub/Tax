"""
Metadata

Title: dash
Author: Ami Kano
Date: March 31, 2023

Comments:
- Issues:
  - Plots may not work depending on combination of inputs. May have to hardcode numerous if statements. 
  - Search result may stop working if only one column is selected for display.
  - Query takes a long time / crashes the application. This has been temporarily mitigated by limiting the number of outputted rows to 20.
- Areas for Improvement:
  - Need to figure out how to connect the two outputs (May not be neccessary if we are moving onto Flask)
  - There is no systematic way to group the columns by datatype. This has been hardcoded. 

"""

import numpy as np
import pandas as pd
from pymongo import MongoClient
import plotly.graph_objects as go
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import dash
from dash import dcc, html, dash_table as dt
from dash.dependencies import Input, Output, State

#--------------------------------------------------------------

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
    
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server # this needs to be commented out if you run on AWS - IanL

#--------------------------------------------------------------

# URI is specific to Ami's login credentials
uri = "mongodb+srv://DS6013_Students_Ami:DS6013_Students_AK@countyrecords.4cdfgz2.mongodb.net/?retryWrites=true&w=majority"

# connect to database
client = MongoClient(uri)
database = client['TaxRecords']

data_dict = pd.DataFrame(list(database['Data_Dict'].find()))
dict_fig = ff.create_table(data_dict[["Column", "Data Type", "Description"]])

data = pd.DataFrame(list(database['Tax_Record_1867'].find()))

cat_col=['EventDateYear',
            'EventImageLink',
            'EventLocJurisdictionCounty',
            'EventTitle',
            'PersonEventRole',
            'PersonGivenNames',
            'PersonNameAlternate',
            'PersonNameSuffix',
            'PersonRoleGivenNamesEmployer',
            'PersonRoleLocResidence',
            'PersonRoleLocSurnameEmployer',
            'PersonSurname',
            'PersonTaxCommissionerRemarks',
            'SourceAuthorName',
            'SourceCreator',
            'SourceDateYearCreated',
            'SourceLocCity',
            'SourceLocCreatedCounty',
            'SourceLocState',
            'SourceSteward',
            'SourceTitle',
            'SourceType',
            '_id', 'none']
num_col=['PersonTaxCountCarriageWagon',
                'PersonTaxCountCattle',
                'PersonTaxCountClocks',
                'PersonTaxCountHogs',
                'PersonTaxCountHorsesMules',
                'PersonTaxCountMusicalInstruments',
                'PersonTaxCountNMalesover16',
                'PersonTaxCountSheep',
                'PersonTaxCountWMalesover16',
                'PersonTaxCountWatches',
                'PersonTaxLeviedLand',
                'PersonTaxStateAll',
                'PersonTaxTotalCountyValue',
                'PersonTaxValueAggregatePersonlProperty',
                'PersonTaxValueCarriageWagon',
                'PersonTaxValueCattle',
                'PersonTaxValueClocks',
                'PersonTaxValueFurnishings',
                'PersonTaxValueHogs',
                'PersonTaxValueHorsesMules',
                'PersonTaxValueJewelry',
                'PersonTaxValueMusicalInstruments',
                'PersonTaxValueSheep',
                'PersonTaxValueWatches',
                'PersonsTaxedCountNMalesover21',
                'PersonsTaxedCountWMalesover21']

col = data.columns

for column in num_col:
    data[column] = data[column].replace(r'^\s*$', 0, regex=True).replace(np.nan, 0, regex=True).fillna(0)
    data[column] = data[column].astype(float)

#--------------------------------------------------------------

app.layout = html.Div([
    html.H1(
        children='DataViz Dashboard',
        style={
            'textAlign': 'center',
            'color': 'black'
        }
    ), 
    html.Br(),
    html.Div([
        html.H4("X-Value"),
        dcc.Dropdown(id = 'var_1',
             options=[{'label': i, 'value': i} 
                      for i in col],
              multi=False,
              value='PersonTaxLeviedLand'
             ),
        html.H4("Y-Value"),
        dcc.Dropdown(id = 'var_2',
             options=[{'label': i, 'value': i} 
                      for i in col],
             multi=False,
             value='PersonTaxValueAggregatePersonlProperty'
        ),
        html.H4("Third Variable (Group)"),
        dcc.Dropdown(id = 'var_3',
             options=[{'label': i, 'value': i} 
                      for i in cat_col],
             multi=False,
             value="none"
             )],
        style={'width': '49%', 'display': 'inline-block', 'float': 'left'}),
    html.Div([
        html.H4("Figure Type"),
        dcc.Dropdown(id = 'fig_type',
             options=[{'label': 'tab', 'value': 'tab'}, 
                      {'label':'bar', 'value':'bar'},
                     {'label':'scatter', 'value':'scatter'}],
             multi=False,
             value='scatter'
             ),
        html.H4("Aggregate Function"),
        dcc.Dropdown(id = 'agg_func',
             options=[{'label': 'mean', 'value': 'mean'}, 
                      {'label':'median', 'value':'median'},
                     {'label':'count', 'value':'count'},
                     {'label':'sum', 'value':'sum'},
                     {'label':'none', 'value':'none'}],
             multi=False,
             value='none'
             )
    ], 
        style={'width': '49%', 'display': 'inline-block', 'float': 'right'}),
    html.Br(),
    html.Div([
        dcc.Graph(id='result')  
    ], style={'width':'90%','display': 'inline-block', 'float': 'center'}),
    
    html.Br(), #-----------Search Aspect
    
    html.H1(
        children='Search Dashboard',
        style={
            'textAlign': 'center',
            'color': 'black'
        }
    ), 
    html.Div([
        html.H4("Given Name"),
        dcc.Input(id="given_name", type="text"),
        html.H4("Surname"),
        dcc.Input(id="surname", type="text"),
        html.H4("Select Columns to Display"),
        dcc.Dropdown(id = 'chosen_col',
             options=[{'label': i, 'value': i} 
                      for i in col],
             multi=True,
             value=['_id', 'EventDateYear']
             )
        ],
        style={'width': '49%', 'display': 'inline-block', 'float': 'left'}),
    html.Div([
        html.H4("From Year:"),
        dcc.Input(id="date_range_0", type="text"),
        html.H4("To Year:"),
        dcc.Input(id="date_range_1", type="text"),
        html.H4("Location"),
        dcc.Input(id="location", type="text")
    ], 
        style={'width': '49%', 'display': 'inline-block', 'float': 'right'}),
    html.Div([
        dcc.Graph(id='search_result')  
    ], style={'width':'90%','display': 'inline-block', 'float': 'center'}),
    
    html.Br(), #-----------Data Dict
    html.Br(),
    
    html.H1(
        children='Data Dictionary',
        style={
            'textAlign': 'center',
            'color': 'black'
        }
    ),    
    html.Div([
        dcc.Graph(figure=dict_fig)
    ], style={'width':'90%','display': 'inline-block', 'float': 'center'})
    
])

#--------------------------------------------------------------

@app.callback(output= Output("result", "figure"), 
              inputs=[Input("var_1", "value"),
                      Input("var_2", "value"),
                      Input("fig_type", "value"),
                      Input("agg_func", "value"),
                      Input("var_3", "value")])

#--------------------------------------------------------------

def update_graph(var1, var2, fig_type, agg_func, var_3):
    
    
    if agg_func != "none":
        new_data = data.groupby(var1)\
                .agg({var2:agg_func})\
                .reset_index()
        if var_3 != "none":
            new_data = data.groupby([var1, var_3])\
                    .agg({var2:agg_func})\
                    .reset_index()
    else:
        if var_3 != "none":
            new_data = data[[var1, var2, var_3]]
        else:
            new_data = data[[var1, var2]]
    
    if fig_type=="tab":
        fig=ff.create_table(new_data)
    elif fig_type=="bar":
        if var_3 != "none":
            fig = px.bar(new_data, x=var1, y=var2, color=var_3,
                         hover_name=var2,
                        height=600, width=1000)
        else:
            fig = px.bar(new_data, x=var1, y=var2, 
                         hover_name=var2,
                        height=600, width=1000)
    elif fig_type=="scatter":
        if var_3 != "none":
            fig = px.scatter(new_data, x=var1, y=var2, color=var_3,
                     hover_data=[var1, var2, var_3],
                     height=600, width=1000)
        else:
            fig = px.scatter(new_data, x=var1, y=var2, 
                     hover_data=[var1, var2],
                     height=600, width=1000)
    
    return fig

#--------------------------------------------------------------

@app.callback(output= Output("search_result", "figure"), 
              inputs=[Input("given_name", "value"),
                      Input("surname", "value"),
                      Input("date_range_0", "value"),
                      Input("date_range_1", "value"),
                      Input("location", "value"),
                      Input("chosen_col", "value")])

#--------------------------------------------------------------

def query(given_name, surname, date_range_0, date_range_1, location, chosen_col):

    if date_range_0 != None and date_range_1 != None:
        date_range_0 = int(date_range_0)
        date_range_1 = int(date_range_1)
        date_range = [date_range_0, date_range_1]
    else:
        date_range = []

    # SEARCH FUNCTION
    #----------------------------------------------

    # get column names
    keys = database['Tax_Record_1867'].find_one()

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
        output = pd.DataFrame(list(database["Tax_Record_1867"].find().limit(5)))[chosen_col]
    elif pd.DataFrame(list(database["Tax_Record_1867"].find(query))).empty:
        output = pd.DataFrame(columns=list(database['Tax_Record_1867'].find_one().keys()))[chosen_col]
    else:
        output = pd.DataFrame(list(database["Tax_Record_1867"].find(query).limit(20)))[chosen_col]

    #----------------------------------------------
    # END SEARCH FUNCTION
    
    fig2 = ff.create_table(output)
    
    return fig2


if __name__ == '__main__':
    app.run_server(debug=True, port=8051)
