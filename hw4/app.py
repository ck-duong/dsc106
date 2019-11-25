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


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([dcc.Graph(figure = fig)])

if __name__ == '__main__':
    app.run_server(debug=True)