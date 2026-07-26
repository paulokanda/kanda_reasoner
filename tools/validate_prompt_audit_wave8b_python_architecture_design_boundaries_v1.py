"""Validate Wave 8B Python architecture and design boundaries."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

FEATURE_ID = "prompt-audit-wave8b-python-architecture-design-boundaries-v1"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    args = parser.parse_args()
    root = Path(args.project_root).resolve()
    lib = root / "kanda_prompt_workspace/prompt_library"
    active08 = lib / "ACTIVE_PROMPTS/08_python_engineering_core"
    meta_root = lib / "METADATA"
    routing = lib / "ROUTING"

    expected = {
        "python_clean_architecture": (
            "KPR-08-001",
            "python_dependency_direction_specialist",
            (
                "Applicability gate",
                "Ports and adapters",
                "Composition root",
                "Do not perform a ceremonial four-layer rewrite",
                "does not\nauthorize source changes",
            ),
            (
                "20+ years of experience",
                "prioritise the Dependency Rule above all else",
                "exactly four layers",
                "one class per use case",
            ),
        ),
        "python_clean_code": (
            "KPR-08-002",
            "local_python_readability_specialist",
            (
                "Project-style inputs",
                "Duplication and abstraction",
                "Do not enforce a universal line count",
                "does not\nauthorize source changes",
            ),
            (
                "canonical_id: clean_code_python",
                "status: audited_candidate",
                "No flag arguments",
                "Always write docstrings",
            ),
        ),
        "python_design_patterns": (
            "KPR-08-003",
            "pragmatic_python_pattern_selection_specialist",
            (
                "Recommendation outcomes",
                "PYTHON_LANGUAGE_FEATURE",
                "Distinguish the GoF Decorator pattern",
                "does\nnot authorize source mutation",
            ),
            (
                "20+ years of experience",
                "t.\nDesign Patterns Prompt",
                "apply all of them",
                "Exactly one resource instance",
            ),
        ),
        "python_domain_driven_design": (
            "KPR-08-004",
            "strategic_tactical_domain_modeling_specialist",
            (
                "Applicability gate",
                "Bounded Contexts and Context Maps",
                "Domain events and integration events",
                "publishing after commit guarantees delivery",
                "does not authorize source\nchanges",
            ),
            (
                "prompt_id: A023",
                "status: audited_candidate_after_update",
                "ten-business-rule threshold",
                "DDD is Clean Architecture",
            ),
        ),
    }

    for prompt_id, (code, classification, markers, forbidden) in expected.items():
        path = active08 / (prompt_id + ".md")
        require(path.is_file(), prompt_id + " source missing")
        text = read(path)
        require(text.startswith("---\n"), prompt_id + " frontmatter must start at byte zero")
        require("prompt_id: " + prompt_id in text, prompt_id + " canonical source identity missing")
        require("prompt_code: " + code in text, prompt_id + " prompt_code missing")
        require("version: 2.0.0" in text, prompt_id + " version mismatch")
        require("status: active" in text, prompt_id + " status mismatch")
        require("load_type: on_request" in text, prompt_id + " load_type mismatch")
        for marker in markers:
            require(marker in text, prompt_id + " marker missing: " + marker)
        for stale in forbidden:
            require(stale not in text, prompt_id + " stale doctrine remains: " + stale)

        meta = json.loads(read(meta_root / (prompt_id + ".meta.json")))
        require(meta.get("prompt_code") == code, prompt_id + " metadata code mismatch")
        require(meta.get("canonical_path") == "ACTIVE_PROMPTS/08_python_engineering_core/" + prompt_id + ".md", prompt_id + " metadata path mismatch")
        require(meta.get("category") == "08_python_engineering_core", prompt_id + " metadata category mismatch")
        require(meta.get("status") == "active", prompt_id + " metadata status mismatch")
        require(meta.get("version") == "2.0.0", prompt_id + " metadata version mismatch")
        require(meta.get("load_type") == "on_request", prompt_id + " metadata load_type mismatch")
        require(meta.get("classification") == classification, prompt_id + " metadata classification mismatch")
        require(meta.get("box_logic_required") is False, prompt_id + " box_logic_required must be false")
        require(meta.get("required_companion_prompts") == [], prompt_id + " must not force companion loading")

    nav = json.loads(read(routing / "prompt_navigation_index.json"))
    entries = {entry.get("prompt_id"): entry for entry in nav.get("entries", [])}
    broad_aliases = {"clean", "code", "design", "software design", "python engineering", "architecture"}
    for prompt_id, (code, _classification, _markers, _forbidden) in expected.items():
        entry = entries[prompt_id]
        require(entry.get("prompt_code") == code, prompt_id + " navigation code mismatch")
        require(entry.get("category") == "08_python_engineering_core", prompt_id + " navigation category mismatch")
        require(entry.get("required_companion_prompts") == [], prompt_id + " navigation must not force companions")
        aliases = set(entry.get("aliases") or [])
        require(not aliases.intersection(broad_aliases), prompt_id + " retains broad over-routing alias")

    with (routing / "prompt_route_coverage_table.csv").open("r", encoding="utf-8-sig", newline="") as handle:
        coverage = {row["prompt_id"]: row for row in csv.DictReader(handle)}
    for prompt_id, (code, _classification, _markers, _forbidden) in expected.items():
        row = coverage[prompt_id]
        require(code in row["aliases"], prompt_id + " coverage code missing")
        require(row["companions"] == "", prompt_id + " coverage still forces companions")
        require(not broad_aliases.intersection(set(row["aliases"].split(" | "))), prompt_id + " coverage retains broad alias")

    nav_md = read(routing / "PROMPT_NAVIGATION_INDEX.md")
    active_nav = read(lib / "ACTIVE_PROMPTS/02_prompt_routing_and_indexing/prompt_navigation_index.md")
    substitution = read(lib / "ACTIVE_PROMPTS/02_prompt_routing_and_indexing/prompt_substitution_map.md")
    folder = read(active08 / "_FOLDER_ASSIMILATION.md")
    for prompt_id, (code, _classification, _markers, _forbidden) in expected.items():
        require("**Code:** `" + code + "`" in nav_md, prompt_id + " detailed navigation code missing")
        require(code + " = " + prompt_id in active_nav, prompt_id + " active navigation route missing")
        require(code + " " + prompt_id in folder, prompt_id + " folder owner record missing")

    require("clean_code_python" in substitution and "KPR-08-002" in substitution, "Clean Code historical alias missing")
    require("A023" in substitution and "KPR-08-004" in substitution, "DDD historical alias missing")
    require("Do not load them as a default\nbundle" in active_nav, "Independent specialist load rule missing")

    startup_map = root / "kanda_prompt_workspace/prompt_tools/STARTUP_ROUTING_KERNEL_SOURCES.json"
    startup_text = read(startup_map)
    for prompt_id in expected:
        require(prompt_id not in startup_text, prompt_id + " must not become directly startup-loaded")

    print("WAVE8B_CLASS08_CANONICAL_IDENTITIES: PASS")
    print("WAVE8B_CLEAN_ARCHITECTURE_BOUNDARY: PASS")
    print("WAVE8B_CLEAN_CODE_LOCAL_SCOPE: PASS")
    print("WAVE8B_PATTERN_SELECTION_BOUNDARY: PASS")
    print("WAVE8B_DDD_MODELING_BOUNDARY: PASS")
    print("WAVE8B_ROUTING_COMPLETENESS: PASS")
    print("WAVE8B_NO_FORCED_COMPANIONS: PASS")
    print("WAVE8B_NO_STARTUP_PROMOTION: PASS")
    print("WAVE8B_PYTHON_ARCHITECTURE_DESIGN_BOUNDARIES_REGRESSION_SET: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
