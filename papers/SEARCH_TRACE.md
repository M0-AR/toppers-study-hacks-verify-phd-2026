# Search trace — one search at a time, no parallel websearch (429 avoidance)

Date (UTC): 2026-10-15. All queries sequential.

1. `websearch` deep: "Ebbinghaus forgetting curve systematic spaced repetition 24 hours 7 days evidence 2026"
   -> Kornmeier 12h spacing; Murre&Dros replication; Latimier g=0.74; Cepeda ridgeline; Nature Reviews Psychology spacing+retrieval.
2. `duckduckgo_search`: "testing effect retrieval practice versus rereading Dunlosky 2013 meta-analysis"
   -> Donoghue 2021 meta (242/1619/169179, mean 0.56); Rowland g=0.50 81%; Dunlosky monograph summary.
3. `openresearch_web_search`: "Pomodoro technique focused attention ultradian rhythm study breaks effectiveness"
   -> 25-min vs 90-min ultradian; restorative breaks; 2025 self-regulated Pomodoro/Flowtime study.
4. `paper-search_search_papers` (arxiv,semantic,openalex,crossref): "interleaving blocked practice mathematics physics problem solving Rohrer"
   -> Samani & Pan 2021 npj Science of Learning (+50%/+125% medians, doi 10.1038/s41539-021-00110-x); Nemeth 2019 subtraction.
5. `openresearch_search_openalex`: "sleep memory consolidation review before sleep academic performance"
   -> Feld & Diekelmann 2015 SWS; Gomez-Fonseca & Genzel 2020 timing/chronotype.
6. `agent-reach_search web`: "JEE NEET cutoff marks 2024 2025 easy average difficult question distribution"
   -> NEET 2023: 35.3/46.3/18.4; 2025: 37/45/18; JEE Lumi 599Q 20% numerical 13% hard; SATHEE 15-yr success/time table; qualifying cutoffs 117..162; JEE percentile 93.23 (2024).
7. `kaggle_search_everything`: "student performance exam study habits spaced repetition" -> grading/student-performance kernels.
8. `wiki_search`: "spacing effect" / "spacing effect testing effect primacy recency Dunlosky" -> Spacing effect, Distributed practice, Spaced repetition, Desirable difficulty.
9. `gsd_websearch`: "Cornell notes mind mapping Leitner flashcards evidence 2025 2026" -> empty (no Brave config); recorded as attempted.
10. `openresearch_search_hacker_news`: "spaced repetition Anki medical exams" -> no results; recorded.
11. `openresearch_search_openalex`: "growth mindset goal setting implementation intentions academic achievement" -> Velasquez-Sheehy; Zeeb 2020; Clarke 2023; Verdin 2025 (n=148 mastery->mindset).
12. `paper-search_search_semantic`: "negative marking intelligent guessing multiple choice elimination strategy" -> empty; closed-form EV used instead (verifiable by arithmetic, Monte-Carlo in exp05).
13. `paper-search_search_arxiv`: "retrieval practice test-enhanced learning" -> IR-retrieval false positives; discarded, kept Dunlosky/Rowland from steps 1-2.
14. `websearch` fast: "Dunlosky 2013 ten learning techniques high utility practice testing distributed practice low utility rereading highlighting"
    -> Scientific American + Sage monograph text confirming high/moderate/low tiers.
15. `superpowers_semantic_search_skills`: "reproducible research repository docker compose benchmark evaluation" -> generic guidance only.
16. `openresearch_search_news`: "effective study techniques evidence retrieval practice" -> TOI 2026-10-04, WaPo 2026-09-30 (retrieval over cramming) via DuckDuckGo fallback (GDELT unavailable).
17. `kaggle_kernels_list`: "student exam score prediction" -> 20 hits incl. votes 42/20/238 etc. (public-data voting).
18. `kaggle_datasets_list`: attempted, param error recorded (sort_by enum) — no data invented.

Fallback rule honoured: DuckDuckGo / webfetch-lite bypass noted; no Exa key needed.
Every number in data/ and src/ traces to one of the above or to closed-form arithmetic checked by pytest/exp asserts.
