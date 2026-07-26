from __future__ import annotations

from kanda_reasoner_app.routing_signal_scorer.prompt_intake_boundary import (
    ManualHintStatus,
    add_manual_hint,
    clear_manual_hint,
    remove_manual_hint,
    replace_manual_hint,
)

FEATURE_ID = "rss_ml_advisory_prompt_intake_boundary_v1"


def test_manual_code_hint_add_remove_replace_clear() -> None:
    hint = add_manual_hint("rss-0005")
    assert hint.code.value == "RSS-0005"
    assert hint.status is ManualHintStatus.ACTIVE
    assert hint.is_classification_hint_only() is True

    removed = remove_manual_hint(hint)
    assert removed.status is ManualHintStatus.REMOVED
    assert removed.code.value == "RSS-0005"

    cleared = clear_manual_hint(hint)
    assert cleared.status is ManualHintStatus.CLEARED

    replaced = replace_manual_hint(hint, "FRZ-0005")
    assert replaced.status is ManualHintStatus.REPLACED
    assert replaced.superseded_by is not None
    assert replaced.superseded_by.value == "FRZ-0005"


def test_manual_code_hint_rejects_plain_numeric_code() -> None:
    try:
        add_manual_hint("0005")
    except ValueError:
        pass
    else:
        raise AssertionError("Plain numeric manual code was accepted")


def test_manual_code_hint_is_not_route_authority() -> None:
    hint = add_manual_hint("PROJECT-KANDA-RSS-0005")
    assert hint.is_classification_hint_only() is True
    assert hint.status is ManualHintStatus.ACTIVE
    assert hint.removable is True


if __name__ == "__main__":
    test_manual_code_hint_add_remove_replace_clear()
    test_manual_code_hint_rejects_plain_numeric_code()
    test_manual_code_hint_is_not_route_authority()
    print(f"VALIDATION OK: {FEATURE_ID}")
