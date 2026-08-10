# project-path: kanda_reasoner_app/routing_signal_scorer/generator_candidate_human_decision_record_design.py
"""Generator candidate human decision record design for routing scorer v3.

This module is intentionally standard-library-only and human-decision-record-schema-only.
It follows the generator candidate human decision gate and defines how a future
explicit human decision record could be represented. The current record remains
``not_recorded`` and has no approval effect.

It does not record a real human decision, does not infer approval from prior
schemas, does not approve or authorize a candidate patch, does not authorize a
generator, does not install dependencies, does not authorize side effects, does
not generate, write, read, load, or discover semantic artifacts, does not scan
sources, does not materialize raw text, does not generate embeddings or vectors,
does not instantiate providers, does not run semantic scoring, does not modify
router authority, and does not change runtime behavior.
"""

from __future__ import annotations

__all__ = [
    'build_generator_candidate_human_decision_record_contract',
    'classify_generator_candidate_human_decision_record_request',
    'validate_generator_candidate_human_decision_record_contract',
]

from kanda_reasoner_app.routing_signal_scorer._generator_candidate_human_decision_record_schema import (
    build_generator_candidate_human_decision_record_contract as _public_build_generator_candidate_human_decision_record_contract,
    classify_generator_candidate_human_decision_record_request as _public_classify_generator_candidate_human_decision_record_request,
)
from kanda_reasoner_app.routing_signal_scorer._generator_candidate_human_decision_record_validation import (
    validate_generator_candidate_human_decision_record_contract as _public_validate_generator_candidate_human_decision_record_contract,
)

build_generator_candidate_human_decision_record_contract = _public_build_generator_candidate_human_decision_record_contract
classify_generator_candidate_human_decision_record_request = _public_classify_generator_candidate_human_decision_record_request
validate_generator_candidate_human_decision_record_contract = _public_validate_generator_candidate_human_decision_record_contract
