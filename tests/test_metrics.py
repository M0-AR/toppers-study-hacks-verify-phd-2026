"""Smoke tests for book arithmetic — all values verified against text + literature.

Run: pytest -q
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from forgetting import cohen_g_to_cohens_u3, optimal_spacing_days  # noqa: E402
from guessing import breakeven_p, ev_guess  # noqa: E402
from metrics import book_table_example, effective_speed_sec_per_correct, speed_sec_per_q, strike_rate  # noqa: E402


def test_book_table():
    ex = book_table_example()
    assert abs(speed_sec_per_q(ex) - 51.724) < 0.01
    assert abs(effective_speed_sec_per_correct(ex) - 66.176) < 0.01
    assert abs(strike_rate(ex) - 0.7816) < 0.001


def test_guessing_ev():
    assert abs(breakeven_p() - 0.20) < 1e-9
    assert abs(ev_guess(0.25) - 0.25) < 1e-9
    assert abs(ev_guess(0.5) - 1.5) < 1e-9


def test_spacing_rule():
    lo, hi = optimal_spacing_days(7.0)
    assert abs(lo - 0.7) < 1e-9 and abs(hi - 1.4) < 1e-9
    assert 0.76 <= cohen_g_to_cohens_u3(0.74) <= 0.78
