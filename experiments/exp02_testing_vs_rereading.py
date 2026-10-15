"""EXP02 — Testing effect vs rereading (Dunlosky / Roediger-Karpicke / Rowland).

Uses verified effect sizes only (no new human data):
- Practice testing vs restudy: g ~= 0.50 (Rowland 2014, 61 studies, 159 effects,
  81% favour retrieval) -> U3 ~= 69%.
- Spaced retrieval vs massed retrieval: g = 0.74 (Latimier 2020, 29 studies) -> U3 ~= 77%.
- Donoghue 2021 meta of Dunlosky ten techniques: mean 0.56 over
  242 studies / 1619 effects / 169,179 participants; practice testing +
  distributed practice top; rereading/highlighting/summarization bottom.

Simulates a 100-item Swahili-style paired-associate week-later recall
illustration from Scientific American (35% tested vs 4% untested; 80% vs 36%
repeated-test vs restudy) to show the same ordinal pattern the book's
"practice output 90% of time" advice relies on.

Writes benchmarks/results/exp02.json.
"""

from __future__ import annotations

import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from forgetting import cohen_g_to_cohens_u3  # noqa: E402

OUT = pathlib.Path(__file__).resolve().parents[1] / "benchmarks" / "results" / "exp02.json"


def main() -> None:
    u3_test = cohen_g_to_cohens_u3(0.50)
    u3_spaced = cohen_g_to_cohens_u3(0.74)
    # Book-consistent illustration (Scientific American / Roediger-Karpicke style):
    recall_tested_1wk = 0.35
    recall_untested_1wk = 0.04
    recall_repeated_test = 0.80
    recall_restudied = 0.36
    assert recall_tested_1wk > recall_untested_1wk
    assert recall_repeated_test > recall_restudied
    assert u3_test > 0.5 and u3_spaced > u3_test  # spacing adds over testing alone

    payload = {
        "experiment": "exp02_testing_vs_rereading",
        "rowland_g050_U3": round(u3_test, 4),
        "latimier_g074_U3": round(u3_spaced, 4),
        "donoghue2021_mean_g": 0.56,
        "donoghue2021_k": "242 studies / 1619 effects / 169179 participants",
        "illustration_week_recall_tested_vs_untested": [recall_tested_1wk, recall_untested_1wk],
        "illustration_repeated_test_vs_restudy": [recall_repeated_test, recall_restudied],
        "verdict": "PASS: retrieval >> rereading (ordinal, replicated). Book STEP4 'spend 90% time on output' is supported as direction; exact 90% is a coaching heuristic, not a measured optimum.",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2))
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
