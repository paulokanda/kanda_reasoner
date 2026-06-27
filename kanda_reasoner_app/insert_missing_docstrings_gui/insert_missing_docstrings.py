# kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings.py
"""Insert missing module/class/function docstrings without rewriting other code.

AI CONTEXT - REFACTORED MODULE
This module has been decomposed into submodules.
MANIFEST : kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_help.json
FOLDER   : kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_help/
Read the manifest before editing backend logic here.
"""

from __future__ import annotations

try:
    from .insert_missing_docstrings_help.ast_safety import (
        docstring_free_ast_dump,
        validate_docstring_only_change,
    )
    from .insert_missing_docstrings_help.cli import build_parser, main
    from .insert_missing_docstrings_help.diff_output import diff_text
    from .insert_missing_docstrings_help.heuristic_docstrings import (
        build_class_docstring,
        build_function_docstring,
        build_module_docstring,
        class_summary,
        function_summary,
        iter_function_parameters,
        module_summary,
    )
    from .insert_missing_docstrings_help.insertion_collector import (
        collect_missing_docstring_insertions,
    )
    from .insert_missing_docstrings_help.insertion_formatting import (
        apply_insertions_to_text,
        build_module_header_payload,
        has_inline_body,
        indentation_for_body,
        is_overload_function,
        module_insert_index,
        module_path_comment,
        payload_with_optional_uncertainty,
        render_docstring_body,
        wrap_docstring_lines,
    )
    from .insert_missing_docstrings_help.project_exclusion_rules import (
        is_relaxed_path,
        is_test_like_path,
        iter_python_files,
        iter_selected_python_files,
        load_project_exclusion_rules,
        normalize_rel_path,
        resolve_target_module_path,
        resolve_target_package_path,
        should_exclude_path,
    )
    from .insert_missing_docstrings_help.reporting import (
        build_report_row,
        function_report_kind_and_name,
        mark_report_rows_for_write_result,
        print_post_write_verification,
        result_confidence,
        result_source,
        write_report_jsonl,
    )
    from .insert_missing_docstrings_help.file_processing import (
        collect_changes,
        load_manifest,
    )
    from .insert_missing_docstrings_help.run_orchestrator import run
    from .insert_missing_docstrings_help.source_io import (
        UTF8_BOM,
        parse_source,
        read_source_text,
        write_source_text,
    )
    from .insert_missing_docstrings_help.symbol_naming import (
        expr_to_text,
        extract_internal_import_modules,
        extract_public_symbols,
        prettify_name,
        split_words,
        to_module_id,
    )
except ImportError:
    from insert_missing_docstrings_help.ast_safety import (
        docstring_free_ast_dump,
        validate_docstring_only_change,
    )
    from insert_missing_docstrings_help.cli import build_parser, main
    from insert_missing_docstrings_help.diff_output import diff_text
    from insert_missing_docstrings_help.heuristic_docstrings import (
        build_class_docstring,
        build_function_docstring,
        build_module_docstring,
        class_summary,
        function_summary,
        iter_function_parameters,
        module_summary,
    )
    from insert_missing_docstrings_help.insertion_collector import (
        collect_missing_docstring_insertions,
    )
    from insert_missing_docstrings_help.insertion_formatting import (
        apply_insertions_to_text,
        build_module_header_payload,
        has_inline_body,
        indentation_for_body,
        is_overload_function,
        module_insert_index,
        module_path_comment,
        payload_with_optional_uncertainty,
        render_docstring_body,
        wrap_docstring_lines,
    )
    from insert_missing_docstrings_help.project_exclusion_rules import (
        is_relaxed_path,
        is_test_like_path,
        iter_python_files,
        iter_selected_python_files,
        load_project_exclusion_rules,
        normalize_rel_path,
        resolve_target_module_path,
        resolve_target_package_path,
        should_exclude_path,
    )
    from insert_missing_docstrings_help.reporting import (
        build_report_row,
        function_report_kind_and_name,
        mark_report_rows_for_write_result,
        print_post_write_verification,
        result_confidence,
        result_source,
        write_report_jsonl,
    )
    from insert_missing_docstrings_help.file_processing import (
        collect_changes,
        load_manifest,
    )
    from insert_missing_docstrings_help.run_orchestrator import run
    from insert_missing_docstrings_help.source_io import (
        UTF8_BOM,
        parse_source,
        read_source_text,
        write_source_text,
    )
    from insert_missing_docstrings_help.symbol_naming import (
        expr_to_text,
        extract_internal_import_modules,
        extract_public_symbols,
        prettify_name,
        split_words,
        to_module_id,
    )

__all__ = [
    "UTF8_BOM",
    "apply_insertions_to_text",
    "build_class_docstring",
    "build_function_docstring",
    "build_module_docstring",
    "build_module_header_payload",
    "build_parser",
    "build_report_row",
    "class_summary",
    "collect_changes",
    "collect_missing_docstring_insertions",
    "diff_text",
    "docstring_free_ast_dump",
    "expr_to_text",
    "extract_internal_import_modules",
    "extract_public_symbols",
    "function_report_kind_and_name",
    "function_summary",
    "has_inline_body",
    "indentation_for_body",
    "is_overload_function",
    "is_relaxed_path",
    "is_test_like_path",
    "iter_function_parameters",
    "iter_python_files",
    "iter_selected_python_files",
    "load_manifest",
    "load_project_exclusion_rules",
    "main",
    "mark_report_rows_for_write_result",
    "module_insert_index",
    "module_path_comment",
    "module_summary",
    "normalize_rel_path",
    "parse_source",
    "payload_with_optional_uncertainty",
    "prettify_name",
    "print_post_write_verification",
    "read_source_text",
    "render_docstring_body",
    "resolve_target_module_path",
    "resolve_target_package_path",
    "result_confidence",
    "result_source",
    "run",
    "should_exclude_path",
    "split_words",
    "to_module_id",
    "validate_docstring_only_change",
    "wrap_docstring_lines",
    "write_report_jsonl",
    "write_source_text",
]


if __name__ == "__main__":
    raise SystemExit(main())
