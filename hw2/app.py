#imports for website dev
import dash
import dash_core_components as dcc
import dash_html_components as html
from flask import send_file

#imports for reading csv/plotting
import pandas as pd
import numpy as np
import plotly.graph_objs as go

#other imports
import os
import datetime

daily_data_path = os.path.join('data', 'daily_sales.csv')
monthly_data_path = os.path.join('data', 'monthly_sales.csv')

daily = pd.read_csv(daily_data_path)
monthly = pd.read_csv(monthly_data_path)

daily = daily.rename(columns = {'Unnamed: 0': 'Day of Week'})

daily['Day of Week'] = pd.Categorical(daily['Day of Week'], categories=
    ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday', 'Sunday'],
    ordered=True)

regions = ['NE', 'NW', 'SE', 'SW', 'C']
food = ['HM', 'CF', 'FF']

avgs = daily.groupby('Day of Week').apply(np.mean)

regional = avgs.T
regional.index = [regional.index.str[:2], regional.index.str[3:]]
regional = regional.rename_axis(("food", "region"))
regional.sort_index(inplace = True)

######################

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(
        children= "They're (Not Really) Lovin' It: McDonalds Sales Report",
        style={
            'textAlign': 'center'
        }
    ),
    html.Div([html.H3('How to recover from the Impossible (Burger)')], style={
        'textAlign': 'center',
    }),
    html.Div([dcc.Link('DOWNLOAD REPORT', href='/')],
              style={
                  'textAlign': 'center',
                  'font-size': '24px'
    }),
    dcc.Graph(
        id='MonthlyBurgerSales',
        figure={
            'data': [
                {'x': monthly['Month, Year'], 'y': monthly['HM-NE'], 'type': 'line', 'name': 'North East'},
                {'x': monthly['Month, Year'], 'y': monthly['HM-NW'], 'type': 'line', 'name': 'North West'},
                {'x': monthly['Month, Year'], 'y': monthly['HM-SE'], 'type': 'line', 'name': 'South East'},
                {'x': monthly['Month, Year'], 'y': monthly['HM-SW'], 'type': 'line', 'name': 'South West'},
                {'x': monthly['Month, Year'], 'y': monthly['HM-C'], 'type': 'line', 'name': 'Central'},
            ],
            'layout': {
                    'title': 'Monthtly Hamburger Sales',
                    'xaxis': {'title': 'Date'},
                    'yaxis': {'title': 'Sales in Millions (USD)'}
                }
        },
        config={
			'staticPlot': True,
            },
        style={"width" : '150vh'}
    ),
    dcc.Graph(
        id='MonthlyChickenSales',
        figure={
            'data': [
                {'x': monthly['Month, Year'], 'y': monthly['CF-NE'], 'type': 'line', 'name': 'North East'},
                {'x': monthly['Month, Year'], 'y': monthly['CF-NW'], 'type': 'line', 'name': 'North West'},
                {'x': monthly['Month, Year'], 'y': monthly['CF-SE'], 'type': 'line', 'name': 'South East'},
                {'x': monthly['Month, Year'], 'y': monthly['CF-SW'], 'type': 'line', 'name': 'South West'},
                {'x': monthly['Month, Year'], 'y': monthly['CF-C'], 'type': 'line', 'name': 'Central'},
            ],
            'layout': {
                    'title': 'Monthtly Chicken Filet Sales',
                    'xaxis': {'title': 'Date'},
                    'yaxis': {'title': 'Sales in Millions (USD)'}
                }
        },
        config={
			'staticPlot': True,
            }
    ),
    dcc.Graph(
        id='MonthlyFishSales',
        figure={
            'data': [
                {'x': monthly['Month, Year'], 'y': monthly['FF-NE'], 'type': 'line', 'name': 'North East'},
                {'x': monthly['Month, Year'], 'y': monthly['FF-NW'], 'type': 'line', 'name': 'North West'},
                {'x': monthly['Month, Year'], 'y': monthly['FF-SE'], 'type': 'line', 'name': 'South East'},
                {'x': monthly['Month, Year'], 'y': monthly['FF-SW'], 'type': 'line', 'name': 'South West'},
                {'x': monthly['Month, Year'], 'y': monthly['FF-C'], 'type': 'line', 'name': 'Central'},
            ],
            'layout': {
                    'title': 'Monthtly Fish Filet Sales',
                    'xaxis': {'title': 'Date'},
                    'yaxis': {'title': 'Sales in Millions (USD)'}
                }
        },
        config={
			'staticPlot': True,
            }
    )
])

@app.server.route('/download') 
def download():
    return send_file('ceo.pdf',
                     attachment_filename='ceo.pdf',
                     as_attachment=True)

if __name__ == '__main__':
    app.run_server(debug=True)