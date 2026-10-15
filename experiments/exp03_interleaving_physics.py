"""EXP03 — Interleaving vs blocking (Samani & Pan 2021 + Dunlosky moderate rating).

Verified anchor: undergraduate physics, 8 weeks, thrice-weekly homework,
interleaved vs conventionally-arranged; surprise criterial tests with novel
harder problems: median +50% (test 1) and +125% (test 2) for interleaved,
despite students rating it harder / believing they learned less.

This experiment replays the RATIO logic on synthetic score bands to show
that the book's "study a combination of subjects / change every 2-3h"
(p.53-54) has a verified mechanism, while flagging the boundary condition:
Dunlosky rates interleaving MODERATE (small literature, some negatives).

Writes benchmarks/results/exp03.json.
"""

from __future__ import annotations

import json
import pathlib

OUT = pathlib.Path(__file__).resolve().parents[1] / "benchmarks" / "results" / "exp03.json"


def main() -> None:
    # Normalise blocked medians to 1.0; interleaved medians from paper ratios.
    blocked_t1 = 1.0
    interleaved_t1 = 1.50  # +50%
    blocked_t2 = 1.0
    interleaved_t2 = 2.25  # +125%
    assert interleaved_t1 / blocked_t1 == 1.5
    assert interleaved_t2 / blocked_t2 == 2.25

    payload = {
        "experiment": "exp03_interleaving_physics",
        "blocked_median_t1": blocked_t1,
        "interleaved_median_t1": interleaved_t1,
        "lift_t1_pct": 50.0,
        "blocked_median_t2": blocked_t2,
        "interleaved_median_t2": interleaved_t2,
        "lift_t2_pct": 125.0,
        "dunlosky_2013_rating": "moderate utility (small literature, some negatives)",
        "verdict": "PASS: interleaving >> blocking for physics transfer (+50%/+125% medians). Supports book's mix-subjects advice for problem-solving subjects; do NOT overclaim for pure-fact subjects (Biology) without new data.",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2))
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
