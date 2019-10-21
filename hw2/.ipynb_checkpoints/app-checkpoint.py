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

def growth_from_prev(ser):
    if ser.dtype != int and ser.dtype != float:
        return ser
    shifted = ser.shift(1)
    change = ser - shifted
    change_per = (change/ser) * 100
    return change_per.fillna(0)

def diff_from_mean(ser):
    if ser.dtype != int and ser.dtype != float:
        return ser
    avg = ser.mean()
    stf = ser.std() #for z-score if wanted, easier for CEO to understand difference
    dev = (ser - avg)
    return dev

monthly_change = monthly.apply(growth_from_prev)

total_sales = monthly.sum(axis = 1).to_frame('Total Sales')
total_sales['Month, Year'] = monthly['Month, Year']
total_sales = total_sales[['Month, Year', 'Total Sales']]

hm_cols = [col for col in monthly.columns if 'HM' in col]
hm_sales = monthly[hm_cols].sum(axis = 1).to_frame('HM Sales')

cf_cols = [col for col in monthly.columns if 'CF' in col]
cf_sales = monthly[cf_cols].sum(axis = 1).to_frame('CF Sales')

ff_cols = [col for col in monthly.columns if 'FF' in col]
ff_sales = monthly[ff_cols].sum(axis = 1).to_frame('FF Sales')

total_sales['Total Sales Diff'] = total_sales[['Total Sales']].apply(diff_from_mean)
total_sales['Hamburger Sales'] = hm_sales
total_sales['Hamburger Sales Diff'] = hm_sales.apply(diff_from_mean)
total_sales['Chicken Sales'] = cf_sales
total_sales['Chicken Sales Diff'] = cf_sales.apply(diff_from_mean)
total_sales['Fish Sales'] = ff_sales
total_sales['Fish Sales Diff'] = ff_sales.apply(diff_from_mean)

inflection = total_sales.iloc[19:]

daily_sales = daily.groupby('Day of Week').sum()
daily_sales['Hamburgers'] = daily_sales[hm_cols].sum(axis = 1)
daily_sales['Chicken'] = daily_sales[cf_cols].sum(axis = 1)
daily_sales['Fish'] = daily_sales[ff_cols].sum(axis = 1)
daily_sales = daily_sales.reset_index()

daily_per = daily_sales[['Hamburgers', 'Chicken', 'Fish']].apply(lambda x: (x/x.sum()) * 100, axis = 1)
daily_avg = daily_per.mean().to_frame('Percentage of Total Sales')

monthly_per = total_sales[['Hamburger Sales', 'Chicken Sales', 'Fish Sales']].apply(lambda x: (x/x.sum()) * 100, axis = 1)
monthly_avg = monthly_per.mean().to_frame('Percentage of Total Sales')

######################

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(
        children= "They're (Still Kinda) Lovin' It: McDonalds Sales Report",
        style={
            'textAlign': 'center'
        }
    ),
    html.Div([html.H3('Recovering from the Impossible (Burger)')], style={
        'textAlign': 'center',
    }),
    html.Div([dcc.Link('DOWNLOAD REPORT', href='/')],
              style={
                  'textAlign': 'center',
                  'font-size': '24px'
    }),
        html.Div([
        html.Div([dcc.Graph(
        id='MonthlySales',
        figure={
            'data': [
                {'x': inflection['Month, Year'], 'y': inflection['Total Sales'], 'type': 'line', 'name': 'Total Sales'},
                {'x': inflection['Month, Year'], 'y': inflection['Hamburger Sales'], 'type': 'line', 'name': 'Hamburger Sales'},
                {'x': inflection['Month, Year'], 'y': inflection['Chicken Sales'], 'type': 'line', 'name': 'Chicken Sales'},
                {'x': inflection['Month, Year'], 'y': inflection['Fish Sales'], 'type': 'line', 'name': 'Fish Sales'}
            ],
            'layout': {
                    'title': 'Monthly Sales',
                    'xaxis': {'title': 'Date'},
                    'yaxis': {'title': 'Average Monthly Sales (USD)'}
                }
        },
        config={
			'staticPlot': True,
            }
    )], className = 'six columns'),
        html.Div([dcc.Graph(
        id='TotalDiff',
        figure={
            'data': [
                {'x': inflection['Month, Year'], 'y': inflection['Total Sales Diff'], 'type': 'bar', 'name': 'Total Change'},
                {'x': inflection['Month, Year'], 'y': inflection['Hamburger Sales Diff'], 'type': 'bar', 'name': 'Hamburger Change'},
                {'x': inflection['Month, Year'], 'y': inflection['Chicken Sales Diff'], 'type': 'bar', 'name': 'Chicken Change'},
                {'x': inflection['Month, Year'], 'y': inflection['Fish Sales Diff'], 'type': 'bar', 'name': 'Fish Change'}
            ],
            'layout': {
                    'title': 'Back to Basics: Monthly Difference from Average Sales',
                    'xaxis': {'title': 'Date'},
                    'yaxis': {'title': 'Difference from Average Sales Gross (USD)'}
                }
        },
        config={
			'staticPlot': True,
            }
    )], className = 'six columns')
    ], className = 'row'),
    html.Div([
       html.Div([dcc.Graph(id='dailyPer',
                           figure=go.Figure(
                               data=[go.Pie(labels=daily_avg.index,
                                            values=daily_avg['Percentage of Total Sales'])],
                               layout=go.Layout(
                                   title='Tried and True: Daily Sales Breakdown')
                           ),
                          config={
                                   'staticPlot': True,
                               })], className="six columns"),
        html.Div([dcc.Graph(id='monthlyPer',
                           figure=go.Figure(
                               data=[go.Pie(labels=monthly_avg.index,
                                            values=monthly_avg['Percentage of Total Sales'])],
                               layout=go.Layout(
                                   title='Same Old Same Old: Monthly Sales Breakdown')
                           ),
                           config={
                                   'staticPlot': True,
                               })], className="six columns")
    ], className="row"),
    html.Div([
        html.Div([dcc.Graph(
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
                    'title': 'Burgers Make Bucks: Monthly Hamburger Sales',
                    'xaxis': {'title': 'Date'},
                    'yaxis': {'title': 'Sales in Millions (USD)'}
                }
        },
        config={
			'staticPlot': True,
            },
    )]),
        html.Div([dcc.Graph(
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
                    'title': 'Flightless Sales: Monthly Chicken Filet Sales',
                    'xaxis': {'title': 'Date'},
                    'yaxis': {'title': 'Sales in Thousands (USD)'}
                }
        },
        config={
			'staticPlot': True,
            }
    )]),
        html.Div([dcc.Graph(
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
                    'title': 'Fish Out of Water: Monthly Fish Filet Sales',
                    'xaxis': {'title': 'Date'},
                    'yaxis': {'title': 'Sales in Thousands (USD)'}
                }
        },
        config={
			'staticPlot': True,
            }
    )])
    ], className = 'row'),
    html.Div([
        html.Div([dcc.Graph(
        id='Dailys',
        figure={
            'data': [
                {'x': daily_sales['Day of Week'], 'y': daily_sales['Hamburgers'], 'type': 'line', 'name': 'Hamburgers'},
                {'x': daily_sales['Day of Week'], 'y': daily_sales['Chicken'], 'type': 'line', 'name': 'Chicken'},
                {'x': daily_sales['Day of Week'], 'y': daily_sales['Fish'], 'type': 'line', 'name': 'Fish'}
            ],
            'layout': {
                    'title': 'Daily Duty: Daily Sales',
                    'xaxis': {'title': 'Day of Week'},
                    'yaxis': {'title': 'Average Daily Sales (USD)'}
                }
        },
        config={
			'staticPlot': True,
            }
    )], className = 'nine columns'),
        html.Div([html.Img(src = 'https://github.com/ck-duong/dsc106/blob/master/hw2/imgs/peak_weak.png?raw=true')], className = 'three columns')
             ], className = 'row')
])

@app.server.route('/download') 
def download():
    return send_file('ceo.pdf',
                     attachment_filename='ceo.pdf',
                     as_attachment=True)

if __name__ == '__main__':
    app.run_server(debug=True)