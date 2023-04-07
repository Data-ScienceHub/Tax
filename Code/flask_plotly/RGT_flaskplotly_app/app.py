from flask import Flask, config, render_template, request
import pandas as pd
import json
import plotly
import plotly.express as px
import numpy as np

app = Flask(__name__)

@app.route('/callback', methods=['POST', 'GET'])
def cb():
    return gm(request.args.get('data'))
   
@app.route('/')
def index():
    return render_template('chartsajax.html',  graphJSON=gm())

def gm(EventLocJurisdictionCounty='Fluvanna'):
#def gm():
    df = pd.read_csv('Tax_1867_Cleaned.csv')
    
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

# TO DO:
# - add CSS styling to the HTML for visuals, adding descriptions, etc.
# - fix callback function, add functionality for exploration and changing other graphs
# - look into adding interactivity with graphs