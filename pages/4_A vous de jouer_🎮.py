import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

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

def get_initial_features(df):
    length_selected = df['Longueur (m)'].mean()
    masse_selected = df['Poids (kg)'].mean()
    coffre_selected = df['Coffre (L)'].mean()
    puissance_selected = df['Puissance (chevaux)'].mean()
    couple_selected = df['Couple (mkg)'].mean()
    conso_selected = df['Consommation mixte (L)'].mean()
    prix_selected = df['Cote LaCentrale'].mean()
    notes_selected = df['Note proprietaires'].mean()
    norme_euro_selected = np.abs(df['Norme Euro'].mean())
    return [length_selected, masse_selected,coffre_selected,puissance_selected, couple_selected, conso_selected, prix_selected, notes_selected, norme_euro_selected]

def notation_voiture(df,liste_coeff):
    df['Rapport Coffre/Longueur']=df['Coffre (L)']/df['Longueur (m)']
    df['note_coffre']=liste_coeff[0]*(df['Rapport Coffre/Longueur']/df['Rapport Coffre/Longueur'].max())
    df['note_puissance']=liste_coeff[1]*(df['(Puissance/Poids) x 100']/df['(Puissance/Poids) x 100'].max())
    df['note_couple']=liste_coeff[2]*(df['(Couple/Poids) x 100']/df['(Couple/Poids) x 100'].max())
    df['note_conso']=liste_coeff[3]*(df['Consommation mixte (L)'].min()/df['Consommation mixte (L)'])
    df['note_prix']=liste_coeff[4]*(df['Cote LaCentrale'].min()/df['Cote LaCentrale'])
    df['note_proprio']=liste_coeff[5]*(df['Note proprietaires']/df['Note proprietaires'].max())
    df['note_environnement'] =liste_coeff[6]*(df['Norme Euro']/df['Norme Euro'].max())
    df['note_finale']=df['note_coffre']+df['note_puissance']+df['note_couple']+df['note_conso']+df['note_prix']+df['note_proprio']+df['note_environnement']
    return

def note_vehicule_user(dic,liste_coeff,df):
    dic_note_user={}
    columns_notes = ['note_coffre', 'note_puissance', 'note_couple', 'note_conso', 'note_prix', 'note_proprio','note_environnement', 'note_finale']
    coffre_longueur=dic['Coffre']/dic['Longueur']
    puissance_poids=dic['Puissance']/dic['Poids']*100
    couple_poids=dic['Couple']/dic['Poids']*100
    dic_note_user[columns_notes[0]]=liste_coeff[0]*(coffre_longueur/df['Rapport Coffre/Longueur'].max())
    dic_note_user[columns_notes[1]]=liste_coeff[1]*(puissance_poids/df['(Puissance/Poids) x 100'].max())
    dic_note_user[columns_notes[2]]=liste_coeff[2]*(couple_poids/df['(Couple/Poids) x 100'].max())
    dic_note_user[columns_notes[3]]=liste_coeff[3]*(df['Consommation mixte (L)'].min()/dic['Consommation'])
    dic_note_user[columns_notes[4]]=liste_coeff[4]*(df['Cote LaCentrale'].min()/dic['Prix'])
    dic_note_user[columns_notes[5]]=liste_coeff[5]*(dic['Note']/df['Note proprietaires'].max())
    dic_note_user[columns_notes[6]] =liste_coeff[6]*(dic['Environnement']/df['Norme Euro'].max())
    dic_note_user[columns_notes[7]]=dic_note_user[columns_notes[0]]+dic_note_user[columns_notes[1]]+dic_note_user[columns_notes[2]]+dic_note_user[columns_notes[3]]+dic_note_user[columns_notes[4]]+dic_note_user[columns_notes[5]]+dic_note_user[columns_notes[6]]
    return dic_note_user

# ___________________________________________________________________________________________________

df = pd.read_csv('data/base_donnees_whatcar.csv', index_col=0)
df2=cleaning(df)
df3=ajout_cols(df2)
df3=df3.sort_values(by='Nom',ascending=True)
st.write(df3)
# ____________________________________________________________________________________________________

st.write("Les classements définis lors de la page précédente comportent un biais. En effet, un même modèle peut présenter des caractéristiques techniques très différentes (motorisation, carburant, etc.). Nous n'allons pas préciser chaque version des modèles, au risque de s'y perdre.")
st.write("Notre idée est donc la suivante. Prenez le véhicule que vous souhaitez, avec ses caractéristiques propres. Vous pouvez tout aussi bien faire varier la puissance du moteur, son couple, son prix. Ce faisant, vous obtiendrez le véhicule que vous recherchez, ou celui sur lequel vous êtes tombé sur une annonce en ligne.")

# Choix du véhicule par utilisateur
st.header("Votre véhicule")
longueur_init,masse_init,coffre_init,puissance_init, couple_init, conso_init, prix_init, note_init, norme_euro_init = get_initial_features(df3)
slider_L = st.slider("Longueur du véhicule (m)", min_value=float(min(df3['Longueur (m)'])), max_value=float(max(df3['Longueur (m)'])),value=float(longueur_init), step=0.05)
slider_m = st.slider("Masse du véhicule (kg)", min_value=float(min(df3['Poids (kg)'])), max_value=float(max(df3['Poids (kg)'])),value=float(masse_init), step=10.0)
slider_coffre = st.slider("Volume du coffre (L)", min_value=float(min(df3['Coffre (L)'])), max_value=float(max(df3['Coffre (L)'])), value=float(coffre_init), step=5.0)
slider_puiss = st.slider("Puissance (chevaux)", min_value=float(df3['Puissance (chevaux)'].min()), max_value=float(df3['Puissance (chevaux)'].max()),value=float(puissance_init), step=5.0)
slider_couple = st.slider("Couple (mkg)", min_value=float(df3['Couple (mkg)'].min()), max_value=float(df3['Couple (mkg)'].max()),value=float(couple_init), step=5.0)
slider_conso = st.slider("Consommation mixte (L)", min_value=float(df3['Consommation mixte (L)'].min()), max_value=float(df3['Consommation mixte (L)'].max()),value=float(conso_init), step=0.2)
slider_prix = st.slider("Prix (€)", min_value=500.0, max_value=float(df3['Cote LaCentrale'].max()), value=float(prix_init), step=100.0)
slider_note = st.slider("Avis propriétaires", min_value=float(df3['Note proprietaires'].min()), max_value=float(df3['Note proprietaires'].max()), value=float(note_init), step=0.25)
slider_euro = st.slider("Norme Euro", min_value=int(df3['Norme Euro'].min()), max_value=int(df3['Norme Euro'].max()),  value=int(norme_euro_init), step=1)

ratio_puiss_m = (slider_puiss/slider_m)*100
ratio_couple_m = (slider_couple/slider_m)*100

# Grille de notations
st.header("Votre grille de notation")
st.write("Veuillez allouer un nombre de points pour chaque critère de notation. Plus vous allouez de points, plus le critère est important à vos yeux.")
slider_note_coffre=st.slider("Nombre de points - Coffre",min_value=0,max_value=20,value=3)
slider_note_puiss=st.slider("Nombre de points - Puissance/Poids",min_value=0,max_value=20,value=2)
slider_note_couple=st.slider("Nombre de points - Couple/Poids",min_value=0,max_value=20,value=2)
slider_note_conso=st.slider("Nombre de points - Consommation",min_value=0,max_value=20,value=2)
slider_note_prix=st.slider("Nombre de points - Prix",min_value=0,max_value=20,value=4)
slider_note_avis=st.slider("Nombre de points - Avis propriétaires",min_value=0,max_value=20,value=3)
slider_note_norme_euro=st.slider("Nombre de points - Environnement",min_value=0,max_value=20,value=4)

sum_points=slider_note_coffre+slider_note_puiss+slider_note_couple+slider_note_conso+slider_note_prix+slider_note_avis+slider_note_norme_euro
st.write("D'après votre grille de notation, les véhicules seront notés sur **{} points**".format(sum_points))

# Resultats - Classement final
st.header("Résultats - Classement final")
coeff_note_user=[slider_note_coffre,slider_note_puiss,slider_note_couple,slider_note_conso,slider_note_prix,slider_note_avis,slider_note_norme_euro]

notation_voiture(df3,coeff_note_user)

# ------ Fusion dataframes ------------------
columns_notes=['note_coffre','note_puissance','note_couple','note_conso','note_prix','note_proprio','note_environnement','note_finale']

dic_vehicule_user={'Longueur':slider_L,
                   'Poids':slider_m,
                   "Coffre":slider_coffre,
                   'Puissance':slider_puiss,
                   'Couple':slider_couple,
                   'Consommation':slider_conso,
                   "Prix":slider_prix,
                   'Note':slider_note,
                   'Environnement':slider_euro}

dic_note_vehicule_user=note_vehicule_user(dic_vehicule_user,coeff_note_user,df3)

df4=df3[columns_notes]
df5=pd.DataFrame(dic_note_vehicule_user,index=["Votre vehicule cible"])
df6=pd.concat([df4,df5])

if st.checkbox('Tableau des notes',value=True):
    pass
else:
    st.write(df6)

# ------------ Classement final -------------------
df7=df6.sort_values(by='note_finale')
df7['Nom']=df7.index
note_vehicule_user=df7.loc[df7['Nom']=='Votre vehicule cible']['note_finale'][0]
index_vehicule_user=df7.loc[df7['Nom']=='Votre vehicule cible'].index[0]
df8=df7.drop([index_vehicule_user])
df8_best=df8.loc[df8['note_finale']>note_vehicule_user]
df8_bad=df8.loc[df8['note_finale']<=note_vehicule_user]



fig, ax1 = plt.subplots(facecolor=(1, 1, 1), figsize=(11, 15))
ax1.barh(df8_bad['Nom'], df8_bad['note_finale'],label='Voitures base de données',color='blue',alpha=0.3)
ax1.barh('Votre vehicule cible',note_vehicule_user,label='Votre véhicule cible',color='blue')
ax1.barh(df8_best['Nom'], df8_best['note_finale'],label='Voitures base de données',color='blue',alpha=0.3)
ax1.set_title('Classement final')
ax1.set_ylabel('Véhicules')
ax1.set_xlabel('Note')
st.pyplot(fig);

st.write('Votre véhicule est le **n°{} du classement** selon votre grille de notations.'.format(df8_best.shape[0]+1))
