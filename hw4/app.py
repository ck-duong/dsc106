#imports for website dev/plotting
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.express as px

from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
%matplotlib inline

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

text = rachel_df['plot'].str.cat(sep=' ').lower()
text = text.replace(':', '').replace('-', '').replace(',','').replace('.', '').strip(' ').replace('"', '').replace("'", '')

words = pd.Series(text.split(' ')).value_counts()
words = words.loc[~words.index.isin(stopwords)]
words = words[words.index != '']
words = words.to_frame('count').reset_index().rename({'index': 'word'}, axis = 1)
words['rank'] = words.index + 1
words = words[['rank', 'word', 'count']]

tab = go.Figure(data=[go.Table(
    header=dict(values=list(words.columns),
                align='left'),
    cells=dict(values=[words['rank'], words['word'], words['count']],
               align='left'))
])

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
    html.Div(children = [
        html.H3('table and cloud'),
        html.Img('wordcloud.png')
        dcc.Graph(figure = tab),
        html.P('text decr')
    ]),
])

if __name__ == '__main__':
    app.run_server(debug=True)