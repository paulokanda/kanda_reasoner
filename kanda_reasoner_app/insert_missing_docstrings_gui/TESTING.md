# TESTING.md

Run the automated test suite from the project root:

```bash
python -m unittest discover -s tests -v
```

Useful manual checks:

```bash
python insert_missing_docstrings.py --root benchmark_corpus/benchpkg --scan
python insert_missing_docstrings.py --root benchmark_corpus/benchpkg --diff
python benchmark_runner.py
```
