import math
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import dash_core_components as dcc
from components.functions_data import col_sum, data_pie, data_bar, data_serieTemp

#######################################################################################
################################## POUR LES KPI #######################################
#######################################################################################

color_l=["darkturquoise","deepskyblue","dodgerblue","royalblue","blue","darkblue"]
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


def affichage_kpi():

    card1 = create_card("Nombre de sujet JT de TF1", col_sum(2),color_l[0])
    card2 = create_card("Nombre de sujet JT de France 2", col_sum(3),color_l[1])
    card3 = create_card("Nombre de sujet JT de France 3", col_sum(4),color_l[2])
    card4 = create_card("Nombre de sujet JT de Canal +", col_sum(5),color_l[3])
    card5 = create_card("Nombre de sujet JT de Arte", col_sum(6),color_l[4])
    card6 = create_card("Nombre de sujet JT de M6", col_sum(7),color_l[5])

    card = dbc.Row([dbc.Col(id='card1', children=[card1], lg=2,width=3), 
                    dbc.Col(id='card2', children=[card2], lg=2,width=3), 
                    dbc.Col(id='card3', children=[card3], lg=2,width=3), 
                    dbc.Col(id='card4', children=[card4], lg=2,width=3),
                    dbc.Col(id='card5', children=[card5], lg=2,width=3),
                    dbc.Col(id='card6', children=[card6], lg=2,width=3)
                    ],style={'width': '97%', 'padding': '25px 25px 25px 25px'},
                    align="center",
                )
    return card


#######################################################################################
############################### TABLEAU DES DONNNEES ##################################
#######################################################################################

def generate_table(dataframe, max_rows=20):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ], style={ 'width': '100%',
                'border-collapse': 'collapse',
                'border': '3px solid blue',
                'overflowY': 'scroll' }
    )
    
#######################################################################################
############################### GRAPHIQUE CIRCULAIRE ##################################
#######################################################################################

def affichage_pie(Chaine_TV):
    df = data_pie(Chaine_TV)
    # Réalisation du graphique circulaire
    fig = px.pie(df, values=Chaine_TV, names=df["THEMATIQUES"],title="Repartition du "+(Chaine_TV[0].lower())+Chaine_TV[1:]+"<br>toutes périodes confondues")
    fig.update_layout(title_x=0.5)
    return fig

#######################################################################################
################################ GRAPHIQUE BAR ########################################
#######################################################################################


def affichage_bar():
    df = data_bar()
    fig = go.Figure(go.Bar(x=df["THEMATIQUES"], y=df[df.columns[1]], name=df.columns[1].split("de ")[2]))
    for i in range(2,7):
        fig.add_trace(go.Bar(x=df["THEMATIQUES"], y=df[df.columns[i]], name=df.columns[i].split("de ")[2]))
    fig.update_layout(barmode='stack', xaxis={'categoryorder':'category ascending'},title_text='Répartition par thématique du nombre de sujets traités par chaîne')
    fig.update_yaxes(title_text='Part du nombre de sujets traités par chaine')
    fig.update_xaxes(title_text="Thématiques")
    return fig


#######################################################################################
############################### SERIES TEMPORELLES## ##################################
#######################################################################################

def affichage_serieTemps(Chaine_TV,FiltreVisionDate):
    df = data_serieTemp(Chaine_TV)
    if( FiltreVisionDate == "Mois"):
        df = df.pivot_table(columns="THEMATIQUES",values=Chaine_TV,index=["MOIS"],aggfunc=sum)
        df = df.div(df.sum(axis=1), axis=0).reset_index()
        df = df.sort_values(by="MOIS")
        fig2 = px.line(df, x = (df["MOIS"]),y=df.columns[1:,],title="Taux de présence des thèmes sur le "+(Chaine_TV[0].lower())+Chaine_TV[1:])
    elif (FiltreVisionDate == "Année"):
        df = df.pivot_table(columns="THEMATIQUES",values=Chaine_TV,index=["ANNEE"],aggfunc=sum)
        df = df.div(df.sum(axis=1), axis=0).reset_index()
        df = df.sort_values(by="ANNEE")
        fig2 = px.line(df, x = (df["ANNEE"]),y=df.columns[1:,],title="Taux de présence des thèmes sur le "+(Chaine_TV[0].lower())+Chaine_TV[1:])

    fig2.update_yaxes(title_text='Pourcentage du thème dans les sujets traités')
    fig2.update_xaxes(rangeslider_visible=True)
    return fig2



#######################################################################################
############################### FILTRE AFFICHAGE DATES ################################
#######################################################################################

def boutonradio():
    radio = dcc.RadioItems(
        id ="FiltreVisionDate",
        options=[
            #{'label': 'choix date', 'value': 'choix'},
            {'label': 'Vision au mois', 'value': 'Mois'},
            {'label': 'Vision à l\'année', 'value': 'Année',},
            
        ], 
        value='Mois',
        labelStyle={'display': 'inline-block', 'width': '20%','color': 'black','marginTop': 13},
        )
    filtre_label =html.H2("Sélection de la vision : ",style={'color':'black'})
    filtre_line = dbc.Row([dbc.Col(filtre_label , lg=3,width=6), dbc.Col(radio, lg=6, width=6)])
    return filtre_line

