# Import packages
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# _____________________________ FONCTIONS _____________________________________
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


# Import donnees
df = pd.read_csv('data/base_donnees_whatcar.csv', index_col=0)
st.write("Jeu de données :")
st.write(df)

# Description du jeu de données
st.header("Descriptions statistique du jeu de données")
df2=cleaning(df)


if st.checkbox('Cacher description des données',value=True):
    pass
else:
    st.subheader('Description statistique :')
    st.write('Le tableau ci-dessous présente le nombre de véhicules, la moyenne, valeur minimale et maximale entre autres de chaque paramètre étudié (colonne)')
    st.write(df2.describe())

# Selection caracteristique technique
st.subheader("Distribution d'une caractéristique technique")
st.write("Regardons la distribution d'une variable selon les catégories des véhicules étudiés. Quelle caractéristique technique souhaitez-vous analyser ?")
features=['Longueur (m)', 'Largeur (m)', 'Puissance (chevaux)', 'Couple (mkg)','Coffre (L)', 'Consommation mixte (L)', 'Emissions CO2', 'Norme Euro','Note Caradisiac', 'Note proprietaires']
feature_name = st.selectbox("Sélection de la caractéristique technique",features)

# Distribution par catégorie de véhicules
fig, ax1 = plt.subplots(facecolor=(1, 1, 1))
ax1=sns.kdeplot(data=df2, x=feature_name,hue="Categorie",color=['midnightblue','blue','royalblue','dodgerblue','lightskyblue','lavender','plum']);
ax1.set_title("Distribution de la caractéristique choisie")
st.pyplot(fig)
