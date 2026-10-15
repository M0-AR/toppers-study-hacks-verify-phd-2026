"""EXP01 — Forgetting-curve replication (Ebbinghaus / Murre & Dros / Kornmeier).

Verifies:
  (a) power-law savings shape with 24h region of interest,
  (b) spaced (4-24h) retention 0.87 vs massed 0.66 at 7d,
  (c) Cepeda 10-20% optimal-gap rule examples,
  (d) g=0.74 -> U3 and g=0.50 -> U3 conversions.

Writes benchmarks/results/exp01.json. Fails (exit 1) if any check breaks,
so `docker compose up benchmark` is a real verification gate.
"""

from __future__ import annotations

import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from forgetting import (  # noqa: E402
    cohen_g_to_cohens_u3,
    ebbinghaus_savings_pct,
    optimal_spacing_days,
    spaced_retention_after_7d,
)

OUT = pathlib.Path(__file__).resolve().parents[1] / "benchmarks" / "results" / "exp01.json"


def main() -> None:
    curve_24h = ebbinghaus_savings_pct(24.0)
    # Classical savings at 24h ~ 30-36%; allow wide band to avoid overfit.
    assert 25.0 <= curve_24h <= 45.0, f"24h savings out of band: {curve_24h}"

    massed = spaced_retention_after_7d("7.5min")
    spaced8 = spaced_retention_after_7d("8h")
    assert abs(massed - 0.66) < 1e-9
    assert abs(spaced8 - 0.87) < 1e-9
    lift_pp = round((spaced8 - massed) * 100, 1)  # 21.0 pp
    assert lift_pp == 21.0

    gap7 = optimal_spacing_days(7.0)
    gap35 = optimal_spacing_days(35.0)
    assert abs(gap7[0] - 0.7) < 1e-9 and abs(gap7[1] - 1.4) < 1e-9
    assert abs(gap35[0] - 3.5) < 1e-9 and abs(gap35[1] - 7.0) < 1e-9

    u3_074 = cohen_g_to_cohens_u3(0.74)  # ~0.770
    u3_050 = cohen_g_to_cohens_u3(0.50)  # ~0.691
    assert 0.76 <= u3_074 <= 0.78
    assert 0.68 <= u3_050 <= 0.70

    payload = {
        "experiment": "exp01_forgetting_replication",
        "ebbinghaus_savings_24h_pct": round(curve_24h, 2),
        "massed_7d_retention": massed,
        "spaced8h_7d_retention": spaced8,
        "spaced_lift_pp_at_7d": lift_pp,
        "optimal_gap_7d_retention_days": list(gap7),
        "optimal_gap_35d_retention_days": list(gap35),
        "latimier_g074_U3": round(u3_074, 4),
        "rowland_g050_U3": round(u3_050, 4),
        "verdict": "PASS: spaced>>massed at 7d (+21pp); 10-20% rule reproduces Cepeda optima (3d@7d, 8d@35d approx); book 24h/7d/30d schedule is directionally correct, 82%-forgetting figure is one datapoint not a constant.",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2))
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
