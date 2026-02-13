# -*- coding: utf-8 -*-
"""
Created on Wed Nov  7 15:32:10 2025

@author: juliette
"""

# classe rpz une grille de Sudoku

class SudokuGrid:
    def __init__(self, initial_grid, solution):
        """
        initial_grid : liste 9x9 contenant grille de départ (0 = case vide)
        solution     : liste 9x9 contenant solution complète
        """
        self.initial_grid = initial_grid # Grille de départ 

        self.solution = solution # solution  complete

        # grille que le joueur va remplir
        # copie pour pas modif grille initiale
        self.player_grid = [row[:] for row in initial_grid]

    def fill_cell(self, row, col, value):
    
        if self.initial_grid[row][col] == 0:
            self.player_grid[row][col] = value


    def erase_cell(self, row, col):
        """
        erase (corrige) une case si elle était vide ds grille init
        """
        if self.initial_grid[row][col] == 0:
            self.player_grid[row][col] = 0

    def is_correct(self, row, col):
        """
        check si aleur entrée ds une case est ok
        """
        return self.player_grid[row][col] == self.solution[row][col]

    def is_completed(self):
        """
        check si tte la grille correctement remplie
        """
        for i in range(9):
            for j in range(9):
                if self.player_grid[i][j] != self.solution[i][j]:
                    return False
        return True

    def show_solution(self):
        """
        affiche la solution complete du Sudoku
        """
        print("\n--- Solution ---")
        for row in self.solution:
            print(row)

    def display(self):
        """
        affiche la grille actuelle du joueur dans la console
        """
        print("\n--- Grille actuelle ---")
        for i, row in enumerate(self.player_grid):
            line = ""
            for j, value in enumerate(row):
                if value == 0:
                    line += ". "
                else:
                    line += str(value) + " "

                if (j + 1) % 3 == 0 and j < 8:
                    line += "| "

            print(line)
            if (i + 1) % 3 == 0 and i < 8:
                print("- - - + - - - + - - -")
