# -*- coding: utf-8 -*-
"""
Created on Sat Jan  1 03:41:28 2022

@author: gohjh
"""


# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.io as pio
# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Get unique launch sites
uniqueLaunchSites = spacex_df['Launch Site'].unique().tolist()
LaunchSites = []
LaunchSites.append({'label': 'All Sites', 'value': 'ALL'})
for site in uniqueLaunchSites:
    LaunchSites.append({'label': site, 'value': site})
    
    
# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id='site-dropdown',
                                            options=LaunchSites,
                                            value='ALL',
                                            placeholder="Select a Launch Site here", 
                                            searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0,max=10000,step=1000,
                                                value=[min_payload,max_payload],
                                                marks={0: '0', 2500:'2500',5000:'5000',
                                                7500:'7500', 10000: '10000'}),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value'))

def piechart_graph(site_dropdown):
    if site_dropdown == 'ALL':
        piechart = px.pie(spacex_df, names='Launch Site', values='class', title='Total Launches for All Sites')
        return piechart
    else:
        filtered_df = spacex_df.loc[spacex_df['Launch Site'] == site_dropdown]
        piechart = px.pie(filtered_df, names='class', title='Total Launches from '+site_dropdown)
        return piechart
    
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
    Input(component_id='payload-slider', component_property='value')])

def scatterplot_graph(site_dropdown, payload_slider):
    low, high = payload_slider
    if site_dropdown == 'ALL':
        sel_range = (spacex_df['Payload Mass (kg)'] > low) & (spacex_df['Payload Mass (kg)'] < high)
        fig = px.scatter(
                spacex_df[sel_range], 
                x = "Payload Mass (kg)", 
                y = "class",
                title = 'Correlation between Payload and Success for all sites',
                color="Booster Version Category",
                size='Payload Mass (kg)',
                hover_data=['Payload Mass (kg)']
            )

    else:
        filtered_df = spacex_df.loc[spacex_df['Launch Site'] == site_dropdown]
        sel_range = (filtered_df['Payload Mass (kg)'] > low) & (filtered_df['Payload Mass (kg)'] < high)
        fig = px.scatter(
                filtered_df[sel_range],
                x = "Payload Mass (kg)",
                y = "class",
                title = 'Correlation between Payload and Success for Site '+site_dropdown,
                color="Booster Version Category",
                size='Payload Mass (kg)',
                hover_data=['Payload Mass (kg)']
            )
    
    return fig
    pio.write_html(fig, file='figure.html', auto_open=True)





# Run the app
if __name__ == '__main__':
    app.run_server()




