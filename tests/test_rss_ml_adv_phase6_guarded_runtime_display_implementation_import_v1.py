from pathlib import Path


MODULE = Path(
    "kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/"
    "guarded_runtime_display.py"
)


def test_phase6_display_implementation_import_boundary():
    text = MODULE.read_text(encoding="utf-8")
    forbidden = (
        "requests",
        "urllib",
        "httpx",
        "socket",
        "subprocess",
        "pickle",
        "sqlite3",
        "open(",
        "Path(",
        "os.",
        "sys.",
    )
    lowered = text.lower()
    for token in forbidden:
        assert token.lower() not in lowered, token

    assert "MockAdvisor" in text
    assert "validate_advisory_output" in text
    assert "route_authority_enabled: bool = False" in text
    assert "router_final_selection_modified: bool = False" in text


if __name__ == "__main__":
    test_phase6_display_implementation_import_boundary()
    print("VALIDATION OK: phase6 display implementation import boundary")
