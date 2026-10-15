"""Benchmark runner: executes exp01..exp07 sequentially, aggregates PASS/FAIL.

Usage:
  python benchmarks/run_all.py
  python benchmarks/run_all.py --audit-data   # print data CSV + search trace

Exit code 0 iff all experiments PASS. Writes benchmarks/results/summary.json.
One experiment at a time (avoids the parallel-fetch 429 class of errors).
"""

from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import pathlib
import sys
import traceback

ROOT = pathlib.Path(__file__).resolve().parents[1]
RESULTS = ROOT / "benchmarks" / "results"
EXPS = [
    "exp01_forgetting_replication",
    "exp02_testing_vs_rereading",
    "exp03_interleaving_physics",
    "exp04_speed_strike_selection",
    "exp05_guessing_ev",
    "exp06_neet_distribution_audit",
    "exp07_student_public_data",
]


def run_one(name: str) -> dict:
    path = ROOT / "experiments" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.argv = [str(path)]
    try:
        spec.loader.exec_module(mod)  # type: ignore[union-attr]
        mod.main()
        res_path = RESULTS / f"{name.split('_')[0]}.json"
        # exp0N.json naming: exp01..exp07
        num = name.split("_")[0]
        res_path = RESULTS / f"{num}.json"
        payload = json.loads(res_path.read_text()) if res_path.exists() else {"status": "ran-no-json"}
        return {"experiment": name, "status": "PASS", "payload": payload}
    except Exception as exc:  # noqa: BLE001
        traceback.print_exc()
        return {"experiment": name, "status": "FAIL", "error": f"{type(exc).__name__}: {exc}"}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--audit-data", action="store_true")
    args = ap.parse_args()

    if args.audit_data:
        csv_path = ROOT / "data" / "neet_jee_snapshot_2023_2025.csv"
        print("=== data/neet_jee_snapshot_2023_2025.csv ===")
        print(csv_path.read_text())
        print("=== papers/SEARCH_TRACE.md ===")
        print((ROOT / "papers" / "SEARCH_TRACE.md").read_text())
        return

    RESULTS.mkdir(parents=True, exist_ok=True)
    outcomes = [run_one(n) for n in EXPS]
    passed = sum(1 for o in outcomes if o["status"] == "PASS")
    summary = {
        "total": len(outcomes),
        "passed": passed,
        "failed": len(outcomes) - passed,
        "outcomes": [{k: v for k, v in o.items() if k != "payload"} for o in outcomes],
        "gate": "PASS" if passed == len(outcomes) else "FAIL",
    }
    (RESULTS / "summary.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))
    if summary["gate"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
