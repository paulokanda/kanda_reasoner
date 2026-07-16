# Benchmarks and rollout checks

## Benchmark corpus
Use `benchmark_corpus/benchpkg` as the first quality gate. It includes:

- module exports in `__init__.py`
- plain utility functions
- keyword-only parameters
- a property
- async methods
- overload stubs
- explicit `raise` statements
- a dataclass

## Run commands

Heuristic baseline:

```bash
python benchmark_runner.py --output benchmark_report_heuristic.json
```

AI baseline:

```bash
python benchmark_runner.py --ai --workers 4 --min-confidence medium --output benchmark_report_ai.json
```

Custom config:

```bash
python benchmark_runner.py --ai ai_config.example.json --workers 4 --output benchmark_report_custom.json
```

## Minimum rollout checks

Before broad `--write --ai` use, verify:

1. `scan.exit_code == 0`
2. `diff.exit_code == 0`
3. `write.exit_code == 0`
4. `post_write_scan.summary.files_with_missing_docstrings == 0`
5. `write.files_written > 0`
6. `diff.fallbacks` is understood and acceptable
7. `diff.low_confidence_events` is reviewed
8. no invalid Python is written
9. generated diffs are acceptable to human review

## Suggested rollout path

1. Run heuristic benchmark first.
2. Run AI benchmark with the local model unavailable to verify safe fallback.
3. Run AI benchmark with the local model available.
4. Review diffs manually on the benchmark corpus.
5. Run against a small real project copy before broader use.
