# Dots and Boxes

## Introduction
Dots and Boxes est un jeu classique de stratégie joué sur une grille de points. Les joueurs alternent pour relier des points adjacents avec des lignes. Le but est de compléter des carrés pour marquer des points.

Ce projet utilise **Poetry** comme gestionnaire de dépendances et pour la gestion du packaging. Le jeu a été développé en Python et utilise la bibliothèque **pygame** pour la partie graphique.


## Prérequis
Avant de pouvoir exécuter ce projet, vous devez avoir installé :
- **Python 3.11** ou une version compatible
- **Poetry** (gestionnaire de dépendances Python)


## Installation et Execution
1. Clonez ce dépôt :
   ```bash
   git clone https://github.com/nashoba1er/dots-and-boxes.git
   cd dots-and-boxes
2. installez les dépendances :
   ```bash 
   cd dots-and-boxes
   poetry install
3. Executez le jeu : 
   ```bash
   poetry run python dots_and_boxes/main.py

## Structure du projet
.
├── README.md                      # Ce fichier
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
└── tests                           # Tests du projet
    └── test_algos.py

## Fichier `pyproject.toml
Le fichier pyproject.toml est utilisé pour gérer les dépendances et les métadonnées du projet. 

## Auteurs et Licence 
Antoine Dumont
