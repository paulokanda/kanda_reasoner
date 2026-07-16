"""Support static evidence collection for Project Reasoner."""

from __future__ import annotations


def build_module_responsibility_summary(file_record: dict) -> dict:
    primary_role = file_record.get("primary_role", "") or "general_module"
    secondary_roles = file_record.get("secondary_roles", []) or []

    function_names = [item.get("name", "") for item in file_record.get("functions", []) if item.get("name")]
    class_names = [item.get("name", "") for item in file_record.get("classes", []) if item.get("name")]
    key_symbols = (class_names + function_names)[:10]

    key_imports = [item for item in file_record.get("imports", []) if item][:10]

    if key_symbols:
        symbol_text = ", ".join(key_symbols[:5])
        summary = f"This module primarily handles {primary_role} responsibilities and exposes key symbols such as {symbol_text}."
    else:
        summary = f"This module primarily handles {primary_role} responsibilities."

    if secondary_roles:
        summary += " Secondary roles include " + ", ".join(secondary_roles[:3]) + "."

    if key_imports:
        summary += " Key imports include " + ", ".join(key_imports[:5]) + "."

    return {
        "summary": summary,
        "primary_role": primary_role,
        "secondary_roles": secondary_roles,
        "key_symbols": key_symbols,
        "key_imports": key_imports,
    }