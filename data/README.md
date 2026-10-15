# Data provenance — live/public data only, no hand-invented numbers
#
# 1) data/neet_jee_snapshot_2023_2025.csv
#    - Transcribed from websearch/agent-reach_search results on 2026-10-15
#      (zollege, targetpublications, lumineet, sathee.iitk.ac.in, unacademy).
#    - Each row keeps a source_hint. Re-verify by re-running:
#        python benchmarks/run_all.py --audit-data
#      which prints the CSV and the search-trace IDs in papers/SEARCH_TRACE.md.
#    - Qualifying cutoffs are percentile-based (50th pct UR/EWS, 40th OBC/SC/ST),
#      NOT fixed marks — this corrects the book's shorthand "62-67%".
#      Admission cutoffs (AIIMS etc.) are far higher; see README §3.4.
#
# 2) Public student-performance datasets (optional, for exp07):
#    - UCI Student Performance (Cortez & Silva) — access via OpenML id 3201 / UCI ML repo.
#    - Kaggle kernels: search "student exam score prediction" (voting step found
#      20+ kernels, e.g. ahmedelawady8, chitranshusinha, raiblaze).
#    - exp07 auto-downloads UCI if network allows, else uses bundled synthetic
#      fallback with identical schema and clearly labels it SYNTHETIC.
#    - No dataset is vendored here to respect licences; loader cites origin.
#
# 3) "Live market data": this repo interprets that as live PUBLIC exam/telemetry
#    data (PYQ analytics, cutoff trackers). It does NOT trade or fetch paid APIs.
#    All live fetches are read-only, cached to benchmarks/results/ with timestamp.
