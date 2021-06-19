
import math
import pandas as pd
import locale #Pour le format de date
import datetime

import ssl
ssl._create_default_https_context=ssl._create_unverified_context

data = pd.read_csv("https://static.data.gouv.fr/resources/classement-thematique-des-sujets-de-journaux-televises-janvier-2005-septembre-2020/20201202-114045/ina-barometre-jt-tv-donnees-mensuelles-2005-2020-nombre-de-sujets.csv",
    encoding='cp1252',sep=";")

#Quand pb d'encodage : tester utf8, cp1252, latin1

#Je remarque qu'il y a des headers  dans le csv mais ils ne sont pas complets car on a les chaînes de télé sur la première ligne.
#J'aurais voulu que dans les headers on ait directement la chaîne inscrite.

headers = data.columns.values
ligne0 = (data.iloc[0])
for i in range(2,8):
    headers[i] = "Nombre de sujets JT de " + ligne0[i]
headers[8]= "Nombre de sujets JT de toutes les chaînes"
data.drop(data.columns.values[9],axis=1,inplace=True)
data.drop(0,axis=0,inplace=True)
headers= headers[0:9]

#Format de date
locale.setlocale(locale.LC_TIME,'fr_FR'); #Obligatoire pour que ça reconnaisse janvier/février...
data['MOIS']=data['MOIS'].apply(lambda _: datetime.datetime.strptime(_,"%B-%y").strftime("%m-%Y"))

#format entier
data.iloc[0:,2]=data.iloc[0:,2].astype(float)
data.iloc[0:,3]=data.iloc[0:,3].astype(float)
data.iloc[0:,4]=data.iloc[0:,4].astype(float)
data.iloc[0:,5]=data.iloc[0:,5].astype(float)
data.iloc[0:,6]=data.iloc[0:,6].astype(float)
data.iloc[0:,7]=data.iloc[0:,7].astype(float)
data.iloc[0:,8]=data.iloc[0:,8].astype(float)


#######################################################################################
################################## POUR LES KPI #######################################
#######################################################################################

def col_sum(col_idx):
    r = 0
    for i in range(2,data.shape[0]-1):
        if(math.isnan(data.iloc[i,col_idx])==False): #ATTENTION IL Y A DES NA DANS LA COLONNE ARTE
            r = r + data.iloc[i,col_idx]
    return r

#######################################################################################
############################### GRAPHIQUE CIRCULAIRE ##################################
#######################################################################################

def data_pie(Chaine_TV):
     # Préparation des données pour réaliser le graphique circulaire
    df= pd.to_numeric(data[Chaine_TV])
    col = ["THEMATIQUES", Chaine_TV]
    df= data[col].groupby("THEMATIQUES").sum().reset_index()
    return df


#######################################################################################
################################ GRAPHIQUE BAR ########################################
#######################################################################################

def data_bar():
    data.iloc[0:,2:9]=data.iloc[0:,2:9].astype(float)
    df =data[data.columns[1:9]].groupby("THEMATIQUES").sum().reset_index()
    x=df["THEMATIQUES"]
    for i in df.columns[1:9]:
        df[i]=round(df[i]/df["Nombre de sujets JT de toutes les chaînes"]*100,2)
    return df
    
#######################################################################################
############################### SERIES TEMPORELLES## ##################################
#######################################################################################

def data_serieTemp(Chaine_TV):
    # Préparation des données pour réaliser le graphique circulaire
    df= pd.to_numeric(data[Chaine_TV])
    col = ["MOIS","THEMATIQUES", Chaine_TV]
    df= data[col]
    df['MOIS']= pd.to_datetime(df['MOIS'],format="%m-%Y")
    df["ANNEE"] = df["MOIS"].dt.year
    return df

