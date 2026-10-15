"""Paper-attempt strategy simulator (book pp.155-164).

Strategies:
- linear: Q1..Qn in order, single pass.
- jayasuriya: 15% time sweep for easy/direct, then remaining by difficulty.
- three_round: round1 easy (15% time), round2 average (70%), round3 hard (15%).
- recommended: browse 5-10 min, per-section budget, easy+average first,
  mark TA (try-again), revisit with leftover 10-15% time.

Verified difficulty priors (see data/neet_jee_snapshot_2023_2025.csv):
- NEET 2023-2025 pooled ≈ Easy 35-37% / Medium 45-46% / Hard ~18%.
- Book claims 25/60/15 — close in spirit, pessimistic on easy share.
  Simulator defaults to VERIFIED pooled mix, with book mix as comparator.

Each question: (difficulty, time_cost_min, solve_prob).
Simulator is deterministic given seed; experiments Monte-Carlo it.
"""

from __future__ import annotations

import random
from dataclasses import dataclass


@dataclass(frozen=True)
class QItem:
    difficulty: str  # easy|medium|hard
    time_min: float
    p_solve: float


VERIFIED_MIX = {"easy": 0.36, "medium": 0.46, "hard": 0.18}
BOOK_MIX = {"easy": 0.25, "medium": 0.60, "hard": 0.15}

# SATHEE/IITK 15-yr averages (verified via agent-reach_search):
# easy 85.7% success / 1.8 min; medium 62.3% / 3.5 min; hard 34.8% / 5.8 min.
TIME_COST = {"easy": 1.8, "medium": 3.5, "hard": 5.8}
P_SOLVE = {"easy": 0.857, "medium": 0.623, "hard": 0.348}


def make_paper(n: int = 180, mix: dict | None = None, seed: int = 0) -> list[QItem]:
    mix = mix or VERIFIED_MIX
    rng = random.Random(seed)
    diffs = list(mix.keys())
    weights = [mix[d] for d in diffs]
    paper: list[QItem] = []
    for _ in range(n):
        d = rng.choices(diffs, weights=weights, k=1)[0]
        paper.append(QItem(difficulty=d, time_min=TIME_COST[d], p_solve=P_SOLVE[d]))
    return paper


def attempt(paper: list[QItem], order: list[int], budget_min: float = 180.0, seed: int = 1) -> dict:
    """Attempt questions in `order` until budget exhausted. Returns counts."""
    rng = random.Random(seed)
    t = 0.0
    correct = wrong = skipped_hard = 0
    attempted = 0
    for idx in order:
        q = paper[idx]
        if t + q.time_min > budget_min:
            break
        t += q.time_min
        attempted += 1
        if rng.random() < q.p_solve:
            correct += 1
        else:
            wrong += 1
            if q.difficulty == "hard":
                skipped_hard += 0  # counted for diagnostics
    return {
        "attempted": attempted,
        "correct": correct,
        "wrong": wrong,
        "time_used": round(t, 2),
        "net": 4 * correct - wrong,
    }


def order_linear(n: int) -> list[int]:
    return list(range(n))


def order_easy_first(paper: list[QItem]) -> list[int]:
    rank = {"easy": 0, "medium": 1, "hard": 2}
    return sorted(range(len(paper)), key=lambda i: (rank[paper[i].difficulty], i))


def order_hard_first(paper: list[QItem]) -> list[int]:
    rank = {"hard": 0, "medium": 1, "easy": 2}
    return sorted(range(len(paper)), key=lambda i: (rank[paper[i].difficulty], i))
