"""Validate Wave 8C enterprise, performance, and legacy boundaries."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any

FEATURE_ID = "prompt-audit-wave8c-enterprise-performance-legacy-boundaries-v1"
MIN_VERSION = (2, 0, 0)


def require(condition: bool, message: str) -> None:
    """Raise a focused validation error when a contract is missing."""
    if not condition:
        raise AssertionError(message)


def read(path: Path) -> str:
    """Read one UTF-8 text artifact."""
    return path.read_text(encoding="utf-8-sig")


def version_tuple(value: str) -> tuple[int, ...]:
    """Parse a numeric semantic version for minimum compatibility checks."""
    parts = str(value).strip().split(".")
    require(parts and all(part.isdigit() for part in parts), "invalid version: " + value)
    return tuple(int(part) for part in parts)


def frontmatter(text: str) -> dict[str, str]:
    """Parse the simple scalar front matter used by these prompts."""
    require(text.startswith("---\n"), "front matter must start at byte zero")
    end = text.find("\n---\n", 4)
    require(end > 4, "front matter terminator missing")
    data: dict[str, str] = {}
    for raw_line in text[4:end].splitlines():
        if not raw_line or raw_line.startswith(" ") or ":" not in raw_line:
            continue
        key, value = raw_line.split(":", 1)
        data[key.strip()] = value.strip()
    return data


def validate_prompt(
    active08: Path,
    meta_root: Path,
    prompt_id: str,
    code: str,
    classification: str,
    required_markers: tuple[str, ...],
    forbidden_markers: tuple[str, ...],
) -> None:
    """Validate one Wave 8C prompt and its canonical metadata."""
    source_path = active08 / (prompt_id + ".md")
    meta_path = meta_root / (prompt_id + ".meta.json")
    require(source_path.is_file(), prompt_id + " source missing")
    require(meta_path.is_file(), prompt_id + " metadata missing")

    source = read(source_path)
    header = frontmatter(source)
    require(header.get("prompt_id") == prompt_id, prompt_id + " source ID mismatch")
    require(header.get("prompt_code") == code, prompt_id + " source code mismatch")
    require(header.get("status") == "active", prompt_id + " source status mismatch")
    require(header.get("load_type") == "on_request", prompt_id + " source load type mismatch")
    require(header.get("owner_box") == "08_python_engineering_core", prompt_id + " source owner mismatch")
    require(version_tuple(header.get("version", "")) >= MIN_VERSION, prompt_id + " source version below minimum")
    require(len(source.splitlines()) <= 500, prompt_id + " exceeds 500 physical lines")

    for marker in required_markers:
        require(marker in source, prompt_id + " required behavior missing: " + marker)
    for marker in forbidden_markers:
        require(marker not in source, prompt_id + " stale doctrine remains: " + marker)

    meta: dict[str, Any] = json.loads(read(meta_path))
    require(meta.get("prompt_id") == prompt_id, prompt_id + " metadata ID mismatch")
    require(meta.get("prompt_code") == code, prompt_id + " metadata code mismatch")
    require(meta.get("classification") == classification, prompt_id + " classification mismatch")
    require(meta.get("canonical_path") == "ACTIVE_PROMPTS/08_python_engineering_core/" + prompt_id + ".md", prompt_id + " canonical path mismatch")
    require(meta.get("category") == "08_python_engineering_core", prompt_id + " metadata category mismatch")
    require(meta.get("status") == "active", prompt_id + " metadata status mismatch")
    require(meta.get("load_type") == "on_request", prompt_id + " metadata load type mismatch")
    require(meta.get("owner_box") == "08_python_engineering_core", prompt_id + " metadata owner mismatch")
    require(meta.get("version") == header.get("version"), prompt_id + " source and metadata version mismatch")
    require(version_tuple(str(meta.get("version", ""))) >= MIN_VERSION, prompt_id + " metadata version below minimum")
    require(meta.get("source_stage") == meta.get("updated_for") and bool(meta.get("source_stage")), prompt_id + " provenance mismatch")
    require(meta.get("box_logic_required") is False, prompt_id + " must not force Box Logic")
    require(meta.get("required_companion_prompts") == [], prompt_id + " must not force companions")


def main() -> int:
    """Run the focused Wave 8C contract."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    args = parser.parse_args()

    root = Path(args.project_root).expanduser().resolve()
    lib = root / "kanda_prompt_workspace/prompt_library"
    active08 = lib / "ACTIVE_PROMPTS/08_python_engineering_core"
    active02 = lib / "ACTIVE_PROMPTS/02_prompt_routing_and_indexing"
    meta_root = lib / "METADATA"
    routing = lib / "ROUTING"

    expected = {
        "python_enterprise_architecture": (
            "KPR-08-005",
            "enterprise_application_pattern_transaction_specialist",
            (
                "Enterprise problem record",
                "Patterns address different forces; they are not a linear maturity ladder",
                "A strong scoped map is the normal semantic model",
                "JWT, `functools.lru_cache`, and `contextvars` are not interchangeable",
                "CQRS-style split only when read and write needs materially diverge",
                "source-write authorization: `NO`",
            ),
            (
                "20+ years of experience",
                "Transaction Script -> Table Module -> Domain Model -> Service Layer",
                "weakref.WeakValueDictionary keyed by",
                "Connection pooling - Essential",
                "All writes go through domain objects",
            ),
        ),
        "python_high_performance": (
            "KPR-08-006",
            "evidence_driven_python_performance_specialist",
            (
                "Record a baseline",
                "small reproducible benchmark",
                "Provide benchmark commands",
                "Correctness equivalence",
                "NO_OPTIMIZATION_JUSTIFIED",
                "source-write authorization: `NO`",
            ),
            (
                "15+ years of experience",
                ">=20% improvement",
                "80% of runtime usually lives in 20% of code",
                "reduces memory by 50-70%",
                "Vectorise or die",
                "gc.disable()",
            ),
        ),
        "python_legacy_code_workflow": (
            "KPR-08-007",
            "legacy_code_stabilization_characterization_specialist",
            (
                "Legacy-risk classification",
                "OBSERVED_UNCONFIRMED",
                "Privacy and side-effect containment",
                "A small testability-enabling change may precede",
                "EMERGENCY_REPAIR",
                "source-write authorization: `NO`",
            ),
            (
                "prompt_id: A022",
                "20+ years of experience",
                "Legacy code is code without tests",
                "Refuse to generate code unless a test is provided or created",
                "importlib.reload is a reliable",
            ),
        ),
    }

    for prompt_id, values in expected.items():
        validate_prompt(active08, meta_root, prompt_id, *values)

    nav = json.loads(read(routing / "prompt_navigation_index.json"))
    entries = {entry.get("prompt_id"): entry for entry in nav.get("entries", [])}
    broad_aliases = {
        "architecture",
        "enterprise",
        "performance",
        "high",
        "code",
        "legacy",
        "workflow",
        "software design",
        "python engineering",
    }
    for prompt_id, (code, _class, _required, _forbidden) in expected.items():
        entry = entries.get(prompt_id)
        require(isinstance(entry, dict), prompt_id + " navigation entry missing")
        require(entry.get("prompt_code") == code, prompt_id + " navigation code mismatch")
        require(entry.get("category") == "08_python_engineering_core", prompt_id + " navigation category mismatch")
        require(entry.get("required_companion_prompts") == [], prompt_id + " navigation companions must be empty")
        aliases = set(entry.get("aliases") or [])
        require(code in aliases, prompt_id + " navigation code alias missing")
        require(not aliases.intersection(broad_aliases), prompt_id + " broad navigation alias remains")

    with (routing / "prompt_route_coverage_table.csv").open(
        "r", encoding="utf-8-sig", newline=""
    ) as handle:
        coverage = {row["prompt_id"]: row for row in csv.DictReader(handle)}
    for prompt_id, (code, _class, _required, _forbidden) in expected.items():
        row = coverage[prompt_id]
        require(code in row["aliases"].split(" | "), prompt_id + " coverage code missing")
        require(row["companions"] == "", prompt_id + " coverage companions must be empty")
        require(
            not broad_aliases.intersection(set(row["aliases"].split(" | "))),
            prompt_id + " broad coverage alias remains",
        )

    nav_md = read(routing / "PROMPT_NAVIGATION_INDEX.md")
    active_nav = read(active02 / "prompt_navigation_index.md")
    substitution = read(active02 / "prompt_substitution_map.md")
    folder = read(active08 / "_FOLDER_ASSIMILATION.md")
    for prompt_id, (code, _class, _required, _forbidden) in expected.items():
        require("**Code:** `" + code + "`" in nav_md, prompt_id + " detailed navigation code missing")
        require(code + " = " + prompt_id in active_nav, prompt_id + " startup navigation route missing")
        require(code + " " + prompt_id in folder, prompt_id + " folder owner record missing")
    require("A022" in substitution and "KPR-08-007" in substitution, "A022 compatibility record missing")
    require("Generic aliases such as `enterprise`, `performance`" in substitution, "broad alias retirement missing")

    startup_map = root / "kanda_prompt_workspace/prompt_tools/STARTUP_ROUTING_KERNEL_SOURCES.json"
    startup_text = read(startup_map)
    for prompt_id in expected:
        require(prompt_id not in startup_text, prompt_id + " must not become directly startup-loaded")

    print("WAVE8C_CLASS08_CANONICAL_IDENTITIES: PASS")
    print("WAVE8C_ENTERPRISE_PATTERN_TRANSACTION_BOUNDARY: PASS")
    print("WAVE8C_PERFORMANCE_EVIDENCE_BOUNDARY: PASS")
    print("WAVE8C_LEGACY_STABILIZATION_BOUNDARY: PASS")
    print("WAVE8C_SOURCE_METADATA_ALIGNMENT: PASS")
    print("WAVE8C_FORWARD_COMPATIBLE_IDENTITY: PASS")
    print("WAVE8C_ROUTING_COMPLETENESS: PASS")
    print("WAVE8C_NO_FORCED_COMPANIONS: PASS")
    print("WAVE8C_NO_STARTUP_PROMOTION: PASS")
    print("WAVE8C_ENTERPRISE_PERFORMANCE_LEGACY_BOUNDARIES_REGRESSION_SET: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
