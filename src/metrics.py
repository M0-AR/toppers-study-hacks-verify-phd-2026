"""Core output metrics from Toppers' Study Hacks STEP 4 (pp.87-105).

Book definitions (verbatim logic, re-implemented):
  speed = total_seconds / attempted
  effective_average_speed = total_seconds / correct
  strike_rate = correct / attempted
  net_score (NEET/JEE +4/-1) = 4*correct - 1*wrong
  M/T score = marks / minutes per subject
  success_gap = cutoff_marks - scored_marks (per subject/total)

All functions are pure, tested, and used by experiments/ and benchmarks/.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TestResult:
    total_questions: int
    attempted: int
    correct: int
    total_seconds: int

    @property
    def wrong(self) -> int:
        return self.attempted - self.correct

    @property
    def unattempted(self) -> int:
        return self.total_questions - self.attempted


def speed_sec_per_q(res: TestResult) -> float:
    """Average seconds per attempted question."""
    if res.attempted <= 0:
        raise ValueError("attempted must be > 0")
    return res.total_seconds / res.attempted


def effective_speed_sec_per_correct(res: TestResult) -> float:
    """Average seconds per *correct* question (book p.89-90)."""
    if res.correct <= 0:
        raise ValueError("correct must be > 0 for effective speed")
    return res.total_seconds / res.correct


def strike_rate(res: TestResult) -> float:
    """Fraction correct among attempted (book p.90)."""
    if res.attempted <= 0:
        raise ValueError("attempted must be > 0")
    return res.correct / res.attempted


def net_score_neet(correct: int, wrong: int, plus: int = 4, minus: int = 1) -> int:
    """NEET/JEE style net score with negative marking."""
    return plus * correct - minus * wrong


def mt_score(marks: float, minutes: float) -> float:
    """Marks-per-minute (book M/T score, p.101-102)."""
    if minutes <= 0:
        raise ValueError("minutes must be > 0")
    return marks / minutes


def success_gap(scored: float, cutoff: float) -> float:
    """Positive means under-performance vs cutoff (book p.104)."""
    return cutoff - scored


def book_table_example() -> TestResult:
    """Book's worked example p.88: 200 Q, 174 attempted, 136 correct, 150 min."""
    return TestResult(total_questions=200, attempted=174, correct=136, total_seconds=150 * 60)
