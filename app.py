
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
    html.H2('Hello World'),
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in ['LA', 'NYC', 'MTL']],
        value='LA'
    ),
    html.Div(id='display-value')
])

@app.callback(dash.dependencies.Output('display-value', 'children'),
              [dash.dependencies.Input('dropdown', 'value')])
def display_value(value):
    return 'You have selected "{}"'.format(value)

if __name__ == '__main__':
    app.run_server(debug=True)
