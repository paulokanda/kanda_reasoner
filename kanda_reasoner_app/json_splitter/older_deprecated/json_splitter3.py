import sys
import json
import os
import math
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QFileDialog, QRadioButton,
    QButtonGroup, QSpinBox, QDoubleSpinBox, QProgressBar,
    QTextEdit, QGroupBox, QFrame, QComboBox
)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QFont

# ----------------------------------------------------------------------
# Constants for size estimation (extra bytes per entry in JSON arrays/objects)
# ----------------------------------------------------------------------
OVERHEAD_PER_ENTRY = 10          # rough estimate for quotes, commas, colons, braces

# ----------------------------------------------------------------------
# Helper functions – operate on direct children only
# ----------------------------------------------------------------------
def get_entries(node):
    """Return list of (key, value) for direct children of node."""
    if isinstance(node, dict):
        return list(node.items())
    elif isinstance(node, list):
        return list(enumerate(node))
    return []

def rebuild(entries, is_list):
    """Reconstruct container from (key, value) entries."""
    if is_list:
        return [v for _, v in entries]
    return {k: v for k, v in entries}

def estimate_entry_size(entry, is_list):
    """Return approximate JSON byte size of a single entry in its container."""
    sample = rebuild([entry], is_list)
    # actual JSON size without outer container's overhead
    return len(json.dumps(sample, ensure_ascii=False).encode())

# ----------------------------------------------------------------------
# Worker thread
# ----------------------------------------------------------------------
class SplitterWorker(QThread):
    progress = Signal(int)
    log      = Signal(str)
    finished = Signal(bool, str)

    def __init__(self, filepath, out_dir, mode, value, split_key):
        super().__init__()
        self.filepath  = filepath
        self.out_dir   = out_dir      # where to write the split files
        self.mode      = mode          # "parts" | "kb" | "top_keys"
        self.value     = value
        self.split_key = split_key     # only meaningful when root is a dict

    def run(self):
        try:
            self.log.emit(f"📂 Reading: {self.filepath}")
            with open(self.filepath, "r", encoding="utf-8") as f:
                data = json.load(f)

            # ----------------------------------------------------------
            # Determine what we are splitting
            # ----------------------------------------------------------
            root_is_list = isinstance(data, list)

            if root_is_list:
                # whole file is a list → split its items directly
                preserved   = None
                tree        = data
                is_list     = True
                split_label = "root list"   # for logging only
                self.log.emit("✅ Root is a list – will split its items.")
            else:
                # root is a dict – we split a specific key
                if self.split_key not in data:
                    self.finished.emit(False,
                        f"❌ Key '{self.split_key}' not found in the root dictionary.")
                    return

                subtree = data[self.split_key]
                if not isinstance(subtree, (dict, list)):
                    self.finished.emit(False,
                        f"❌ Key '{self.split_key}' must be a dict or list, got {type(subtree).__name__}.")
                    return

                preserved = {k: v for k, v in data.items() if k != self.split_key}
                tree      = subtree
                is_list   = isinstance(tree, list)
                split_label = f"'{self.split_key}'"
                self.log.emit(f"✅ Splitting key {split_label} ({'list' if is_list else 'dict'})")

            # ----------------------------------------------------------
            # Get direct children of the chosen subtree
            # ----------------------------------------------------------
            entries = get_entries(tree)
            total   = len(entries)
            if total == 0:
                self.finished.emit(False, f"❌ No entries found under {split_label}.")
                return
            self.log.emit(f"   {total} direct entries.")

            # ----------------------------------------------------------
            # Build chunks according to selected mode
            # ----------------------------------------------------------
            if self.mode == "parts":
                n = max(1, min(int(self.value), total))
                chunk_size = math.ceil(total / n)
                chunks = [entries[i:i+chunk_size] for i in range(0, total, chunk_size)]
                self.log.emit(f"   Splitting into {len(chunks)} part(s), ~{chunk_size} entries each.")

            elif self.mode == "kb":
                target_bytes = float(self.value) * 1024

                # Size of the preserved part (only relevant when root is dict)
                if preserved is not None:
                    preserved_sz = len(json.dumps(preserved, ensure_ascii=False).encode())
                else:
                    preserved_sz = 0

                # Available space for the chunk itself (with a safety margin)
                effective_limit = max(target_bytes - preserved_sz - 64, 512)

                chunks, cur, cur_sz = [], [], 0
                for entry in entries:
                    entry_sz = estimate_entry_size(entry, is_list)
                    # add overhead that will appear when this entry is placed inside the chunk
                    total_entry_sz = entry_sz + OVERHEAD_PER_ENTRY

                    if cur_sz + total_entry_sz > effective_limit and cur:
                        # current chunk is full enough
                        chunks.append(cur)
                        cur, cur_sz = [entry], entry_sz
                    else:
                        cur.append(entry)
                        cur_sz += entry_sz   # we postpone overhead until final chunk measurement

                if cur:
                    chunks.append(cur)

                self.log.emit(f"   Built {len(chunks)} chunk(s) aiming for ≤ {self.value} KB per file.")

            else:  # "top_keys" – one file per direct child (only valid for dict)
                if is_list:
                    self.finished.emit(False,
                        "❌ 'By top-level children' can only be used when the split key contains a dictionary.")
                    return
                chunks = [[e] for e in entries]
                self.log.emit(f"   Will create one file per top-level key ({len(chunks)} files).")

            # ----------------------------------------------------------
            # Write the chunks to disk
            # ----------------------------------------------------------
            total_chunks = len(chunks)
            padding      = len(str(total_chunks))
            base_name    = os.path.splitext(os.path.basename(self.filepath))[0]

            self.log.emit(f"🔀 Writing {total_chunks} file(s) to:\n   {self.out_dir}")

            for idx, chunk in enumerate(chunks, start=1):
                num_str = str(idx).zfill(padding)
                out_filename = f"{num_str}_{base_name}.json"
                out_path = os.path.join(self.out_dir, out_filename)

                # Rebuild the chunk into a proper dict/list
                subtree_chunk = rebuild(chunk, is_list)

                if root_is_list:
                    # Output is a plain list
                    out_data = subtree_chunk
                else:
                    # Output is dict with preserved keys + the split key containing the chunk
                    out_data = dict(preserved)
                    out_data[self.split_key] = subtree_chunk

                try:
                    with open(out_path, "w", encoding="utf-8") as f:
                        json.dump(out_data, f, ensure_ascii=False, indent=2)

                    size_kb = os.path.getsize(out_path) / 1024
                    self.log.emit(
                        f"   ✔ {out_filename}  ({len(chunk)} entries, {size_kb:.1f} KB)")
                except Exception as e:
                    self.log.emit(f"   ❌ {out_filename} FAILED: {e}")

                self.progress.emit(int(idx / total_chunks * 100))

            self.finished.emit(True, f"🎉 Done! {total_chunks} file(s) created.")

        except json.JSONDecodeError as e:
            self.finished.emit(False, f"❌ Invalid JSON: {e}")
        except Exception as e:
            import traceback
            self.finished.emit(False, f"❌ Unexpected error: {e}\n{traceback.format_exc()}")

# ----------------------------------------------------------------------
# Main window (UI)
# ----------------------------------------------------------------------
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("JSON File Splitter")
        self.setMinimumSize(720, 760)
        self.worker = None
        self._build_ui()
        self._apply_style()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setSpacing(14)
        root.setContentsMargins(20, 20, 20, 20)

        # Title
        title = QLabel("JSON File Splitter")
        title.setAlignment(Qt.AlignCenter)
        f = QFont(); f.setPointSize(18); f.setBold(True)
        title.setFont(f); title.setObjectName("title")
        root.addWidget(title)

        sub = QLabel("Splits nested JSON — preserves meta/header keys in every output file")
        sub.setAlignment(Qt.AlignCenter); sub.setObjectName("subtitle")
        root.addWidget(sub)

        sep = QFrame(); sep.setFrameShape(QFrame.HLine); sep.setObjectName("separator")
        root.addWidget(sep)

        # ---- File picker ----
        file_group = QGroupBox("Input File")
        fl = QHBoxLayout(file_group)
        self.file_edit = QLineEdit()
        self.file_edit.setPlaceholderText("Select a JSON file…")
        self.file_edit.setReadOnly(True)
        browse_btn = QPushButton("Browse…")
        browse_btn.setObjectName("browse_btn")
        browse_btn.clicked.connect(self._browse_file)
        fl.addWidget(self.file_edit); fl.addWidget(browse_btn)
        root.addWidget(file_group)

        # ---- Output directory picker ----
        out_group = QGroupBox("Output Directory (optional)")
        out_layout = QHBoxLayout(out_group)
        self.out_edit = QLineEdit()
        self.out_edit.setPlaceholderText("Same as input file (leave empty)")
        out_browse = QPushButton("Browse…")
        out_browse.setObjectName("browse_btn")
        out_browse.clicked.connect(self._browse_output)
        out_layout.addWidget(self.out_edit); out_layout.addWidget(out_browse)
        root.addWidget(out_group)

        # ---- Key selector ----
        key_group = QGroupBox("Key to Split")
        kl = QVBoxLayout(key_group)
        hint = QLabel(
            "Choose the top-level key whose contents will be divided.\n"
            "All other top-level keys are copied into every output file."
        )
        hint.setObjectName("hint"); hint.setWordWrap(True)
        kl.addWidget(hint)
        kr = QHBoxLayout()
        kr.addWidget(QLabel("Split key:"))
        self.key_combo = QComboBox()
        self.key_combo.setMinimumWidth(220)
        kr.addWidget(self.key_combo); kr.addStretch()
        kl.addLayout(kr)
        root.addWidget(key_group)

        # ---- Split mode ----
        mode_group = QGroupBox("Split Mode")
        ml = QVBoxLayout(mode_group)
        ml.setSpacing(3)
        ml.setContentsMargins(12, 10, 12, 10)

        small_font = QFont(); small_font.setPointSize(10)

        self.radio_parts = QRadioButton("By number of parts  (evenly distribute entries)")
        self.radio_kb    = QRadioButton("By max file size (KB)  (fill each file up to limit)")
        self.radio_top   = QRadioButton("By top-level children  (one file per immediate child key)")

        self.spin_parts = QSpinBox()
        self.spin_parts.setRange(2, 9999); self.spin_parts.setValue(5)
        self.spin_parts.setSuffix(" parts")
        self.spin_parts.setSingleStep(1)
        self.spin_parts.setAccelerated(True)
        self.spin_parts.setMinimumHeight(48)
        self.spin_parts.setMinimumWidth(160)

        self.spin_kb = QDoubleSpinBox()
        self.spin_kb.setRange(0.1, 999999); self.spin_kb.setValue(500)
        self.spin_kb.setSuffix(" KB"); self.spin_kb.setDecimals(1)
        self.spin_kb.setMinimumHeight(48)
        self.spin_kb.setMinimumWidth(160)
        self.spin_kb.setVisible(False)

        bg = QButtonGroup(self)
        for r in (self.radio_parts, self.radio_kb, self.radio_top):
            r.setFont(small_font); bg.addButton(r)
        self.radio_parts.setChecked(True)
        self.radio_parts.toggled.connect(self._toggle_mode)
        self.radio_kb.toggled.connect(self._toggle_mode)
        self.radio_top.toggled.connect(self._toggle_mode)

        row_parts = QHBoxLayout(); row_parts.setSpacing(10)
        row_parts.addWidget(self.radio_parts)
        row_parts.addWidget(self.spin_parts)
        row_parts.addStretch()

        row_kb = QHBoxLayout(); row_kb.setSpacing(10)
        row_kb.addWidget(self.radio_kb)
        row_kb.addWidget(self.spin_kb)
        row_kb.addStretch()

        ml.addLayout(row_parts)
        ml.addLayout(row_kb)
        ml.addWidget(self.radio_top)
        root.addWidget(mode_group)

        # ---- Progress ----
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0); self.progress_bar.setObjectName("progress")
        root.addWidget(self.progress_bar)

        # ---- Log ----
        log_group = QGroupBox("Log")
        ll = QVBoxLayout(log_group)
        self.log_box = QTextEdit(); self.log_box.setReadOnly(True)
        self.log_box.setMinimumHeight(140); self.log_box.setObjectName("log_box")
        ll.addWidget(self.log_box)
        root.addWidget(log_group)

        # ---- Buttons ----
        btn_row = QHBoxLayout()
        self.clear_btn = QPushButton("Clear Log")
        self.clear_btn.setObjectName("clear_btn")
        self.clear_btn.clicked.connect(self._clear_log)
        self.run_btn = QPushButton("▶  Split JSON")
        self.run_btn.setObjectName("run_btn")
        self.run_btn.clicked.connect(self._run)
        btn_row.addWidget(self.clear_btn); btn_row.addStretch(); btn_row.addWidget(self.run_btn)
        root.addLayout(btn_row)

    def _apply_style(self):
        self.setStyleSheet("""
            QMainWindow, QWidget { background:#1e1e2e; color:#cdd6f4;
                font-family:'Segoe UI','Helvetica Neue',sans-serif; font-size:13px; }
            QGroupBox { border:1px solid #45475a; border-radius:8px; margin-top:10px;
                padding:10px 8px 8px 8px; font-weight:bold; color:#89b4fa; }
            QGroupBox::title { subcontrol-origin:margin; left:10px; padding:0 4px; }
            QLabel#title { color:#89b4fa; font-size:20px; }
            QLabel#subtitle { color:#6c7086; font-size:12px; }
            QLabel#hint { color:#6c7086; font-size:12px; }
            QFrame#separator { color:#313244; }
            QLineEdit { background:#313244; border:1px solid #45475a; border-radius:5px;
                padding:6px 10px; color:#cdd6f4; }
            QLineEdit:focus { border-color:#89b4fa; }
            QComboBox { background:#313244; border:1px solid #45475a; border-radius:5px;
                padding:5px 10px; color:#cdd6f4; min-height:28px; }
            QComboBox QAbstractItemView { background:#313244; color:#cdd6f4;
                selection-background-color:#45475a; }
            QSpinBox, QDoubleSpinBox { background:#313244; border:1px solid #45475a;
                border-radius:5px; padding:5px 8px; color:#cdd6f4; min-width:120px; }
            QSpinBox:focus, QDoubleSpinBox:focus { border-color:#89b4fa; }
            QRadioButton { spacing:8px; color:#cdd6f4; padding:2px 0; }
            QRadioButton::indicator { width:14px; height:14px; border-radius:7px;
                border:2px solid #89b4fa; background:transparent; }
            QRadioButton::indicator:checked { background:#89b4fa; }
            QProgressBar#progress { background:#313244; border:1px solid #45475a;
                border-radius:6px; height:18px; text-align:center; color:#1e1e2e; }
            QProgressBar#progress::chunk { background:qlineargradient(x1:0,y1:0,x2:1,y2:0,
                stop:0 #89b4fa,stop:1 #cba6f7); border-radius:5px; }
            QTextEdit#log_box { background:#181825; border:1px solid #313244;
                border-radius:6px; color:#a6e3a1;
                font-family:'Consolas','Courier New',monospace; font-size:12px; padding:6px; }
            QPushButton { border-radius:6px; padding:8px 18px; font-weight:bold; }
            QPushButton#browse_btn { background:#313244; border:1px solid #45475a; color:#cdd6f4; }
            QPushButton#browse_btn:hover { background:#45475a; }
            QPushButton#run_btn { background:#89b4fa; color:#1e1e2e;
                min-width:130px; font-size:14px; }
            QPushButton#run_btn:hover { background:#b4befe; }
            QPushButton#run_btn:disabled { background:#45475a; color:#6c7086; }
            QPushButton#clear_btn { background:transparent; border:1px solid #45475a; color:#6c7086; }
            QPushButton#clear_btn:hover { border-color:#f38ba8; color:#f38ba8; }
        """)

    def _toggle_mode(self):
        if self.radio_parts.isChecked():
            self.spin_parts.setVisible(True); self.spin_kb.setVisible(False)
        elif self.radio_kb.isChecked():
            self.spin_parts.setVisible(False); self.spin_kb.setVisible(True)
        else:
            self.spin_parts.setVisible(False); self.spin_kb.setVisible(False)

    def _browse_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Open JSON File", "", "JSON Files (*.json);;All Files (*)")
        if not path:
            return
        self.file_edit.setText(path)
        # Automatically set output dir to same as input (if not already set)
        if not self.out_edit.text():
            self.out_edit.setText(os.path.dirname(path))
        self._load_keys(path)

    def _browse_output(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select Output Directory")
        if dir_path:
            self.out_edit.setText(dir_path)

    def _load_keys(self, path):
        self.key_combo.clear()
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, list):
                self.key_combo.addItem("(root array – no key needed)")
                self._log("ℹ️  Root is an array – will split items directly.")
            elif isinstance(data, dict):
                # Show each key with its type
                for k, v in data.items():
                    typ = type(v).__name__
                    self.key_combo.addItem(f"{k}  ({typ})", userData=k)
                # Auto-select the largest dict/list key
                container_keys = [k for k, v in data.items() if isinstance(v, (dict, list))]
                if container_keys:
                    best = max(container_keys, key=lambda k: len(data[k]) if isinstance(data[k], (dict, list)) else 0)
                    self.key_combo.setCurrentText(f"{best}  ({type(data[best]).__name__})")
                self._log(f"🔑 Keys found: {list(data.keys())}")
        except Exception as e:
            self._log(f"⚠️  Could not read keys: {e}")

    def _clear_log(self):
        self.log_box.clear(); self.progress_bar.setValue(0)

    def _log(self, msg):
        self.log_box.append(msg)

    def _run(self):
        filepath = self.file_edit.text().strip()
        if not filepath or not os.path.isfile(filepath):
            self._log("⚠️  Please select a valid JSON file first."); return

        out_dir = self.out_edit.text().strip()
        if not out_dir:
            out_dir = os.path.dirname(filepath)
        elif not os.path.isdir(out_dir):
            self._log("⚠️  Output directory does not exist."); return

        # Extract the actual split key from the combo (userData holds the raw key)
        split_key = self.key_combo.currentData()
        if split_key is None:   # root array case
            split_key = "__root__"

        if self.radio_parts.isChecked():
            mode, value = "parts", self.spin_parts.value()
            self._log(f"⚙️  Mode: split into {value} parts  |  key: '{split_key}'")
        elif self.radio_kb.isChecked():
            mode, value = "kb", self.spin_kb.value()
            self._log(f"⚙️  Mode: max {value} KB per file  |  key: '{split_key}'")
        else:
            mode, value = "top_keys", None
            self._log(f"⚙️  Mode: by top-level children  |  key: '{split_key}'")

        self.run_btn.setEnabled(False)
        self.progress_bar.setValue(0)

        self.worker = SplitterWorker(filepath, out_dir, mode, value, split_key)
        self.worker.progress.connect(self.progress_bar.setValue)
        self.worker.log.connect(self._log)
        self.worker.finished.connect(self._on_finished)
        self.worker.start()

    def _on_finished(self, success, message):
        self._log(message)
        self.run_btn.setEnabled(True)
        if success:
            self.progress_bar.setValue(100)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())