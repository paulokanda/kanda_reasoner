from __future__ import annotations

import copy
import hashlib
import json
import math
import os
import traceback
from dataclasses import dataclass
from typing import Any

from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import (
    QApplication,
    QButtonGroup,
    QComboBox,
    QFileDialog,
    QFrame,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QSpinBox,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


#### - JSON helper data container - ####
@dataclass
class SplitPlan:
    input_path: str
    output_dir: str
    target_path: str
    mode: str
    value: int


#### - basic JSON text helper - ####
def json_bytes(value: Any) -> int:
    return len(json.dumps(value, ensure_ascii=False, separators=(",", ":")).encode("utf-8"))


#### - stable content hash helper - ####
def stable_hash(value: Any) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


#### - nested path parser - ####
def parse_target_path(path_text: str) -> list[str]:
    text = str(path_text).strip()
    if not text:
        return []
    return [part.strip() for part in text.split(".") if part.strip()]


#### - nested getter - ####
def get_nested_value(root: Any, path_parts: list[str]) -> Any:
    current = root
    for part in path_parts:
        if not isinstance(current, dict):
            raise KeyError(f"Path segment '{part}' is not inside a dictionary.")
        if part not in current:
            raise KeyError(f"Path segment '{part}' was not found.")
        current = current[part]
    return current


#### - nested setter on a cloned structure - ####
def set_nested_value(root: Any, path_parts: list[str], new_value: Any) -> Any:
    cloned = copy.deepcopy(root)
    if not path_parts:
        return new_value

    current = cloned
    for part in path_parts[:-1]:
        current = current[part]
    current[path_parts[-1]] = new_value
    return cloned


#### - nested direct child names for combo suggestions - ####
def collect_container_paths(root: Any, max_depth: int = 4) -> list[str]:
    paths: list[str] = []

    def walk(node: Any, prefix: list[str], depth: int) -> None:
        if depth > max_depth:
            return
        if isinstance(node, dict):
            if prefix:
                paths.append(".".join(prefix))
            for key, value in node.items():
                if isinstance(value, (dict, list)):
                    walk(value, prefix + [str(key)], depth + 1)
        elif isinstance(node, list):
            if prefix:
                paths.append(".".join(prefix))

    walk(root, [], 0)
    return sorted(set(paths))


#### - direct entries extractor - ####
def get_entries(node: Any) -> list[tuple[Any, Any]]:
    if isinstance(node, dict):
        return list(node.items())
    if isinstance(node, list):
        return list(enumerate(node))
    raise TypeError("Target value must be a dictionary or list.")


#### - direct container rebuild - ####
def rebuild_container(entries: list[tuple[Any, Any]], is_list: bool) -> Any:
    if is_list:
        return [value for _key, value in entries]
    return {key: value for key, value in entries}


#### - exact file size estimate using real wrapper - ####
def build_part_document(root: Any, path_parts: list[str], chunk_value: Any) -> Any:
    return set_nested_value(root, path_parts, chunk_value)


#### - worker thread for split and reassemble - ####
class SplitterWorker(QThread):
    progress = Signal(int)
    log = Signal(str)
    finished = Signal(bool, str)

    def __init__(self, action: str, payload: dict[str, Any]) -> None:
        super().__init__()
        self.action = action
        self.payload = payload

    def run(self) -> None:
        try:
            if self.action == "split":
                self._run_split()
            elif self.action == "reassemble":
                self._run_reassemble()
            else:
                self.finished.emit(False, f"Unknown action: {self.action}")
        except Exception as exc:
            self.finished.emit(False, f"Unexpected error: {exc}\n{traceback.format_exc()}")

    #### - split runner - ####
    def _run_split(self) -> None:
        plan = SplitPlan(**self.payload)

        self.log.emit(f"Reading JSON: {plan.input_path}")
        with open(plan.input_path, "r", encoding="utf-8") as handle:
            root = json.load(handle)

        path_parts = parse_target_path(plan.target_path)
        target = get_nested_value(root, path_parts) if path_parts else root
        is_list = isinstance(target, list)
        if not isinstance(target, (dict, list)):
            raise TypeError("Selected target path must point to a dict or list.")

        entries = get_entries(target)
        if not entries:
            raise ValueError("Selected target container is empty.")

        self.log.emit(f"Target path: {plan.target_path or '<root>'}")
        self.log.emit(f"Target container type: {'list' if is_list else 'dict'}")
        self.log.emit(f"Direct entries found: {len(entries)}")

        chunks = self._build_chunks(root, path_parts, entries, is_list, plan.mode, plan.value)
        if not chunks:
            raise RuntimeError("No chunks were produced.")

        os.makedirs(plan.output_dir, exist_ok=True)
        base_name = os.path.splitext(os.path.basename(plan.input_path))[0]
        total = len(chunks)
        digits = max(3, len(str(total)))
        manifest_parts: list[dict[str, Any]] = []

        for index, chunk_entries in enumerate(chunks, start=1):
            chunk_value = rebuild_container(chunk_entries, is_list)
            document = build_part_document(root, path_parts, chunk_value)
            part_name = f"{str(index).zfill(digits)}_{base_name}.json"
            part_path = os.path.join(plan.output_dir, part_name)

            with open(part_path, "w", encoding="utf-8") as handle:
                json.dump(document, handle, ensure_ascii=False, indent=2)

            size_bytes = os.path.getsize(part_path)
            manifest_parts.append(
                {
                    "index": index,
                    "filename": part_name,
                    "entries": len(chunk_entries),
                    "size_bytes": size_bytes,
                    "sha256": stable_hash(document),
                }
            )
            self.log.emit(
                f"Wrote {part_name} | entries={len(chunk_entries)} | size_kb={size_bytes / 1024.0:.2f}"
            )
            self.progress.emit(int(index / total * 100))

        manifest = {
            "splitter_version": "4.1",
            "source_file": os.path.abspath(plan.input_path),
            "source_sha256": stable_hash(root),
            "target_path": plan.target_path,
            "target_type": "list" if is_list else "dict",
            "mode": plan.mode,
            "value": plan.value,
            "part_count": total,
            "parts": manifest_parts,
        }

        manifest_name = f"{base_name}__split_manifest.json"
        manifest_path = os.path.join(plan.output_dir, manifest_name)
        with open(manifest_path, "w", encoding="utf-8") as handle:
            json.dump(manifest, handle, ensure_ascii=False, indent=2)

        self.progress.emit(100)
        self.finished.emit(True, f"Done. Created {total} JSON parts and manifest: {manifest_path}")

    #### - chunk builder - ####
    def _build_chunks(
        self,
        root: Any,
        path_parts: list[str],
        entries: list[tuple[Any, Any]],
        is_list: bool,
        mode: str,
        value: int,
    ) -> list[list[tuple[Any, Any]]]:
        if mode == "parts":
            part_count = max(1, min(int(value), len(entries)))
            return self._build_balanced_part_chunks(root, path_parts, entries, is_list, part_count)

        if mode == "per_child":
            return [[entry] for entry in entries]

        if mode == "kb":
            max_bytes = max(1024, int(value) * 1024)
            chunks: list[list[tuple[Any, Any]]] = []
            current: list[tuple[Any, Any]] = []

            for entry in entries:
                candidate = current + [entry]
                candidate_value = rebuild_container(candidate, is_list)
                candidate_doc = build_part_document(root, path_parts, candidate_value)
                candidate_size = json_bytes(candidate_doc)

                if current and candidate_size > max_bytes:
                    chunks.append(current)
                    current = [entry]
                else:
                    current = candidate

                single_value = rebuild_container([entry], is_list)
                single_doc = build_part_document(root, path_parts, single_value)
                single_size = json_bytes(single_doc)
                if single_size > max_bytes:
                    self.log.emit(
                        "Warning: one single entry already exceeds the selected size limit. "
                        "It will be written alone in its own file."
                    )

            if current:
                chunks.append(current)
            return chunks

        raise ValueError(f"Unknown split mode: {mode}")

    #### - balanced chunk builder for near-equal part sizes - ####
    def _build_balanced_part_chunks(
        self,
        root: Any,
        path_parts: list[str],
        entries: list[tuple[Any, Any]],
        is_list: bool,
        part_count: int,
    ) -> list[list[tuple[Any, Any]]]:
        if part_count <= 1 or len(entries) <= 1:
            return [entries]

        estimated_sizes: list[int] = []
        for entry in entries:
            single_value = rebuild_container([entry], is_list)
            single_doc = build_part_document(root, path_parts, single_value)
            estimated_sizes.append(json_bytes(single_doc))

        total_size = sum(estimated_sizes)
        target_size = max(1, int(math.ceil(total_size / float(part_count))))

        chunks: list[list[tuple[Any, Any]]] = []
        current_chunk: list[tuple[Any, Any]] = []
        current_size = 0

        for index, entry in enumerate(entries):
            remaining_entries = len(entries) - index
            remaining_slots = part_count - len(chunks)
            entry_size = estimated_sizes[index]

            must_close_for_slot_reserve = (
                current_chunk
                and remaining_entries == remaining_slots
            )

            would_cross_target = (
                current_chunk
                and current_size + entry_size > target_size
                and len(chunks) < part_count - 1
            )

            if must_close_for_slot_reserve or would_cross_target:
                chunks.append(current_chunk)
                current_chunk = []
                current_size = 0

            current_chunk.append(entry)
            current_size += entry_size

        if current_chunk:
            chunks.append(current_chunk)

        while len(chunks) > part_count:
            tail = chunks.pop()
            chunks[-1].extend(tail)

        while len(chunks) < part_count and any(len(chunk) > 1 for chunk in chunks):
            largest_index = max(range(len(chunks)), key=lambda i: len(chunks[i]))
            largest_chunk = chunks[largest_index]
            moved_entry = largest_chunk.pop()
            chunks.insert(largest_index + 1, [moved_entry])

        return [chunk for chunk in chunks if chunk]

    #### - reassemble runner - ####
    def _run_reassemble(self) -> None:
        manifest_path = self.payload["manifest_path"]
        output_path = self.payload["output_path"]

        self.log.emit(f"Reading manifest: {manifest_path}")
        with open(manifest_path, "r", encoding="utf-8") as handle:
            manifest = json.load(handle)

        target_path = str(manifest.get("target_path", ""))
        path_parts = parse_target_path(target_path)
        target_type = str(manifest.get("target_type", "dict"))
        is_list = target_type == "list"

        manifest_dir = os.path.dirname(os.path.abspath(manifest_path))
        parts = manifest.get("parts", [])
        if not parts:
            raise ValueError("Manifest has no parts.")

        root_template = None
        merged_entries: list[tuple[Any, Any]] = []

        total = len(parts)
        for index, part_info in enumerate(parts, start=1):
            filename = str(part_info["filename"])
            part_path = os.path.join(manifest_dir, filename)
            self.log.emit(f"Reading part: {part_path}")

            with open(part_path, "r", encoding="utf-8") as handle:
                part_doc = json.load(handle)

            if root_template is None:
                root_template = copy.deepcopy(part_doc)
            target_value = get_nested_value(part_doc, path_parts) if path_parts else part_doc
            part_entries = get_entries(target_value)
            merged_entries.extend(part_entries)
            self.progress.emit(int(index / total * 100))

        if root_template is None:
            raise RuntimeError("Failed to establish a template document during reassembly.")

        merged_value = rebuild_container(merged_entries, is_list)
        merged_document = build_part_document(root_template, path_parts, merged_value)

        with open(output_path, "w", encoding="utf-8") as handle:
            json.dump(merged_document, handle, ensure_ascii=False, indent=2)

        rebuilt_hash = stable_hash(merged_document)
        source_hash = str(manifest.get("source_sha256", ""))
        if source_hash:
            if rebuilt_hash == source_hash:
                self.log.emit("Reassembled JSON hash matches original source hash.")
            else:
                self.log.emit("Warning: reassembled JSON hash does not match original source hash.")

        self.progress.emit(100)
        self.finished.emit(True, f"Reassembly complete: {output_path}")


#### - main GUI window - ####
class JsonSplitterWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.worker: SplitterWorker | None = None
        self.loaded_json: Any = None
        self.setWindowTitle("JSON Splitter 4.1 - Balanced Syntax Safe Splitter")
        self.resize(900, 820)
        self._build_ui()

    #### - build all widgets - ####
    def _build_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(16, 16, 16, 16)
        root.setSpacing(12)

        file_group = QGroupBox("Input JSON")
        file_layout = QGridLayout(file_group)
        self.input_edit = QLineEdit()
        self.browse_input_button = QPushButton("Browse JSON")
        self.inspect_button = QPushButton("Inspect")
        file_layout.addWidget(QLabel("Input file"), 0, 0)
        file_layout.addWidget(self.input_edit, 0, 1)
        file_layout.addWidget(self.browse_input_button, 0, 2)
        file_layout.addWidget(self.inspect_button, 0, 3)

        target_group = QGroupBox("Target Container To Split")
        target_layout = QGridLayout(target_group)
        self.target_edit = QLineEdit()
        self.target_edit.setPlaceholderText("Example: project_summary.git_metadata")
        self.target_combo = QComboBox()
        self.apply_target_button = QPushButton("Use Suggested Path")
        target_layout.addWidget(QLabel("Target path"), 0, 0)
        target_layout.addWidget(self.target_edit, 0, 1, 1, 3)
        target_layout.addWidget(QLabel("Detected container paths"), 1, 0)
        target_layout.addWidget(self.target_combo, 1, 1, 1, 2)
        target_layout.addWidget(self.apply_target_button, 1, 3)

        mode_group = QGroupBox("Split Mode")
        mode_layout = QGridLayout(mode_group)
        self.parts_radio = QRadioButton("Split by number of parts")
        self.kb_radio = QRadioButton("Split by max size in KB")
        self.child_radio = QRadioButton("One file per direct child")
        self.parts_radio.setChecked(True)
        self.mode_group = QButtonGroup(self)
        self.mode_group.addButton(self.parts_radio)
        self.mode_group.addButton(self.kb_radio)
        self.mode_group.addButton(self.child_radio)
        self.parts_spin = QSpinBox()
        self.parts_spin.setRange(1, 100000)
        self.parts_spin.setValue(10)
        self.kb_spin = QSpinBox()
        self.kb_spin.setRange(1, 1024 * 1024)
        self.kb_spin.setValue(512)
        mode_layout.addWidget(self.parts_radio, 0, 0)
        mode_layout.addWidget(self.parts_spin, 0, 1)
        mode_layout.addWidget(self.kb_radio, 1, 0)
        mode_layout.addWidget(self.kb_spin, 1, 1)
        mode_layout.addWidget(self.child_radio, 2, 0, 1, 2)

        output_group = QGroupBox("Output")
        output_layout = QGridLayout(output_group)
        self.output_edit = QLineEdit()
        self.browse_output_button = QPushButton("Browse Folder")
        output_layout.addWidget(QLabel("Output folder"), 0, 0)
        output_layout.addWidget(self.output_edit, 0, 1)
        output_layout.addWidget(self.browse_output_button, 0, 2)

        action_row = QHBoxLayout()
        self.split_button = QPushButton("Split JSON")
        self.reassemble_button = QPushButton("Reassemble From Manifest")
        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        action_row.addWidget(self.split_button)
        action_row.addWidget(self.reassemble_button)
        action_row.addWidget(self.progress, 1)

        self.summary_label = QLabel("No JSON inspected yet.")
        self.summary_label.setFrameShape(QFrame.Shape.StyledPanel)
        self.summary_label.setMinimumHeight(60)
        self.summary_label.setWordWrap(True)

        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)

        root.addWidget(file_group)
        root.addWidget(target_group)
        root.addWidget(mode_group)
        root.addWidget(output_group)
        root.addLayout(action_row)
        root.addWidget(QLabel("Summary"))
        root.addWidget(self.summary_label)
        root.addWidget(QLabel("Log"))
        root.addWidget(self.log_box, 1)

        self.browse_input_button.clicked.connect(self._browse_input)
        self.browse_output_button.clicked.connect(self._browse_output)
        self.inspect_button.clicked.connect(self._inspect_json)
        self.apply_target_button.clicked.connect(self._apply_target_from_combo)
        self.split_button.clicked.connect(self._start_split)
        self.reassemble_button.clicked.connect(self._start_reassemble)

    #### - log helper - ####
    def _append_log(self, text: str) -> None:
        self.log_box.append(text)

    #### - browse input file - ####
    def _browse_input(self) -> None:
        path, _filter = QFileDialog.getOpenFileName(self, "Select JSON", "", "JSON Files (*.json)")
        if path:
            self.input_edit.setText(path)

    #### - browse output folder - ####
    def _browse_output(self) -> None:
        path = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if path:
            self.output_edit.setText(path)

    #### - inspect JSON and populate target paths - ####
    def _inspect_json(self) -> None:
        input_path = self.input_edit.text().strip()
        if not input_path:
            QMessageBox.warning(self, "Missing file", "Select an input JSON file first.")
            return

        try:
            with open(input_path, "r", encoding="utf-8") as handle:
                self.loaded_json = json.load(handle)
        except Exception as exc:
            QMessageBox.critical(self, "Read error", str(exc))
            return

        self.target_combo.clear()
        self.target_combo.addItem("")
        for path in collect_container_paths(self.loaded_json, max_depth=6):
            self.target_combo.addItem(path)

        root_type = type(self.loaded_json).__name__
        size_kb = os.path.getsize(input_path) / 1024.0
        path_count = max(0, self.target_combo.count() - 1)
        self.summary_label.setText(
            f"Root type: {root_type}\n"
            f"File size: {size_kb:.2f} KB\n"
            f"Detected container paths: {path_count}"
        )
        self._append_log(f"Inspected JSON: {input_path}")

    #### - apply selected target path from combo - ####
    def _apply_target_from_combo(self) -> None:
        self.target_edit.setText(self.target_combo.currentText().strip())

    #### - start split action - ####
    def _start_split(self) -> None:
        input_path = self.input_edit.text().strip()
        output_dir = self.output_edit.text().strip()
        target_path = self.target_edit.text().strip()

        if not input_path or not output_dir:
            QMessageBox.warning(self, "Missing data", "Select input JSON and output folder.")
            return

        if self.parts_radio.isChecked():
            mode = "parts"
            value = int(self.parts_spin.value())
        elif self.kb_radio.isChecked():
            mode = "kb"
            value = int(self.kb_spin.value())
        else:
            mode = "per_child"
            value = 1

        payload = {
            "input_path": input_path,
            "output_dir": output_dir,
            "target_path": target_path,
            "mode": mode,
            "value": value,
        }
        self._start_worker("split", payload)

    #### - start reassemble action - ####
    def _start_reassemble(self) -> None:
        manifest_path, _filter = QFileDialog.getOpenFileName(
            self,
            "Select Split Manifest",
            self.output_edit.text().strip() or "",
            "JSON Files (*.json)",
        )
        if not manifest_path:
            return

        output_path, _filter = QFileDialog.getSaveFileName(
            self,
            "Save Reassembled JSON",
            os.path.join(os.path.dirname(manifest_path), "reassembled.json"),
            "JSON Files (*.json)",
        )
        if not output_path:
            return

        payload = {
            "manifest_path": manifest_path,
            "output_path": output_path,
        }
        self._start_worker("reassemble", payload)

    #### - common worker bootstrap - ####
    def _start_worker(self, action: str, payload: dict[str, Any]) -> None:
        if self.worker is not None and self.worker.isRunning():
            QMessageBox.information(self, "Busy", "Another operation is already running.")
            return

        self.progress.setValue(0)
        self.worker = SplitterWorker(action, payload)
        self.worker.log.connect(self._append_log)
        self.worker.progress.connect(self.progress.setValue)
        self.worker.finished.connect(self._on_worker_finished)
        self.worker.start()

    #### - worker finish handler - ####
    def _on_worker_finished(self, ok: bool, message: str) -> None:
        self._append_log(message)
        if ok:
            QMessageBox.information(self, "Finished", message)
        else:
            QMessageBox.critical(self, "Error", message)


#### - app entry point - ####
def main() -> None:
    app = QApplication([])
    window = JsonSplitterWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
