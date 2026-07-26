from __future__ import annotations

import os
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.project_analysis_evidence_paths import (
    SECOND_PROMPT_FILES_BUILDING_DIR,
    SECOND_PROMPT_FILES_DIR,
    SHOW_PROJECT_TO_AI_JSON_COMPLETE_DIR_ENV,
    analysis_json_building_dir,
    analysis_json_complete_dir,
    project_analysis_evidence_root,
)
from kanda_reasoner_app.reasoner_tools_shell.runner_help import zip_json_files_private_impl


def test_env_override_routes_child_generation_to_build_folder() -> None:
    root = Path('/tmp/demo_publish_project')
    show_root = project_analysis_evidence_root(root)
    build_dir = show_root / SECOND_PROMPT_FILES_BUILDING_DIR
    old = os.environ.get(SHOW_PROJECT_TO_AI_JSON_COMPLETE_DIR_ENV)
    try:
        os.environ[SHOW_PROJECT_TO_AI_JSON_COMPLETE_DIR_ENV] = str(build_dir)
        assert analysis_json_complete_dir(root) == build_dir
        assert analysis_json_building_dir(root) == build_dir
    finally:
        if old is None:
            os.environ.pop(SHOW_PROJECT_TO_AI_JSON_COMPLETE_DIR_ENV, None)
        else:
            os.environ[SHOW_PROJECT_TO_AI_JSON_COMPLETE_DIR_ENV] = old


def test_publish_building_folder_preserves_final_until_success_and_rewrites_paths() -> None:
    with TemporaryDirectory(ignore_cleanup_errors=True) as temp_name:
        show_root = Path(temp_name) / 'demo_project_show_project_to_AI'
        final_dir = show_root / SECOND_PROMPT_FILES_DIR
        build_dir = show_root / SECOND_PROMPT_FILES_BUILDING_DIR
        final_dir.mkdir(parents=True)
        build_dir.mkdir(parents=True)

        old_final = final_dir / 'old_delivery.json'
        old_final.write_text('{"old": true}', encoding='utf-8')
        artifact = build_dir / 'demo_project__bundle_manifest.json'
        artifact.write_text(
            '{"path": "show_project_to_AI/second_prompt_files_building/demo_project__bundle_manifest.json", '
            '"absolute": "' + str(build_dir).replace('\\', '\\\\') + '"}',
            encoding='utf-8',
        )
        nested = build_dir / 'nested'
        nested.mkdir()
        (nested / 'payload.txt').write_text('second_prompt_files_building', encoding='utf-8')

        assert old_final.exists(), 'old final delivery must remain visible before publish'
        result = zip_json_files_private_impl.publish_second_prompt_files_building_dir(
            build_dir,
            final_dir,
            project_root=Path(temp_name) / 'demo_project',
        )

        assert result['moved_items'] >= 2
        assert not old_final.exists(), 'old final delivery is cleared only at publish time'
        published = final_dir / 'demo_project__bundle_manifest.json'
        assert published.exists()
        published_text = published.read_text(encoding='utf-8')
        assert 'second_prompt_files_building' not in published_text
        assert 'show_project_to_AI/second_prompt_files/demo_project__bundle_manifest.json' in published_text
        assert (final_dir / 'nested' / 'payload.txt').read_text(encoding='utf-8') == 'second_prompt_files'
        assert (final_dir / zip_json_files_private_impl.STATUS_FILE_NAME).exists()
        assert list(build_dir.iterdir()) == []


def test_clear_building_folder_rejects_final_folder() -> None:
    with TemporaryDirectory(ignore_cleanup_errors=True) as temp_name:
        show_root = Path(temp_name) / 'demo_project_show_project_to_AI'
        final_dir = show_root / SECOND_PROMPT_FILES_DIR
        final_dir.mkdir(parents=True)
        try:
            zip_json_files_private_impl.clear_second_prompt_files_building_dir(final_dir)
        except ValueError as exc:
            assert 'second_prompt_files_building' in str(exc)
        else:
            raise AssertionError('final folder must not be accepted as the build-cleanup folder')


def main() -> int:
    test_env_override_routes_child_generation_to_build_folder()
    test_publish_building_folder_preserves_final_until_success_and_rewrites_paths()
    test_clear_building_folder_rejects_final_folder()
    print('VALIDATION OK: show_project_to_ai_second_prompt_files_publish_v1')
    print('VALIDATION OK: show project to AI second prompt files publish')
    print('STATUS: IN_SYNC')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
