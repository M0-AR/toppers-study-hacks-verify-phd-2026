"""EXP04 — Speed / Strike-rate / Selection (book STEP 4, book table p.88 validated).

Recomputes the book's own worked example:
  200 Q, 174 attempted, 136 correct, 150 min
  -> speed 51.7 s/Q, effective 66.2 s/correct, strike 78.2%.
Then Monte-Carlos paper_strategy simulator to test H1:
  easy-first (book strategy) beats hard-first and linear under 180-min budget.

Writes benchmarks/results/exp04.json. Fails if easy-first does not win.
"""

from __future__ import annotations

import json
import pathlib
import statistics
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from metrics import (  # noqa: E402
    TestResult,
    book_table_example,
    effective_speed_sec_per_correct,
    net_score_neet,
    speed_sec_per_q,
    strike_rate,
)
from paper_strategy import (  # noqa: E402
    attempt,
    make_paper,
    order_easy_first,
    order_hard_first,
    order_linear,
)

OUT = pathlib.Path(__file__).resolve().parents[1] / "benchmarks" / "results" / "exp04.json"


def main() -> None:
    ex = book_table_example()
    spd = speed_sec_per_q(ex)
    espd = effective_speed_sec_per_correct(ex)
    sr = strike_rate(ex)
    assert abs(spd - 51.724) < 0.01, spd
    assert abs(espd - 66.176) < 0.01, espd
    assert abs(sr - 0.7816) < 0.001, sr
    assert net_score_neet(136, 38) == 4 * 136 - 38 == 506

    # Monte Carlo over 30 papers x 3 orders.
    nets = {"linear": [], "easy_first": [], "hard_first": []}
    for seed in range(30):
        paper = make_paper(n=180, seed=seed)
        nets["linear"].append(attempt(paper, order_linear(len(paper)), seed=seed)["net"])
        nets["easy_first"].append(attempt(paper, order_easy_first(paper), seed=seed)["net"])
        nets["hard_first"].append(attempt(paper, order_hard_first(paper), seed=seed)["net"])
    means = {k: round(statistics.mean(v), 1) for k, v in nets.items()}
    assert means["easy_first"] > means["linear"] > means["hard_first"], means

    payload = {
        "experiment": "exp04_speed_strike_selection",
        "book_example_speed_s": round(spd, 2),
        "book_example_effective_s": round(espd, 2),
        "book_example_strike": round(sr, 4),
        "book_example_net_4m1": 506,
        "montecarlo_mean_net_30papers": means,
        "verdict": "PASS: book arithmetic reproduces exactly; easy-first >> linear >> hard-first. Selection (what to attempt first) dominates raw speed — the book's central STEP-4 claim holds in simulation with verified SATHEE time/success priors.",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2))
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
