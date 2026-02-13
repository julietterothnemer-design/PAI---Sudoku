# Jeu de Sudoku – Projet PAI (Python)
Ce projet consiste à développer un **jeu de Sudoku interactif en Python**, en utilisant :

- Programmation orientée objet
- Interface graphique Qt (PySide6)
- Gestion des dépendances avec **uv**
- Tests automatisés avec **pytest**
- Lint automatique avec **pre-commit**
- Intégration continue via **GitHub Actions**

---

## Objectifs du projet

- Concevoir un jeu de Sudoku jouable sur ordinateur
- Mettre en œuvre une architecture orientée objet claire et modulaire
- Séparer la logique métier et l’interface graphique
- Proposer une interface ergonomique, jouable uniquement à la souris
- Exploiter une base de données externe de grilles de Sudoku
- Appliquer les bonnes pratiques d’ingénierie logicielle

---

##  Fonctionnalités

- Sélection du niveau de difficulté : `easy`, `medium`, `hard`
- Deux modes de jeu :
  - **Immediate** : validation instantanée des coups
  - **Delayed** : vérification uniquement à la fin
- Interface graphique comprenant :
  - grille Sudoku 9×9
  - séparation visuelle des blocs 3×3
  - sélection des cases à la souris
  - pavé numérique (1 à 9)
  - bouton pour effacer une case
  - bouton « Voir la solution »
- Détection automatique de fin de partie correcte

---

##  Architecture du projet

Le projet suit la structure du template `supop-pai` :
PAI---Sudoku/
│
├─ pai_sudoku/ # Code source principal
│ ├─ grid.py # Classe SudokuGrid (gestion grille)
│ ├─ game.py # Classe SudokuGame (logique)
│ ├─ data_loader.py # Chargement du dataset
│ ├─ interface_qt.py # Interface graphique PySide6
│ └─ main_qt.py # Point d’entrée du programme
│
├─ test_pai_sudoku/ # Tests pytest
│
├─ .github/workflows/ # CI GitHub Actions
│
├─ pyproject.toml # Configuration du projet (uv, pytest, etc.)
├─ uv.lock # Lockfile des dépendances
└─ README.md

La logique métier (`grid.py`, `game.py`) est indépendante de l’interface graphique.

---

## Base de données – sudoku.csv

Le projet utilise le dataset Kaggle :

**Sudoku Dataset – Bryan Park**  
https://www.kaggle.com/datasets/bryanpark/sudoku

Le fichier `sudoku.csv` n’est **pas inclus dans le dépôt** (taille > 100MB).

###  Installation du dataset

1. Télécharger `sudoku.csv` depuis Kaggle
2. Créer un dossier à la racine du projet : dataset/
3. Placer le fichier : dataset/sudoku.csv

⚠️ Le fichier est ignoré par Git (`.gitignore`) pour éviter les problèmes de taille.

---

##  Gestion de la difficulté

Le dataset ne fournit pas directement de difficulté.

Une heuristique simple est utilisée :
- tri des grilles selon le nombre de cases vides
- division en trois groupes :
  - `easy`
  - `medium`
  - `hard`

Ce système peut être amélioré ultérieurement.
---

# 🚀 Installation et utilisation

## 🔹 Prérequis

- Python ≥ 3.10
- `uv` installé  
  https://docs.astral.sh/uv/

Vérifier l’installation :

```bash
uv --version
```

---

## 🔹 Installation des dépendances

Depuis la racine du projet :

```bash
uv sync --group test --group dev
```

Cela installe :
- les dépendances principales
- les outils de test (`pytest`)
- les outils de qualité de code (`pre-commit`, `ruff`)

---

## Installation des hooks pre-commit (une seule fois)

```bash
uv run pre-commit install
```

Les vérifications de qualité seront automatiquement exécutées avant chaque commit.

---

# ▶️ Lancer le jeu

```bash
uv run main_qt
```

L’interface graphique Qt s’ouvre et le jeu démarre.

---

# 🧪 Lancer les tests

```bash
uv run pytest -q
```

Les tests couvrent :
- la logique de la grille (`SudokuGrid`)
- la logique du jeu (`SudokuGame`)
- le chargement des données

---

#  Vérifier la qualité du code (lint)

```bash
uv run pre-commit run --all-files
```

---

#  Dataset sudoku.csv

Le fichier `sudoku.csv` n’est pas inclus dans le dépôt (taille > 100MB).

Pour l’utiliser :

1. Télécharger le dataset depuis :
   https://www.kaggle.com/datasets/bryanpark/sudoku

2. Créer un dossier à la racine du projet :

```
dataset/
```

3. Placer le fichier :

```
dataset/sudoku.csv
```

Le fichier est ignoré par Git via `.gitignore`.

---

#  Intégration Continue (CI)

À chaque `push` ou `pull request`, GitHub Actions exécute automatiquement :

- installation des dépendances avec `uv`
- vérification du code avec `pre-commit`
- exécution des tests avec `pytest`

La validation du projet correspond à une CI verte.



