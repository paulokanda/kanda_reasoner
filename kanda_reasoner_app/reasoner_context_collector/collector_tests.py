"""Support static evidence collection for Project Reasoner."""

from __future__ import annotations

from pathlib import Path


def link_tests_to_sources(files_payload: list[dict]) -> list[dict]:
    paths = [record["path"] for record in files_payload]
    test_files = [path for path in paths if "test" in Path(path).name.lower()]

    results: list[dict] = []

    for source_path in paths:
        if source_path in test_files:
            continue

        stem = Path(source_path).stem.lower()
        linked = []

        for test_path in test_files:
            test_stem = Path(test_path).stem.lower()
            if stem in test_stem or test_stem in stem:
                linked.append(test_path)

        if linked:
            results.append(
                {
                    "source_file": source_path,
                    "linked_tests": sorted(set(linked)),
                    "confidence": 0.7,
                }
            )

    return results