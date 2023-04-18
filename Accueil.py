import streamlit as st

st.title('	WhatCar	:car:')
st.header('Contexte')

st.write("Pour 75% des français (source Insee), la voiture est le mode de transport privilégié domicile-travail. Cependant, posséder une voiture peut représenter un poste de dépenses très important. En effet, les frais d'entretien, d'assurance et de carburant peuvent vite devenir considérables. Et c'est sans compter les prix d'achat des véhicules neufs qui flambent depuis 10 ans.")
st.write("https://www.lemonde.fr/economie/article/2021/12/13/avec-des-prix-qui-flambent-depuis-dix-ans-l-automobile-redevient-un-produit-de-luxe_6105885_3234.html")
st.write('https://www.auto-moto.com/pratique/prix-du-neuf/prix-voitures-neuves-augmentations-delirantes-an-348885.html#item=1')
st.write("https://www.insee.fr/fr/statistiques/5013868#graphique-figure1")
st.write("Malgré ces coûts élevés, et des fins de mois difficiles, la voiture reste le moyen de transport privilégié des français. Le paradoxe est d'autant plus marqué pour les personnes vivant en zones péri-urbaines ou rurales, pour qui la voiture est bien souvent leur seule solution de déplacement.")

st.header('Objectif du projet WhatCar')
st.write("Aujourd'hui, il est difficile de considérer l'achat d'une voiture neuve, en raison du prix de vente trop important. C'est pourquoi le marché de l'occasion est en très forte augmentation.")
st.write("Nous nous tournons donc de plus en plus vers des véhicules de seconde main. WhatCar est née de ce constat, avec l'envie d' **analyser le maximum de véhicules d'occasion à des cotes inférieures à 15 000 €**. WhatCar a pour objectif de  recenser, regrouper, traiter, analyser et établir une notation dont vous aurez défini vous-même le poids des paramètres étudiés.")
st.write("Il est important avant d'acheter son véhicule de prendre le temps de bien évaluer les différentes options disponibles sur le marché. Un système de classification de voitures selon des critères techniques, comme celui que nous avons développé, pourra vous aider, nous l'espérons, à trouver la voiture qui offre le meilleur rapport qualité-prix selon vos besoins.")

st.header("Base de données étudiée")
st.write("La base de données que nous utiliserons pour établir notre système de notations a été créée par nos soins. Il s'agit d'un ensemble de véhicules que l'on retrouve souvent sur le marché de l'occasion, ayant fortement décoté depuis leur sortie d'usine, en veillant néanmoins à présenter des véhicules suffisamment récents (> 2000), pour éviter les modèles trop kilométrés. Toutes ces données ont été extraites du site www.caradisiac.com. Nous précisons que nous n'avons aucun partenariat avec Caradisiac, mais il s'agissait pour nous d'une source de données précieuse, bien documentée, avec des avis d'anciens propriétaires nous donnant la fiabilité réellement perçue du véhicule. Nous remercions vivement Caradisiac pour le travail fourni, et la précision des données qu'ils nous offrent. Maintenant, à nous de jouer !")