# -*- coding: utf-8 -*-
"""
Created on Sat Jan 10 18:34:29 2026

@author: juliette
"""

# src/data_loader.py
import pandas as pd


def string81_to_grid(s: str) -> list[list[int]]:
    """Convertit une chaîne 81 caractères ('0'..'9') en grille 9x9."""
    s = str(s).strip()
    if len(s) != 81:
        raise ValueError(f"Grille invalide: attendu 81 caractères, reçu {len(s)}")
    return [[int(s[i * 9 + j]) for j in range(9)] for i in range(9)]


def load_raw_puzzles(csv_path: str, limit: int | None = 5000) -> list[dict]:
    """
    Charge des grilles depuis le dataset Kaggle (colonnes 'quizzes', 'solutions').
    Retourne une liste temporaire contenant aussi le nombre de zéros.
    """
    df = pd.read_csv(csv_path, usecols=["quizzes", "solutions"])
    if limit is not None:
        df = df.head(limit)

    raw = []
    for _, row in df.iterrows():
        pz = str(row["quizzes"])
        sol = str(row["solutions"])
        raw.append({
            "puzzle": string81_to_grid(pz),
            "solution": string81_to_grid(sol),
            "zeros": pz.count("0"),
        })
    return raw


def assign_difficulty_terciles(raw: list[dict]) -> list[dict]:
    """
    Assigne easy/medium/hard en 3 groupes (1/3-1/3-1/3) selon le nombre de zéros.
    simple, remplaçable plus tard.
    """
    raw_sorted = sorted(raw, key=lambda d: d["zeros"])
    n = len(raw_sorted)
    if n == 0:
        raise ValueError("Aucune grille chargée.")

    one_third = n // 3

    puzzles = []
    for i, item in enumerate(raw_sorted):
        if i < one_third:
            diff = "easy"
        elif i < 2 * one_third:
            diff = "medium"
        else:
            diff = "hard"

        puzzles.append({
            "puzzle": item["puzzle"],
            "solution": item["solution"],
            "difficulty": diff,
        })
    return puzzles


def load_puzzles(csv_path: str, limit: int | None = 5000) -> list[dict]:
    """Fonction unique appelée par le reste du projet"""
    raw = load_raw_puzzles(csv_path, limit=limit)
    return assign_difficulty_terciles(raw)
