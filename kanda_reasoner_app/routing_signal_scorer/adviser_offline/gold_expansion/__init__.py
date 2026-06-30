# project-path: kanda_reasoner_app/routing_signal_scorer/adviser_offline/gold_expansion/__init__.py
"""Offline advisory gold-set expansion planning helpers.

M15 exports pure in-memory plan builders only. It does not create gold cases,
persist plan records, mutate gold data, run candidates, or grant router
authority.
"""

from .gold_set_expansion_plan import (
    FEATURE_ID,
    SCHEMA_VERSION,
    assert_gold_set_expansion_plan_valid,
    build_gold_set_expansion_plan,
    validate_gold_set_expansion_plan,
)

__all__ = [
    "FEATURE_ID",
    "SCHEMA_VERSION",
    "assert_gold_set_expansion_plan_valid",
    "build_gold_set_expansion_plan",
    "validate_gold_set_expansion_plan",
]
