import streamlit as st
import pandas as pd
from interactive_application_for_musical_analysis.app_ops import (
    load_data, normalize_data, calculate_genre_metrics, plot_genre_metrics,
    apply_kmeans, plot_clusters, plot_cluster_genres, add_new_data, search_csv
)
import numpy as np 

# Chargement des données CSV
df = load_data("data/dataset.csv")

# Sélectionner les colonnes à normaliser
metrics = ['danceability', 'popularity', 'speechiness', 'acousticness', 'instrumentalness', 'liveness']

# Normalisation des données
df = normalize_data(df, metrics)

# Calcul des moyennes des métriques par genre
genre_metrics = calculate_genre_metrics(df)

# Configuration de la page
st.set_page_config(
    page_title="Maximisez vos ventes musicales",
    page_icon="🎵",
    layout="wide",
)

# Ajout de CSS pour le style
st.markdown(
    """
    <style>
    /* Centrer tout le contenu principal */
    .main {
        text-align: center;
    }

    /* Personnaliser les titres */
    h1 {
        font-family: 'Arial', sans-serif;
        font-size: 3.5em;
        color: #2E3B55;
        text-transform: uppercase;
        font-weight: bold;
        margin-bottom: 0.5em;
    }

    h2 {
        font-family: 'Arial', sans-serif;
        font-size: 2.5em;
        color: #4A6FA5;
        margin-bottom: 0.3em;
    }

    h3 {
        font-family: 'Arial', sans-serif;
        font-size: 1.8em;
        color: #4A6FA5;
        margin-bottom: 0.2em;
    }

    /* Ajuster la taille et l'espacement du contenu */
    p, .markdown-text-container {
        font-size: 1.5em;
        line-height: 1.8em;
        color: #555555;
    }

    /* Styliser les onglets */
    div[role="tablist"] {
        justify-content: center;
        font-size: 1.5em;
        font-weight: bold;
        color: #333333;
    }

    /* Ajouter une couleur d'arrière-plan */
    body {
        background-color: #f7f9fc;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Titre du Dashboard
st.title("MusicMax Dashboard 🎵")

# Création des onglets
tabs = st.tabs(["Accueil", "Dashboard", "Ajouter des Informations", "ChatBot"])

# Onglet Accueil
with tabs[0]:
    st.title("🎵 Bienvenue sur MusicMax 🎵")
    st.subheader("L'application qui aide les producteurs musicaux à maximiser leurs ventes")
    st.markdown(
        """
        **MusicMax** est une application interactive conçue pour vous aider à découvrir 
        les styles musicaux les plus prometteurs pour augmenter vos ventes. Grâce à des 
        analyses de données avancées et une interface conviviale, prenez des décisions 
        éclairées pour booster vos performances dans l'industrie musicale.
        """
    )

# Onglet Dashboard
with tabs[1]:
    st.title("📊 Dashboard")
    st.subheader("Visualisez vos données musicales")

    # Créer un classement des genres par popularité
    genre_popularity = df.groupby('track_genre')['popularity'].mean().sort_values(ascending=False).reset_index()

    # Afficher la liste complète des genres populaires
    top_genres = genre_popularity

    # Sélectionner combien de genres afficher
    num_genres = st.slider(
        "Sélectionner le nombre de genres à afficher",
        min_value=10,
        max_value=int(top_genres.shape[0]),
        value=10,
        step=5
    )

    # Affichage des genres populaires
    st.subheader("Top des genres populaires :")
    for i, row in top_genres.head(num_genres).iterrows():
        st.write(f"{i+1}. {row['track_genre']} (Popularité : {row['popularity']:.2f})")

    # Menu déroulant pour sélectionner un genre
    genre_selector = st.selectbox(
        "Sélectionnez un genre musical",
        df['track_genre'].unique()
    )

    # Affichage du graphique pour le genre sélectionné
    fig = plot_genre_metrics(genre_selector, genre_metrics)
    st.plotly_chart(fig)

    # Appliquer K-Means et visualiser les clusters
    st.subheader("🎯 Regroupement des styles musicaux par K-Means")

    # Choisir le nombre de clusters
    n_clusters = st.slider("Nombre de clusters", min_value=2, max_value=20, value=3, step=1)

    # Appliquer K-Means
    genre_metrics = apply_kmeans(genre_metrics, n_clusters)

    # Visualisation des clusters
    fig_clusters = plot_clusters(genre_metrics)
    st.plotly_chart(fig_clusters)

    # Nouvelle visualisation : Afficher les genres par cluster
    st.subheader("📂 Genres par Cluster")
    fig_cluster_genres = plot_cluster_genres(genre_metrics)
    st.plotly_chart(fig_cluster_genres)

# Onglet Ajouter des Informations
with tabs[2]:
    st.title("📝 Ajouter des Informations")
    st.subheader("Ajoutez des données sur vos styles musicaux")

    # Saisie des informations pour chaque colonne
    new_data = {}
    for col in df.columns:
        if col in ['Unnamed: 0']:
            continue

        if df[col].dtype == 'object':  # Colonnes textuelles
            new_data[col] = st.text_input(f"{col}", placeholder=f"Saisissez la valeur pour {col}")
        
        elif np.issubdtype(df[col].dtype, np.number):  # Colonnes numériques
            min_val, max_val = df[col].min(), df[col].max()
            new_data[col] = st.number_input(
                f"{col}",
                min_value=float(min_val),
                max_value=float(max_val),
                value=float(min_val),
                step=(max_val - min_val) / 100
            )
        
        elif df[col].dtype.name == 'category':  # Colonnes catégoriques
            unique_values = df[col].unique()
            new_data[col] = st.selectbox(f"{col}", options=unique_values)

    # Ajouter un bouton pour soumettre les données
    if st.button("Ajouter"):
        df = add_new_data(df, new_data)
        st.success("Les informations ont été ajoutées avec succès !")
        df.to_csv("data/dataset.csv")

# Onglet ChatBot
with tabs[3]:
    st.title("💬 ChatBot")
    api_key = st.text_input("Enter your Claude API key:", type="password")

    if st.button("Submit"):
        if api_key:
            # Stocker la clé API dans la session
            st.session_state['claude_api_key'] = api_key
            st.success("API key successfully saved!")
        else:
            st.error("Please enter a valid API key.")

    query = st.text_input("Entrez votre question ici :")
    
    if query:
        results = search_csv(query, df)
        if results:
            st.write("Résultats trouvés :")
            st.json(results)
        else:
            st.write("Aucun résultat trouvé.")
