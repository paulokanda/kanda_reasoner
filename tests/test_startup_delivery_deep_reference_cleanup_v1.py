"""Regression tests for startup delivery deep stale-reference cleanup."""
from __future__ import annotations

import importlib.util
import sys
import zipfile
from pathlib import Path
from tempfile import TemporaryDirectory

PROJECT_ROOT = Path.cwd()
WORKSPACE_ROOT = PROJECT_ROOT / "kanda_prompt_workspace"
PROMPT_LIBRARY_ROOT = WORKSPACE_ROOT / "prompt_library"
SYNC_SCRIPT = WORKSPACE_ROOT / "prompt_tools" / "sync_startup_routing_kernel_pack.py"
FREEZE_CONTEXT_SCRIPT = WORKSPACE_ROOT / "prompt_tools" / "startup_freeze_context.py"
PROMPT_TOOLS_ROOT = WORKSPACE_ROOT / "prompt_tools"
if str(PROMPT_TOOLS_ROOT) not in sys.path:
    sys.path.insert(0, str(PROMPT_TOOLS_ROOT))

RETIRED_PROJECT_NAME = "developer" + "_tools"
RETIRED_DELIVERY_FOLDER = "first" + "_AI_deliver"
RETIRED_PASTE_FILE = "paste_after_" + "first_prompts_to_ai.md"

ACTIVE_PROMPT_SOURCE_PATHS = [
    PROMPT_LIBRARY_ROOT / "ACTIVE_PROMPTS" / "01_session_start_and_navigation" / "handoff_at_end_of_work.md",
    PROMPT_LIBRARY_ROOT / "ACTIVE_PROMPTS" / "02_prompt_routing_and_indexing" / "chatgpt_kanda_routing_choice_output_protocol.md",
    PROMPT_LIBRARY_ROOT / "ROUTING" / "GROUP_ASSIMILATION_INDEX.md",
    PROMPT_LIBRARY_ROOT / "ROUTING_TESTS" / "PHASE_2_PROMPT_CALL_ACCURACY" / "phase2_prompt_call_rubric.md",
    PROMPT_LIBRARY_ROOT / "ROUTING_TESTS" / "PHASE_2_PROMPT_CALL_ACCURACY" / "README.md",
]


def _load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def test_active_prompt_sources_do_not_contain_retired_operational_names() -> None:
    forbidden = [RETIRED_PROJECT_NAME, RETIRED_DELIVERY_FOLDER, RETIRED_PASTE_FILE]
    offenders: list[str] = []
    for path in ACTIVE_PROMPT_SOURCE_PATHS:
        text = path.read_text(encoding="utf-8", errors="replace")
        for term in forbidden:
            if term in text:
                offenders.append(f"{path.as_posix()} contains {term}")
    assert not offenders, "; ".join(offenders)


def test_prompt_library_payload_excludes_generated_archives_and_bundle_scratch() -> None:
    sync = _load_module(SYNC_SCRIPT, "sync_startup_routing_kernel_pack_for_deep_cleanup_test")
    payload_paths = [sync._prompt_library_relpath(WORKSPACE_ROOT, path) for path in sync.iter_prompt_library_payload_files(WORKSPACE_ROOT)]

    assert "prompt_library.zip" not in payload_paths
    assert "ACTIVE_PROMPTS.zip" not in payload_paths
    assert not any(path.endswith(".zip") for path in payload_paths)
    assert not any(path.startswith("_bundle_temp/") for path in payload_paths)


def test_startup_freeze_context_sanitizes_retired_names_in_generated_exposure() -> None:
    freeze_context = _load_module(FREEZE_CONTEXT_SCRIPT, "startup_freeze_context_for_deep_cleanup_test")
    raw = " ".join([RETIRED_PROJECT_NAME, RETIRED_DELIVERY_FOLDER, RETIRED_PASTE_FILE])
    sanitized = freeze_context._sanitize_startup_freeze_exposure_text(raw)

    assert RETIRED_PROJECT_NAME not in sanitized
    assert RETIRED_DELIVERY_FOLDER not in sanitized
    assert RETIRED_PASTE_FILE not in sanitized
    assert "[retired legacy project name]" in sanitized
    assert "[retired startup delivery folder]" in sanitized
    assert "[retired startup paste filename]" in sanitized


def test_generated_startup_artifacts_do_not_reintroduce_retired_active_names() -> None:
    sync = _load_module(SYNC_SCRIPT, "sync_startup_routing_kernel_pack_generation_test")
    with TemporaryDirectory() as tmp:
        output_dir = Path(tmp) / "first_prompt_files"
        code, zip_path = sync.make_zip(WORKSPACE_ROOT, output_dir, PROJECT_ROOT, dry_run=False)
        assert code == 0

        first_zip = output_dir / "first_prompts_to_ai.zip"
        prompt_zip = output_dir / "prompt_library.zip"
        assert first_zip == zip_path
        assert first_zip.is_file()
        assert prompt_zip.is_file()

        forbidden = [RETIRED_PROJECT_NAME, RETIRED_DELIVERY_FOLDER, RETIRED_PASTE_FILE]
        offenders: list[str] = []
        for archive in (first_zip, prompt_zip):
            with zipfile.ZipFile(archive, "r") as z:
                names = z.namelist()
                assert not any(name.endswith(".zip") for name in names if archive == prompt_zip)
                assert not any(name.startswith("_bundle_temp/") for name in names if archive == prompt_zip)
                for name in names:
                    if name.endswith("/"):
                        continue
                    data = z.read(name)
                    try:
                        text = data.decode("utf-8")
                    except UnicodeDecodeError:
                        continue
                    for term in forbidden:
                        if term in text:
                            offenders.append(f"{archive.name}::{name} contains {term}")
        assert not offenders, "; ".join(offenders[:20])


def main() -> int:
    test_active_prompt_sources_do_not_contain_retired_operational_names()
    test_prompt_library_payload_excludes_generated_archives_and_bundle_scratch()
    test_startup_freeze_context_sanitizes_retired_names_in_generated_exposure()
    test_generated_startup_artifacts_do_not_reintroduce_retired_active_names()
    print("VALIDATION OK: startup_delivery_deep_reference_cleanup_v1")
    print("VALIDATION OK: startup delivery deep reference cleanup")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
