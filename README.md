🚀 Projet MLOps - Industrialisation du modèle Iris
Ce dépôt contient l'infrastructure nécessaire pour automatiser le cycle de vie d'un modèle de classification Iris. L'objectif est de répondre aux exigences de production : reproductibilité, sécurité, et observabilité.

🏗️ Structure du projet
src/ : Scripts d'entraînement (train.py) avec gestion de la reproductibilité (seed) et logique d'inférence.

api/ : Service FastAPI pour l'exposition du modèle.

docker/ : Dockerfiles optimisés pour le training et le serving.

models/ : Artefacts du modèle (.joblib) et suivi des performances (metrics.json).

data/ : Dossier réservé au stockage des datasets.

🛠️ Guide de démarrage (Équipe)
Le projet est entièrement conteneurisé. Vous n'avez pas besoin d'installer de dépendances Python sur votre machine si vous utilisez Docker ou GitHub Codespaces.

1. Lancer l'environnement
Pour entraîner le modèle et démarrer l'API automatiquement, exécutez la commande suivante à la racine :

Bash
docker compose up --build
2. Tester l'API
Une fois les conteneurs actifs :

Health Check : Allez sur /health pour vérifier l'état du service et les métriques de latence.

Inférence : La documentation interactive (Swagger) est disponible sur /docs. Vous pourrez y tester des prédictions manuellement.

⚙️ Choix techniques
🔒 Sécurité
Privilèges réduits : Les images Docker tournent via un utilisateur non-root (mluser).

Hygiène du code : Un fichier .dockerignore exclut les fichiers sensibles ou inutiles du build.

Validation : Les types de données entrants sont contrôlés par Pydantic pour éviter les erreurs d'exécution.

🧪 Reproductibilité
Seed fixe : Utilisation d'une graine aléatoire fixe (SEED = 42) pour garantir des résultats d'entraînement identiques d'un environnement à l'autre.

Versioning : Chaque run génère un fichier metrics.json pour assurer la traçabilité des performances.

📈 Observabilité
Logs JSON : L'API génère des logs structurés facilitant l'ingestion par des outils de monitoring (ELK, Datadog, etc.).

Monitoring : Suivi en direct de la latence et du statut du modèle via l'endpoint de santé.

🚨 Gestion des incidents (Point 9)
Scénario : Détection d'une baisse de performance ou dérive des données (Data Drift). Procédure de remédiation :

Identification de la dérive via les logs JSON.

Mise à jour du dataset dans le dossier data/.

Ré-entraînement du modèle : docker compose up --build training.

L'API charge automatiquement le nouvel artefact au redémarrage, sans modification du code.

Projet réalisé dans le cadre du module MLOps (M2).
