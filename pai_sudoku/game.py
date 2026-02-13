"""
Created on Wed Nov  17 15:32:10 2025

@author: juliette
"""

# src/game.py
import random

from pai_sudoku.grid import SudokuGrid


class SudokuGame:
    def __init__(self, puzzles):
        """
        puzzles : liste de dico
                 chaque dict contient :
                 - 'puzzle' : grille 9x9 (0 = vide)
                 - 'solution' : grille 9x9 solution
                 - 'difficulty' : 'easy'/'medium'/'hard'
        """
        self.puzzles = puzzles
        self.mode = "immediate"  # "immediate" ou "delayed" mode par défaut
        self.difficulty = "easy"  # "easy", "medium", "hard" easy par defaut
        self.grid = None  # instance de SudokuGrid
        self.errors = 0  # compteur d'erreurs (utile en mode immédiat)

    def start_new_game(self, difficulty, mode):  # lance nouvelle partie :
        # - choisit une grille random de la difficulté demandée
        self.difficulty = difficulty  # - crée l'objet SudokuGrid correspondant
        self.mode = mode
        self.errors = 0

        possible = [p for p in self.puzzles if p["difficulty"] == difficulty]
        if not possible:
            raise ValueError(f"Aucune grille trouvée pour la difficulté : {difficulty}")

        chosen = random.choice(possible)
        self.grid = SudokuGrid(chosen["puzzle"], chosen["solution"])

    def play_move(self, row, col, value):
        """
        joue un coup : remplit une case.
        en mode immediate :
          - renvoie True si correct
          - renvoie False si incorrect (et incrémente errors)
        en mode delayed :
          - renvoie None (pas de feedback immédiat)
        """
        self.grid.fill_cell(row, col, value)

        if self.mode == "immediate":
            if self.grid.is_correct(row, col):
                return True
            else:
                self.errors += 1
                return False
        return None

    def erase(self, row, col):
        """Efface une case (si modifiable)"""
        self.grid.erase_cell(row, col)

    def show_solution(self):
        """Affiche la solution complète"""
        self.grid.show_solution()

    def is_finished(self):
        """Vérifie si la grille est entièrement correcte"""
        return self.grid.is_completed()
