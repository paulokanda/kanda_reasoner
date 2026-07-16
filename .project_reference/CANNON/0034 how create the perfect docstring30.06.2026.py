#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
Docstring Corrector
====================
Single-file, dependency-free tool (stdlib only: ast, os, tkinter).

Workflow implemented:
1. Scan a project path for Python files missing docstrings
   (modules, classes, functions, methods).
2. Left column: list of missing-docstring locations.
3. Click an item: it is highlighted, right column shows the real code
   snippet with an EDITABLE suggested docstring inserted in place.
4. "Other suggestion" button: cycles to the next heuristic suggestion
   for the same item, replacing only the suggested text in the snippet.
5. "Save to file" button: writes the (possibly user-edited) docstring
   into the real source file at the correct location, clears the right
   panel, removes the item from the left list, and auto-selects /
   highlights the next remaining item. "<-" and "->" buttons let the
   user move between remaining items manually.

No BOM is ever written. All file I/O is plain ASCII / UTF-8 without BOM.
No external packages required.
"""

import ast
import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

PY_EXT = ".py"


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

class MissingItem(object):
    """One missing-docstring location found during a scan."""

    def __init__(self, file_path, qualname, kind, def_lineno, insert_lineno,
                 indent, signature, args, has_return, raises):
        self.file_path = file_path
        self.qualname = qualname
        self.kind = kind                # "module" | "class" | "function" | "method"
        self.def_lineno = def_lineno    # line of "def"/"class" (or 1 for module)
        self.insert_lineno = insert_lineno  # line BEFORE which to insert text
        self.indent = indent            # indentation string to use
        self.signature = signature      # human readable signature
        self.args = args                # list of arg names
        self.has_return = has_return
        self.raises = raises            # list of exception names
        self.suggestion_index = 0

    def label(self):
        rel = self.file_path
        return "%s:%d  %s" % (rel, self.def_lineno, self.qualname)


# ---------------------------------------------------------------------------
# Scanning
# ---------------------------------------------------------------------------

def iter_python_files(root):
    """Yield every .py file under root, skipping common noise dirs."""
    skip_dirs = {".git", "__pycache__", ".venv", "venv", "node_modules",
                 ".tox", "build", "dist"}
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in skip_dirs]
        for fn in filenames:
            if fn.endswith(PY_EXT):
                yield os.path.join(dirpath, fn)


def _read_source(path):
    with open(path, "rb") as fh:
        raw = fh.read()
    # Strip a UTF-8 BOM if present on read; we never write one back.
    if raw.startswith(b"\xef\xbb\xbf"):
        raw = raw[3:]
    return raw.decode("utf-8", errors="replace")


def _first_body_insert_point(node):
    """Return (insert_lineno, indent) for inserting a docstring as the
    first statement of node.body. insert_lineno is the line number the
    new docstring lines should be inserted BEFORE (1-based)."""
    first_stmt = node.body[0]
    indent = " " * (first_stmt.col_offset)
    return first_stmt.lineno, indent


def _collect_raises(node):
    names = []
    for child in ast.walk(node):
        if isinstance(child, ast.Raise) and child.exc is not None:
            exc = child.exc
            if isinstance(exc, ast.Call):
                exc = exc.func
            if isinstance(exc, ast.Name):
                if exc.id not in names:
                    names.append(exc.id)
            elif isinstance(exc, ast.Attribute):
                if exc.attr not in names:
                    names.append(exc.attr)
    return names


def _has_return_value(node):
    for child in ast.walk(node):
        if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)) and child is not node:
            continue  # do not descend into nested functions
        if isinstance(child, ast.Return) and child.value is not None:
            return True
    return False


def _arg_names(node):
    args = node.args
    names = [a.arg for a in args.args if a.arg not in ("self", "cls")]
    if args.vararg:
        names.append("*" + args.vararg.arg)
    for a in args.kwonlyargs:
        names.append(a.arg)
    if args.kwarg:
        names.append("**" + args.kwarg.arg)
    return names


def _signature_text(node, qualname):
    args = ", ".join(_arg_names(node))
    prefix = "async def" if isinstance(node, ast.AsyncFunctionDef) else "def"
    return "%s %s(%s)" % (prefix, qualname.rsplit(".", 1)[-1], args)


def scan_file(path, project_root):
    """Return a list of MissingItem for one file. Errors are swallowed
    (unparseable files are simply skipped)."""
    rel = os.path.relpath(path, project_root)
    try:
        source = _read_source(path)
        tree = ast.parse(source, filename=path)
    except (SyntaxError, UnicodeDecodeError, ValueError):
        return []

    items = []

    # Module-level docstring
    if not (tree.body and isinstance(tree.body[0], ast.Expr)
            and isinstance(getattr(tree.body[0], "value", None), ast.Constant)
            and isinstance(tree.body[0].value.value, str)):
        if tree.body:
            insert_lineno = tree.body[0].lineno
            indent = ""
        else:
            insert_lineno = 1
            indent = ""
        items.append(MissingItem(
            file_path=rel, qualname="<module>", kind="module",
            def_lineno=1, insert_lineno=insert_lineno, indent=indent,
            signature="module %s" % os.path.basename(path),
            args=[], has_return=False, raises=[]))

    def has_docstring(node):
        return (node.body and isinstance(node.body[0], ast.Expr)
                and isinstance(getattr(node.body[0], "value", None), ast.Constant)
                and isinstance(node.body[0].value.value, str))

    class Visitor(ast.NodeVisitor):
        def __init__(self):
            self.stack = []

        def _qualname(self, name):
            if self.stack:
                return ".".join(self.stack + [name])
            return name

        def visit_ClassDef(self, node):
            qual = self._qualname(node.name)
            if not has_docstring(node) and node.body:
                insert_lineno, indent = _first_body_insert_point(node)
                items.append(MissingItem(
                    file_path=rel, qualname=qual, kind="class",
                    def_lineno=node.lineno, insert_lineno=insert_lineno,
                    indent=indent, signature="class %s" % node.name,
                    args=[], has_return=False, raises=[]))
            self.stack.append(node.name)
            self.generic_visit(node)
            self.stack.pop()

        def _visit_func(self, node):
            qual = self._qualname(node.name)
            kind = "method" if self.stack else "function"
            if not has_docstring(node) and node.body:
                insert_lineno, indent = _first_body_insert_point(node)
                items.append(MissingItem(
                    file_path=rel, qualname=qual, kind=kind,
                    def_lineno=node.lineno, insert_lineno=insert_lineno,
                    indent=indent, signature=_signature_text(node, qual),
                    args=_arg_names(node),
                    has_return=_has_return_value(node),
                    raises=_collect_raises(node)))
            self.stack.append(node.name)
            self.generic_visit(node)
            self.stack.pop()

        def visit_FunctionDef(self, node):
            self._visit_func(node)

        def visit_AsyncFunctionDef(self, node):
            self._visit_func(node)

    Visitor().visit(tree)
    items.sort(key=lambda it: it.def_lineno)
    return items


def scan_project(root):
    """Scan every .py file under root. Returns list of MissingItem."""
    results = []
    for path in iter_python_files(root):
        results.extend(scan_file(path, root))
    return results


# ---------------------------------------------------------------------------
# Heuristic docstring suggestions (no AI / no network required)
# ---------------------------------------------------------------------------

def _humanize(name):
    words = name.replace("_", " ").strip()
    if not words:
        return "Do something."
    words = words[0].upper() + words[1:]
    if not words.endswith("."):
        words += "."
    return words


def build_suggestions(item):
    """Return a list of candidate docstring bodies (without quotes) for
    the given item. "Other suggestion" cycles through this list."""
    suggestions = []

    if item.kind == "module":
        base = os.path.splitext(os.path.basename(item.file_path))[0]
        suggestions.append(_humanize(base + " module"))
        suggestions.append("Module %s.\n\nDescribe the purpose of this module here." % base)
        suggestions.append("TODO: document this module.")
        return suggestions

    if item.kind == "class":
        name = item.qualname.rsplit(".", 1)[-1]
        suggestions.append(_humanize(name))
        suggestions.append("%s\n\nDescribe responsibilities and usage of this class." % _humanize(name))
        suggestions.append("TODO: document class %s." % name)
        return suggestions

    # function / method
    name = item.qualname.rsplit(".", 1)[-1]
    summary = _humanize(name)

    # Short one-liner
    suggestions.append(summary)

    # Google-style detailed
    lines = [summary, ""]
    if item.args:
        lines.append("Args:")
        for a in item.args:
            clean = a.lstrip("*")
            lines.append("    %s: Description of %s." % (clean, clean))
        lines.append("")
    if item.has_return:
        lines.append("Returns:")
        lines.append("    Description of the return value.")
        lines.append("")
    if item.raises:
        lines.append("Raises:")
        for exc in item.raises:
            lines.append("    %s: Description of when this is raised." % exc)
        lines.append("")
    while lines and lines[-1] == "":
        lines.pop()
    suggestions.append("\n".join(lines))

    # TODO placeholder
    suggestions.append("TODO: document %s." % item.signature)

    return suggestions


def docstring_block(text, indent):
    """Wrap suggestion text into a properly indented triple-quoted
    docstring, returned as a single string with trailing newline,
    ASCII only (non-ascii characters are replaced)."""
    text = text.encode("ascii", errors="replace").decode("ascii")
    body_lines = text.split("\n")
    if len(body_lines) == 1:
        block = '%s"""%s"""\n' % (indent, body_lines[0])
        return block
    out = [indent + '"""' + body_lines[0]]
    for ln in body_lines[1:]:
        out.append(indent + ln if ln else "")
    out.append(indent + '"""')
    return "\n".join(out) + "\n"


# ---------------------------------------------------------------------------
# Snippet rendering (for the right-hand editable preview)
# ---------------------------------------------------------------------------

CONTEXT_BEFORE = 2
CONTEXT_AFTER = 6


def read_lines(path):
    text = _read_source(path)
    return text.splitlines(keepends=True)


def render_snippet(abs_path, item, suggestion_text):
    """Return (snippet_text, doc_start_offset, doc_end_offset) where the
    offsets are character offsets into snippet_text marking the editable
    docstring region (quotes included)."""
    lines = read_lines(abs_path)
    insert_idx = item.insert_lineno - 1  # 0-based index of line to insert before

    start = max(0, insert_idx - CONTEXT_BEFORE)
    end = min(len(lines), insert_idx + CONTEXT_AFTER)

    block = docstring_block(suggestion_text, item.indent)

    before_lines = lines[start:insert_idx]
    after_lines = lines[insert_idx:end]

    pre_text = "".join(before_lines)
    post_text = "".join(after_lines)

    doc_start = len(pre_text)
    doc_end = doc_start + len(block)

    snippet = pre_text + block + post_text
    return snippet, doc_start, doc_end


def apply_to_file(abs_path, item, new_docstring_text):
    """Insert new_docstring_text (raw, already a full docstring block
    string including triple quotes and trailing newline) into the real
    file at item.insert_lineno. Returns number of inserted lines so the
    caller can shift subsequent items' line numbers. Writes the file
    back with no BOM, preserving original line endings as found."""
    lines = read_lines(abs_path)
    insert_idx = item.insert_lineno - 1
    block_lines = new_docstring_text.splitlines(keepends=True)
    if block_lines and not block_lines[-1].endswith("\n"):
        block_lines[-1] += "\n"

    new_lines = lines[:insert_idx] + block_lines + lines[insert_idx:]
    new_text = "".join(new_lines)

    with open(abs_path, "wb") as fh:
        fh.write(new_text.encode("ascii", errors="replace"))

    return len(block_lines)


# ---------------------------------------------------------------------------
# GUI
# ---------------------------------------------------------------------------

class DocstringCorrectorApp(object):
    def __init__(self, root):
        self.root = root
        self.root.title("Docstring Corrector")
        self.root.geometry("1100x650")

        self.project_root = None
        self.items = []          # list[MissingItem], in display order
        self.current_index = None
        self.doc_start = None
        self.doc_end = None

        self._build_widgets()

    # -- layout ------------------------------------------------------
    def _build_widgets(self):
        top = ttk.Frame(self.root)
        top.pack(side=tk.TOP, fill=tk.X, padx=6, pady=6)

        ttk.Button(top, text="Scan project...", command=self.on_scan).pack(side=tk.LEFT)
        self.path_label = ttk.Label(top, text="(no project scanned)")
        self.path_label.pack(side=tk.LEFT, padx=10)
        self.count_label = ttk.Label(top, text="")
        self.count_label.pack(side=tk.RIGHT)

        main = ttk.Panedwindow(self.root, orient=tk.HORIZONTAL)
        main.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)

        left_frame = ttk.Frame(main)
        right_frame = ttk.Frame(main)
        main.add(left_frame, weight=1)
        main.add(right_frame, weight=2)

        ttk.Label(left_frame, text="Missing docstrings").pack(anchor=tk.W)
        list_container = ttk.Frame(left_frame)
        list_container.pack(fill=tk.BOTH, expand=True)
        self.listbox = tk.Listbox(list_container, exportselection=False)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar = ttk.Scrollbar(list_container, orient=tk.VERTICAL, command=self.listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.config(yscrollcommand=scrollbar.set)
        self.listbox.bind("<<ListboxSelect>>", self.on_list_select)

        nav = ttk.Frame(left_frame)
        nav.pack(fill=tk.X, pady=4)
        ttk.Button(nav, text="<-", command=self.on_prev).pack(side=tk.LEFT)
        ttk.Button(nav, text="->", command=self.on_next).pack(side=tk.LEFT)

        ttk.Label(right_frame, text="Code snippet with editable docstring").pack(anchor=tk.W)
        self.text = tk.Text(right_frame, wrap=tk.NONE, undo=True, font=("Courier New", 10))
        self.text.pack(fill=tk.BOTH, expand=True)
        self.text.tag_configure("doc_region", background="#fff2b2")

        btns = ttk.Frame(right_frame)
        btns.pack(fill=tk.X, pady=4)
        ttk.Button(btns, text="Other suggestion", command=self.on_other_suggestion).pack(side=tk.LEFT)
        ttk.Button(btns, text="Save to file", command=self.on_save).pack(side=tk.LEFT, padx=6)

        self.status = ttk.Label(self.root, text="Ready.", anchor=tk.W)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

    # -- scanning ------------------------------------------------------
    def on_scan(self):
        path = filedialog.askdirectory(title="Select project root")
        if not path:
            return
        self.project_root = path
        self.items = scan_project(path)
        self.path_label.config(text=path)
        self._refresh_listbox()
        self.clear_editor()
        self.set_status("Scanned %d file(s), found %d missing docstring(s)." % (
            sum(1 for _ in iter_python_files(path)), len(self.items)))

    def _refresh_listbox(self):
        self.listbox.delete(0, tk.END)
        for it in self.items:
            self.listbox.insert(tk.END, it.label())
        self.count_label.config(text="%d remaining" % len(self.items))

    # -- selection -------------------------------------------------------
    def on_list_select(self, event=None):
        sel = self.listbox.curselection()
        if not sel:
            return
        self.select_index(sel[0])

    def select_index(self, idx):
        if idx is None or idx < 0 or idx >= len(self.items):
            self.clear_editor()
            return
        self.current_index = idx
        self.listbox.selection_clear(0, tk.END)
        self.listbox.selection_set(idx)
        self.listbox.see(idx)
        self.load_item(self.items[idx])

    def on_prev(self):
        if self.current_index is None:
            return
        self.select_index(max(0, self.current_index - 1))

    def on_next(self):
        if self.current_index is None:
            return
        self.select_index(min(len(self.items) - 1, self.current_index + 1))

    # -- editor ----------------------------------------------------------
    def clear_editor(self):
        self.text.delete("1.0", tk.END)
        self.current_index = None
        self.doc_start = None
        self.doc_end = None

    def load_item(self, item):
        abs_path = os.path.join(self.project_root, item.file_path)
        suggestions = build_suggestions(item)
        item.suggestion_index = item.suggestion_index % len(suggestions)
        suggestion_text = suggestions[item.suggestion_index]

        try:
            snippet, doc_start, doc_end = render_snippet(abs_path, item, suggestion_text)
        except (OSError, IOError) as exc:
            messagebox.showerror("Error", "Could not read file:\n%s" % exc)
            return

        self.text.delete("1.0", tk.END)
        self.text.insert("1.0", snippet)

        start_index = self._char_offset_to_index(doc_start)
        end_index = self._char_offset_to_index(doc_end)
        self.text.tag_remove("doc_region", "1.0", tk.END)
        self.text.tag_add("doc_region", start_index, end_index)
        self.doc_start = start_index
        self.doc_end = end_index

        self.set_status("Editing: %s (suggestion %d/%d)" % (
            item.label(), item.suggestion_index + 1, len(suggestions)))

    def _char_offset_to_index(self, offset):
        return self.text.index("1.0 + %dc" % offset)

    # -- suggestions -------------------------------------------------
    def on_other_suggestion(self):
        if self.current_index is None:
            return
        item = self.items[self.current_index]
        suggestions = build_suggestions(item)
        item.suggestion_index = (item.suggestion_index + 1) % len(suggestions)
        self.load_item(item)

    # -- save ----------------------------------------------------------
    def on_save(self):
        if self.current_index is None:
            return
        item = self.items[self.current_index]
        abs_path = os.path.join(self.project_root, item.file_path)

        new_doc_text = self.text.get(self.doc_start, self.doc_end)
        new_doc_text = new_doc_text.encode("ascii", errors="replace").decode("ascii")
        if not new_doc_text.endswith("\n"):
            new_doc_text += "\n"

        try:
            inserted_lines = apply_to_file(abs_path, item, new_doc_text)
        except (OSError, IOError) as exc:
            messagebox.showerror("Error", "Could not save file:\n%s" % exc)
            return

        self._shift_line_numbers(item, inserted_lines)

        del self.items[self.current_index]
        self._refresh_listbox()
        self.set_status("Saved docstring for %s." % item.label())

        next_idx = self.current_index
        if next_idx >= len(self.items):
            next_idx = len(self.items) - 1
        self.clear_editor()
        if next_idx >= 0:
            self.select_index(next_idx)

    def _shift_line_numbers(self, saved_item, inserted_lines):
        """After inserting lines into saved_item.file_path at
        saved_item.insert_lineno, bump line numbers of every other item
        in the same file that sits at or after the insertion point."""
        for it in self.items:
            if it is saved_item:
                continue
            if it.file_path != saved_item.file_path:
                continue
            if it.def_lineno >= saved_item.insert_lineno:
                it.def_lineno += inserted_lines
            if it.insert_lineno >= saved_item.insert_lineno:
                it.insert_lineno += inserted_lines

    def set_status(self, msg):
        self.status.config(text=msg)


def main():
    root = tk.Tk()
    app = DocstringCorrectorApp(root)
    if len(sys.argv) > 1 and os.path.isdir(sys.argv[1]):
        app.project_root = sys.argv[1]
        app.items = scan_project(sys.argv[1])
        app.path_label.config(text=sys.argv[1])
        app._refresh_listbox()
    root.mainloop()


if __name__ == "__main__":
    main()
