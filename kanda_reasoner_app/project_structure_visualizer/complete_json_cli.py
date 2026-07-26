"""CLI process boundary for Project Structure 3D JSON creation and update."""

from __future__ import annotations

import argparse
import json
import sys

from .complete_json_builder import build_project_structure_complete_json


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--mode", choices=("create", "incremental"), required=True)
    args = parser.parse_args(argv)

    def progress(message: str) -> None:
        print("PROGRESS: " + str(message), flush=True)

    try:
        result = build_project_structure_complete_json(
            args.root,
            mode=args.mode,
            progress=progress,
        )
    except Exception as exc:
        print("ERROR_TYPE: " + exc.__class__.__name__, file=sys.stderr, flush=True)
        print("ERROR_MESSAGE: " + str(exc), file=sys.stderr, flush=True)
        return 1
    print("RESULT: " + json.dumps(result, sort_keys=True), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
