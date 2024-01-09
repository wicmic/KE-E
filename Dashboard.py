#LIBRARIES
import pandas as pd
from dash import Dash, dcc, html, dash_table, Input, Output
import dash_bootstrap_components as dbc
import folium
#_______________________________________________________________________________________________________________________

#DATA

from RDF_Study_pickeln import pickeln_data_from_wikidata

fhgr = pd.read_csv("D:/Studium/3_HS 2023/KE and E/Projekt/masterstudiengang_base_fhgr.csv")
fhnw = pd.read_csv("D:/Studium/3_HS 2023/KE and E/Projekt/masterstudiengang_base_fhnw.csv")

#_______________________________________________________________________________________________________________________

# FUNKTIONEN
#Karte
def create_university_map():
    data_all = pickeln_data_from_wikidata()
    data = data_all.iloc[[9, 67]]

    start_location = (47.36667, 8.55) #Zürich
    university_map = folium.Map(location=start_location, zoom_start=7)

    for index, row in data.iterrows():
        if row['location_coordinates']:
            lon, lat = map(float, row['location_coordinates'][6:-1].split(' '))

            marker_location = (lat, lon)
            marker_objects = folium.Marker(
                location=marker_location,
                icon=folium.Icon(color="orange", icon="info-sign"),
                popup=f"{row['label_school']} - {row['label_location']}"
            )
            marker_objects.add_to(university_map)

    return university_map

#Tabelle
def get_school_names_list():
    data_all = pickeln_data_from_wikidata()

    school_names_list = data_all['label_school'].tolist()
    unique_school_names = list(set(school_names_list))
    school_names_df = pd.DataFrame(unique_school_names, columns=['label_school'])
    schools_to_select = [
        'University of Applied Sciences of the Grisons',
        'Fachhochschule Nordwestschweiz. Hochschule für Technik'
    ]
    selected_rows_df = school_names_df.loc[school_names_df['label_school'].isin(schools_to_select)]
    return selected_rows_df

data_df = get_school_names_list()
#_______________________________________________________________________________________________________________________

# START APP

app = Dash(__name__, external_stylesheets=[dbc.themes.SOLAR])

# LAYOUT SECTION: BOOTSTRAP
#-----------------------------------------------------------------------------------------------------------------------
app.layout = html.Div([
    dcc.Loading(
        id='loading',
        children=[
            dbc.Container([
                dbc.Row(html.H3('Masterstudium in der Schweiz',
                        className='text-left d-flex align-items-center',
                        style={'font-family': 'Source Sans Pro', 'font-size': '38px', 'font-weight': 'bold','color': '#FFFFFF'}),
                    className='mt-1 d-flex align-items-start',
                    style={'height': '55px', 'border-radius': '2px', 'background-color': "#fca311"}),

                html.Div(style={'height': '9px'}),

                dbc.Row(html.H3('Finde deinen Master',
                        className='text-left d-flex align-items-center',
                        style={'font-family': 'Source Sans Pro', 'font-size': '22px', 'font-weight': 'bold','color': '#000000'}),
                        className='mt-1 d-flex align-items-end',
                        style={'height': '45px', 'border-radius': '2px', 'background-color': "#e5e5e5"}
                ),
            ]),
                html.Div(style={'height': '9px'}),

                dbc.Row([
                    dbc.Col([
                            html.Iframe(id='map',
                                        height='320px',
                                        width="60%",
                                        style={'background-color':'white', 'border-radius': '13px','margin-left': '110px',
                                                        'boxShadow': '2px 2px 2px rgba(0, 0, 0, 0.25)'}),
                    ], width=8),
                            html.Div(id='hidden-div', style={'display': 'none'}),

                    dbc.Col([
                        dbc.Row([html.H1("Schulauswahl:", style={'margin-left': '-150px'}),
                            dcc.Checklist(
                                id='school-checklist',
                                options=[
                                    {'label': 'University of Applied Sciences of the Grisons', 'value': 'fhgr'},
                                    {'label': 'Fachhochschule Nordwestschweiz. Hochschule für Technik', 'value': 'fhnw'}
                                ],
                                value=[],
                                labelStyle={'display': 'block'},
                                style={'margin-left': '-150px'}
                            ),
                            html.Div(id='output-container', style={'margin-left': '-150px'})
                        ]),
                    ], width=4),
                html.Div(style={'height': '11px'}),
                dbc.Row([
                        dbc.Col(html.H1("MASTERSTUDIENANGEBOT:"),
                            width=10,
                            className='text-left d-flex align-items-right',
                            style={'background-color': '#fcbf49', 'font-size': '32px', 'font-weight': 'bold', 'border-radius': '5px',
                                   'height': '44px', 'weight': 'bold', 'color': '#000000', 'margin-left': '0px'}),
                        html.Div(style={'height': '7px'}),
                        dbc.Col(dash_table.DataTable(
                            id='table',
                            columns=[{'name': i, 'id': i, 'deletable': False, 'selectable': True} for i in fhnw.columns],
                            data=[],
                            sort_action='native',
                            page_action='native',
                            page_current= 0,
                            page_size= 11,
                            style_cell={'textAlign': 'left',
                                        'fontSize': '65%',
                                        'fontFamily': 'Arial, sans-serif',
                                        'whiteSpace': 'normal',
                                        'height': 'auto'},
                            style_table={'overflowX': 'auto', 'fontFamily': '-apple-system', 'margin-left': '0px'},
                            style_header={
                                'fontWeight': 'bold', },
                            style_as_list_view=True,
                            style_data_conditional=[
                                {'if': {'row_index': 'odd'},'backgroundColor': '#F9FCFD'}],
                        ),width=10)
                ], className='d-flex justify-content-center',),
            ], className='d-flex justify-content-center',)
        ]
    )
])

# CALLBACK FUNCTION
#-----------------------------------------------------------------------------------------------------------------------
@app.callback(
      Output('map', 'srcDoc'),
        [Input('hidden-div', 'children')]
)
def show_map(dummy):
    map_object = create_university_map()
    return map_object._repr_html_()

@app.callback(
    Output('output-container', 'children'),
    [Input('school-checklist', 'value')]
)
def update_output(selected_schools):
    return 'Sie haben folgende Schulen ausgewählt: ' + ', '.join(selected_schools)

@app.callback(
    Output('table', 'data'),
    Output('table', 'columns'),
    Input('school-checklist', 'value')
)
def update_table(selected_schools):
    if 'fhgr' in selected_schools:
        return fhgr.to_dict('records'), [{'name': i, 'id': i} for i in fhgr.columns]
    elif 'fhnw' in selected_schools:
        return fhnw.to_dict('records'), [{'name': i, 'id': i} for i in fhnw.columns]
    else:
        return [], []
# RUN THE APP
#-----------------------------------------------------------------------------------------------------------------------
if __name__=='__main__':
    app.run_server(debug=True, port=8520)