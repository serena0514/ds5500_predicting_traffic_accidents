#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author: Dachuan Zhang
"""
from datetime import datetime
import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
import numpy as np
import utils
import predict_for_city
import requests
from dash.dash_table import DataTable
import dash_bootstrap_components as dbc
import joblib
import sklearn

#Gets Geojson file for cholopleth
url = 'https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json'
response = requests.get(url)
counties_geojson = response.json()

# Process the IMPACT dataset
crash_data = pd.read_csv('crash_data.csv')

# Process date format to YYYY-MM-DD, time to H:MM
crash_data['Crash Date'] = pd.to_datetime(crash_data['Crash Date'],
                                          format='%m/%d/%y')
crash_data['Crash Date'] = crash_data['Crash Date'].dt.strftime('%Y-%m-%d')

crash_data['Crash Time'] = pd.to_datetime(crash_data['Crash Time'],
                                          format='%I:%M %p').dt.strftime('%H:%M')

crash_data['Crash Time'] = pd.to_datetime(crash_data['Crash Time'], format='%H:%M')

#if speed limit is null, fill as 25
crash_data['Speed Limit'] = crash_data['Speed Limit'].fillna(25)

"""
# This section processes the national data - MA/Boston
"""

ma_national = pd.read_csv('MA_US_Accidents_March23.csv')

county_counts = ma_national.groupby('County').agg({
    'Start_Lat': 'first',
    'Start_Lng': 'first',
    'County': 'count'
}).rename(columns={'County': 'record_count'}).reset_index()

county_to_fips = {
    'Barnstable': '25001',
    'Berkshire': '25003',
    'Bristol': '25005',
    'Dukes': '25007',
    'Essex': '25009',
    'Franklin': '25011',
    'Hampden': '25013',
    'Hampshire': '25015',
    'Middlesex': '25017',
    'Nantucket': '25019',
    'Norfolk': '25021',
    'Plymouth': '25023',
    'Suffolk': '25025',
    'Worcester': '25027'
}

county_counts['fips'] = county_counts['County'].map(county_to_fips)

# Process the Boston data
boston_national = pd.read_csv('Boston_US_Accidents_March23.csv')

boston_national['date'] = pd.to_datetime(boston_national['Start_Time'], format='%Y-%m-%d %H:%M:%S', errors='coerce')
boston_national['date'] = boston_national['date'].dt.strftime('%Y-%m-%d')

national_important_columns = [
    'ID', 'Severity', 'Start_Time', 'Start_Lat', 'Start_Lng',
    'Distance(mi)', 'Temperature(F)', 'Wind_Chill(F)', 'Humidity(%)', 'Pressure(in)',
    'Visibility(mi)', 'Wind_Direction', 'Wind_Speed(mph)',
    'Precipitation(in)', 'Weather_Condition', 'Amenity', 'Bump', 'Crossing',
    'Give_Way', 'Junction', 'No_Exit', 'Railway', 'Roundabout', 'Station',
    'Stop', 'Traffic_Calming', 'Traffic_Signal', 'Turning_Loop',
    'Sunrise_Sunset', 'Civil_Twilight', 'Nautical_Twilight',
    'Astronomical_Twilight', 'Crash']

final_data = pd.read_csv('final_data.csv')
final_data['City'] = final_data.apply(lambda row: utils.assign_city(row['Start_Lat'], row['Start_Lng']), axis=1)

fig = px.choropleth_mapbox(county_counts,
                           geojson=counties_geojson,
                           locations='fips',
                           featureidkey="id",
                           color='record_count',
                           color_continuous_scale="bluered",
                           hover_name='County',
                           hover_data=['record_count'],
                           mapbox_style="carto-positron",
                           zoom=7,
                           center={"lat": 42, "lon": -71},
                           opacity=0.5,
                           )

fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

#Make data table
columns_selected = ['Start_Time', 'Severity', 'Street', 'City', 'County', 'State', 'Weather_Condition']

crash_data_reduced = ma_national[columns_selected]
dt = DataTable(data=crash_data_reduced.to_dict('records'),
               columns=[{"name": i, "id": i} for i in crash_data_reduced.columns],
               sort_action='native',
               filter_action='native',
               page_current=0,
               page_size=13,
               page_action='native',
               style_cell=({
                   'textAlign': 'left'
               }),
               style_header=({
                   'background-color': 'black',
                   'color': 'white'
               }),
               column_selectable='single'
               )

app = dash.Dash(__name__)

app.layout = html.Div(
    children=[
        *utils.make_break(1),
        html.H2('Massachusetts/Boston Crash Locations'),
        *utils.make_break(1),

        # Option to select date range
        html.Div(
            children=[
                html.Div(dt,
                         style={'width': '1500px',
                                'height': '400px',
                                'margin': '10px auto',
                                'padding-right': '30px'}),
                *utils.make_break(4),
                html.B('Select Date'),
                *utils.make_break(2),
                dcc.DatePickerRange(
                    id="date_filter",
                    start_date=crash_data["Crash Date"].min(),
                    end_date=crash_data["Crash Date"].max(),
                    display_format="YYYY-MM-DD"
                ),
                *utils.make_break(2)
            ]),

        # Option to select which variable to color
        html.Div(
            children=[
                html.B('Select Coloring Variable'),
                *utils.make_break(2),
                dcc.Dropdown(
                    id='color-dropdown',
                    options=[
                        {'label': 'Light Conditions', 'value': 'Light Conditions'},
                        {'label': 'Crash Severity', 'value': 'Crash Severity'},
                        {'label': 'Weather Conditions', 'value': 'Weather Conditions'},
                        {'label': 'Speed Limit', 'value': 'Speed Limit'}
                    ],
                    value='Light Conditions'
                ),
                *utils.make_break(2)

            ],
            style={'width': '15%',
                   'margin': 'auto'}),

        html.Div([
            dcc.Input(
                id='town-search',
                type='text',
                placeholder='Search for a town',
            ),
            *utils.make_break(2),
            dcc.Dropdown(
                id='road_condition_selector',
                options=[
                    {'label': 'Wet', 'value': 'Wet'},
                    {'label': 'Dry', 'value': 'Dry'},
                    {'label': 'Ice', 'value': 'Ice'},
                    {'label': 'Snow', 'value': 'Snow'}
                ]
            ),
            *utils.make_break(4),
        ], style={'width': '15%',
                  'margin': 'auto'}),

        # Scatterplot map
        html.Div([
            dcc.Graph(id='graph',
                      style={'width': '1300px',
                             'height': '800px',
                             'margin': 'auto'}),
            *utils.make_break(2)
        ]),
        *utils.make_break(2),

        # Choropleth map
        html.Div(children=[
        html.B('Massachusetts Accident Counts'),
        *utils.make_break(2),
            dcc.Graph(id='ma_counties',
                      figure=fig,
                      style={'width': '1300px',
                             'height': '800px',
                             'margin': 'auto'}),
        ]),

        *utils.make_break(2),
        dcc.Store(id='predictions'),
        dbc.Col([
            html.Ul(id='selected_args'),
        ]),
        *utils.make_break(3),
        html.Button('Generate Priority List',
                    id='submit-button',
                    n_clicks=0),

        *utils.make_break(3),
        dbc.Col([
            html.Ul(id='priority_list'),
        ], style={'margin': 'auto'}),
        *utils.make_break(2),

    ],
    style={'text-align': 'center',
           'background-color': 'rgb(226, 255, 252)'})


@app.callback(
    Output('graph', 'figure'),
    Input('date_filter', 'start_date'),
    Input('date_filter', 'end_date'),
    Input('color-dropdown', 'value'),
    Input('town-search', 'value')
)
def update_map(start_date, end_date, selected_color, selected_town):
    if selected_town:
        filtered_crash_data = crash_data[(crash_data['Crash Date'] >= start_date) &
                                         (crash_data['Crash Date'] <= end_date) &
                                         crash_data['City Town Name'].str.contains(selected_town, case=False)]
    else:
        filtered_crash_data = crash_data[(crash_data['Crash Date'] >= start_date) &
                                         (crash_data['Crash Date'] <= end_date)]

    #Massachusetts speed limit
    color_range = [5, 65]

    fig = px.scatter_mapbox(data_frame=filtered_crash_data,
                            lat="Latitude",
                            lon="Longitude",
                            color=selected_color,
                            hover_name="City Town Name",
                            hover_data=["Crash Date", 'Crash Time'],
                            zoom=11,
                            range_color=color_range)

    fig.update_layout(mapbox_style="carto-positron")
    fig.update_layout(margin={"r": 1, "t": 0, "l": 1, "b": 0})

    return fig


@app.callback(
    Output('selected_args', 'children'),
    Output('predictions', 'data'),
    Input('date_filter', 'start_date'),
    Input('date_filter', 'end_date'),
    Input('road_condition_selector', 'value'),
    Input('town-search', 'value')


)
def update_args(start_date, end_date, road_condition, selected_town='Boston'):
    with open('random_forest_accident_likelihood_model.pkl', 'rb') as file:
        loaded_model = joblib.load(file)

    print("Model Load complete")
    dt = datetime.strptime(start_date, '%Y-%m-%d')

    print('Start Predictions')
    predictions = predict_for_city.predict_for_city(final_data,
                                   selected_town,
                                   road_condition,
                                   dt.month,
                                   dt.day,
                                   0,
                                   0,
                                   0)[['Start_Lat', 'Start_Lng', 'Severity']].sort_values('Severity', ascending=False).head(5)
    print("Prediction Complete")

    return (f'Start Date: {start_date}, '
            f'End Date: {end_date}, '
            f'Road Condition: {road_condition}, '
            f'Selected Town: {selected_town}.'), predictions


@app.callback(
    Output('priority_list', 'children'),
    Input('submit-button', 'n_clicks'),
    Input('predictions', 'data'),
    prevent_initial_call=True
)
def update_priority_list(n_clicks, data):
    predictions = pd.DataFrame(data)
    if n_clicks:
        return html.Ul([
            html.Li(f"Latitute: {row.Start_Lat}, Longitute: {row.Start_Lng}, Predicted Severity: {row.Severity}")
            for row in predictions.itertuples()
        ])


if __name__ == '__main__':
    app.run_server(debug=True, port=8003)
