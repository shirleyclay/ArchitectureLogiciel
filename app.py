from logging import info
import dash
#import pandas as pd
import dash_html_components as html
#import datetime
#import locale #Pour le format de date
import dash_bootstrap_components as dbc
#import math
import dash_core_components as dcc
from dash.dependencies import Input, Output
#import plotly.express as px
#import plotly.graph_objects as go
# from components.functions_graph import generate_table, affichage_kpi, affichage_pie, affichage_bar, affichage_serieTemps,boutonradio
# from components.functions_data import data

from datagraph.functions_graph import generate_table, affichage_kpi, affichage_pie, affichage_bar, affichage_serieTemps,boutonradio
from datagraph.functions_data import data

import ssl
ssl._create_default_https_context=ssl._create_unverified_context


bootstrap_theme=[dbc.themes.BOOTSTRAP,'https://use.fontawesome.com/releases/v5.9.0/css/all.css']

#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app = dash.Dash(__name__, external_stylesheets=bootstrap_theme)


#######################################################################################
############################### TABLEAU DES DONNNEES ##################################
#######################################################################################

# L'appel de cette fonction est réalisée dans le fichier functions.graph
    

#######################################################################################
################################ ENCADRES DE DONNEES ##################################
#######################################################################################

# L'appel de cette fonction est réalisée dans le fichier functions.graph


#######################################################################################
############################### GRAPHIQUE CIRCULAIRE ##################################
#######################################################################################

@app.callback(
    Output("pie-chart", "figure"), 
    Input("Chaine_TV", "value"))
def generate_chart(Chaine_TV):
    return affichage_pie(Chaine_TV)



#######################################################################################
################################ GRAPHIQUE BAR ########################################
#######################################################################################

def generate_bar():
    return affichage_bar()



#######################################################################################
############################### SERIES TEMPORELLES## ##################################
#######################################################################################
@app.callback(
    Output("timeline", "figure"), 
    Input("Chaine_TV", "value"),
    Input("FiltreVisionDate","value"))
def generate_timeline(Chaine_TV,FiltreVisionDate):
   return affichage_serieTemps(Chaine_TV,FiltreVisionDate)



#######################################################################################
############################### FILTRE AFFICHAGE DATES ################################
#######################################################################################

# L'appel de cette fonction est réalisée dans le fichier functions.graph


#######################################################################################
####################################### LAYOUT ########################################
#######################################################################################

app.layout = html.Div(children=[
    html.Br(),
    html.H2(children='Classement des thématiques des sujets de journaux télévisés de janvier 2005 à septembre 2020',
        style={'text-align': 'center','border-style':'solid',"border-color":"orange"}),
    html.Br(),
    affichage_kpi(),
    html.Br(),
    html.H3("Filtre :"),
    dcc.Dropdown(
        id='Chaine_TV', 
        value=data.columns[8], 
        options=[{'value': x, 'label': x} 
                 for x in data.columns[2:,]],
        clearable=False,
        style={'width': '70%'}

    ),
    dcc.Graph(id="pie-chart",style={'width': '50%', 'padding': '1em 2em 2em','float':'left'}),
    dcc.Graph(figure=generate_bar(),style={'width': '50%','padding': '1em 2em 2em','float':'right'}),
    html.Br(),
    boutonradio(),
    dcc.Graph(id="timeline"),
    html.H3("Aperçu du jeu de données : "),
    generate_table(data),
    html.Footer(children="By Marianne Bellahmar - Shirley Clay - Romain Douesnard",style={'text-align': 'center'}),
    html.Img(src='/assets/image.png', style={'width': '8%', 'text-align':'left'})
    ]
)


if __name__ == '__main__':
    app.run_server(debug=True)

