#!/usr/bin/env python3
"""List OpenRouter models available to the current API key."""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from decimal import Decimal, InvalidOperation
from typing import Any


ACCOUNT_MODELS_URL = "https://openrouter.ai/api/v1/models/user"
CATALOG_MODELS_URL = "https://openrouter.ai/api/v1/models"

CODING_KEYWORDS = (
    "code",
    "coding",
    "coder",
    "programming",
    "python",
    "software engineering",
    "software development",
    "swe",
    "developer",
    "debugging",
    "refactoring",
    "repository",
    "terminal",
    "agentic software",
)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="List models available through OpenRouter."
    )
    parser.add_argument(
        "--catalog",
        action="store_true",
        help="Use the full public catalog instead of the account-aware list.",
    )
    parser.add_argument(
        "--free-only",
        action="store_true",
        help="Show only models with zero prompt and completion pricing.",
    )
    parser.add_argument(
        "--coding-only",
        action="store_true",
        help="Show only models whose metadata suggests coding capability.",
    )
    parser.add_argument(
        "--tools-only",
        action="store_true",
        help="Show only models advertising tool-call support.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print the filtered models as JSON.",
    )
    parser.add_argument(
        "--save-json",
        metavar="FILE",
        help="Save the complete API response to a JSON file.",
    )
    return parser.parse_args()


def fetch_models(api_key: str, use_catalog: bool) -> dict[str, Any]:
    url = CATALOG_MODELS_URL if use_catalog else ACCOUNT_MODELS_URL

    request = urllib.request.Request(
        url=url,
        method="GET",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json",
            "User-Agent": "KANDA-OpenRouter-Model-Inspector/1.0",
        },
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            raw_body = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"OpenRouter returned HTTP {exc.code}: {error_body}"
        ) from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(
            f"Could not connect to OpenRouter: {exc.reason}"
        ) from exc

    try:
        payload = json.loads(raw_body)
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            "OpenRouter returned invalid JSON."
        ) from exc

    if not isinstance(payload, dict):
        raise RuntimeError("Unexpected OpenRouter response shape.")

    return payload


def decimal_value(value: Any) -> Decimal | None:
    try:
        return Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError):
        return None


def is_free(model: dict[str, Any]) -> bool:
    pricing = model.get("pricing")
    if not isinstance(pricing, dict):
        return False

    prompt_price = decimal_value(pricing.get("prompt"))
    completion_price = decimal_value(pricing.get("completion"))

    return (
        prompt_price is not None
        and completion_price is not None
        and prompt_price == 0
        and completion_price == 0
    )


def supports_tools(model: dict[str, Any]) -> bool:
    parameters = model.get("supported_parameters", [])
    if not isinstance(parameters, list):
        return False

    normalized = {str(item).strip().lower() for item in parameters}
    return "tools" in normalized


def coding_score(model: dict[str, Any]) -> int:
    searchable_text = " ".join(
        [
            str(model.get("id", "")),
            str(model.get("name", "")),
            str(model.get("description", "")),
        ]
    ).lower()

    return sum(
        1 for keyword in CODING_KEYWORDS if keyword in searchable_text
    )


def price_per_million(model: dict[str, Any], field: str) -> str:
    pricing = model.get("pricing")
    if not isinstance(pricing, dict):
        return "unknown"

    value = decimal_value(pricing.get(field))
    if value is None:
        return "unknown"

    per_million = value * Decimal("1000000")

    if per_million == 0:
        return "free"

    return f"${per_million:.4f}"


def context_length(model: dict[str, Any]) -> str:
    value = model.get("context_length")
    return str(value) if isinstance(value, int) else "unknown"


def maximum_output(model: dict[str, Any]) -> str:
    provider = model.get("top_provider")
    if not isinstance(provider, dict):
        return "unknown"

    value = provider.get("max_completion_tokens")
    return str(value) if isinstance(value, int) else "unknown"


def filter_models(
    models: list[dict[str, Any]],
    free_only: bool,
    coding_only: bool,
    tools_only: bool,
) -> list[dict[str, Any]]:
    selected: list[dict[str, Any]] = []

    for model in models:
        if free_only and not is_free(model):
            continue

        if coding_only and coding_score(model) == 0:
            continue

        if tools_only and not supports_tools(model):
            continue

        selected.append(model)

    return sorted(
        selected,
        key=lambda item: (
            -coding_score(item),
            str(item.get("id", "")).lower(),
        ),
    )


def print_table(models: list[dict[str, Any]]) -> None:
    headers = (
        "MODEL ID",
        "FREE",
        "TOOLS",
        "CODE SCORE",
        "CONTEXT",
        "MAX OUTPUT",
        "PROMPT/1M",
        "OUTPUT/1M",
    )

    rows: list[tuple[str, ...]] = []

    for model in models:
        rows.append(
            (
                str(model.get("id", "unknown")),
                "yes" if is_free(model) else "no",
                "yes" if supports_tools(model) else "no",
                str(coding_score(model)),
                context_length(model),
                maximum_output(model),
                price_per_million(model, "prompt"),
                price_per_million(model, "completion"),
            )
        )

    widths = [
        max(len(headers[index]), *(len(row[index]) for row in rows))
        if rows
        else len(headers[index])
        for index in range(len(headers))
    ]

    print(
        "  ".join(
            header.ljust(widths[index])
            for index, header in enumerate(headers)
        )
    )
    print("  ".join("-" * width for width in widths))

    for row in rows:
        print(
            "  ".join(
                value.ljust(widths[index])
                for index, value in enumerate(row)
            )
        )


def main() -> int:
    arguments = parse_arguments()

    api_key = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if not api_key:
        print(
            "ERROR: Set the OPENROUTER_API_KEY environment variable.",
            file=sys.stderr,
        )
        return 1

    try:
        payload = fetch_models(api_key, arguments.catalog)
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if arguments.save_json:
        with open(arguments.save_json, "w", encoding="utf-8") as output_file:
            json.dump(payload, output_file, indent=2, ensure_ascii=True)
            output_file.write("\n")

    raw_models = payload.get("data", [])
    if not isinstance(raw_models, list):
        print("ERROR: Response does not contain a model list.", file=sys.stderr)
        return 1

    models = [
        model for model in raw_models if isinstance(model, dict)
    ]

    selected = filter_models(
        models=models,
        free_only=arguments.free_only,
        coding_only=arguments.coding_only,
        tools_only=arguments.tools_only,
    )

    source = "public catalog" if arguments.catalog else "account-aware list"

    print(f"OpenRouter source: {source}", file=sys.stderr)
    print(f"Models returned by API: {len(models)}", file=sys.stderr)
    print(f"Models after filters: {len(selected)}", file=sys.stderr)
    print("", file=sys.stderr)

    if arguments.json:
        json.dump(selected, sys.stdout, indent=2, ensure_ascii=True)
        print()
    else:
        print_table(selected)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())