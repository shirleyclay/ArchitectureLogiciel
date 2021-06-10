import dash
import pandas as pd
import dash_html_components as html

data = pd.read_csv("https://static.data.gouv.fr/resources/classement-thematique-des-sujets-de-journaux-televises-janvier-2005-septembre-2020/20201202-114045/ina-barometre-jt-tv-donnees-mensuelles-2005-2020-nombre-de-sujets.csv",
    encoding='Windows-1250',sep=";")

#Je remarque qu'il y a des headers  dans le csv mais ils ne sont pas complets car on a les chaînes de télé sur la première ligne.
#J'aurais voulu que dans les headers on ait directement la chaîne inscrite.

######################
#Reformatage des headers
headers = data.columns.values
ligne0 = (data.iloc[0])
for i in range(2,9):
    headers[i] = "Nombre de sujets JT de "+ " " + ligne0[i]
data.drop(data.columns.values[9],axis=1,inplace=True)
data.drop(0,axis=0,inplace=True)
headers= headers[0:9]
######################

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


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H4(children='Classement thématique des sujets de journaux télévisés de janvier 2005 à septembre 2020'),
    generate_table(data)
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
