"""
Created on Sat Jan 10 18:35:09 2026

@author: juliette
"""

# ui/interface_qt.py
import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class CellButton(QPushButton):
    """Bouton représentant une cellule (row, col) du Sudoku."""

    def __init__(self, row: int, col: int):
        super().__init__("")
        self.row = row
        self.col = col
        self.setFixedSize(46, 46)
        self.setFocusPolicy(Qt.NoFocus)


class SudokuWindow(QMainWindow):
    """Fenêtre principale de l'application Sudoku (jouable à la souris)."""

    def __init__(self, game):
        super().__init__()
        self.game = game
        self.selected = None  # (r,c) indices 0..8

        self.setWindowTitle("Sudoku (PAI)")

        central = QWidget()
        self.setCentralWidget(central)

        root = QHBoxLayout()
        central.setLayout(root)

        # Zone gauche: grille 9x9
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(2)
        left = QWidget()
        left.setLayout(self.grid_layout)
        root.addWidget(left)

        # Zone droite: contrôles
        right = QVBoxLayout()
        root.addLayout(right)

        self.info = QLabel("Clique une case, puis clique un chiffre.")
        right.addWidget(self.info)

        right.addWidget(QLabel("Difficulté"))
        self.diff_combo = QComboBox()
        self.diff_combo.addItems(["easy", "medium", "hard"])
        right.addWidget(self.diff_combo)

        right.addWidget(QLabel("Mode"))
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["immediate", "delayed"])
        self.mode_combo.currentTextChanged.connect(self.on_mode_changed)

        right.addWidget(self.mode_combo)

        self.btn_new = QPushButton("Nouvelle grille")
        self.btn_new.clicked.connect(self.new_game)
        right.addWidget(self.btn_new)

        self.btn_solution = QPushButton("Voir la solution")
        self.btn_solution.clicked.connect(self.show_solution)
        right.addWidget(self.btn_solution)

        right.addWidget(QLabel("Entrer un chiffre"))

        # Pavé 1..9
        num_layout = QGridLayout()
        for n in range(1, 10):
            b = QPushButton(str(n))
            b.setFixedSize(44, 44)
            b.setFocusPolicy(Qt.NoFocus)
            b.clicked.connect(lambda checked=False, val=n: self.place_number(val))
            num_layout.addWidget(b, (n - 1) // 3, (n - 1) % 3)
        num_box = QWidget()
        num_box.setLayout(num_layout)
        right.addWidget(num_box)

        self.btn_erase = QPushButton("Effacer")
        self.btn_erase.clicked.connect(self.erase_cell)
        right.addWidget(self.btn_erase)

        right.addStretch(1)

        # Création des 81 boutons
        self.cells = [[CellButton(r, c) for c in range(9)] for r in range(9)]
        for r in range(9):
            for c in range(9):
                btn = self.cells[r][c]
                btn.clicked.connect(
                    lambda checked=False, rr=r, cc=c: self.select_cell(rr, cc)
                )
                self.grid_layout.addWidget(btn, r, c)

        self.new_game()

    # Actions
    def new_game(self):
        diff = self.diff_combo.currentText()
        mode = self.mode_combo.currentText()
        self.game.start_new_game(diff, mode)
        self.selected = None
        self.info.setText(f"Nouvelle grille : {diff} / {mode}")
        self.refresh()

    def on_mode_changed(self, new_mode: str):
        # change le mode sans recharger de grille
        self.game.mode = new_mode
        self.info.setText(f"Mode changé : {new_mode}")

    def select_cell(self, r: int, c: int):
        self.selected = (r, c)
        self.info.setText(f"Case sélectionnée : ligne {r + 1}, colonne {c + 1}")
        self.refresh()

    def place_number(self, value: int):
        if self.selected is None:
            QMessageBox.information(self, "Info", "Clique d'abord une case.")
            return

        r, c = self.selected
        result = self.game.play_move(r, c, value)

        if self.game.mode == "immediate":
            if result is True:
                self.info.setText("Correct")
            elif result is False:
                self.info.setText(f"Incorrect (erreurs : {self.game.errors})")

        self.refresh()

        if self.game.is_finished():
            QMessageBox.information(self, "Bravo", "Sudoku terminé !")

    def erase_cell(self):
        if self.selected is None:
            QMessageBox.information(self, "Info", "Clique d'abord une case.")
            return
        r, c = self.selected
        self.game.erase(r, c)
        self.refresh()

    def show_solution(self):
        sol = self.game.grid.solution
        text = "\n".join(" ".join(str(x) for x in row) for row in sol)
        QMessageBox.information(self, "Solution", text)

    # Affichage
    def refresh(self):
        g = self.game.grid.player_grid
        init = self.game.grid.initial_grid

        for r in range(9):
            for c in range(9):
                btn = self.cells[r][c]
                val = g[r][c]
                btn.setText("" if val == 0 else str(val))

                if init[r][c] != 0:
                    btn.setEnabled(False)
                else:
                    btn.setEnabled(True)

                # CODE DES BORDURES
                top = 3 if r % 3 == 0 else 1
                left = 3 if c % 3 == 0 else 1
                right = 3 if c == 8 else 1
                bottom = 3 if r == 8 else 1

                border_style = (
                    f"border-top: {top}px solid black;"
                    f"border-left: {left}px solid black;"
                    f"border-right: {right}px solid black;"
                    f"border-bottom: {bottom}px solid black;"
                )

                style = border_style + "font-size: 16px;"

                if self.selected == (r, c):
                    style += "background-color: #d0e8ff;"

                btn.setStyleSheet(style)


def run_qt_app(game):
    """Lance l'app Qt"""
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    win = SudokuWindow(game)
    win.show()
    app.exec()
