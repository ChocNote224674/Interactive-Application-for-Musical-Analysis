import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans

# Fonction pour charger le fichier CSV
def load_data(file_path):
    return pd.read_csv(file_path)

# Fonction de normalisation Min-Max
def normalize_data(df, metrics):
    scaler = MinMaxScaler()
    df[metrics] = scaler.fit_transform(df[metrics])
    return df

# Calculer les moyennes des métriques pour chaque genre
def calculate_genre_metrics(df):
    genre_metrics = df.groupby('track_genre').agg({
        'popularity': 'mean',
        'danceability': 'mean',
        'speechiness': 'mean',
        'acousticness': 'mean',
        'instrumentalness': 'mean',
        'liveness': 'mean'
    }).reset_index()
    return genre_metrics

# Fonction pour générer un graphique des métriques par genre
def plot_genre_metrics(genre, genre_metrics):
    genre_data = genre_metrics[genre_metrics['track_genre'] == genre].melt(id_vars='track_genre', var_name='Métriques', value_name='Valeur')
    fig = px.bar(
        genre_data,
        x='Métriques',
        y='Valeur',
        color='Métriques',
        title=f"Métriques musicales pour le genre {genre}",
        labels={'Valeur': 'Valeur normalisée', 'Métriques': 'Métriques'}
    )
    fig.update_layout(yaxis=dict(range=[0, 1]))
    return fig

# Appliquer K-Means sur les métriques des genres
def apply_kmeans(genre_metrics, n_clusters):
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    genre_metrics['cluster'] = kmeans.fit_predict(genre_metrics.drop(columns=['track_genre']))
    return genre_metrics

# Fonction pour générer un graphique des clusters
def plot_clusters(genre_metrics):
    cluster_sizes = genre_metrics['cluster'].value_counts().reset_index()
    cluster_sizes.columns = ['Cluster', 'Taille']
    fig = px.scatter(
        cluster_sizes,
        x='Cluster',
        y=[1] * len(cluster_sizes),
        size='Taille',
        size_max=100,
        color='Cluster',
        title="Distribution des clusters (Taille proportionnelle au nombre de genres)",
        labels={'Cluster': 'Cluster', 'Taille': 'Nombre de genres'}
    )
    fig.update_yaxes(visible=False)
    return fig

# Fonction pour ajouter des données dans le DataFrame
def add_new_data(df, new_data):
    new_row = pd.DataFrame([new_data])
    df = pd.concat([df, new_row], ignore_index=True)
    return df

# Fonction pour rechercher dans le CSV
def search_csv(query, df):
    results = df[df.apply(lambda row: query.lower() in row.to_string().lower(), axis=1)]
    if not results.empty:
        return results.head(3).to_dict(orient="records")
    return None
