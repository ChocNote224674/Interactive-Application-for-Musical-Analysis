import streamlit as st
import pandas as pd
from interactive_application_for_musical_analysis.app_ops import (
    load_data, normalize_data, calculate_genre_metrics, plot_genre_metrics,
    apply_kmeans, plot_clusters, plot_cluster_genres, add_new_data, search_csv
)
import numpy as np 
import anthropic

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
    st.write("En fonction du nombre de clusters choisi ci-dessous, voici les genres présents dans chaque cluster")
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

    # Stocker la clé API de Claude dans la session
    if "claude_api_key" not in st.session_state:
        api_key = st.text_input("Entrez votre clé API Claude :", type="password")
        if st.button("Enregistrer la clé API"):
            if api_key:
                st.session_state["claude_api_key"] = api_key
                st.success("Clé API enregistrée avec succès !")
            else:
                st.error("Veuillez saisir une clé API valide.")
    else:
        st.info("Clé API déjà enregistrée.")

    # Initialiser l'historique de conversation s'il n'existe pas
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = ""

    st.markdown("### Historique de la conversation")
    st.text_area("Conversation", value=st.session_state["chat_history"], height=300, disabled=True)

    # Saisie de la question utilisateur
    user_query = st.text_input("Entrez votre question ici :")
    if st.button("Envoyer") and user_query:
        # Recherche dans le CSV pour obtenir des informations pertinentes
        results = search_csv(user_query, df)
        context_info = ""
        if results:
            context_info = "Voici des informations pertinentes extraites des données CSV :\n"
            for r in results:
                context_info += f"- {r}\n"
        
        # Préparer la requête complète avec le contexte éventuel
        full_query = context_info + "\n" + user_query

        # Construire le prompt en incluant l'historique de conversation
        prompt = st.session_state["chat_history"] + f"{HUMAN_PROMPT} {full_query}\n{AI_PROMPT}"
        
        try:
            client = anthropic.Client(st.session_state["claude_api_key"])
            response = client.completion(
                prompt=prompt,
                model="claude-v1",
                max_tokens_to_sample=300,
                stop_sequences=[HUMAN_PROMPT]
            )
            answer = response.completion.strip()

            # Mettre à jour l'historique de conversation
            st.session_state["chat_history"] += f"{HUMAN_PROMPT} {full_query}\n{AI_PROMPT} {answer}\n"

            st.markdown("### Réponse de Claude")
            st.write(answer)
        except Exception as e:
            st.error(f"Erreur lors de l'appel à l'API Claude : {e}")
