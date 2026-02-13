import copy
import time
from pathlib import Path

import pytest

from pai_sudoku.data_loader import load_puzzles
from pai_sudoku.game import SudokuGame
from pai_sudoku.grid import SudokuGrid
from pai_sudoku.stats_db import StatsDB


# -------------------------
# Helpers: grilles de test
# -------------------------
@pytest.fixture
def sample_puzzle_and_solution():
    """Retourne une paire (puzzle, solution) cohérente.

    - puzzle : grille 9x9 avec des 0 (cases modifiables)
    - solution : grille 9x9 complète
    """
    solution = [
        [5, 3, 4, 6, 7, 8, 9, 1, 2],
        [6, 7, 2, 1, 9, 5, 3, 4, 8],
        [1, 9, 8, 3, 4, 2, 5, 6, 7],
        [8, 5, 9, 7, 6, 1, 4, 2, 3],
        [4, 2, 6, 8, 5, 3, 7, 9, 1],
        [7, 1, 3, 9, 2, 4, 8, 5, 6],
        [9, 6, 1, 5, 3, 7, 2, 8, 4],
        [2, 8, 7, 4, 1, 9, 6, 3, 5],
        [3, 4, 5, 2, 8, 6, 1, 7, 9],
    ]

    # On enlève quelques valeurs (0 = vide / modifiable)
    puzzle = copy.deepcopy(solution)
    puzzle[0][0] = 0
    puzzle[1][1] = 0
    puzzle[4][4] = 0
    puzzle[8][8] = 0

    return puzzle, solution


@pytest.fixture
def sample_puzzles(sample_puzzle_and_solution):
    """Liste de puzzles"""
    puzzle, solution = sample_puzzle_and_solution
    return [
        {"puzzle": puzzle, "solution": solution, "difficulty": "easy"},
        {"puzzle": puzzle, "solution": solution, "difficulty": "medium"},
    ]


# -------------------------
# Tests SudokuGrid
# -------------------------
def test_grid_initial_copy(sample_puzzle_and_solution):
    """player_grid doit être une copie (ne pas aliaser initial_grid)."""
    puzzle, solution = sample_puzzle_and_solution
    g = SudokuGrid(puzzle, solution)

    # On modifie player_grid et on vérifie que initial_grid ne bouge pas
    g.player_grid[0][0] = 9
    assert g.initial_grid[0][0] == 0


def test_fill_cell_only_if_empty(sample_puzzle_and_solution):
    """On ne peut remplir que les cases vides (0) dans la grille initiale."""
    puzzle, solution = sample_puzzle_and_solution
    g = SudokuGrid(puzzle, solution)

    # Case vide dans puzzle => modifiable
    assert g.initial_grid[0][0] == 0
    g.fill_cell(0, 0, 5)
    assert g.player_grid[0][0] == 5

    # Case non vide dans puzzle => non modifiable
    assert g.initial_grid[0][1] == 3
    before = g.player_grid[0][1]
    g.fill_cell(0, 1, 9)
    assert g.player_grid[0][1] == before


def test_erase_cell_only_if_empty(sample_puzzle_and_solution):
    """On ne peut effacer que les cases qui étaient vides au départ."""
    puzzle, solution = sample_puzzle_and_solution
    g = SudokuGrid(puzzle, solution)

    # Case modifiable
    g.fill_cell(0, 0, 5)
    assert g.player_grid[0][0] == 5
    g.erase_cell(0, 0)
    assert g.player_grid[0][0] == 0

    # Case non modifiable
    before = g.player_grid[0][1]
    g.erase_cell(0, 1)
    assert g.player_grid[0][1] == before


def test_is_correct_true_when_matches_solution(sample_puzzle_and_solution):
    puzzle, solution = sample_puzzle_and_solution
    g = SudokuGrid(puzzle, solution)

    g.fill_cell(0, 0, 5)
    assert g.is_correct(0, 0) is True


def test_is_correct_false_when_differs(sample_puzzle_and_solution):
    puzzle, solution = sample_puzzle_and_solution
    g = SudokuGrid(puzzle, solution)

    g.fill_cell(0, 0, 9)
    assert g.is_correct(0, 0) is False


def test_is_completed_false_initially(sample_puzzle_and_solution):
    """Avec des 0 dans le puzzle, ce n'est pas complété."""
    puzzle, solution = sample_puzzle_and_solution
    g = SudokuGrid(puzzle, solution)
    assert g.is_completed() is False


def test_is_completed_true_when_filled_correctly(sample_puzzle_and_solution):
    puzzle, solution = sample_puzzle_and_solution
    g = SudokuGrid(puzzle, solution)

    # Remplir toutes les cases vides correctement
    for i in range(9):
        for j in range(9):
            if g.initial_grid[i][j] == 0:
                g.fill_cell(i, j, solution[i][j])

    assert g.is_completed() is True


# -------------------------
# Tests SudokuGame
# -------------------------
def test_start_new_game_selects_difficulty(sample_puzzles):
    game = SudokuGame(sample_puzzles)
    game.start_new_game(difficulty="easy", mode="immediate")

    assert game.difficulty == "easy"
    assert game.mode == "immediate"
    assert game.errors == 0
    assert isinstance(game.grid, SudokuGrid)


def test_start_new_game_raises_if_no_puzzle_for_difficulty(sample_puzzles):
    game = SudokuGame(sample_puzzles)
    with pytest.raises(ValueError):
        game.start_new_game(difficulty="hard", mode="immediate")


def test_play_move_immediate_correct_increments_nothing(
    sample_puzzles, sample_puzzle_and_solution
):
    puzzle, solution = sample_puzzle_and_solution
    game = SudokuGame(sample_puzzles)
    game.start_new_game(difficulty="easy", mode="immediate")

    # Jouer un coup correct sur une case vide
    assert game.grid.initial_grid[0][0] == 0
    ok = game.play_move(0, 0, solution[0][0])

    assert ok is True
    assert game.errors == 0


def test_play_move_immediate_wrong_increments_error(
    sample_puzzles, sample_puzzle_and_solution
):
    puzzle, solution = sample_puzzle_and_solution
    game = SudokuGame(sample_puzzles)
    game.start_new_game(difficulty="easy", mode="immediate")

    ok = game.play_move(0, 0, 9)  # faux
    assert ok is False
    assert game.errors == 1


def test_play_move_delayed_returns_none(sample_puzzles, sample_puzzle_and_solution):
    puzzle, solution = sample_puzzle_and_solution
    game = SudokuGame(sample_puzzles)
    game.start_new_game(difficulty="easy", mode="delayed")

    out = game.play_move(0, 0, solution[0][0])
    assert out is None
    assert game.errors == 0  # en delayed, pas de compteur d'erreurs


def test_erase_calls_grid(sample_puzzles, sample_puzzle_and_solution):
    puzzle, solution = sample_puzzle_and_solution
    game = SudokuGame(sample_puzzles)
    game.start_new_game(difficulty="easy", mode="immediate")

    game.play_move(0, 0, solution[0][0])
    assert game.grid.player_grid[0][0] == solution[0][0]
    game.erase(0, 0)
    assert game.grid.player_grid[0][0] == 0


def test_show_solution_does_not_crash(sample_puzzles):
    """On teste juste que ça ne lève pas d'exception."""
    game = SudokuGame(sample_puzzles)
    game.start_new_game(difficulty="easy", mode="immediate")
    game.show_solution()


def test_is_finished_true_when_grid_completed(
    sample_puzzles, sample_puzzle_and_solution
):
    puzzle, solution = sample_puzzle_and_solution
    game = SudokuGame(sample_puzzles)
    game.start_new_game(difficulty="easy", mode="immediate")

    # Remplir toutes les cases vides correctement
    for i in range(9):
        for j in range(9):
            if game.grid.initial_grid[i][j] == 0:
                game.play_move(i, j, solution[i][j])

    assert game.is_finished() is True


# -------------------------
# Tests data_loader (intégrité dataset)
# -------------------------
def test_load_puzzles_returns_list():
    """Charge quelques puzzles depuis dataset/sudoku.csv.

    Vérification que le dataset est bien commité et lisible.
    """
    project_root = Path(__file__).resolve().parents[1]
    csv_path = project_root / "dataset" / "sudoku.csv"
    if not csv_path.exists():
        pytest.skip("dataset/sudoku.csv not present (not tracked in git)")

    puzzles = load_puzzles(str(csv_path), limit=10)
    assert isinstance(puzzles, list)
    assert len(puzzles) > 0


def test_loaded_puzzles_have_required_keys():
    project_root = Path(__file__).resolve().parents[1]
    csv_path = project_root / "dataset" / "sudoku.csv"
    if not csv_path.exists():
        pytest.skip("dataset/sudoku.csv not present (not tracked in git)")

    puzzles = load_puzzles(str(csv_path), limit=5)
    required = {"puzzle", "solution", "difficulty"}
    for p in puzzles:
        assert required.issubset(p.keys())


def test_loaded_puzzle_shapes_are_9x9():
    project_root = Path(__file__).resolve().parents[1]

    csv_path = project_root / "dataset" / "sudoku.csv"
    if not csv_path.exists():
        pytest.skip("dataset/sudoku.csv not present (not tracked in git)")
    puzzles = load_puzzles(str(csv_path), limit=3)
    for p in puzzles:
        puzzle = p["puzzle"]
        solution = p["solution"]
        assert len(puzzle) == 9 and all(len(row) == 9 for row in puzzle)
        assert len(solution) == 9 and all(len(row) == 9 for row in solution)


@pytest.fixture
def temp_db(tmp_path: Path) -> StatsDB:
    """DB sqlite temporaire pour tests (ne touche pas stats.sqlite réel)."""
    return StatsDB(tmp_path / "test_stats.sqlite")


def test_statsdb_record_and_summary(temp_db: StatsDB):
    s0 = temp_db.summary()
    assert s0.solved_count == 0
    assert s0.total_time_sec == 0.0
    assert s0.avg_time_sec == 0.0

    temp_db.record_solved("easy", "immediate", 12.5)
    temp_db.record_solved("hard", "delayed", 7.5)

    s1 = temp_db.summary()
    assert s1.solved_count == 2
    assert pytest.approx(s1.total_time_sec, rel=1e-6) == 20.0
    assert pytest.approx(s1.avg_time_sec, rel=1e-6) == 10.0


def test_statsdb_reset(temp_db: StatsDB):
    temp_db.record_solved("easy", "immediate", 1.0)
    assert temp_db.summary().solved_count == 1

    temp_db.reset()
    s = temp_db.summary()
    assert s.solved_count == 0
    assert s.total_time_sec == 0.0


def test_game_records_stats_once(tmp_path: Path):
    """Vérifie que SudokuGame enregistre UNE seule fois quand la grille est terminée."""
    # On force une DB temporaire en remplaçant l'attribut après création
    db = StatsDB(tmp_path / "game_stats.sqlite")

    # Une solution valide + puzzle avec quelques zéros
    solution = [
        [5, 3, 4, 6, 7, 8, 9, 1, 2],
        [6, 7, 2, 1, 9, 5, 3, 4, 8],
        [1, 9, 8, 3, 4, 2, 5, 6, 7],
        [8, 5, 9, 7, 6, 1, 4, 2, 3],
        [4, 2, 6, 8, 5, 3, 7, 9, 1],
        [7, 1, 3, 9, 2, 4, 8, 5, 6],
        [9, 6, 1, 5, 3, 7, 2, 8, 4],
        [2, 8, 7, 4, 1, 9, 6, 3, 5],
        [3, 4, 5, 2, 8, 6, 1, 7, 9],
    ]
    puzzle = [row[:] for row in solution]
    puzzle[0][0] = 0
    puzzle[1][1] = 0

    puzzles = [{"puzzle": puzzle, "solution": solution, "difficulty": "easy"}]
    game = SudokuGame(puzzles)

    # Remplace la DB réelle par la DB temporaire
    game.stats = db

    game.start_new_game("easy", "immediate")

    # Simule une partie finie : on met la grille joueur = solution
    game.grid.player_grid = [row[:] for row in solution]

    # Force un start_time ancien pour avoir une durée > 0
    game._start_time = time.perf_counter() - 5.0

    assert game.is_finished() is True
    assert db.summary().solved_count == 1

    # Appel multiple -> ne doit PAS ré-enregistrer
    assert game.is_finished() is True
    assert db.summary().solved_count == 1
