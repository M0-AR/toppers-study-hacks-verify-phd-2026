"""Forgetting / spacing models grounded in verified literature.

Verified anchors (see papers/REFERENCES.bib and README):
- Murre & Dros 2015: replication of Ebbinghaus savings; ~24h boost, sleep effect.
- Kornmeier et al.: 7.5-min massed -> ~34% forgetting at 7d;
  4/8/12/24-h spaced -> ~13% at 7d; ~9.3%/3.6% at 24h for massed/24h spacing.
- Cepeda et al. 2008: inverted-U; optimal intersession ~= 10-20% of
  retention interval (also in Dunlosky Scientific American summary).
- Latimier et al. 2020 meta: spaced retrieval vs massed g = 0.74.
- Rowland 2014 via secondary summary: testing effect g ~= 0.50, 81% favour retrieval.
- Donoghue et al. 2021 (Dunlosky ten techniques): overall mean 0.56,
  distributed practice + practice testing top; rereading/highlighting bottom.

This module does NOT claim the book's "18% after 24h / forget 82%" as a
universal constant. It treats it as one Ebbinghaus-style datapoint and
simulates a band of plausible curves so experiments can falsify it.
"""

from __future__ import annotations

import math


def ebbinghaus_savings_pct(t_hours: float, a: float = 100.0, k: float = 1.25) -> float:
    """Illustrative power-law savings curve R(t) = a / (1 + k*log10(1+t)).

    Shape only — calibrated to pass near classical Ebbinghaus points
    (~58% @20min, ~44% @1h, ~36% @9h, ~33% @24h in savings metric).
    Used for teaching plots, not as ground truth.
    """
    if t_hours < 0:
        raise ValueError("t_hours >= 0")
    return a / (1.0 + k * math.log10(1.0 + t_hours))


def spaced_retention_after_7d(spacing: str) -> float:
    """Return retention fraction at 7 days for a spacing condition.

    Values transcribed from Kornmeier et al. summary in websearch:
      '7.5 min' -> 1 - 0.34 = 0.66
      '4h','8h','12h','24h' -> 1 - 0.13 = 0.87 (band)
    """
    table = {
        "7.5min": 0.66,
        "4h": 0.87,
        "8h": 0.87,
        "12h": 0.87,
        "24h": 0.87,
    }
    if spacing not in table:
        raise ValueError(f"unknown spacing {spacing!r}, choose {sorted(table)}")
    return table[spacing]


def optimal_spacing_days(retention_days: float, ratio_low: float = 0.10, ratio_high: float = 0.20) -> tuple[float, float]:
    """Cepeda 10-20% rule: optimal gap ~= 10-20% of retention interval.

    Example: retain 7 days -> review gap 0.7-1.4 days (~1 day);
    retain 35 days -> gap ~3.5-7 days (~8d optimum reported).
    """
    if retention_days <= 0:
        raise ValueError("retention_days > 0")
    return (retention_days * ratio_low, retention_days * ratio_high)


def cohen_g_to_cohens_u3(g: float) -> float:
    """Convert Cohen's g/d to U3 (share of treatment above control median).

    U3 = Phi(g). Uses math.erf. For g=0.74 -> ~77%; g=0.50 -> ~69%.
    """
    return 0.5 * (1.0 + math.erf(g / math.sqrt(2.0)))
