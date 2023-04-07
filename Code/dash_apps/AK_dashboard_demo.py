"""
Metadata

Title: AK_dashboard_demo
Author: Ami Kano
Date: January 28, 2023

Comments:

"""

from pymongo import MongoClient
import numpy as np
import pandas as pd
import queries_v1.queries_v1 as q1
from dash import dash_table as dt
from dash import Dash, html, dcc, Input, Output, State

table = pd.DataFrame(q1.query("George")[0])

#--------------------------------------------------------------

app = Dash()

#--------------------------------------------------------------

app.layout = html.Div([
    html.H1(
        children='OneSharedStory Search Dashboard',
        style={
            'textAlign': 'center',
            'color': 'black'
        }
    ), 
    html.Br(),
    html.H3("Search Type"),
    dcc.Dropdown(id = 'dropdown',
         options=[{'label': i, 'value': i} 
                  for i in ["Overall Search", "Name Search", "Location Search", "Date Search"]],
          multi=False,
                 placeholder = "Select type of search"
         ),
    html.H3("Search Term"),
    dcc.Input(id="term", placeholder="Enter search term ...", type="text"),
    html.Button('Search', id='button', n_clicks=0),
    html.Div(id='search-result')
    
    
])

#--------------------------------------------------------------

@app.callback(output= Output("search-result", "children"), 
              inputs=[Input("button", "n_clicks")], 
             state=[State("dropdown", "value"), 
                State("term", "value")])

#--------------------------------------------------------------

def result_table(n_clicks, dropdown, term):
    
    if n_clicks:
        """
        table = pd.DataFrame(q1.query(term)[0])

        if "Name" in dropdown:
            table = q1.name_query(term)[0]
        elif "Location" in dropdown:
            table = q1.location_query(term)[0]
        elif "Date" in dropdown:
            table = q1.date_query(term)[0]
        else:
            table = q1.query(term)[0] 
    
        data = table.to_dict()
        columns = [{"name": i, "id": i,} for i in (table.columns)]
        """

        return "You selected " + dropdown + " and searched for " + term + ". \n Search Dashboard still in development."

#--------------------------------------------------------------

if __name__ == '__main__':
    app.run_server(debug=True, port=8051)
