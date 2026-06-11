"""Focused tests for the JSONCTX003 project context bundle skeleton."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.reasoner_context_bundle import (  # noqa: E402
    bundle_artifact_paths,
    relative_posix_path,
    resolve_project_context,
    sha256_text_normalized,
    write_json_atomic,
)
from kanda_reasoner_app.reasoner_context_bundle.hashing import (  # noqa: E402
    sha256_bytes,
    sha256_file,
)
from kanda_reasoner_app.reasoner_context_bundle.json_writer import (  # noqa: E402
    write_json_atomic as direct_write_json_atomic,
)
from kanda_reasoner_app.reasoner_context_bundle.output_paths import (  # noqa: E402
    ACTIVE_SNAPSHOT_SUFFIX,
    BUNDLE_MANIFEST_SUFFIX,
    EXCLUSION_RULES_SUFFIX,
    FILE_MANIFEST_SUFFIX,
    VALIDATION_STATE_SUFFIX,
    bundle_artifact_paths as direct_bundle_artifact_paths,
)
from kanda_reasoner_app.reasoner_context_bundle.path_normalization import (  # noqa: E402
    safe_resolve,
    to_posix_path,
)
from kanda_reasoner_app.reasoner_context_bundle.project_context import (  # noqa: E402
    resolve_project_context as direct_resolve_project_context,
)
from kanda_reasoner_app.reasoner_context_bundle.schema_models import (  # noqa: E402
    BundleArtifactPaths,
    ProjectContext,
)


def test_resolve_project_context_uses_dynamic_project_owned_evidence_path() -> None:
    root = Path("D:/alpha project")

    context = resolve_project_context(root)

    assert context.root == root
    assert context.project_slug == "alpha_project"
    assert context.evidence_root == root / "project_analysis_evidence"
    assert context.json_complete_dir == (
        root / "project_analysis_evidence" / "json_complete"
    )
    assert "_project_reference" not in str(context.evidence_root)


def test_bundle_artifact_paths_are_additive_and_do_not_change_complete_json() -> None:
    root = Path("C:/demo_project")

    paths = bundle_artifact_paths(root)

    assert paths.complete_json.as_posix().endswith(
        "project_analysis_evidence/json_complete/demo_project__complete.json"
    )
    assert paths.active_snapshot_json.name == "demo_project__active_snapshot.json"
    assert paths.file_manifest_json.name == "demo_project__file_manifest.json"
    assert paths.exclusion_rules_json.name == "demo_project__exclusion_rules.json"
    assert paths.validation_state_json.name == "demo_project__validation_state.json"
    assert paths.bundle_manifest_json.name == "demo_project__bundle_manifest.json"
    assert len(paths.required_paths()) == 7


def test_relative_posix_path_rejects_paths_outside_project_root() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir) / "project"
        root.mkdir()
        inside = root / 'ask_' 'ai_project_reasoner' / "module.py"
        inside.parent.mkdir()
        inside.write_text("print('ok')\n", encoding="utf-8")
        outside = Path(temp_dir) / "outside.py"
        outside.write_text("print('no')\n", encoding="utf-8")

        assert relative_posix_path(inside, root) == 'ask_' 'ai_project_reasoner' '/module.py'
        try:
            relative_posix_path(outside, root)
        except ValueError as exc:
            assert "outside the project root" in str(exc)
        else:
            raise AssertionError("outside path was not rejected")


def test_write_json_atomic_creates_valid_json_without_partial_file() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        path = Path(temp_dir) / "nested" / "artifact.json"
        payload = {"schema_version": 1, "items": ["a", "b"]}

        written = write_json_atomic(path, payload)

        assert written == path
        assert json.loads(path.read_text(encoding="utf-8")) == payload
        assert not path.with_name(path.name + ".tmp").exists()


def test_sha256_text_normalized_is_newline_stable() -> None:
    assert sha256_text_normalized("a\r\nb\r\n") == sha256_text_normalized("a\nb\n")


def test_direct_module_public_contracts_are_test_protected() -> None:
    root = Path("D:/module_contract_project")
    context = direct_resolve_project_context(root)
    paths = direct_bundle_artifact_paths(context)

    assert isinstance(context, ProjectContext)
    assert isinstance(paths, BundleArtifactPaths)
    assert ACTIVE_SNAPSHOT_SUFFIX == "__active_snapshot.json"
    assert FILE_MANIFEST_SUFFIX == "__file_manifest.json"
    assert EXCLUSION_RULES_SUFFIX == "__exclusion_rules.json"
    assert VALIDATION_STATE_SUFFIX == "__validation_state.json"
    assert BUNDLE_MANIFEST_SUFFIX == "__bundle_manifest.json"
    assert to_posix_path("a\\b") == "a/b"
    assert safe_resolve(".").is_absolute()
    assert sha256_bytes(b"abc") == (
        "ba7816bf8f01cfea414140de5dae2223"
        "b00361a396177a9cb410ff61f20015ad"
    )
    assert direct_write_json_atomic is write_json_atomic


def test_sha256_file_hashes_binary_content() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        path = Path(temp_dir) / "data.bin"
        path.write_bytes(b"abc")

        assert sha256_file(path) == sha256_bytes(b"abc")


def test_project_context_bundle_sources_do_not_hardcode_current_project_root() -> None:
    package_dir = PROJECT_ROOT / "kanda_reasoner_app" / "reasoner_context_bundle"
    combined = "\n".join(
        path.read_text(encoding="utf-8")
        for path in package_dir.glob("*.py")
    )

    assert "E:\\developer_tools" not in combined
    assert "PROJECT_ANALYSIS_EVIDENCE" not in combined
    assert "_project_reference" not in combined


if __name__ == "__main__":
    test_resolve_project_context_uses_dynamic_project_owned_evidence_path()
    test_bundle_artifact_paths_are_additive_and_do_not_change_complete_json()
    test_relative_posix_path_rejects_paths_outside_project_root()
    test_write_json_atomic_creates_valid_json_without_partial_file()
    test_sha256_text_normalized_is_newline_stable()
    test_direct_module_public_contracts_are_test_protected()
    test_sha256_file_hashes_binary_content()
    test_project_context_bundle_sources_do_not_hardcode_current_project_root()
    print("JSONCTX003 project_context_bundle skeleton tests passed.")
