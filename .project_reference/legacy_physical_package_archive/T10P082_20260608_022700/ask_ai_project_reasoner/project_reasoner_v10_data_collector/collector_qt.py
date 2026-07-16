"""Support static evidence collection for Project Reasoner."""

# developer_tools/kanda_reasoner_app/reasoner_context_collector/collector_qt.py

from __future__ import annotations

from typing import Any


def _extract_target_from_call(call: dict[str, Any]) -> tuple[str, str, float]:
    raw_target = call.get("target", "")
    target = str(raw_target or "").strip()

    if target and target.lower() != "unknown":
        lowered = target.lower()

        if lowered.startswith("lambda"):
            return target, "lambda", 0.75

        if "partial(" in lowered:
            return target, "partial", 0.80

        if "." in target:
            return target, "method", 0.95

        return target, "function", 0.90

    lambda_target = str(call.get("lambda_target", "") or "").strip()
    if lambda_target:
        return lambda_target, "lambda", 0.75

    partial_target = str(call.get("partial_target", "") or "").strip()
    if partial_target:
        return partial_target, "partial", 0.80

    callable_name = str(call.get("callable_name", "") or "").strip()
    if callable_name:
        if "." in callable_name:
            return callable_name, "method", 0.95
        return callable_name, "function", 0.90

    handler_name = str(call.get("handler_name", "") or "").strip()
    if handler_name:
        if "." in handler_name:
            return handler_name, "method", 0.95
        return handler_name, "function", 0.90

    return "unknown", "unknown", 0.30


def _build_signal_record(
    source_file: str,
    source_symbol: str,
    call: dict[str, Any],
) -> dict[str, Any]:
    signal_name = str(call.get("call_name", "") or "").strip()
    target, target_kind, target_confidence = _extract_target_from_call(call)

    return {
        "source_file": source_file,
        "source_symbol": source_symbol,
        "signal_name": signal_name,
        "target": target,
        "target_kind": target_kind,
        "target_confidence": target_confidence,
        "line": call.get("lineno"),
        "confidence": target_confidence,
    }


def extract_qt_signal_map(files_payload: list[dict[str, Any]]) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []

    for file_record in files_payload:
        path = str(file_record.get("path", "") or "")

        for fn in file_record.get("functions", []):
            source_symbol = str(fn.get("qualname", fn.get("name", "")) or "")

            for call in fn.get("calls", []):
                call_name = str(call.get("call_name", "") or "").strip()
                if ".connect" in call_name or call_name.endswith("connect"):
                    results.append(
                        _build_signal_record(
                            source_file=path,
                            source_symbol=source_symbol,
                            call=call,
                        )
                    )

        for cls in file_record.get("classes", []):
            for method in cls.get("methods", []):
                source_symbol = str(method.get("qualname", method.get("name", "")) or "")

                for call in method.get("calls", []):
                    call_name = str(call.get("call_name", "") or "").strip()
                    if ".connect" in call_name or call_name.endswith("connect"):
                        results.append(
                            _build_signal_record(
                                source_file=path,
                                source_symbol=source_symbol,
                                call=call,
                            )
                        )

    return results