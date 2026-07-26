from __future__ import annotations

from dataclasses import dataclass

from kanda_reasoner_app.routing_signal_scorer.ml_advisory_signal import (
    AdvisoryInput,
    MockAdvisor,
    validate_advisory_output,
)

FEATURE_ID = "rss_ml_advisory_prompt_intake_boundary_v1"


def test_output_firewall_accepts_mock_output() -> None:
    output = MockAdvisor().advise(
        AdvisoryInput(
            scenario_id="case-003",
            sanitized_context_hash="hash-003",
            candidate_prompt_group_ids=("group-a",),
            ambiguity_score=0.55,
            conflict_score=0.10,
        )
    )
    validate_advisory_output(output)


def test_output_firewall_rejects_authority_field_names() -> None:
    @dataclass(frozen=True)
    class BadOutput:
        final_route: str

    try:
        validate_advisory_output(BadOutput(final_route="select prompt now"))
    except ValueError as exc:
        assert "Forbidden advisory field name" in str(exc)
    else:
        raise AssertionError("final_route field was accepted")


def test_output_firewall_rejects_rankings_and_free_text_authority() -> None:
    @dataclass(frozen=True)
    class BadOutput:
        advisory_explanation: str

    try:
        validate_advisory_output(BadOutput(advisory_explanation="winner is the best candidate"))
    except ValueError:
        pass
    else:
        raise AssertionError("advisory_explanation was accepted")


def test_output_firewall_rejects_dicts_and_lists() -> None:
    for bad_value in (["a"], {"safe": "no"}):
        try:
            validate_advisory_output(bad_value)
        except TypeError:
            pass
        else:
            raise AssertionError("Mutable or generic output was accepted")


if __name__ == "__main__":
    test_output_firewall_accepts_mock_output()
    test_output_firewall_rejects_authority_field_names()
    test_output_firewall_rejects_rankings_and_free_text_authority()
    test_output_firewall_rejects_dicts_and_lists()
    print(f"VALIDATION OK: {FEATURE_ID}")
