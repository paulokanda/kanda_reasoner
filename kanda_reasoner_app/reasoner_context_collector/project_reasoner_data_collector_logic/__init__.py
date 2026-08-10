# project-path: kanda_reasoner_app/reasoner_context_collector/project_reasoner_data_collector_logic/__init__.py
import json
import os
import hashlib
from typing import Any
import copy
import traceback
from PySide6.QtWidgets import (
    QFileDialog,
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QPushButton,
    QApplication,
    QLabel,
)


# Helper functions (for example, stable_hash, get_entries, etc.) are assumed to be the same as before.

def stable_hash(value: Any) -> str:
    """Helper to generate a stable hash for the JSON object."""
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def get_entries(node: Any) -> list[tuple[Any, Any]]:
    """Extract entries from a dictionary or list."""
    if isinstance(node, dict):
        return list(node.items())
    if isinstance(node, list):
        return list(enumerate(node))
    raise TypeError("Target value must be a dictionary or list.")


def rebuild_container(entries: list[tuple[Any, Any]], is_list: bool) -> Any:
    """Rebuild a container (dict or list) from entries."""
    if is_list:
        return [value for _key, value in entries]
    return {key: value for key, value in entries}


def build_part_document(root: Any, path_parts: list[str], chunk_value: Any) -> Any:
    """Rebuild the document with chunked data."""
    return set_nested_value(root, path_parts, chunk_value)


def set_nested_value(root: Any, path_parts: list[str], new_value: Any) -> Any:
    """Set a nested value in the root, based on path_parts."""
    cloned = copy.deepcopy(root)
    if not path_parts:
        return new_value

    current = cloned
    for part in path_parts[:-1]:
        current = current[part]
    current[path_parts[-1]] = new_value
    return cloned


def split_json(input_path: str, output_dir: str, target_path: str, mode: str = "parts", value: int = 10) -> None:
    """Split JSON into parts or per-child based on the provided mode."""
    try:
        with open(input_path, "r", encoding="utf-8") as handle:
            root = json.load(handle)
    except Exception as e:
        print(f"Error opening file {input_path}: {e}")
        return

    path_parts = parse_target_path(target_path)
    target = get_nested_value(root, path_parts) if path_parts else root
    is_list = isinstance(target, list)

    entries = get_entries(target)
    if not entries:
        raise ValueError("Selected target container is empty.")

    # Process split logic
    chunks = _build_chunks(root, path_parts, entries, is_list, mode, value)
    os.makedirs(output_dir, exist_ok=True)

    base_name = os.path.splitext(os.path.basename(input_path))[0]
    total = len(chunks)
    digits = max(3, len(str(total)))

    for index, chunk_entries in enumerate(chunks, start=1):
        chunk_value = rebuild_container(chunk_entries, is_list)
        document = build_part_document(root, path_parts, chunk_value)
        part_name = f"{str(index).zfill(digits)}_{base_name}.json"
        part_path = os.path.join(output_dir, part_name)

        with open(part_path, "w", encoding="utf-8") as handle:
            json.dump(document, handle, ensure_ascii=False, indent=2)

        print(f"Wrote {part_name} | entries={len(chunk_entries)}")


def parse_target_path(path_text: str) -> list[str]:
    """Parse the target path into a list of parts."""
    text = str(path_text).strip()
    if not text:
        return []
    return [part.strip() for part in text.split(".") if part.strip()]


def get_nested_value(root: Any, path_parts: list[str]) -> Any:
    """Get nested value from JSON object using path."""
    current = root
    for part in path_parts:
        if not isinstance(current, dict):
            raise KeyError(f"Path segment '{part}' is not inside a dictionary.")
        if part not in current:
            raise KeyError(f"Path segment '{part}' was not found.")
        current = current[part]
    return current


def _build_chunks(root: Any, path_parts: list[str], entries: list[tuple[Any, Any]], is_list: bool, mode: str,
                  value: int) -> list[list[tuple[Any, Any]]]:
    """Build chunks based on the provided split mode."""
    if mode == "parts":
        part_count = max(1, min(int(value), len(entries)))
        return _build_balanced_part_chunks(root, path_parts, entries, is_list, part_count)
    elif mode == "per_child":
        return [[entry] for entry in entries]
    elif mode == "kb":
        max_bytes = max(1024, int(value) * 1024)
        return _build_kb_chunks(root, path_parts, entries, is_list, max_bytes)
    else:
        raise ValueError(f"Unknown split mode: {mode}")


def _build_balanced_part_chunks(root: Any, path_parts: list[str], entries: list[tuple[Any, Any]], is_list: bool,
                                part_count: int) -> list[list[tuple[Any, Any]]]:
    """Balanced chunk builder for near-equal part sizes with syntax preservation."""
    if part_count <= 1 or len(entries) <= 1:
        return [entries]

    estimated_sizes: list[int] = []
    for entry in entries:
        single_value = rebuild_container([entry], is_list)
        single_doc = build_part_document(root, path_parts, single_value)
        estimated_sizes.append(json_bytes(single_doc))

    total_size = sum(estimated_sizes)
    target_size = max(1, int(total_size / float(part_count)))

    chunks: list[list[tuple[Any, Any]]] = []
    current_chunk: list[tuple[Any, Any]] = []
    current_size = 0

    for index, entry in enumerate(entries):
        entry_size = estimated_sizes[index]
        if current_size + entry_size > target_size:
            chunks.append(current_chunk)
            current_chunk = [entry]
            current_size = entry_size
        else:
            current_chunk.append(entry)
            current_size += entry_size

    if current_chunk:
        chunks.append(current_chunk)

    return chunks


def _build_kb_chunks(root: Any, path_parts: list[str], entries: list[tuple[Any, Any]], is_list: bool, max_bytes: int) -> \
list[list[tuple[Any, Any]]]:
    """Split by KB size."""
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

    if current:
        chunks.append(current)

    return chunks


def json_bytes(value: Any) -> int:
    """Calculate the byte size of the JSON object."""
    return len(json.dumps(value, ensure_ascii=False, separators=(",", ":")).encode("utf-8"))


#### - App GUI for Folder Selection ####


class FolderSelectionWindow(QWidget):
    """Represent folder selection window."""
    
    def __init__(self):
        """Support init behavior.
        """
        
        super().__init__()
        self.setWindowTitle("Select Folder and JSON File")
        self.setGeometry(100, 100, 400, 200)

        # UI Elements
        self.layout = QVBoxLayout(self)
        self.file_line_edit = QLineEdit(self)
        self.file_line_edit.setPlaceholderText("Selected JSON file will appear here")
        self.layout.addWidget(self.file_line_edit)

        self.browse_button = QPushButton("Browse Folder", self)
        self.browse_button.clicked.connect(self.browse_folder)
        self.layout.addWidget(self.browse_button)

        self.select_button = QPushButton("Select JSON File", self)
        self.select_button.clicked.connect(self.select_json_file)
        self.layout.addWidget(self.select_button)

        self.split_button = QPushButton("Start Splitting", self)
        self.split_button.clicked.connect(self.start_splitting)
        self.layout.addWidget(self.split_button)

        self.summary_label = QLabel("", self)
        self.layout.addWidget(self.summary_label)

    def browse_folder(self):
        """Support browse folder behavior.
        """
        
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.file_line_edit.setText(folder)

    def select_json_file(self):
        """Support select json file behavior.
        """
        
        folder = self.file_line_edit.text().strip()
        if not folder:
            self.summary_label.setText("Please select a folder first!")
            return
        file, _ = QFileDialog.getOpenFileName(self, "Select JSON File", folder, "JSON Files (*.json)")
        if file:
            self.summary_label.setText(f"Selected file: {file}")
            print(f"Selected file: {file}")

    def start_splitting(self):
        """Support start splitting behavior.
        """
        
        folder = self.file_line_edit.text().strip()
        if not folder:
            self.summary_label.setText("Please select a folder first!")
            return
        file, _ = QFileDialog.getOpenFileName(self, "Select JSON File", folder, "JSON Files (*.json)")
        if not file:
            self.summary_label.setText("No file selected!")
            return

        output_dir = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if not output_dir:
            self.summary_label.setText("Please select an output folder!")
            return

        # Assuming we split by parts here, adjust based on your selection logic
        target_path = "project_summary.git_metadata"  # Example target path
        split_json(file, output_dir, target_path, mode="parts", value=10)


if __name__ == "__main__":
    app = QApplication([])
    window = FolderSelectionWindow()
    window.show()
    app.exec()
