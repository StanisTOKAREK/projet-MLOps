# 🚀 Projet MLOps - Industrialisation d'un modèle de Classification Iris

Ce projet vise à industrialiser le cycle de vie d'un modèle de Machine Learning en suivant les principes MLOps : reproductibilité, conteneurisation, observabilité et sécurité.

## 🏗️ Architecture du Projet
- **`src/`** : Scripts d'entraînement (`train.py`) avec seed fixe et script d'inférence (`inference.py`).
- **`api/`** : Interface FastAPI exposant le modèle.
- **`docker/`** : Dockerfiles isolés pour l'entraînement et le déploiement.
- **`models/`** : Stockage des artefacts (modèle `.joblib`) et des métriques de performance (`.json`).
- **`data/`** : Dossier destiné à recevoir les données d'entrée.

## 🛠️ Installation et Utilisation (Guide pour l'équipe)

Le projet est entièrement conteneurisé. Aucune installation locale de Python n'est requise si vous utilisez Docker ou GitHub Codespaces.

### 1. Lancer l'usine complète
Pour entraîner le modèle et démarrer l'API simultanément, tapez dans votre terminal :
```bash
docker compose up --build
2. Accéder à l'API
Une fois les containers lancés :

Santé et Métriques : Accédez à /health pour voir l'état du système et les stats de latence.

Documentation & Tests : Accédez à /docs pour l'interface interactive Swagger. Vous pourrez y tester des prédictions manuellement.

⚙️ Choix Techniques & MLOps
🔒 Sécurité (Critère 4 & 8)
Utilisateur Non-Root : Les images Docker utilisent l'utilisateur mluser pour limiter les privilèges en cas d'attaque.

Isolation : Utilisation d'un fichier .dockerignore pour éviter d'inclure des données sensibles ou des fichiers inutiles dans les images.

Validation : Les entrées de l'API sont strictement validées par des schémas Pydantic.

🧪 Reproductibilité (Critère 3)
Seed Fixée : Une graine aléatoire (SEED = 42) est utilisée pour garantir que l'entraînement donne toujours le même résultat, peu importe l'ordinateur.

Versionnage : Chaque entraînement génère un fichier metrics.json permettant de suivre la précision du modèle.

📈 Observabilité (Critère 7)
Logs Structurés : L'API génère des logs au format JSON, facilitant l'analyse automatisée.

Monitoring : Suivi en temps réel de la latence de prédiction et du volume de requêtes via l'endpoint de santé.

🚨 Scénario d'Incident & Remédiation (Critère 9)
Problème détecté : Baisse de performance (Data Drift) ou erreur de prédiction. Solution mise en place :

Analyse via les logs JSON pour identifier le moment de la dérive.

Mise à jour du dataset dans le dossier data/.

Relance du container de training : docker compose up --build training.

L'API charge automatiquement le nouvel artefact au redémarrage sans modification du code source.

Projet réalisé dans le cadre du module MLOps (M2).


---

### 🚀 Dernière étape pour toi :
1.  **Copie ce texte** dans ton fichier `README.md`.
2.  **Sauvegarde (Save)**.
3.  **Commit & Push** vers GitHub (comme on l'a vu avec l'icône Source Control).



Tes collègues n'auront plus qu'à lire ce fichier sur la page d'accueil de ton dépôt GitHub pour savoir exactement quoi faire. 

**Souhaites-tu que je t'explique comment tes collègues peuvent maintenant créer leur propre branche pour travailler sans modifier ton code principal ?** (C'est le top pour la collaboration en équipe).