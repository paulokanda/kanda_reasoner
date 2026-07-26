#!/usr/bin/env python3
"""Validate router/prompt terminal-footer contract enforcement for v15."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FILES = {
    "daily": ROOT / "kanda_prompt_workspace" / "prompt_library" / "ACTIVE_PROMPTS" / "01_session_start_and_navigation" / "daily_patch_delivery_guardrails.md",
    "pre_output": ROOT / "kanda_prompt_workspace" / "prompt_library" / "ACTIVE_PROMPTS" / "03_governance_freeze_and_handoff" / "pre_output_contract_gates.md",
    "router": ROOT / "kanda_prompt_workspace" / "prompt_library" / "ACTIVE_PROMPTS" / "02_prompt_routing_and_indexing" / "prompt_navigation_index.md",
    "pir": ROOT / "kanda_prompt_workspace" / "prompt_library" / "ACTIVE_PROMPTS" / "01_session_start_and_navigation" / "patch_install_delivery_error_register.md",
}

REQUIRED_BY_FILE = {
    "daily": [
        "TERMINAL_FOOTER_SELF_AUDIT_V15_START",
        "Never deliver a KANDA install block without the 5-second success clear footer.",
        "INSTALL OK. Terminal will clear in 5 seconds...",
        "Start-Sleep -Seconds 5",
        "Read-Host \"Press Enter to clear terminal\"",
        "Read-Host \"Press Enter again to finish\"",
        "footer is still a delivery regression",
    ],
    "pre_output": [
        "Terminal footer self-audit gate - v15",
        "Pass criteria for an install block:",
        "Pass criteria for validation, diagnostic, repair, staging-check, freeze-merge,",
        "Never deliver a KANDA install block without the 5-second success clear footer.",
        "Never deliver a validation, diagnostic, staging-check, repair, or other terminal",
    ],
    "router": [
        "TERMINAL_FOOTER_SELF_AUDIT",
        "install blocks require the 5-second `INSTALL OK. Terminal will clear in 5 seconds...` footer",
        "validation, diagnostic, staging-check, repair, freeze/evidence-merge, and all other terminal blocks require Enter",
    ],
    "pir": [
        "PIR-007 - Install success footer omitted from delivered install block",
        "Write-Host \"INSTALL OK\"",
        "user-facing terminal command UX contract",
        "block the answer and repair the command before showing it",
    ],
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    for key, path in FILES.items():
        require(path.is_file(), f"missing required file: {path}")
        text = path.read_text(encoding="utf-8")
        for phrase in REQUIRED_BY_FILE[key]:
            require(phrase in text, f"{key} missing required phrase: {phrase}")

    daily_text = FILES["daily"].read_text(encoding="utf-8")
    pre_text = FILES["pre_output"].read_text(encoding="utf-8")
    combined = daily_text + "\n" + pre_text

    install_success_terms = [
        "INSTALL OK. Terminal will clear in 5 seconds...",
        "Start-Sleep -Seconds 5",
        "Clear-Host",
    ]
    diagnostic_terms = [
        "Read-Host \"Press Enter to clear terminal\"",
        "Read-Host \"Press Enter again to finish\"",
        "Clear-Host",
    ]
    for term in install_success_terms + diagnostic_terms:
        require(term in combined, f"terminal cleanup contract missing term: {term}")

    require(
        combined.count("TERMINAL_FOOTER_SELF_AUDIT_V15_START") >= 2,
        "terminal footer self-audit must be present in both startup guardrail and pre-output gate",
    )

    print("VALIDATION OK: router-terminal-footer-contract-v15")
    print("ROUTER_TERMINAL_FOOTER: install success 5-second footer enforced")
    print("ROUTER_TERMINAL_FOOTER: validation diagnostic enter-enter footer enforced")
    print("ROUTER_TERMINAL_FOOTER: PIR-007 regression registered")
    print("ROUTER_TERMINAL_FOOTER: output-time self-audit required")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
