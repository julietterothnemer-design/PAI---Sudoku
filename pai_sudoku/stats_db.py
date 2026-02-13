from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class StatsSummary:
    total_time_sec: float
    solved_count: int

    @property
    def avg_time_sec(self) -> float:
        return self.total_time_sec / self.solved_count if self.solved_count else 0.0


class StatsDB:
    """Tiny SQLite-backed stats store.

    Stores one row per solved grid.
    """

    def __init__(self, db_path: str | Path | None = None) -> None:
        if db_path is None:
            # default: project_root/stats.sqlite
            project_root = Path(__file__).resolve().parents[1]
            db_path = project_root / "stats.sqlite"

        self.db_path = Path(db_path)
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA journal_mode=WAL;")
        return conn

    def _init_db(self) -> None:
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS runs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    finished_at TEXT NOT NULL DEFAULT (datetime('now')),
                    difficulty TEXT NOT NULL,
                    mode TEXT NOT NULL,
                    duration_sec REAL NOT NULL
                )
                """
            )
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_runs_finished_at ON runs(finished_at)"
            )
            conn.commit()

    def record_solved(self, difficulty: str, mode: str, duration_sec: float) -> None:
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO runs(difficulty, mode, duration_sec) VALUES (?, ?, ?)",
                (difficulty, mode, float(duration_sec)),
            )
            conn.commit()

    def summary(self) -> StatsSummary:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT COALESCE(SUM(duration_sec), 0), COUNT(*) FROM runs"
            ).fetchone()
        total, count = row[0], row[1]
        return StatsSummary(total_time_sec=float(total), solved_count=int(count))

    def reset(self) -> None:
        """Delete all recorded runs."""
        with self._connect() as conn:
            conn.execute("DELETE FROM runs")
            conn.commit()
