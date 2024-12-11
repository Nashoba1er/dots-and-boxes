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
│   ├── main.py
│   └── logger.py 
├── pyproject.toml                 # Configuration du projet (Poetry)
├── poetry.lock                    # Verrouillage des dépendances
└── tests                          # Tests du projet
    └── test_algos.py
```

## Fichier `pyproject.toml
Le fichier pyproject.toml est utilisé pour gérer les dépendances et les métadonnées du projet. 

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

## Automatisation de l’analyse statique avec pre-commit
L’analyse statique est automatisée grâce à un hook pre-commit qui utilise Flake8. Ce hook vérifie automatiquement le code avant chaque commit pour s’assurer qu’il respecte les normes PEP 8.

### Configuration

Le fichier **.pre-commit-config.yaml** configure le hook pour exécuter Flake8 :
```bash
repos:
  - repo: https://github.com/pycqa/flake8
    rev: v6.0.0
    hooks:
      - id: flake8
```

Lien vers la configuration : https://github.com/username/dots-and-boxes/blob/main/.pre-commit-config.yaml

### Installation

1. Installez **pre-commit** :
```bash
pip install pre-commit
```
2. Installez les hooks dans le dépôt :
```bash
pre-commit install
```
3. Testez la configuration en effectuant un commit :
```bash
git add .
git commit -m "Test commit"

```

## Logging dans le projet

Le projet utilise un système de **logging** pour enregistrer les événements importants pendant l'exécution du jeu, afin de faciliter le débogage et la surveillance de l'application.

### Configuration du Logger

Un fichier `logger.py` a été créé pour centraliser la configuration du logger. Le logger est configuré avec les niveaux suivants :

- **DEBUG** : pour les messages détaillés destinés au débogage.
- **INFO** : pour les messages informatifs sur l'exécution normale du jeu.
- **WARNING** : pour signaler des situations non idéales mais non critiques.
- **ERROR** : pour des erreurs qui ne bloquent pas le programme.
- **CRITICAL** : pour des erreurs graves qui peuvent empêcher l'exécution du jeu.

Voici un extrait de la configuration du logger dans le fichier `logger.py` :

```python
# dots_and_boxes/logger.py
import logging

def setup_logger():
    logger = logging.getLogger('dots_and_boxes')
    logger.setLevel(logging.DEBUG)

    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(log_format)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    file_handler = logging.FileHandler('game.log')
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger

logger = setup_logger()


## Auteurs et Licence 
Antoine Dumont
