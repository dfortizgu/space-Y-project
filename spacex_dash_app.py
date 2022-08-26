# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

pie_fig = px.pie(spacex_df, values='Flight Number', names='Launch Site', title='% of launches by Launch Site')
plottt = dcc.Graph(figure = pie_fig)


# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id='site-dropdown',
                                                     options=[
                                                        {'label': 'All', 'value': "All"},
                                                        {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                        {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                                        {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                        {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}
                                                    ], 
                                                    placeholder = "Select launch site",
                                                    style = {"width" : "100%", "padding" : "3px", "font-size" : "20px", "textAlign" : "center"}
                                        ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div([ ],id='success-pie-chart'),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)

                                dcc.RangeSlider(min_payload, max_payload, value=[min_payload, max_payload], id='payload-slider'),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div([],id='success-payload-scatter-chart'),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

@app.callback( [Output(component_id = "success-pie-chart", component_property = "children")],
               [Input(component_id='site-dropdown', component_property='value')]
            )
def pie_plot(launch_site):
    if launch_site == "All":
        pie_fig = px.pie(spacex_df[spacex_df["class"] == 1], names='Launch Site', title='% of success launches by Launch Site')
        return [dcc.Graph(figure = pie_fig)]
    
    if launch_site != None:
        data = spacex_df[spacex_df["Launch Site"] == launch_site]
        pie_fig = px.pie(data, names='class', title=f'% of Succes for {launch_site}')
        #The callback function must return always a list
        return [dcc.Graph(figure = pie_fig)]    

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
    
@app.callback( [Output(component_id = "success-payload-scatter-chart", component_property = "children")],
               [Input(component_id='site-dropdown', component_property='value'),
                Input(component_id='payload-slider', component_property='value')]
            )
def scatter_plot(launch_site, payload_slider):
    min_payload_kg = payload_slider[0]
    max_payload_kg = payload_slider[1]
    if launch_site == "All":
        data = spacex_df[spacex_df["Payload Mass (kg)"].between(min_payload_kg, max_payload_kg, inclusive = True)]
        scatter_fig = px.scatter(data, x="Payload Mass (kg)", y="class", color="Launch Site", hover_data=['Launch Site'], title = "Succes vs Payload Mass for all Launch Site")
        return [dcc.Graph(figure = scatter_fig)]

    if launch_site != None:
        data = spacex_df[spacex_df["Payload Mass (kg)"].between(min_payload_kg, max_payload_kg, inclusive = True)]
        data = data[data["Launch Site"] == launch_site]
        scatter_fig = px.scatter(data, x="Payload Mass (kg)", y="class", hover_data=['Launch Site'], title = f"Succes vs Payload Mass for {launch_site}")
        return [dcc.Graph(figure = scatter_fig)]


# Run the app
if __name__ == '__main__':
    app.run_server()
