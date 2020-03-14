
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import re
import plotly.express as px
from dash.dependencies import Input, Output
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
competitor_data=pd.read_csv('competitors_data.csv')
competitor_data.drop(columns=['Unnamed: 0'],inplace=True)
competitor_data.reset_index(drop=True,inplace=True)
competitor_data = competitor_data[['homestay_name', 'area','region','place', 'price', 'amenities']]
competitor_data.area=competitor_data.area.apply(lambda x:x.strip())
competitor_data.region=competitor_data.region.apply(lambda x:x.strip())
competitor_data.place=competitor_data.place.apply(lambda x:x.strip())
competitor_data.price=competitor_data.price.apply(lambda x:re.sub('[^0-9]','',x))
competitor_data.price=competitor_data.price.apply(lambda x:int(x))
# data cleaning trip thrills
trip_thrills_data=pd.read_csv('homestays_trip_thrills.csv')
trip_thrills_data.area=trip_thrills_data.area.fillna('unknown')
trip_thrills_data.area=trip_thrills_data.area.apply(lambda x:x.strip())
trip_thrills_data.region=trip_thrills_data.region.fillna('unknown')
trip_thrills_data.region=trip_thrills_data.region.apply(lambda x:x.strip())
# data for area histogram competitor
data_for_histogram=competitor_data.region.value_counts().reset_index()
data_for_histogram=data_for_histogram[data_for_histogram['index'].isin(['north goa','south goa','unknown'])]
data_for_histogram.sort_values(['index'],inplace=True)
data_for_histogram_area=competitor_data.area.value_counts().reset_index()
data_for_histogram_area=data_for_histogram_area[data_for_histogram_area['index']!='unknown']

data_for_histogram_trip_thrills=trip_thrills_data.region.value_counts().reset_index()
data_for_histogram_trip_thrills.loc[2]=['unknown',0]
data_for_histogram_trip_thrills.sort_values(['index'],inplace=True)
data_for_histogram_area_trip_thrills=trip_thrills_data.area.value_counts().reset_index()

data_for_plotting_histogram_area=data_for_histogram_area[0:5]
data_for_plotting_histogram_area_trip=data_for_histogram_area_trip_thrills[0:5]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

app.layout = html.Div([
                       html.H1('Basic Info',style={'textAlign': 'center','overflow':'hidden',
  'background-color':'#1F77b4',
  'color':'#FFFFFF',
  'padding': '20px 20px'
}), html.Hr(),
html.Div([
    dcc.Graph(
            id='region_details',
            style={'display': 'inline-block','width':'33%'},
            figure={
            'data': [
                {'x':list(data_for_histogram['index']), 'y': data_for_histogram.region, 'type': 'bar', 'name': 'Competitors'},
                {'x':list(data_for_histogram_trip_thrills['index']), 'y': data_for_histogram_trip_thrills.region, 'type': 'bar', 'name': 'Trip Thrills'},
            ],
            'layout': {
                'title': 'Hotel Count Region-Wise'
            }
        }
            )
     , dcc.Graph(
             id='area_details_comp',
             style={'display': 'inline-block','width':'33%'},
             figure={
             'data': [
                 {'x':list(data_for_plotting_histogram_area['index']), 'y': data_for_plotting_histogram_area.area, 'type': 'bar', 'name': 'Area'}
                 
             ],
             'layout': {
                 'title': 'Hotel Count Area-Wise Competitors'
             }
         }
             ),
   dcc.Graph(
             id='area_details_trip',
             style={'display': 'inline-block','width':'33%'},
             figure={
             'data': [
                 {'x':list(data_for_plotting_histogram_area_trip['index']), 'y': data_for_plotting_histogram_area_trip.area, 'type': 'bar', 'name': 'Area'}
                 
             ],
             'layout': {
                 'title': 'Hotel Count Area-Wise Trip Thrills'
             }
         }
             )])
    ,
    html.Br(),
    dcc.Graph(
            id='hist',
            figure=px.histogram(competitor_data, x="price",title='Price variation competitor',color_discrete_sequence=['#1F77b4']),
            
             )
    ,
    html.Br(),
    dcc.Graph(
            id='hist_trip_thrills',
            figure=px.histogram(trip_thrills_data, x="price",title='Price variation Trip Thrills',color_discrete_sequence=['#1F77b4']),
            
             )
    ,
#html.Div([dcc.Dropdown(
#        id='region',
#        options=[
#            {'label': i.capitalize(), 'value':i} for i in competitor_data.region.unique()       
#        ],
#        searchable=False,
#        value=[],
#        placeholder="Select a region",
#        multi=True
#    ,style={'display': 'inline-block','width':'50%'}),
#    dcc.Dropdown(
#        options=[
#            {'label': i.capitalize(), 'value':i} for i in competitor_data.area.unique()       
#        ],
#        searchable=False,
#        value=[],
#        placeholder="Select an area",
#        multi=True
#    ,style={'display': 'inline-block','width':'50%'})]),
#    html.Br(), 
#    html.Label('Price Range',style={'fontWeight': 'bold'}),
#    
#    html.Br(),
#    html.Br(),
#    
#    dcc.RangeSlider(
#        id='price_slider',
#        min=competitor_data.price.min(),
#        max=competitor_data.price.max(),
#        value=[competitor_data.price.min(),competitor_data.price.max()],
#        marks={
#        int(competitor_data.price.min()): {'label':'', 'style': {'color': '#77b0b1'}},
#        5000: {'label': 'Budget','style': {'color': '#0B6623'}},
#        15000: {'label': 'Standard','style': {'color': '#FFA500'}}, 
#        int(competitor_data.price.max()): {'label':'Luxury', 'style': {'color': '#D21F3C'}}},
#    ),
#    html.Br(),
    html.Div(id='graph_area_wise'),
    html.H3('Competitors Data',style={'textAlign': 'center'
}),
    dash_table.DataTable(
    id='table',
    columns=[{"name": i.capitalize(), "id": i} for i in competitor_data.columns],
    data=competitor_data.to_dict('records'),
    style_cell={
        'overflow': 'hidden',
        'textOverflow': 'ellipsis',
        'maxWidth': 0,
    },
    style_cell_conditional=[
         {'if': {'column_id': 'homestay_name'},
         'width': '20%'},
        {'if': {'column_id': 'amenities'},
         'width': '40%'},
        {'if': {'column_id': 'area'},
         'width': '10%','textAlign': 'center'},
        {'if': {'column_id': 'region'},
         'width': '10%','textAlign': 'center'},
         {'if': {'column_id': 'place'},
         'width': '10%','textAlign': 'center'},
          {'if': {'column_id': 'price'},
         'width': '10%','textAlign': 'center'}
    ],
    style_data_conditional=[
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(248, 248, 248)'
        }
    ],
    style_header={
        'backgroundColor': '#1F77b4',
        'fontWeight': 'bold',
         'fontSize': 16,
         'color':'white',
         'textAlign': 'center'
         
    },
    editable=True,
    filter_action="native",
    sort_action="native",
    sort_mode="multi",
    column_selectable="single",
    row_selectable="multi",
    row_deletable=True,
    selected_columns=[],
    selected_rows=[],
    page_action="native",
    page_current= 0,
    page_size= 10,
),
html.Br(),
html.Br(),

html.Hr()
    ])



if __name__ == '__main__':
    app.run_server(debug=True)
