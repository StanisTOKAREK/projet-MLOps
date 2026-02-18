Projet MLOps - Industrialisation du modèle Iris
1. Introduction
Ce projet vise à industrialiser le cycle de vie d'un modèle de Machine Learning pour la classification des fleurs d'Iris. L'objectif principal est de garantir la reproductibilité, le déploiement sécurisé et l'observabilité du système, plutôt que d'optimiser les performances statistiques du modèle.
+3

2. Architecture du Projet
La structure respecte la séparation des responsabilités entre l'entraînement et l'inférence:


api/ : Code source de l'interface de service FastAPI.

data/ : Stockage des jeux de données.


docker/ : Dockerfiles distincts pour l'entraînement et l'inférence.


models/ : Artefacts du modèle (.joblib) et métriques de performance (.json).
+2


src/ : Logique métier comprenant les scripts d'entraînement et les utilitaires d'inférence.

3. Déploiement et Exécution
Le projet utilise Docker Compose pour orchestrer les conteneurs.

Prérequis
Docker et Docker Compose installés sur la machine hôte.

Installation
Pour lancer le pipeline complet (entraînement suivi de la mise en service de l'API), exécutez :

Bash
docker compose up --build
Validation du service

Point de terminaison de santé : Accédez à http://localhost:8000/health pour vérifier l'état du service.

Documentation API : L'interface Swagger est disponible sur http://localhost:8000/docs.

4. Choix Techniques et Industrialisation
Reproductibilité
Une graine aléatoire fixe (SEED = 42) est appliquée globalement pour garantir que les résultats d'entraînement soient identiques entre différents environnements.

Conteneurisation et Sécurité

Images légères : Utilisation de bases Python-slim sans tag "latest" pour garantir la stabilité du build.


Sécurité Runtime : Les conteneurs s'exécutent avec un utilisateur non-privilégié (mluser), limitant la surface d'attaque en cas de compromission.


Validation des données : L'utilisation de Pydantic dans l'API assure une validation stricte des types de données entrants avant traitement.

Observabilité

Métriques : Un fichier metrics.json est généré à chaque entraînement pour versionner les performances du modèle.
+1


Logs : L'API implémente des logs structurés permettant le suivi de la latence et des volumes de prédiction.

5. Gestion des Incidents (Scénario de Dérive)
Conformément au scénario d'incident simulé (dérive des données ou obsolescence du modèle), la procédure de remédiation est la suivante :


Analyse : Identification de la perte de performance via les métriques ou les logs de l'API.

Mise à jour : Intégration des nouvelles données dans le dossier data/.


Ré-entraînement : Exécution du conteneur de training pour générer un nouvel artefact de modèle.


Redéploiement : L'API recharge automatiquement le nouveau fichier model.joblib stocké sur le volume partagé sans nécessiter de modification du code source.

6. Test de prédiction
Exemple de requête via curl pour tester l'inférence :

curl -X 'POST' \
  'http://localhost:8000/predict' \
  -H 'Content-Type: application/json' \
  -d '{
  "sepal_length": 5.1,
  "sepal_width": 3.5,
  "petal_length": 1.4,
  "petal_width": 0.2
}'