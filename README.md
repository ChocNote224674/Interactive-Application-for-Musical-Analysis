# 🎵 MusicMax - Optimisation des Ventes Musicales avec IA


## URL du projet déployé sur Streamlit

URL Streamlit : https://interactive-application-for-musical-analysis-ztfwxe3srmsb3cdkm.streamlit.app/

## 📌 Description
MusicMax est une application interactive conçue pour aider les producteurs musicaux à maximiser leurs ventes en exploitant l’analyse de données et l’intelligence artificielle.

L’application permet :
- **L’analyse des tendances musicales** grâce à des métriques comme la popularité, la dansabilité, etc.
- **La visualisation des clusters de genres musicaux** en utilisant l’algorithme K-Means.
- **L’ajout et la recherche de nouvelles données** afin de maintenir l'analyse à jour.
- **L'utilisation d'un chatbot alimenté par l’API Claude** (Anthropic) pour fournir des conseils basés sur les données du dataset.

## 🛠️ Installation et Exécution

### 📥 Prérequis
- **Python 3.8+**
- **Poetry** (pour la gestion des dépendances)

### 🚀 Installation
1. **Clonez le projet** :
   ```bash
   git clone <URL_DU_DEPOT>
   cd MusicMax
   
2. **Installez les dépendances avec Poetry**
   ```bash
   poetry install
## Lancer L'application 
1. **Activez l'environnement virtuel**
   ```bash
   poetry shell
   
2. **Demarrez Streamlit**
   ```bash
   streamlit run app.py

## Structure du Projet
   ```bash
   MusicMax/
   │── data/           # Dossier contenant le dataset CSV
   │── dist/           # Dossier de distribution (paquets compilés)
   │── src/            # Code source principal
   │── tests/          # Tests unitaires et d'intégration
   │── app.py          # Script principal Streamlit
   │── poetry.lock     # Verrouillage des dépendances
   │── pyproject.toml  # Configuration de Poetry ```





   
   
