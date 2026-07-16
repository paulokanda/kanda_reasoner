"""Source-preserving compatibility facade."""

from __future__ import annotations

from kanda_reasoner_app.backend_payloads.loader import load_payload

load_payload(__name__, globals(), 'g')
apply_insertions_to_text = globals()['apply_insertions_to_text']; build_module_header_payload = globals()['build_module_header_payload']; has_inline_body = globals()['has_inline_body']; indentation_for_body = globals()['indentation_for_body']; is_overload_function = globals()['is_overload_function']; module_insert_index = globals()['module_insert_index']; module_path_comment = globals()['module_path_comment']; payload_with_optional_uncertainty = globals()['payload_with_optional_uncertainty']; render_docstring_body = globals()['render_docstring_body']; wrap_docstring_lines = globals()['wrap_docstring_lines']
__all__ = ['apply_insertions_to_text', 'build_module_header_payload', 'has_inline_body', 'indentation_for_body', 'is_overload_function', 'module_insert_index', 'module_path_comment', 'payload_with_optional_uncertainty', 'render_docstring_body', 'wrap_docstring_lines']
