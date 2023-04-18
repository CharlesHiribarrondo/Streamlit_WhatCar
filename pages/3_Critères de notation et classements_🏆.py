# Import packages
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# _______________________________ FONCTION __________________________________
def cleaning(df):
    cols_num_1 = ['Longueur (m)', 'Largeur (m)', 'Puissance (chevaux)', 'Couple (mkg)',
                  'Coffre (L)', 'Consommation mixte (L)', 'Emissions CO2', 'Norme Euro',
                  'Note Caradisiac', 'Note proprietaires']

    # Copie dataframe
    df2 = df.copy()

    # Transformation en données numériques pour valeurs allant de 0 à 999
    for element in cols_num_1:
        df2[element] = df[element].apply(lambda x: str(x).replace(',', '.'))
        df2[element] = df2[element].apply(lambda x: str(x).replace('-', 'nan'))
        mean = df2[element].loc[df2[element] != 'nan'].astype(float).mean()
        df2[element] = df2[element].replace(to_replace='nan', value=mean)
        df2[element] = pd.to_numeric(df2[element])

    # Transformation en données numériques pour valeurs > 1000
    df2['Poids (kg)'] = df['Poids (kg)'].apply(lambda x: str(x).replace(',', '.'))
    df2['Poids (kg)'] = df2['Poids (kg)'].apply(lambda x: str(x).replace('-', 'nan'))
    df2['Poids (kg)'] = df2['Poids (kg)'].apply(lambda x: (str(x)[0] + str(x)[-6:]))
    df2['Poids (kg)'] = pd.to_numeric(df2['Poids (kg)'])

    df2['Cote LaCentrale'] = df['Cote LaCentrale'].apply(lambda x: str(x).replace(',', '.'))
    df2['Cote LaCentrale'] = df2['Cote LaCentrale'].apply(lambda x: str(x).split('\u202f'))
    df2['Cote LaCentrale'] = df2['Cote LaCentrale'].apply(lambda x: (x[0] + x[1]))
    df2['Cote LaCentrale'] = pd.to_numeric(df2['Cote LaCentrale'])

    df2['Motorisation'] = df2['Motorisation'].replace('Esence', 'Essence')

    return df2


def ajout_cols(df):
    df['(Puissance/Poids) x 100'] = df['Puissance (chevaux)']/df['Poids (kg)'] * 100
    df['(Couple/Poids) x 100'] = df['Couple (mkg)'] / df['Poids (kg)'] * 100
    return df

# Critères de notations
st.header("Critères de notation")
st.write('Voici les critères principaux sur lesquels nous pouvons jouer :')
st.write("*   Taille du coffre \n *   Rapport puissance / poids : confort de conduite \n *   Rapport couple / poids : confort de conduite \n *   Consommation du véhicule (L) \n *   Cote La Centrale : prix espéré \n *   Notes propriétaires : avis des personnes ayant réellement conduit le véhicule pendant plusieurs années \n * Norme Euro : respect de l'Environnement")
st.write("Pour cela, nous ajoutons deux colonnes à notre jeu de données : \n * Rapport (Puissance / Poids) \n * Rapport (Couple / Poids)")
st.write("Jeu de données final :")
df = pd.read_csv('data/base_donnees_whatcar.csv', index_col=0)
df2=cleaning(df)
df3=ajout_cols(df2)
df3=df3.sort_values(by='Nom',ascending=True)
st.write(df3)

# Classements
st.header("Classements")
colors=['midnightblue','darkblue','blue','royalblue','dodgerblue','lightskyblue','lavender','plum']
st.write("Vous trouverez ci-dessous les classements des véhicules selon chaque critère de notation. Nous vous invitons à décocher les cases que vous souhaitez pour analyser vous-même ces classements.")

# ------ Figure 1 - Coffre ------------------
st.subheader("Taille du coffre")
if st.checkbox('Classement coffre',value=True):
    pass
else:
    df4 = df3.sort_values(by=['Coffre (L)'], ascending=True)
    vehicles = df4.index
    coffre = df4['Coffre (L)']
    fig, ax1 = plt.subplots(facecolor=(1, 1, 1), figsize=(11, 15))
    ax1.barh(vehicles, coffre, label='Coffre véhicule', color=colors[0])
    ax1.set_xlabel('Volume du coffre (L)')
    ax1.set_title("Classement des véhicules selon leurs volumes de coffre")
    st.pyplot(fig);

# ------ Figure 2 - Puissance / Poids ------------------
st.subheader("Puissance / Poids")
if st.checkbox('Classement puissance / poids',value=True):
    pass
else:
    df5=df3.sort_values(by=['(Puissance/Poids) x 100'],ascending=True)
    vehicles = df5.index
    puissance = df5['(Puissance/Poids) x 100']
    fig, ax1 = plt.subplots(facecolor=(1, 1, 1),figsize=(11,15))
    ax1.barh(vehicles, puissance,color=colors[1])
    ax1.set_xlabel('Rapport (Puissance / Poids) x100')
    ax1.set_title("Classement des véhicules selon leurs ratios Puissance / Poids")
    st.pyplot(fig);

# ------ Figure 3 - Couple / Poids ------------------
st.subheader("Couple / Poids")
if st.checkbox('Classement couple / poids',value=True):
    pass
else:
    df6=df3.sort_values(by=['(Couple/Poids) x 100'],ascending=True)
    vehicles = df6.index
    couple = df6['(Couple/Poids) x 100']
    fig, ax1 = plt.subplots(facecolor=(1, 1, 1),figsize=(11,15))
    ax1.barh(vehicles, couple,color=colors[2])
    ax1.set_xlabel('Rapport (Couple / Poids) x100')
    ax1.set_title("Classement des véhicules selon leurs ratios Couple moteur / Poids")
    st.pyplot(fig);

# ------ Figure 4 - Consommation ------------------
st.subheader("Consommation")
if st.checkbox('Classement Consommation',value=True):
    pass
else:
    df7=df3.sort_values(by=['Consommation mixte (L)'],ascending=False)
    vehicles = df7.index
    prix = df7['Consommation mixte (L)']
    fig, ax1 = plt.subplots(facecolor=(1, 1, 1),figsize=(11,15))
    ax1.barh(vehicles, prix,color=colors[3])
    ax1.set_xlabel('Consommation mixte (L)')
    ax1.set_title("Classement des véhicules selon leurs consommations")
    st.pyplot(fig);

# ------ Figure 5 - Prix ------------------
st.subheader("Prix")
if st.checkbox('Classement prix',value=True):
    pass
else:
    df8=df3.sort_values(by=['Cote LaCentrale'],ascending=False)
    vehicles = df8.index
    prix = df8['Cote LaCentrale']
    fig, ax1 = plt.subplots(facecolor=(1, 1, 1),figsize=(11,15))
    ax1.barh(vehicles, prix,color=colors[3])
    ax1.set_xlabel('Cote La Centrale')
    ax1.set_title("Classement des véhicules selon leurs prix")
    st.pyplot(fig);

# ------ Figure 6 - Notes Propriétaires ------------------
st.subheader("Notes Propriétaires")
if st.checkbox('Classement notes propriétaires',value=True):
    pass
else:
    df9=df3.sort_values(by=['Note proprietaires'],ascending=True)
    vehicles = df9.index
    notes = df9['Note proprietaires']
    fig, ax1 = plt.subplots(facecolor=(1, 1, 1),figsize=(11,15))
    ax1.barh(vehicles, notes,color=colors[4])
    ax1.set_xlabel('Note proprietaires')
    ax1.set_title("Classement des véhicules selon les notes de leurs propriétaires")
    st.pyplot(fig);

# ------ Figure 7 - Notes Environnement ------------------
st.subheader("Notes Norme Euro")
if st.checkbox('Classement norme Euro',value=True):
    pass
else:
    df10=df3.sort_values(by=['Norme Euro'],ascending=True)
    vehicles = df10.index
    notes = df10['Norme Euro']
    fig, ax1 = plt.subplots(facecolor=(1, 1, 1),figsize=(11,15))
    ax1.barh(vehicles, notes,color=colors[5])
    ax1.set_xlabel('Norme Euro')
    ax1.set_title("Classement des véhicules selon leurs valeurs de norme Euro")
    st.pyplot(fig);