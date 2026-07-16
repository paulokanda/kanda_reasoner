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


# ---------------------------------------------------------------------------
# Split helpers  — operate on DIRECT children, not deep leaves
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# Worker thread
# ---------------------------------------------------------------------------

class SplitterWorker(QThread):
    progress = Signal(int)
    log      = Signal(str)
    finished = Signal(bool, str)

    def __init__(self, filepath, mode, value, split_key):
        super().__init__()
        self.filepath  = filepath
        self.mode      = mode       # "parts" | "kb" | "top_keys"
        self.value     = value
        self.split_key = split_key

    def run(self):
        try:
            self.log.emit(f"📂 Reading: {self.filepath}")
            with open(self.filepath, "r", encoding="utf-8") as f:
                data = json.load(f)

            # ---- isolate the subtree to split --------------------------------
            if isinstance(data, list):
                preserved = {}
                tree      = data
                is_list   = True
                split_key = "__root_list__"
            else:
                split_key = self.split_key
                preserved = {k: v for k, v in data.items() if k != split_key}
                tree      = data.get(split_key, {})
                is_list   = isinstance(tree, list)

            # entries = direct children of the chosen subtree
            entries     = get_entries(tree)
            total       = len(entries)
            self.log.emit(f"✅ {total} direct entries under '{split_key}'.")

            if total == 0:
                self.finished.emit(False, "❌ No entries found under the selected key.")
                return

            # ---- build chunks ------------------------------------------------
            if self.mode == "parts":
                n          = max(1, min(int(self.value), total))
                chunk_size = math.ceil(total / n)
                chunks     = [entries[i:i+chunk_size]
                               for i in range(0, total, chunk_size)]

            elif self.mode == "kb":
                target_bytes  = float(self.value) * 1024
                preserved_sz  = len(json.dumps(preserved, ensure_ascii=False).encode())
                effective_lim = max(target_bytes - preserved_sz - 64, 512)
                chunks, cur, cur_sz = [], [], 0
                for entry in entries:
                    # measure just this one entry as if it were a mini-dict/list
                    sample     = rebuild([entry], is_list)
                    entry_sz   = len(json.dumps(sample, ensure_ascii=False).encode())
                    if cur_sz + entry_sz > effective_lim and cur:
                        chunks.append(cur)
                        cur, cur_sz = [entry], entry_sz
                    else:
                        cur.append(entry)
                        cur_sz += entry_sz
                if cur:
                    chunks.append(cur)

            else:  # "top_keys" — only valid when subtree is a dict
                if is_list:
                    self.finished.emit(
                        False, "❌ 'By top-level children' needs a dict, not a list.")
                    return
                # one chunk per direct key
                chunks = [[e] for e in entries]

            # ---- write files -------------------------------------------------
            total_chunks = len(chunks)
            padding      = max(len(str(total_chunks)), 2)
            output_dir   = os.path.dirname(self.filepath)
            base_name    = os.path.splitext(os.path.basename(self.filepath))[0]

            self.log.emit(f"🔀 Splitting into {total_chunks} file(s)…")

            for idx, chunk in enumerate(chunks, start=1):
                num_str      = str(idx).zfill(padding)
                out_filename = f"{num_str}_{base_name}.json"
                out_path     = os.path.join(output_dir, out_filename)

                subtree  = rebuild(chunk, is_list)
                out_data = dict(preserved)
                out_data[split_key] = subtree

                with open(out_path, "w", encoding="utf-8") as f:
                    json.dump(out_data, f, ensure_ascii=False, indent=2)

                size_kb = os.path.getsize(out_path) / 1024
                self.log.emit(
                    f"  ✔ {out_filename}  ({len(chunk)} entries, {size_kb:.1f} KB)")
                self.progress.emit(int(idx / total_chunks * 100))

            self.finished.emit(
                True, f"🎉 Done! {total_chunks} file(s) → {output_dir}")

        except json.JSONDecodeError as e:
            self.finished.emit(False, f"❌ Invalid JSON: {e}")
        except Exception as e:
            import traceback
            self.finished.emit(False, f"❌ Error: {e}\n{traceback.format_exc()}")


# ---------------------------------------------------------------------------
# Main window
# ---------------------------------------------------------------------------

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("JSON File Splitter")
        self.setMinimumSize(680, 720)
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

        # ---- Key selector ----
        key_group = QGroupBox("Key to Split")
        kl = QVBoxLayout(key_group)
        hint = QLabel(
            "Choose the top-level key whose contents will be divided.\n"
            "All other top-level keys (e.g. 'meta') are copied into every output file."
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

        # Add to group FIRST, then set checked, then connect signals
        bg = QButtonGroup(self)
        for r in (self.radio_parts, self.radio_kb, self.radio_top):
            r.setFont(small_font); bg.addButton(r)
        self.radio_parts.setChecked(True)   # set AFTER group assignment
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
        self._load_keys(path)

    def _load_keys(self, path):
        self.key_combo.clear()
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, list):
                self.key_combo.addItem("(root array — no key needed)")
                self._log("ℹ️  Root is an array — will split items directly.")
            elif isinstance(data, dict):
                all_keys  = list(data.keys())
                dict_keys = [k for k, v in data.items() if isinstance(v, (dict, list))]
                self.key_combo.addItems(all_keys)
                # Auto-select the dict/list key with the MOST direct entries
                if dict_keys:
                    best = max(dict_keys, key=lambda k: len(data[k]) if isinstance(data[k], (dict, list)) else 0)
                    self.key_combo.setCurrentText(best)
                self._log(f"🔑 Keys found: {all_keys}")
                self._log(f"   → Auto-selected: '{self.key_combo.currentText()}' "
                          f"({len(data[self.key_combo.currentText()])} entries — other keys preserved in every output file)")
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

        split_key = self.key_combo.currentText()
        if "(root array" in split_key:
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

        self.worker = SplitterWorker(filepath, mode, value, split_key)
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
