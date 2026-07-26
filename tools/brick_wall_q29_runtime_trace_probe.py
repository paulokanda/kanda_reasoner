"""Child-process audit probe for the bounded Brick Wall Q29 pilot."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import zipfile

__all__: list[str] = []
MAX_EVENTS = 5000


def _path_record(value: object, dir_fd: object = None) -> dict[str, object]:
    raw = os.fspath(value) if isinstance(value, (str, bytes, os.PathLike)) else str(value)
    text = os.fsdecode(raw)
    path = Path(text)
    if path.is_absolute():
        return {
            "raw_path": text,
            "resolved_path": str(path.resolve(strict=False)),
            "path_attribution": "ABSOLUTE",
            "dir_fd": dir_fd,
        }
    if isinstance(dir_fd, int) and dir_fd >= 0:
        return {
            "raw_path": text,
            "resolved_path": "",
            "path_attribution": "DIR_FD_RELATIVE_UNRESOLVED",
            "dir_fd": dir_fd,
        }
    return {
        "raw_path": text,
        "resolved_path": str((Path.cwd() / path).resolve(strict=False)),
        "path_attribution": "CWD_RELATIVE",
        "dir_fd": dir_fd,
    }


def _write_open(mode: object, flags: object) -> bool:
    if isinstance(mode, str) and any(marker in mode for marker in "wax+"):
        return True
    if isinstance(flags, int):
        mask = (
            os.O_WRONLY
            | os.O_RDWR
            | os.O_CREAT
            | os.O_TRUNC
            | os.O_APPEND
        )
        return bool(flags & mask)
    return False


def _install_hook(events: list[dict[str, object]], output_path: Path) -> None:
    output_resolved = output_path.resolve(strict=False)

    def append(category: str, event: str, details: dict[str, object]) -> None:
        if len(events) < MAX_EVENTS:
            events.append({"category": category, "event": event, **details})

    def hook(event: str, args: tuple[object, ...]) -> None:
        if event == "open":
            value = args[0] if args else ""
            mode = args[1] if len(args) > 1 else None
            flags = args[2] if len(args) > 2 else 0
            path_data = _path_record(value)
            if path_data.get("resolved_path") == str(output_resolved):
                return
            suffix = Path(str(path_data.get("raw_path") or "")).suffix.lower()
            if suffix == ".zip":
                append(
                    "archive_operations",
                    event,
                    {**path_data, "mode": str(mode), "flags": flags},
                )
            if _write_open(mode, flags):
                append(
                    "writes",
                    event,
                    {**path_data, "mode": str(mode), "flags": flags},
                )
            return
        if event in {"os.remove", "os.rmdir"}:
            dir_fd = args[1] if len(args) > 1 else None
            append("deletes", event, _path_record(args[0], dir_fd))
            return
        if event in {"os.rename", "os.replace"}:
            source_fd = args[2] if len(args) > 2 else None
            target_fd = args[3] if len(args) > 3 else None
            append(
                "replacements",
                event,
                {
                    "source": _path_record(args[0], source_fd),
                    "target": _path_record(args[1], target_fd),
                },
            )
            return
        if event == "subprocess.Popen":
            append(
                "subprocesses",
                event,
                {"executable": str(args[0]) if args else ""},
            )
            return
        if event == "import":
            append(
                "imports",
                event,
                {"module": str(args[0]) if args else ""},
            )

    sys.addaudithook(hook)


def _synthetic_actions() -> None:
    with tempfile.TemporaryDirectory(prefix="kanda_q29_probe_") as raw:
        root = Path(raw)
        source = root / "source.txt"
        target = root / "target.txt"
        archive = root / "fixture.zip"
        source.write_text("q29\n", encoding="utf-8")
        os.replace(source, target)
        with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as item:
            item.writestr("payload/example.txt", "example\n")
        with zipfile.ZipFile(archive, "r") as item:
            item.read("payload/example.txt")
        subprocess.run(
            [sys.executable, "--version"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        module_name = "kanda_q29_probe_import_target"
        module_path = root / (module_name + ".py")
        module_path.write_text("VALUE = 29\n", encoding="utf-8")
        sys.path.insert(0, str(root))
        try:
            __import__(module_name)
        finally:
            sys.modules.pop(module_name, None)
            sys.path.remove(str(root))
        target.unlink()


def _q20_actions(project_root: Path) -> None:
    tools = project_root / "tools"
    sys.path.insert(0, str(project_root))
    sys.path.insert(0, str(tools))
    from validate_brick_wall_q20_shared_isolated_filesystem_fixtures_v1 import (
        validate_runtime_fixture,
    )

    validate_runtime_fixture(project_root)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=("synthetic", "q20", "attribution_model"),
        required=True,
    )
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--project-root", type=Path)
    args = parser.parse_args()
    output = args.output.expanduser().resolve(strict=False)
    events: list[dict[str, object]] = []
    _install_hook(events, output)
    status = "PASS"
    error = ""
    try:
        if args.mode == "synthetic":
            _synthetic_actions()
        elif args.mode == "attribution_model":
            events.append(
                {
                    "category": "path_attribution_model",
                    "event": "model.dir_fd_relative",
                    **_path_record("relative.txt", 123),
                }
            )
        else:
            if args.project_root is None:
                raise RuntimeError("--project-root is required for q20 mode")
            _q20_actions(args.project_root.expanduser().resolve(strict=True))
    except BaseException as exc:
        status = "FAIL"
        error = type(exc).__name__ + ": " + str(exc)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(
            {
                "schema_version": "1.0",
                "mode": args.mode,
                "status": status,
                "error": error,
                "events": events,
            },
            indent=2,
            ensure_ascii=True,
        )
        + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
