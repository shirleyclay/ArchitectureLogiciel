from logging import info
import dash
from numpy import nan_to_num
import pandas as pd
import dash_html_components as html
import datetime
import locale #Pour le format de date
import dash_bootstrap_components as dbc
import  math

data = pd.read_csv("https://static.data.gouv.fr/resources/classement-thematique-des-sujets-de-journaux-televises-janvier-2005-septembre-2020/20201202-114045/ina-barometre-jt-tv-donnees-mensuelles-2005-2020-nombre-de-sujets.csv",
    encoding='cp1252',sep=";")

#Quand pb d'encodage : tester utf8, cp1252, latin1

#Je remarque qu'il y a des headers  dans le csv mais ils ne sont pas complets car on a les chaînes de télé sur la première ligne.
#J'aurais voulu que dans les headers on ait directement la chaîne inscrite.

headers = data.columns.values
ligne0 = (data.iloc[0])
for i in range(2,9):
    headers[i] = "Nombre de sujets JT de "+ " " + ligne0[i]
data.drop(data.columns.values[9],axis=1,inplace=True)
data.drop(0,axis=0,inplace=True)
headers= headers[0:9]

#Format de date
locale.setlocale(locale.LC_TIME,'fr_FR'); #Obligatoire pour que ça reconnaisse janvier/février...
data['MOIS']=data['MOIS'].apply(lambda _: datetime.datetime.strptime(_,"%B-%y").strftime("%m-%Y"))

#format entier
data.iloc[1:,2]=data.iloc[1:,2].astype(float)
data.iloc[1:,3]=data.iloc[1:,3].astype(float)
data.iloc[1:,4]=data.iloc[1:,4].astype(float)
data.iloc[1:,5]=data.iloc[1:,5].astype(float)
data.iloc[1:,6]=data.iloc[1:,6].astype(float)
data.iloc[1:,7]=data.iloc[1:,7].astype(float)
data.iloc[1:,8]=data.iloc[1:,8].astype(float)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

def generate_table(dataframe, max_rows=100):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])
    

color_l=['info',"secondary","success","warning","danger","Test","Test1"]
def col_sum(data,col_idx):
    r = 0
    for i in range(2,data.shape[0]-1):
        if(math.isnan(data.iloc[i,col_idx])==False): #ATTENTION IL Y A DES NA DANS LA COLONNE ARTE
            r = r + data.iloc[i,col_idx]
    return r

#fonctiond de création des cartes
def create_card(title, content,color):
    card = dbc.Card(
        dbc.CardBody(
            [
                html.H4(title, className="card-title"),
                html.Br(),
                html.H2(content, className="card-subtitle"),
                html.Br(),

                ]
        ),
        color=color, inverse=True
    )
    return(card)


card1 = create_card("Nombre de sujet JT de TF1", col_sum(data,2),color_l[0])
card2 = create_card("Nombre de sujet JT de France 2", col_sum(data,3),color_l[1])
card3 = create_card("Nombre de sujet JT de France 3", col_sum(data,4),color_l[2])
card4 = create_card("Nombre de sujet JT de Canal +", col_sum(data,5),color_l[3])
card5 = create_card("Nombre de sujet JT de Arte", col_sum(data,6),color_l[4])
card6 = create_card("Nombre de sujet JT de M6", col_sum(data,7),color_l[5])

card = dbc.Row([dbc.Col(id='card1', children=[card1], lg=3,width=6), 
                dbc.Col(id='card2', children=[card2], lg=3,width=6), 
                dbc.Col(id='card3', children=[card3], lg=3,width=6), 
                dbc.Col(id='card4', children=[card4], lg=3,width=6),
                dbc.Col(id='card5', children=[card5], lg=3,width=6),
                dbc.Col(id='card6', children=[card6], lg=3,width=6)
                ]
               )


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H4(children='Classement thématique des sujets de journaux télévisés de janvier 2005 à septembre 2020'),
    generate_table(data),
    card
])

if __name__ == '__main__':
    app.run_server(debug=True)

#Graph avec pour chaque chaîne l'évolution d'un sujet sélectionné dans une liste.
#Part de chaque sujet sur une chaîne
#Listes de chaque chaîne
#Somme du nombre de sujets diffusés par chaîne
#Diagramme en barres empilées avec part de chaque sujet 
# Quelles sont les lignes éditoriales de chaque chaîne ? Voir si il y a eu du changement dans chaque ligne éditoriale.
# L'évolution du nombre de sujets de JT par mois par chaîne ( à mettre en relief avec le temps de JT sur chaque chaîne) 
