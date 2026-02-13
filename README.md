Rapport de projet MLOps : Industrialisation du Modèle Iris (M2)
1. Présentation du projet
Ce projet a pour objectif l'industrialisation du cycle de vie d'un modèle de classification (Iris dataset). L'architecture repose sur une séparation stricte entre la phase d'entraînement et la phase d'inférence, garantissant la reproductibilité et la stabilité du système en production.

2. Structure du répertoire
api/ : Code source de l'interface FastAPI et logique de service.

src/ : Scripts d'entraînement (train.py) et fonctions d'inférence (inference.py).

docker/ : Fichiers de configuration Docker (Dockerfile) optimisés pour chaque service.

models/ : Volume persistant contenant les artefacts (modèle .joblib et métriques .json).

3. Déploiement et exécution
L'intégralité de la stack est orchestrée par Docker Compose. Pour initialiser l'entraînement puis déployer l'API, utilisez la commande suivante :

Bash
docker compose up --build
Accès aux services :

Endpoint de santé : /health (Statut du service et métriques du modèle).

Inférence : /predict (Endpoint POST pour les prédictions).

Documentation : /docs (Interface Swagger pour les tests unitaires).

4. Choix techniques et conformité
Sécurité et Conteneurisation (Critères 4 et 8)
Utilisateur non-root : L'exécution des containers est déléguée à un utilisateur mluser pour respecter le principe de moindre privilège.

Optimisation des images : Utilisation de distributions python:3.11-slim pour minimiser la surface d'attaque et le poids des images.

Validation Pydantic : Sécurisation de l'endpoint d'inférence par un typage strict des entrées, rejetant toute donnée non conforme avant traitement.

Reproductibilité et Pipeline (Critères 3 et 5)
Fixation de la graine (Seed) : Utilisation d'une constante SEED = 42 pour assurer la constance des résultats d'entraînement entre différents environnements.

Gestion des artefacts : Séparation des métriques et du modèle binaire, permettant un suivi précis des performances via le fichier metrics.json.

Observabilité (Critère 7)
Logging structuré : Implémentation du module logging pour assurer la traçabilité des événements d'entraînement et des erreurs d'API.

Health Monitoring : L'endpoint /health intègre la lecture dynamique des métriques, permettant une surveillance continue de l'intégrité du modèle exposé.

5. Gestion des incidents (Critère 9)
En cas de détection d'une dérive de données (Data Drift) ou d'une baisse d'accuracy constatée via /health :

Mise à jour du dataset source.

Déclenchement d'un nouvel entraînement via le service training.

Rechargement automatique de l'artefact par le service api.

En cas de régression, l'architecture permet un rollback manuel immédiat vers une version antérieure du fichier .joblib présente dans le volume persistant.