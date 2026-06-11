"""
Daily AI Structural Awareness Engine - v10.0
============================================

Dual-Domain Deterministic Structural State Compiler

Now Includes:
- Stale lock cleanup
- Archive retention policy
- Structural diff viewer
- Persistent domain memory
- Atomic write safety
- Backup rotation
- Corruption recovery
- Immutable archive snapshots
- Stability Analyzer (A)
- Dependency Graph Extractor (shared A + D)
- Constitution Enforcer (D)
- Refactor Strategist (B)
"""

import os
import json
import copy
import shutil
import hashlib
from pathlib import Path
from datetime import datetime
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QTextEdit,
    QPushButton,
    QMessageBox,
    QRadioButton,
    QHBoxLayout,
)

from dev_tools.daily_refactor_report_helpers.project_snapshot_extractor import extract_project_snapshot
from dev_tools.daily_refactor_report_helpers.symbol_index_extractor import extract_symbol_index
from dev_tools.daily_refactor_report_helpers.symbol_churn_analyzer import analyze_symbol_churn
from dev_tools.daily_refactor_report_helpers.analysis_contracts import AnalysisInputs
from dev_tools.daily_refactor_report_helpers.stability_analyzer import analyze_stability
from dev_tools.daily_refactor_report_helpers.dependency_graph_extractor import extract_dependency_graph
from dev_tools.daily_refactor_report_helpers.constitution_enforcer import analyze_constitution
from dev_tools.daily_refactor_report_helpers.refactor_strategist import analyze_refactor_strategy


LOCK_TIMEOUT_SECONDS = 300
ARCHIVE_RETENTION = 50
ROLLING_WINDOW = 7

# ==========================================================
# PATH CONFIG
# ==========================================================

ENGINE_PATH = Path(__file__).resolve()
PROJECT_ROOT = ENGINE_PATH.parents[1]
SETTINGS_PATH = ENGINE_PATH.parent / "engine_settings.json"

TAB1_DIR = PROJECT_ROOT / "tab1_ai_code_refiner" / "daily_refactor_report_Tab1"
TAB3_DIR = PROJECT_ROOT / "tab3_memory_map" / "daily_refactor_report_Tab3"
CORTEX_JSON_DIR = PROJECT_ROOT / "cortex_core" / "daily_refactor_report_jsons"


CANONICAL_KEYS = {
    "state_vector_version",
    "timestamp",
    "incremental",
    "structural_change",
    "complexity_state",
    "governance_state",
    "refactor_pressure",
    "pattern_dynamics",
    "forward_projection",
    "architectural_snapshot",
}

# ==========================================================
# UTILITIES
# ==========================================================

def write_atomic(path: Path, data):
    tmp = path.with_suffix(".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, sort_keys=True)
    tmp.replace(path)


def rotate_backups(path: Path):
    back1 = path.with_suffix(path.suffix + ".back1")
    back2 = path.with_suffix(path.suffix + ".back2")

    if back2.exists():
        back2.unlink()

    if back1.exists():
        back1.rename(back2)

    if path.exists():
        shutil.copy2(path, back1)


def log_corruption(log_path: Path, message: str):
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()} | {message}\n")


def show_warning(message: str):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setWindowTitle("Structural State Warning")
    msg.setText(message)
    msg.exec()


# ==========================================================
# LOCK MANAGEMENT
# ==========================================================

def create_lock(lock_path: Path):
    write_atomic(lock_path, {
        "pid": os.getpid(),
        "timestamp": datetime.now().isoformat()
    })


def remove_lock(lock_path: Path):
    if lock_path.exists():
        lock_path.unlink()


def check_and_cleanup_stale_lock(lock_path: Path):
    if not lock_path.exists():
        return

    try:
        with open(lock_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        ts = datetime.fromisoformat(data.get("timestamp"))
        age = (datetime.now() - ts).total_seconds()

        if age > LOCK_TIMEOUT_SECONDS:
            remove_lock(lock_path)
            show_warning("Stale engine lock removed.")
        else:
            raise RuntimeError("Another engine instance is running.")

    except Exception:
        remove_lock(lock_path)


# ==========================================================
# SAFE LOAD
# ==========================================================

def safe_load_with_recovery(path: Path, log_path: Path):
    if not path.exists():
        return None

    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        log_corruption(log_path, f"{path.name} corrupted. Attempting recovery.")
        show_warning(f"{path.name} corrupted. Attempting recovery.")

        back1 = path.with_suffix(path.suffix + ".back1")
        back2 = path.with_suffix(path.suffix + ".back2")

        for backup in [back1, back2]:
            if backup.exists():
                try:
                    with open(backup, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    shutil.copy2(backup, path)
                    show_warning(f"Recovered from {backup.name}.")
                    return data
                except Exception:
                    continue

        show_warning(f"Recovery failed for {path.name}. Resetting.")
        return None


# ==========================================================
# SETTINGS
# ==========================================================

def load_settings():
    if not SETTINGS_PATH.exists():
        return {"last_domain": "tab1"}
    try:
        with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        if data.get("last_domain") in ["tab1", "tab3", "cortex"]:
            return data
    except Exception:
        pass
    return {"last_domain": "tab1"}


def save_settings(domain: str):
    write_atomic(SETTINGS_PATH, {"last_domain": domain})


# ==========================================================
# DIFF VIEWER
# ==========================================================

def compute_structural_diff(old, new):
    return {
        "magnitude_delta": new["structural_change"]["magnitude"] - old["structural_change"]["magnitude"],
        "debt_delta": new["refactor_pressure"]["debt_index"] - old["refactor_pressure"]["debt_index"],
        "risk_change": f"{old['complexity_state']['risk_level']} -> {new['complexity_state']['risk_level']}",
    }


def show_diff_dialog(diff):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setWindowTitle("Structural Diff")
    msg.setText(json.dumps(diff, indent=4))
    msg.exec()


# ==========================================================
# VALIDATION & RECOMPUTE
# ==========================================================

def validate_schema(obj: dict):
    if set(obj.keys()) != CANONICAL_KEYS:
        raise ValueError("Schema mismatch.")
    if obj["state_vector_version"] != "2.0":
        raise ValueError("Invalid version.")
    if obj["incremental"] is not True:
        raise ValueError("incremental must be true.")


def recompute_fields(v: dict):
    v = copy.deepcopy(v)

    mag = v["structural_change"]["magnitude"]
    debt = v["refactor_pressure"]["debt_index"]

    if mag <= 3:
        risk = "low"
    elif mag <= 10:
        risk = "medium"
    else:
        risk = "high"

    v["complexity_state"]["risk_level"] = risk
    v["governance_state"]["score"] = max(0, 100 - debt)
    v["timestamp"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    return v


# ==========================================================
# ENGINE
# ==========================================================

class StateVectorCompiler(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Structural State Compiler v10.0")

        layout = QVBoxLayout()

        settings = load_settings()
        last = settings.get("last_domain", "tab1")

        radio_layout = QHBoxLayout()
        self.tab1_radio = QRadioButton("Report: Tab1")
        self.tab3_radio = QRadioButton("Report: Tab3")
        self.cortex_radio = QRadioButton("Report: Cortex Core")

        if last == "tab3":
            self.tab3_radio.setChecked(True)
        elif last == "cortex":
            self.cortex_radio.setChecked(True)
        else:
            self.tab1_radio.setChecked(True)

        self.tab1_radio.toggled.connect(self.persist_domain_choice)
        self.tab3_radio.toggled.connect(self.persist_domain_choice)
        self.cortex_radio.toggled.connect(self.persist_domain_choice)

        radio_layout.addWidget(self.tab1_radio)
        radio_layout.addWidget(self.tab3_radio)
        radio_layout.addWidget(self.cortex_radio)
        layout.addLayout(radio_layout)

        self.text_area = QTextEdit()
        layout.addWidget(self.text_area)

        btn = QPushButton("Compile")
        btn.clicked.connect(self.compile_vectors)
        layout.addWidget(btn)

        self.setLayout(layout)

    def persist_domain_choice(self):

        if self.tab1_radio.isChecked():
            domain = "tab1"
        elif self.tab3_radio.isChecked():
            domain = "tab3"
        else:
            domain = "cortex"

        save_settings(domain)

    def resolve_domain(self):

        if self.tab1_radio.isChecked():
            domain = "tab1"
            root = TAB1_DIR

        elif self.tab3_radio.isChecked():
            domain = "tab3"
            root = TAB3_DIR

        else:
            domain = "cortex"
            root = CORTEX_JSON_DIR

        root.mkdir(parents=True, exist_ok=True)

        return {
            "prefix": domain,
            "root": root,
            "current": root / "current_state.json",
            "history": root / "state_history.json",
            "log": root / "corruption_alert.log",
            "lock": root / "engine.lock",
            "archive": root / "archive",
        }


    # ==========================================================
    # MAIN PIPELINE
    # ==========================================================

    def compile_vectors(self):
        config = None

        try:
            config = self.resolve_domain()
            config["archive"].mkdir(exist_ok=True)

            self._acquire_lock_phase(config)

            if config["prefix"] == "tab1":
                domain_root = TAB1_DIR.parent

            elif config["prefix"] == "tab3":
                domain_root = TAB3_DIR.parent

            else:
                domain_root = PROJECT_ROOT / "dev_tools"

            derived_dir = config["root"] / "derived"
            derived_dir.mkdir(parents=True, exist_ok=True)

            derived_data = self._extraction_phase(config, domain_root, derived_dir)

            merged = self._parse_state_vector_input()

            analysis_outputs = self._analysis_phase(
                config,
                domain_root,
                derived_dir,
                derived_data
            )

            merged.update(analysis_outputs)

            self._persistence_phase(config, merged)

            self._archive_phase(config)

            self._compile_ai_upload_bundle(config)


            QMessageBox.information(
                self,
                "Success",
                f"{config['prefix']} state compiled successfully."
            )

            # Clear input window after successful compile
            self.text_area.clear()

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

        finally:
            if config:
                remove_lock(config["lock"])



    # ==========================================================
    # PHASE 1 — LOCK
    # ==========================================================

    def _acquire_lock_phase(self, config):
        check_and_cleanup_stale_lock(config["lock"])
        create_lock(config["lock"])

    # ==========================================================
    # PHASE 2 — EXTRACTION
    # ==========================================================

    def _extraction_phase(self, config, domain_root, derived_dir):

        snapshot_path = derived_dir / "project_snapshot.json"
        symbol_index_path = derived_dir / "symbol_index.json"
        previous_symbol_index_path = derived_dir / "symbol_index.previous.json"
        churn_output_path = derived_dir / "symbol_churn.json"

        extract_project_snapshot(domain_root, snapshot_path, config["prefix"])

        if symbol_index_path.exists():
            shutil.copy2(symbol_index_path, previous_symbol_index_path)

        extract_symbol_index(domain_root, symbol_index_path, config["prefix"])

        if previous_symbol_index_path.exists():
            analyze_symbol_churn(
                previous_path=previous_symbol_index_path,
                current_path=symbol_index_path,
                output_path=churn_output_path,
                prefix=config["prefix"]
            )
        else:
            write_atomic(
                churn_output_path,
                {"added": [], "removed": [], "note": "Initial run"}
            )

        snapshot_data = safe_load_with_recovery(snapshot_path, config["log"]) or {}
        symbol_index_data = safe_load_with_recovery(symbol_index_path, config["log"]) or {}
        churn_data = safe_load_with_recovery(churn_output_path, config["log"]) or {}

        return {
            "snapshot": snapshot_data,
            "symbol_index": symbol_index_data,
            "symbol_churn": churn_data
        }

    # ==========================================================
    # PHASE 3 — ANALYSIS
    # ==========================================================

    def _analysis_phase(self, config, domain_root, derived_dir, derived_data):

        dependency_graph = extract_dependency_graph(domain_root)

        dependency_output_path = derived_dir / "dependency_graph.json"

        write_atomic(dependency_output_path, dependency_graph)

        rules_path = PROJECT_ROOT / "dev_tools" / "governance_rules.json"
        governance_rules = {}
        if rules_path.exists():
            with open(rules_path, "r", encoding="utf-8") as f:
                governance_rules = json.load(f)

        inputs = AnalysisInputs(
            snapshot=derived_data["snapshot"],
            symbol_index=derived_data["symbol_index"],
            symbol_churn=derived_data["symbol_churn"],
            dependency_graph=dependency_graph,
            governance_rules=governance_rules
        )

        stability_result = analyze_stability(inputs)
        constitution_result = analyze_constitution(inputs)
        strategy_result = analyze_refactor_strategy(inputs)

        stability_output_path = derived_dir / "stability_analysis.json"

        write_atomic(stability_output_path, stability_result.result)

        return {
            "dependency_state": dependency_graph,
            "stability_state": stability_result.result,
            "constitution_state": constitution_result.result,
            "strategy_state": strategy_result.result
        }

    # ==========================================================
    # PHASE 4 — STATE VECTOR PARSE
    # ==========================================================

    def _parse_state_vector_input(self):
        raw = self.text_area.toPlainText().strip()
        parsed = json.loads(raw)
        vectors = parsed if isinstance(parsed, list) else [parsed]

        validated = []
        for v in vectors:
            validate_schema(v)
            validated.append(recompute_fields(v))

        return validated[0]

    # ==========================================================
    # PHASE 5 — PERSISTENCE
    # ==========================================================

    def _persistence_phase(self, config, merged):

        history = safe_load_with_recovery(config["history"], config["log"]) or []
        previous = history[-1] if history else None

        history.append(merged)
        history = history[-ROLLING_WINDOW:]

        rotate_backups(config["current"])
        rotate_backups(config["history"])

        write_atomic(config["history"], history)
        write_atomic(config["current"], merged)

        if previous:
            diff = compute_structural_diff(previous, merged)
            show_diff_dialog(diff)

    # ==========================================================
    # PHASE 6 — ARCHIVE
    # ==========================================================

    def _archive_phase(self, config):

        archive_snapshot = config["archive"] / (
            f"current_state_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )

        shutil.copy2(config["current"], archive_snapshot)

        archives = sorted(
            config["archive"].glob("*.json"),
            key=lambda p: p.stat().st_mtime,
            reverse=True
        )

        for old in archives[ARCHIVE_RETENTION:]:
            old.unlink()

    # ==========================================================
    # PHASE 7 — AI UPLOAD BUNDLE (HARDENED)
    # ==========================================================

    def _load_with_status(self, path: Path, log_path: Path):
        if not path.exists():
            return {}, "missing"

        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f), "ok"
        except Exception:
            recovered = safe_load_with_recovery(path, log_path)
            if recovered is not None:
                return recovered, "recovered"
            return {}, "corrupted"

    def _compile_ai_upload_bundle(self, config):

        derived_dir = config["root"] / "derived"

        snapshot, s_status = self._load_with_status(
            derived_dir / "project_snapshot.json", config["log"]
        )

        symbol_index, si_status = self._load_with_status(
            derived_dir / "symbol_index.json", config["log"]
        )

        churn, c_status = self._load_with_status(
            derived_dir / "symbol_churn.json", config["log"]
        )

        dependency, d_status = self._load_with_status(
            derived_dir / "dependency_graph.json", config["log"]
        )

        stability, st_status = self._load_with_status(
            derived_dir / "stability_analysis.json", config["log"]
        )

        current, cur_status = self._load_with_status(
            config["current"], config["log"]
        )

        history, h_status = self._load_with_status(
            config["history"], config["log"]
        )

        bundle_core = {
            "current_state": current,
            "state_history": history,
            "derived": {
                "project_snapshot": snapshot,
                "symbol_index": symbol_index,
                "symbol_churn": churn,
                "dependency_graph": dependency,
                "stability_analysis": stability
            }
        }

        # Deterministic integrity hash
        bundle_bytes = json.dumps(bundle_core, sort_keys=True).encode("utf-8")
        integrity_hash = hashlib.sha256(bundle_bytes).hexdigest()

        bundle = {
            "metadata": {
                "generated_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
                "engine_version": "v10.0",
                "domain": config["prefix"],
                "bundle_type": "ai_upload",
                "load_status": {
                    "project_snapshot": s_status,
                    "symbol_index": si_status,
                    "symbol_churn": c_status,
                    "dependency_graph": d_status,
                    "stability_analysis": st_status,
                    "current_state": cur_status,
                    "state_history": h_status
                },
                "integrity_hash": integrity_hash
            },
            **bundle_core
        }

        bundle_path = config["root"] / "ai_upload_bundle.json"

        write_atomic(bundle_path, bundle)


def main():
    app = QApplication([])
    window = StateVectorCompiler()
    window.resize(820, 560)
    window.show()
    app.exec()


if __name__ == "__main__":
    main()