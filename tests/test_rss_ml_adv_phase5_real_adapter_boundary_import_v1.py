from pathlib import Path

MODULES = (
    Path("kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/real_adapter_boundary_contract.py"),
    Path("kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/offline_real_adapter_boundary.py"),
)

FORBIDDEN_IMPORT_SNIPPETS = (
    "import requests",
    "from requests",
    "import openai",
    "from openai",
    "import anthropic",
    "from anthropic",
    "import httpx",
    "from httpx",
    "import urllib",
    "from urllib",
    "import socket",
    "from socket",
    "import sqlite3",
    "import pickle",
)

FORBIDDEN_CALL_SNIPPETS = (
    ".post(",
    ".get(",
    "open(",
    "Path(",
    "write_text(",
    "read_text(",
)


def test_phase5_real_adapter_boundary_has_no_forbidden_imports_or_io_calls():
    for module_path in MODULES:
        text = module_path.read_text(encoding="utf-8")
        for snippet in FORBIDDEN_IMPORT_SNIPPETS:
            assert snippet not in text, (module_path, snippet)
        for snippet in FORBIDDEN_CALL_SNIPPETS:
            assert snippet not in text, (module_path, snippet)


print("VALIDATION OK: test_rss_ml_adv_phase5_real_adapter_boundary_import_v1")
