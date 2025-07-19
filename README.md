# End-to-end-ML-project Template

## Étape 1 : Description du Contexte et du Problème

**Contexte**:  
BNP Paribas Personal Finance, leader du crédit à la consommation en France et en Europe, propose une large gamme de produits financiers à travers de nombreux canaux et partenaires. Face à la montée des risques de fraude, l'entreprise s'appuie sur des modèles analytiques avancés pour sécuriser ses processus de décision et garantir un équilibre entre profitabilité, expérience client et maîtrise du risque. La détection de la fraude est un enjeu stratégique, car les fraudeurs adaptent constamment leurs méthodes pour contourner les systèmes existants, rendant leur identification complexe, d'autant plus que la fraude reste un phénomène rare dans la population.

**Problème à Résoudre**:  
L'objectif de ce challenge est de développer une méthode efficace pour détecter les opérations frauduleuses à partir des données de panier d'achat d'un partenaire de BNP Paribas Personal Finance. Il s'agit de prédire, pour chaque transaction, la probabilité qu'elle soit frauduleuse, afin de pouvoir refuser les dossiers suspects à l'avenir. Ce problème est d'autant plus complexe que la classe frauduleuse est très minoritaire (environ 1,4% des cas), ce qui nécessite des approches adaptées au déséquilibre des classes.

**Données Disponibles**:  
Le jeu de données fourni contient 115 988 observations et 147 variables, décrivant exclusivement le contenu des paniers financés (jusqu'à 24 items par panier, avec des informations détaillées sur chaque item : catégorie, prix, fabricant, modèle, code produit, nombre de produits, etc.). La variable cible `fraud_flag` indique si la transaction a été identifiée comme frauduleuse (1) ou non (0). Les données sont réparties en un échantillon d'entraînement (80%) et un échantillon de test (20%), avec une distribution similaire de la fraude dans chaque sous-ensemble. La métrique d'évaluation principale est l'aire sous la courbe Précision-Rappel (PR-AUC), adaptée à la détection de la classe minoritaire.

## Étape 2 : Sélection, Mise en Place, Tracking et Registry du Modèle
Choix du Modèle: Sélectionnez un modèle approprié en fonction du type de problème (régression, classification, etc.). Justifiez votre choix du modele et les performances attendues.
Mise en Place du Modèle: Implémentez le modèle sélectionné.
Tracking des Expériences: Utilisez des outils de suivi d’expériences comme MLflow, Weights & Biases, ou TensorBoard pour enregistrer les performances du modèle et les hyperparamètres lors de l’optimisation.
Registry du Modèle: Enregistrez votre modèle final dans registre de modèles (Model Registry) avec MLflow, AWS ECR ou d'autres technos.

## Étape 3 : Orchestration du Workflow
Création d’un Workflow Déployé: Concevez et mettez en place un pipeline de données complet qui inclut la prétraitement, l’entraînement et l'évaluation du modèle. Intégrez des outils d’orchestration comme Apache Airflow, Kubeflow ou Prefect pour automatiser les différents composants de votre workflow.

## Étape 4 : Déploiement du Modèle
Containerisation: Conteneriser le code de déploiement du modèle avec des conteneurs Docker.

## Étape 5 : Monitoring du Modèle
Mettez en palce un système de surveillance pour suivre les performances du modèle déployé ainsi que les métriques clés (ex : précision, rappel, temps de réponse).
Créer des Alertes et Reporting.

## Étape 6 : Reproductibilité
Pour la reproductibilité le code doit être facile à exécuter et reproductible. Utilisez des packages comme pipreqs ou pip freeze pour générer un fichier requirements.txt spécifiant toutes les dépendances.
Bonnes Pratiques:
 - Élaborez des tests unitaires et d’intégration pour assurer la qualité du code.
 - Utilisez des hooks pré-commit pour garantir le formatage et la qualité du code avant chaque commit.
 - Configurez un pipeline d'intégration continue/déploiement continu (CI/CD) pour automatiser le processus de test et de déploiement à chaque mise à jour du code.

La liste des étapes n'est pas exhaustive, vous pouvez ajouter, modifier ou supprimer la liste. 
