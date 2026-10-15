"""Negative-marking expected value for intelligent guessing (book pp.161-163).

NEET/JEE scheme modelled: +4 correct, -1 wrong (configurable).
Blind guess among 4: p=0.25 -> EV = 4*0.25 - 1*0.75 = +0.25 > 0.
Eliminate 1: p~=1/3 -> EV = 4/3 - 2/3 = +2/3.
Eliminate 2: p=0.5 -> EV = 4*0.5 - 0.5 = +1.5.
Break-even: 4p - (1-p) = 0 -> p = 0.20.

So the book's advice ("intelligent guessing after eliminating >=1,
cautious blind guessing only with no penalty or when forced") is
directionally correct under +4/-1, but blind guessing is still +EV
on average — variance/risk aversion is the real reason to skip.
Experiment exp05 verifies this by Monte Carlo.
"""

from __future__ import annotations


def ev_guess(p_correct: float, plus: int = 4, minus: int = 1) -> float:
    if not 0.0 <= p_correct <= 1.0:
        raise ValueError("p_correct in [0,1]")
    return plus * p_correct - minus * (1.0 - p_correct)


def breakeven_p(plus: int = 4, minus: int = 1) -> float:
    return minus / (plus + minus)


BLIND_P = 0.25
ELIM1_P = 1.0 / 3.0
ELIM2_P = 0.50
