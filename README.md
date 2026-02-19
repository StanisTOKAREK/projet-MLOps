Projet MLOps — Industrialisation du modèle Iris
1. Objectif du projet

Ce projet vise à industrialiser le cycle de vie d’un modèle de Machine Learning basé sur le dataset Iris.
L’objectif n’est pas d’optimiser la performance statistique, mais de garantir :

La reproductibilité

La séparation entraînement / inférence

Le déploiement conteneurisé

La sécurité d’exécution

L’observabilité du système

La maintenabilité dans le temps

Le projet transforme un modèle local en un système MLOps structuré et déployable.

2. Architecture du projet

La structure du projet respecte une séparation claire des responsabilités.

api/               Interface FastAPI (exposition HTTP)
src/               Logique métier (entraînement et inférence)
docker/            Dockerfiles pour training et serving
models/            Fichiers générés (model.joblib, metrics.json)
data/              Données (si ajout futur)
docker-compose.yml Orchestration des services
requirements.txt   Dépendances Python

src/train.py

Charge le dataset Iris

Fixe la seed pour la reproductibilité

Effectue un train/test split

Entraîne un modèle RandomForest

Calcule l’accuracy

Sauvegarde :

model.joblib

metrics.json

src/inference.py

Charge le modèle sauvegardé

Expose une fonction de prédiction

Sépare la logique d’inférence de l’entraînement

api/main.py

Charge le modèle au démarrage

Expose les endpoints :

/health

/predict

Valide les entrées via Pydantic

Log la latence des requêtes

3. Reproductibilité

Une graine aléatoire fixe est définie :

SEED = 42


Elle est utilisée pour :

Le générateur aléatoire Python

NumPy

train_test_split

RandomForestClassifier

Cela garantit que deux exécutions identiques produisent les mêmes résultats.

Les métriques enregistrent également la seed utilisée afin d’assurer la traçabilité.

4. Gestion des fichiers produits

Après chaque entraînement, deux fichiers sont générés dans le dossier models/.

model.joblib

Modèle sérialisé avec joblib

Permet de recharger le modèle sans réentraîner

Utilisé par l’API au démarrage

metrics.json

Contient :

Accuracy

Timestamp d’entraînement

Seed utilisée

Ce fichier permet :

La traçabilité

La comparaison entre entraînements

La détection de régression

5. Conteneurisation

Le projet utilise deux Dockerfiles distincts :

Un pour le service d’entraînement

Un pour le service d’inférence (API)

Choix techniques :

Image python:3.11-slim

Pas d’utilisation du tag latest

Exécution avec un utilisateur non-root (mluser)

Variables d’environnement pour la configuration (ex : MODEL_PATH)

6. Orchestration avec Docker Compose

Le fichier docker-compose.yml définit deux services :

Service training

Construit l’image d’entraînement

Exécute train.py

Génère model.joblib et metrics.json

Écrit dans un volume partagé

Service api

Démarre uniquement si training réussit

Monte le même volume models/

Charge le modèle au démarrage

Expose le port 8000

Pipeline global :

Training → model.joblib + metrics.json → API → /predict

7. Déploiement
Prérequis

Docker

Docker Compose

Lancement du pipeline complet
docker compose up --build

8. Vérification du service
Endpoint de santé
http://localhost:8000/health


Permet de vérifier que l’API est active.

Documentation interactive
http://localhost:8000/docs


Interface Swagger générée automatiquement par FastAPI.

9. Exemple de prédiction
curl -X POST \
  http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "sepal_length": 5.1,
    "sepal_width": 3.5,
    "petal_length": 1.4,
    "petal_width": 0.2
}'

10. Gestion d’incident (scénario de dérive)

En cas de dégradation des performances ou de dérive des données :

Analyse des métriques et des logs

Mise à jour des données

Relance du service training

Génération d’un nouveau model.joblib

Redémarrage automatique de l’API avec le nouveau modèle

Cette architecture permet un réentraînement contrôlé sans modification du code applicatif.

Conclusion

Ce projet illustre une démarche MLOps complète :

Séparation des responsabilités

Reproductibilité

Conteneurisation

Sécurité d’exécution

Observabilité

Pipeline automatisé
