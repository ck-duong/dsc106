#imports for website dev/plotting
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.express as px

#imports for data + manipulation
import pandas as pd
import numpy as np
import imdb
from bs4 import BeautifulSoup
import requests
import re

#other imports
import os

####

rachel_df = pd.read_csv('https://raw.githubusercontent.com/ck-duong/dsc106/master/hw4/rachel.csv', index_col = 0)

countries = rachel_df.groupby('year')['countries'].sum()
countries = countries.reset_index()
yearly = countries['countries'].apply(lambda x: pd.Series(x).value_counts()).fillna(0)
yearly['year'] = countries.year
country_df = pd.melt(yearly, 'year').rename({'variable': 'Country', 'value': 'Movie Count', 'year': 'Year'}, axis = 1)
country_df = country_df.loc[country_df['Movie Count'] > 0].sort_values('Year').reset_index(drop = True)

chlor_map = px.choropleth(country_df, locations =  'Country', locationmode = 'country names', color = 'Movie Count', 
             animation_frame="Year")

dropped = rachel_df.dropna(subset = ['domestic', 'international'])\
[['original title', 'year', 'domestic', 'international', 'total']]

grouped = dropped.groupby('year')[['domestic', 'international', 'total']].sum().reset_index().sort_values('total')

labels = grouped['year'].tolist()
parents = ['Rachel Weisz Movies' for x in labels]
values = grouped['total'].tolist()

labels.append('Rachel Weisz Movies')
parents.append('')
values.append(grouped['total'].sum())

def divide_gross(row):
    total = row['total']
    title = row['original title']
    parent = row['year']
    
    labels.append(title)
    parents.append(parent)
    values.append(total)

dropped.apply(divide_gross, axis = 1)

tree = go.Figure(go.Treemap(
    labels = labels,
    parents = parents,
    values = values,
    branchvalues = 'total',
    textinfo = "label+value+percent parent",
))

####

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children = [
    html.H1(children = "Rachel Weisz Movies",
           style={
            'textAlign': 'center'
        }),
    html.P("text descritiopn and stuff"),
    html.Div(children = [
        html.H3('map'),
        dcc.Graph(figure = chlor_map),
        html.P('text decr')
    ]),
    html.Div(children = [
        html.H3('tree'),
        dcc.Graph(figure = tree),
        html.P('text decr')
    ]),
])

if __name__ == '__main__':
    app.run_server(debug=True)