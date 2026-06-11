from __future__ import annotations

import importlib.util
import sys
import tempfile
import types
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.manage_architecture.manage_architecture_help.source_loader_private_impl import (
    load_manage_architecture_source,
)
from kanda_reasoner_app.project_exclusion_policy import (
    load_reasoner_project_exclusion_rules,
    should_exclude_reasoner_project_path,
)

RULE_DEFAULTS_PATH = (
    PROJECT_ROOT
    / 'ask_' 'ai_project_reasoner'
    / "reasoner_tools_gui_shell"
    / "ignore_rules_tab_help"
    / "rule_defaults.py"
)


def _load_rule_defaults_mixin():
    spec = importlib.util.spec_from_file_location(
        "jsonctx014c_rule_defaults_probe",
        RULE_DEFAULTS_PATH,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load rule_defaults.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.IgnoreRulesDefaultsMixin


def test_tab8_defaults_include_workbench_for_reasoner_project() -> None:
    mixin = _load_rule_defaults_mixin()

    class DefaultsProbe(mixin):
        def __init__(self, project_root: Path) -> None:
            self._project_root = project_root

    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir) / "developer_tools"
        (root / 'ask_' 'ai_project_reasoner').mkdir(parents=True)

        probe = DefaultsProbe(root)
        defaults = [item.lower() for item in probe._reasoner_project_folder_defaults()]

        assert "workbench" in defaults


def test_central_exclusion_policy_excludes_workbench_for_reasoner_project() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir) / "developer_tools"
        (root / 'ask_' 'ai_project_reasoner').mkdir(parents=True)
        target = root / "workbench" / "_bundle_temp" / "test_example.py"
        target.parent.mkdir(parents=True)
        target.write_text("print('temporary')\n", encoding="utf-8")

        rules = load_reasoner_project_exclusion_rules(root)
        folders = [item.lower() for item in rules.get("folders", [])]

        assert "workbench" in folders
        assert should_exclude_reasoner_project_path(target, root, rules)


def test_manage_architecture_loads_active_tab8_exclusion_policy() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir) / "developer_tools"
        (root / 'ask_' 'ai_project_reasoner').mkdir(parents=True)
        included = root / 'ask_' 'ai_project_reasoner' / "active_module.py"
        ignored = root / "workbench" / "_bundle_temp" / "test_example.py"
        included.write_text("VALUE = 1\n", encoding="utf-8")
        ignored.parent.mkdir(parents=True)
        ignored.write_text("VALUE = 2\n", encoding="utf-8")

        source = load_manage_architecture_source()
        assert "load_reasoner_project_exclusion_rules" in source

        module_name = "jsonctx014c_architecture_probe"
        probe_module = types.ModuleType(module_name)
        sys.modules[module_name] = probe_module
        namespace = probe_module.__dict__
        namespace["__name__"] = module_name
        exec(compile(source, "<manage_architecture_probe>", "exec"), namespace)

        load_ignore_rules = namespace["load_ignore_rules"]
        iter_python_files = namespace["iter_python_files"]

        folders, files, extensions = load_ignore_rules(root)  # type: ignore[misc]
        folders_lower = [str(item).lower() for item in folders]
        discovered = {
            path.relative_to(root).as_posix()
            for path in iter_python_files(root, folders, files, extensions)  # type: ignore[misc]
        }

        assert "workbench" in folders_lower
        assert 'ask_' 'ai_project_reasoner' '/active_module.py' in discovered
        assert "workbench/_bundle_temp/test_example.py" not in discovered


if __name__ == "__main__":
    test_tab8_defaults_include_workbench_for_reasoner_project()
    test_central_exclusion_policy_excludes_workbench_for_reasoner_project()
    test_manage_architecture_loads_active_tab8_exclusion_policy()
    print("JSONCTX014C Tab 8 exclusion policy alignment tests passed.")
