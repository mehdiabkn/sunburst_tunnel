import pandas as pd
import streamlit as st
import plotly.express as px

# Chargement des données
# ÉTAPE 1: EXTRACTION DES DONNÉES
df = pd.read_csv("tel.csv")
df['val'] = 1 # AJOUT DE CETTE COLONNE POUR L'UTILISER DANS LE PARAMÈTRE VALUE
df["date"] = pd.to_datetime(df["date"], dayfirst=True)

# Sélection de la plage de dates
start_date = st.sidebar.date_input("Date de début", df["date"].min())
end_date = st.sidebar.date_input("Date de fin", df["date"].max())

# Convertir les objets date en datetime
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

filtered_data = df[(df["date"] >= start_date) & (df["date"] <= end_date)]

df = df.dropna()
# ON CALCULE LE NOMBRE DE COLONNE QU'IL NOUS FAUDRA POUR LE SPLIT
nb_etapes = len(df["parcours"].str.split(",", expand=True).columns)
noms_colonnes = []
for i in range(nb_etapes):
    noms_colonnes.append("etape_" + str(i))

# ON SPLIT LA COLONNE PARCOURS EN LE NOMBRE DE COLONNES NÉCESSAIRES

df[noms_colonnes] = df["parcours"].str.split(",", expand=True)

df = pd.DataFrame(
    dict(
        etape1=df['etape_1'], etape2=df['etape_2'], etape3=df['etape_3'],
        etape4=df['etape_4'], etape5=df['etape_5'], etape6=df['etape_6'],
        etape7=df['etape_7'], etape8=df['etape_8'], etape9=df['etape_9'],
        etape10=df['etape_10'], etape11=df['etape_11'], valeurs=df['val'], temps=df['temps_parcours_secondes']
    )
)

df = df.dropna()

fig = px.sunburst(df, path=['etape1', 'etape2', 'etape3', 'etape4', 'etape5', 'etape6', 'etape7', 'etape8', 'etape9', 'etape10', 'etape11'], values='valeurs', title="Tunnel de vente V4", color=df['temps'])

st.plotly_chart(fig, use_container_width=True)
