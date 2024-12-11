# Dots and Boxes

## README

Ce fichier README contient une présentation complète du projet **Dots and Boxes**, incluant :

- Une introduction et une description du jeu.
- Les instructions d'installation et d'exécution.
- La gestion des dépendances via Poetry.
- L'analyse statique du code avec Flake8 et pre-commit.
- Le système de logging du projet.
- Les tests unitaires mis en place.
- la façon dont le code est documenté
- la licence

Tout ce qui est nécessaire pour comprendre, installer et utiliser le projet y est détaillé.

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
.
├── LICENCE.txt
├── Makefile
├── README.md
├── build
│   ├── _sources
│   │   └── index.rst.txt
│   ├── genindex.html
│   ├── index.html
│   ├── objects.inv
│   ├── py-modindex.html
│   ├── search.html
│   └── searchindex.js
├── dots_and_boxes
│   ├── __init__.py
│   ├── affichage.py
│   ├── algos.py
│   ├── fonctions_de_jeu.py
│   ├── logger.py
│   └── main.py
├── make.bat
├── poetry.lock
├── pyproject.toml
├── source
│   ├── _static
│   ├── _templates
│   ├── conf.py
│   ├── game.log
│   └── index.rst
└── tests
    ├── __init__.py
    ├── test_algos.py
    └── test_fonctions_de_jeu.py
```

## Fichier `pyproject.toml`
Le fichier pyproject.toml est utilisé pour gérer les dépendances et les métadonnées du projet. 

## Analyse statique du code
### Outil utilisé : Flake8

L’analyse statique du code est réalisée à l’aide de l’outil Flake8, qui vérifie le respect des normes PEP 8 et détecte d’éventuelles erreurs dans le code.

### Configuration

Le fichier `.flake8` est situé à la racine du projet et contient la configuration suivante :
```bash
[flake8]
max-line-length = 88
ignore = E203, W503
exclude = .git, __pycache__, venv, .venv
```

Ce fichier garantit que le code respecte les normes PEP 8, tout en ignorant certaines règles spécifiques pour des raisons de compatibilité avec les recommandations modernes.

Lien vers la [configuration](https://github.com/nashoba1er/dots-and-boxes/blob/main/.flake8)

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

Le fichier `.pre-commit-config.yaml` configure le hook pour exécuter Flake8 :
```bash
repos:
  - repo: https://github.com/pycqa/flake8
    rev: v6.0.0
    hooks:
      - id: flake8
```

Lien vers la [configuration](https://github.com/username/dots-and-boxes/blob/main/.pre-commit-config.yaml)

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

la configuration du logger est dans le fichier  [`logger.py`](https://github.com/Nashoba1er/dots-and-boxes/blob/main/dots_and_boxes/logger.py)

## Tests unitaires

Ce projet utilise des tests unitaires pour valider certaines fonctions essentielles. Les tests sont définis dans le dossier `tests/`, avec un fichier de test principal `test_fonctions_de_jeu.py` qui teste des fonctions spécifiques du module `fonctions_de_jeu.py`.

### Exemples de tests unitaires

Voici un extrait des tests réalisés pour la fonction `carré` :

```python

class TestFonctionsDeJeu(unittest.TestCase):

    def test_carre(self):
        [H,V,C] = [[[0,0,0],[0,0,0],[0,0,0]],
                   [[0,0,0],[0,0,0],[0,0,0]],
                   [[0,0],[0,0]]]
        self.assertEqual(carre([H,C,V], (0,0,255)), False)
        [H,V,C] = [[[1,1,0],[1,0,0],[0,0,0]],
                   [[1,0,0],[0,0,0],[0,0,0]],
                   [[0,0],[0,0]]]
        self.assertEqual(carre([H,C,V], (0,0,255)), True)
```

### Exécution des tests
Pour exécuter les tests, utilisez la commande suivante dans le terminal :
```bash
python -m unittest tests/test_fonctions_de_jeu.py
```

## Documentation

Une documentation complète du projet a été générée avec **Sphinx**.

### Contenu de la documentation

La documentation inclut :

Une description des modules Python : `affichage`, `algos`, `fonctions_de_jeu`, `logger`, et `main`.
Une explication des fonctions, classes, et méthodes avec leurs paramètres et retours.
Des guides pour comprendre l'architecture du projet et les interactions entre ses composants.

### Accéder à la documentation

Pour consulter la documentation, téléchargez le fichier [index.html](https://github.com/Nashoba1er/dots-and-boxes/blob/main/build/index.html), et ouvrez le dans un navigateur.

### Recréer la documentation

Si vous apportez des modifications au code et souhaitez mettre à jour la documentation :

1. Assurez-vous que Sphinx est installé :
```bash
pip install sphinx
```

2. Naviguez dans le dossier `source` et utilisez la commande suivante :
```bash
sphinx-build -b html . ../build/
```


## Auteurs et Licence 

### Licence

Ce projet est sous licence MIT - voir le fichier [LICENSE](https://github.com/Nashoba1er/dots-and-boxes/blob/main/LICENCE.txt) pour plus de détails.

### Auteurs

Projet réalisé par Antoine Dumont

