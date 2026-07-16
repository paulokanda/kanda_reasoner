"""Source-preserving compatibility facade."""

from __future__ import annotations

from kanda_reasoner_app.backend_payloads.loader import load_payload

load_payload(__name__, globals(), 'j')
build_report_row = globals()['build_report_row']; function_report_kind_and_name = globals()['function_report_kind_and_name']; mark_report_rows_for_write_result = globals()['mark_report_rows_for_write_result']; print_post_write_verification = globals()['print_post_write_verification']; result_confidence = globals()['result_confidence']; result_failure_reason = globals()['result_failure_reason']; result_generation_source = globals()['result_generation_source']; result_issues = globals()['result_issues']; result_review_action_hint = globals()['result_review_action_hint']; result_review_severity = globals()['result_review_severity']; result_review_status = globals()['result_review_status']; result_source = globals()['result_source']; write_report_jsonl = globals()['write_report_jsonl']
__all__ = ['build_report_row', 'function_report_kind_and_name', 'mark_report_rows_for_write_result', 'print_post_write_verification', 'result_confidence', 'result_failure_reason', 'result_generation_source', 'result_issues', 'result_review_action_hint', 'result_review_severity', 'result_review_status', 'result_source', 'write_report_jsonl']
