"""
Main entrypoint for the Qt version of the Sudoku project.

Run with:
    uv run main_qt
"""

from pathlib import Path

from pai_sudoku.data_loader import load_puzzles
from pai_sudoku.game import SudokuGame
from pai_sudoku.interface_qt import run_qt_app


def run() -> None:
    # Project root = folder that contains pyproject.toml
    project_root = Path(__file__).resolve().parents[1]

    # Recommended (HapSight-like): dataset/sudoku.csv
    csv_path = project_root / "dataset" / "sudoku.csv"

    puzzles = load_puzzles(str(csv_path), limit=5000)
    game = SudokuGame(puzzles)

    run_qt_app(game)


if __name__ == "__main__":
    run()
