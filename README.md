# Dots and Boxes

## Introduction
Ce projet utilise **Poetry** comme gestionnaire de dépendances et pour la gestion du packaging. Le jeu a été développé en Python et utilise la bibliothèque **pygame** pour la partie graphique.

## Fonctionnalités du jeu

### Description
"Dots and Boxes" est un jeu où deux joueurs s'affrontent pour créer des cases sur un tableau de points. Le but est de fermer le plus de cases possible pour gagner. 

### Commandes
- **Déplacer la souris** : Déplacer le curseur pour sélectionner une ligne ou une colonne.
- **Cliquer sur une ligne/colonne** : Créer une ligne ou une colonne en cliquant entre deux points voisins.
- **Revenir au menu** : Appuyer sur `M` pour revenir au menu principal.
- **Rejouer** : Après une partie, appuyez sur `R` pour recommencer une nouvelle partie avec les mêmes paramètres.
- **Quitter** : Appuyez sur `Q` pour quitter le jeu.

### Interface
Le menu offre la possibilité de choisir les couleurs des deux joueurs, ainsi que celle du fond.
On peut également choisir le mode de jeu : 
- **Joueur VS Joueur**
- **Joueur VS Robot** (niveaux allant de 1 à 5)
- **Robot VS Robot** (niveaux allant de 1 à 5)

Le jeu comporte un tableau de points de dimension au choix sur lequel les joueurs peuvent cliquer pour ajouter des lignes et des colonnes. 
Le but est de fermer des cases en formant un rectangle. 
Un joueur marque un point en complétant une case. 

### Règles du jeu
- Chaque joueur joue à tour de rôle.
- Lorsqu'un joueur ferme une case, il marque un point et doit rejouer.
- Le joueur avec le plus de cases fermées à la fin de la partie gagne.

## Prérequis
Avant de pouvoir exécuter ce projet, vous devez avoir installé :
- **Python 3.11** ou une version compatible
- **Poetry** (gestionnaire de dépendances Python)

## Analyse statique du code
### Outil utilisé : Flake8

L’analyse statique du code est réalisée à l’aide de l’outil Flake8, qui vérifie le respect des normes PEP 8 et détecte d’éventuelles erreurs dans le code.

### Configuration

Le fichier **.flake8** est situé à la racine du projet et contient la configuration suivante :
```bash
[flake8]
max-line-length = 88
ignore = E203, W503
exclude = .git, __pycache__, venv, .venv
```

Ce fichier garantit que le code respecte les normes PEP 8, tout en ignorant certaines règles spécifiques pour des raisons de compatibilité avec les recommandations modernes.

Lien vers la configuration : https://github.com/nashoba1er/dots-and-boxes/blob/main/.flake8

### Installation de Flake8
Pour installer Flake8, exécutez la commande suivante dans un terminal :
```bash
pip install flake8
```

### Exécution de l’analyse statique

Pour analyser le code source avec Flake8, placez-vous à la racine du projet et exécutez la commande suivante :

```bash
flake8
```
Cette commande vérifie tous les fichiers Python du projet. Si des erreurs sont détectées, elles seront affichées dans le terminal avec les informations nécessaires pour les corriger.

## Installation et Execution
1. Clonez ce dépôt :
   ```bash
   git clone https://github.com/nashoba1er/dots-and-boxes.git
   cd dots-and-boxes
2. installez les dépendances :
   ```bash 
   poetry install
3. Executez le jeu : 
   ```bash
   poetry run python dots_and_boxes/main.py

## Packaging
Ce projet utilise Poetry pour générer des fichiers de distribution (.tar.gz et .whl). Pour cela, exécutez la commande suivante :
   ```bash
   poetry build
   ```
## Structure du projet
```bash
├── README.md                       # Ce fichier
├── dist                            # Dossier contenant les fichiers de distribution
│   ├── dots_and_boxes-1.0.0-py3-none-any.whl
│   └── dots_and_boxes-1.0.0.tar.gz
├── dots_and_boxes                  # Code source du jeu
│   ├── __init__.py
│   ├── affichage.py
│   ├── algos.py
│   ├── fonctions_de_jeu.py
│   └── main.py
├── pyproject.toml                 # Configuration du projet (Poetry)
├── poetry.lock                    # Verrouillage des dépendances
└── tests                          # Tests du projet
    └── test_algos.py
```

## Fichier `pyproject.toml
Le fichier pyproject.toml est utilisé pour gérer les dépendances et les métadonnées du projet. 

## Auteurs et Licence 
Antoine Dumont
