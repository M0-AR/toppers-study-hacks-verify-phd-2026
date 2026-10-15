"""EXP05 — Intelligent-guessing EV under +4/-1 (book pp.161-163).

Monte-Carlo check: 200k trials per p-level. Asserts:
  EV(blind .25) ≈ +0.25, EV(elim1 .333) ≈ +0.667, EV(elim2 .5) ≈ +1.5,
  breakeven p = 0.20.
Writes benchmarks/results/exp05.json.
"""

from __future__ import annotations

import json
import pathlib
import random
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from guessing import BLIND_P, ELIM1_P, ELIM2_P, breakeven_p, ev_guess  # noqa: E402

OUT = pathlib.Path(__file__).resolve().parents[1] / "benchmarks" / "results" / "exp05.json"
N = 200_000


def mc(p: float, seed: int = 7) -> float:
    rng = random.Random(seed)
    tot = 0
    for _ in range(N):
        tot += 4 if rng.random() < p else -1
    return tot / N


def main() -> None:
    assert abs(breakeven_p() - 0.20) < 1e-9
    assert abs(ev_guess(BLIND_P) - 0.25) < 1e-9
    assert abs(ev_guess(ELIM1_P) - (4 / 3 - 2 / 3)) < 1e-9
    assert abs(ev_guess(ELIM2_P) - 1.5) < 1e-9
    sim = {
        "blind_p25": round(mc(BLIND_P), 3),
        "elim1_p33": round(mc(ELIM1_P), 3),
        "elim2_p50": round(mc(ELIM2_P, seed=8), 3),
    }
    assert 0.15 <= sim["blind_p25"] <= 0.35
    assert 0.55 <= sim["elim1_p33"] <= 0.78
    assert 1.35 <= sim["elim2_p50"] <= 1.65
    payload = {
        "experiment": "exp05_guessing_ev",
        "breakeven_p": 0.20,
        "closed_form_ev": {"blind": 0.25, "elim1": round(4 / 3 - 2 / 3, 4), "elim2": 1.5},
        "montecarlo_ev_200k": sim,
        "verdict": "PASS: any elimination is +EV; even blind guessing is +0.25 EV under +4/-1. Book is right to teach elimination; its caution on blind guessing is risk-management (variance), not EV — disclose both.",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2))
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
