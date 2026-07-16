#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
refactor_blueprint.py
=====================
Blueprint / skeleton for a heuristic + LLM-assisted Python module splitter.

TARGET RULES
    ideal  : 400 lines per output file
    maximum: 500 lines per output file
    minimum: 100 lines per output file  (no tiny files; merge instead)

PIPELINE (three phases)
    Phase 1 -- ANALYSIS     (pure AST, stdlib only)
        1a. Parse source into AST
        1b. Extract symbols (functions, classes, constants, globals)
        1c. Build call/dependency graph
        1d. Detect naming clusters (shared prefixes)
        1e. Detect global state and ordered side-effects
        1f. Estimate line-count contribution per symbol

    Phase 2 -- PARTITION    (~70% heuristic, ~20% LLM)
        2a. Greedy bin-packing by dependency subgraph + naming cluster
        2b. Enforce size constraints (merge tiny bins, split oversized bins)
        2c. Flag ambiguous symbols (connected to multiple bins)
        2d. LLM semantic arbitration for ambiguous symbols
              -> qwen3-coder:30b via Ollama decides which bin each belongs to

    Phase 3 -- GENERATION   (~10% LLM for conflict repair)
        3a. Validate proposed partition (circular imports, missing refs)
        3b. LLM conflict repair for ordering / global-state issues
        3c. Write output files (libcst rewriting or ast.unparse fallback)
        3d. Rewrite imports across the whole project
        3e. Post-validation: compile-check every output file

DEPENDENCIES
    stdlib  : ast, os, sys, pathlib, collections, json, itertools,
              urllib.request, urllib.error, textwrap, re
    optional: libcst  (install: pip install libcst)
              networkx (install: pip install networkx)
    runtime : Ollama running locally with qwen3-coder:30b pulled

    The script degrades gracefully when libcst or networkx are absent:
        - without libcst   -> falls back to ast.unparse (Python 3.9+)
        - without networkx -> uses a hand-rolled adjacency-list graph

USAGE (once fully implemented)
    python refactor_blueprint.py  target.py  --out-dir ./split  --dry-run
    python refactor_blueprint.py  target.py  --out-dir ./split
"""

from __future__ import annotations

import ast
import collections
import itertools
import json
import os
import re
import sys
import textwrap
import urllib.error
import urllib.request
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

LINE_IDEAL   = 400
LINE_MAX     = 500
LINE_MIN     = 100

OLLAMA_URL   = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "qwen3-coder:30b"
OLLAMA_TIMEOUT = 120   # seconds; LLM calls can be slow for large contexts

# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

class Symbol:
    """One top-level symbol extracted from the source module."""

    def __init__(
        self,
        name: str,
        kind: str,           # "function" | "class" | "constant" | "global_stmt"
        node: ast.AST,
        start_line: int,
        end_line: int,
        calls: List[str],    # names this symbol references (calls, inherits, etc.)
        prefix: str,         # leading word(s) before first underscore, e.g. "parse"
    ) -> None:
        self.name       = name
        self.kind       = kind
        self.node       = node
        self.start_line = start_line
        self.end_line   = end_line
        self.line_count = end_line - start_line + 1
        self.calls      = calls
        self.prefix     = prefix
        self.bin_id: Optional[int] = None   # assigned during Phase 2

    def __repr__(self) -> str:
        return "Symbol(%s %s L%d-%d)" % (self.kind, self.name,
                                          self.start_line, self.end_line)


class Bin:
    """A proposed output file: a group of symbols."""

    _id_counter = itertools.count(1)

    def __init__(self) -> None:
        self.id: int = next(Bin._id_counter)
        self.symbols: List[Symbol] = []
        self.filename: Optional[str] = None   # decided in Phase 3

    @property
    def line_count(self) -> int:
        return sum(s.line_count for s in self.symbols)

    @property
    def is_too_small(self) -> bool:
        return self.line_count < LINE_MIN

    @property
    def is_too_large(self) -> bool:
        return self.line_count > LINE_MAX

    @property
    def names(self) -> List[str]:
        return [s.name for s in self.symbols]

    def __repr__(self) -> str:
        return "Bin#%d(%d lines, %d symbols)" % (self.id, self.line_count,
                                                   len(self.symbols))


class Graph:
    """Minimal directed graph (adjacency list). Replaces networkx when absent."""

    def __init__(self) -> None:
        self._adj: Dict[str, Set[str]] = collections.defaultdict(set)
        self._nodes: Set[str] = set()

    def add_node(self, n: str) -> None:
        self._nodes.add(n)
        self._adj.setdefault(n, set())

    def add_edge(self, src: str, dst: str) -> None:
        self._nodes.update([src, dst])
        self._adj[src].add(dst)

    def neighbors(self, n: str) -> Set[str]:
        return self._adj.get(n, set())

    def weakly_connected_components(self) -> List[Set[str]]:
        """Return WCCs treating all edges as undirected."""
        visited: Set[str] = set()
        components: List[Set[str]] = []
        undirected: Dict[str, Set[str]] = collections.defaultdict(set)
        for n in self._nodes:
            for nb in self._adj[n]:
                undirected[n].add(nb)
                undirected[nb].add(n)
        for start in self._nodes:
            if start in visited:
                continue
            component: Set[str] = set()
            queue = [start]
            while queue:
                node = queue.pop()
                if node in visited:
                    continue
                visited.add(node)
                component.add(node)
                queue.extend(undirected[node] - visited)
            components.append(component)
        return components


# ---------------------------------------------------------------------------
# PHASE 1 -- ANALYSIS
# ---------------------------------------------------------------------------

def load_source(path: Path) -> Tuple[str, ast.Module]:
    """Read file (strip BOM), parse AST. Returns (source_text, ast_tree)."""
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        raw = raw[3:]
    source = raw.decode("utf-8", errors="replace")
    tree = ast.parse(source, filename=str(path))
    return source, tree


def extract_symbols(source: str, tree: ast.Module) -> List[Symbol]:
    """
    Phase 1b: Walk top-level AST nodes and return a Symbol for each.
    Nested classes/functions are NOT extracted separately; they travel
    with their parent.

    TODO: handle decorated functions (strip decorator lines from count)
    TODO: handle __all__ declarations as a special 'constant' symbol
    """
    source_lines = source.splitlines()
    symbols: List[Symbol] = []

    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            kind = "function"
            name = node.name
        elif isinstance(node, ast.ClassDef):
            kind = "class"
            name = node.name
        elif isinstance(node, ast.Assign):
            # e.g. MY_CONST = 42
            targets = [t.id for t in node.targets if isinstance(t, ast.Name)]
            if not targets:
                continue
            name = targets[0]
            kind = "constant"
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            # imports stay in base module; skip for now
            continue
        else:
            # bare expressions, if/try blocks at module level = global_stmt
            name = "_global_stmt_%d" % node.lineno
            kind = "global_stmt"

        end_line = getattr(node, "end_lineno", node.lineno)
        calls    = _collect_references(node)
        prefix   = _name_prefix(name)

        symbols.append(Symbol(
            name       = name,
            kind       = kind,
            node       = node,
            start_line = node.lineno,
            end_line   = end_line,
            calls      = calls,
            prefix     = prefix,
        ))

    return symbols


def _collect_references(node: ast.AST) -> List[str]:
    """
    Phase 1c helper: collect all Name/Attribute references inside node.
    Used to build the call graph.

    TODO: resolve attribute chains (self.foo -> class attribute)
    TODO: filter out builtins
    """
    refs: List[str] = []
    for child in ast.walk(node):
        if isinstance(child, ast.Name):
            refs.append(child.id)
        elif isinstance(child, ast.Attribute):
            refs.append(child.attr)
    return list(set(refs))


def _name_prefix(name: str) -> str:
    """
    Phase 1d helper: extract the leading cluster word from a symbol name.
    e.g.  parse_user_input -> 'parse'
          UserProfile      -> 'user'  (camelcase split)
          DB_CONNECTION    -> 'db'
    """
    # snake_case: first segment before underscore
    if "_" in name:
        return name.split("_")[0].lower()
    # CamelCase: first lowercase run
    parts = re.sub(r"([A-Z])", r" \1", name).split()
    return parts[0].lower() if parts else name.lower()


def build_dependency_graph(symbols: List[Symbol]) -> Graph:
    """
    Phase 1c: Build a directed call graph between symbols.
    Edge src -> dst means src references dst.

    TODO: weight edges by call frequency (count multiple references)
    """
    known = {s.name for s in symbols}
    g = Graph()
    for s in symbols:
        g.add_node(s.name)
        for ref in s.calls:
            if ref in known and ref != s.name:
                g.add_edge(s.name, ref)
    return g


def detect_global_state(symbols: List[Symbol]) -> List[Symbol]:
    """
    Phase 1e: Return symbols that are likely global state or ordered
    side-effects (module-level assignments to mutable objects, calls
    with side effects like logging.basicConfig, db.connect, etc.).

    These must stay in the base module OR be handled with care.

    TODO: detect module-level calls that are not pure (network, IO, state)
    TODO: detect shared mutable containers (lists, dicts assigned at top level)
    """
    flagged: List[Symbol] = []
    for s in symbols:
        if s.kind == "global_stmt":
            flagged.append(s)
        elif s.kind == "constant" and s.name == s.name.upper():
            # ALL_CAPS constant: safe to move but keep track
            pass
        # TODO: deeper analysis
    return flagged


# ---------------------------------------------------------------------------
# PHASE 2 -- PARTITION
# ---------------------------------------------------------------------------

def heuristic_partition(
    symbols: List[Symbol],
    graph: Graph,
    global_state: List[Symbol],
) -> List[Bin]:
    """
    Phase 2: Produce an initial list of Bins using three heuristics applied
    in order of priority:

        H1. Dependency subgraph  (weakly connected components in call graph)
        H2. Naming prefix cluster (symbols sharing the same prefix word)
        H3. Size enforcement      (merge tiny bins; split oversized bins)

    Returns a list of Bins, each flagging ambiguous symbols for LLM review.

    TODO: implement H1 and H2 properly
    TODO: implement size-enforcement merge/split
    """
    bins: List[Bin] = []
    global_names = {s.name for s in global_state}

    # -- H1: weakly connected components in the dependency graph -----------
    components = graph.weakly_connected_components()
    symbol_map = {s.name: s for s in symbols}

    for component in components:
        b = Bin()
        for name in component:
            if name in symbol_map:
                s = symbol_map[name]
                if s.name not in global_names:
                    b.symbols.append(s)
                    s.bin_id = b.id
        if b.symbols:
            bins.append(b)

    # -- H2: prefix-based merging for orphans and single-symbol bins -------
    # TODO: collect symbols not yet assigned and group by prefix
    # prefix_groups: Dict[str, List[Symbol]] = collections.defaultdict(list)
    # ...

    # -- H3: size enforcement ----------------------------------------------
    bins = _enforce_size_constraints(bins)

    return bins


def _enforce_size_constraints(bins: List[Bin]) -> List[Bin]:
    """
    Phase 2b: Merge bins that are too small (< LINE_MIN) into their
    nearest neighbour, then split bins that are too large (> LINE_MAX)
    by slicing symbol lists at the LINE_IDEAL boundary.

    TODO: 'nearest neighbour' should use dependency graph distance,
          not just list adjacency.
    TODO: split should respect internal dependencies (do not split
          two symbols that call each other into different bins).
    """
    # Merge tiny bins into the smallest existing bin
    stable: List[Bin] = []
    tiny:   List[Bin] = []
    for b in bins:
        (tiny if b.is_too_small else stable).append(b)

    for t in tiny:
        if stable:
            # TODO: pick the best target bin, not just the first
            stable[0].symbols.extend(t.symbols)
            for s in t.symbols:
                s.bin_id = stable[0].id
        else:
            stable.append(t)

    # Split oversized bins
    result: List[Bin] = []
    for b in stable:
        if not b.is_too_large:
            result.append(b)
            continue
        # TODO: smarter split that respects internal call edges
        current = Bin()
        for s in b.symbols:
            if current.line_count + s.line_count > LINE_IDEAL and \
               current.line_count >= LINE_MIN:
                result.append(current)
                current = Bin()
            current.symbols.append(s)
            s.bin_id = current.id
        if current.symbols:
            result.append(current)

    return result


def find_ambiguous_symbols(symbols: List[Symbol], graph: Graph,
                           bins: List[Bin]) -> List[Symbol]:
    """
    Phase 2c: A symbol is 'ambiguous' when its call-graph edges cross
    bin boundaries in both directions (it is called by bin A AND calls
    something in bin B, with A != B).

    These are sent to the LLM for a semantic boundary decision.

    TODO: implement cross-bin edge detection using bin_id of neighbors
    """
    bin_of = {s.name: s.bin_id for s in symbols}
    ambiguous: List[Symbol] = []
    for s in symbols:
        neighbor_bins = {bin_of.get(nb) for nb in graph.neighbors(s.name)
                         if nb in bin_of}
        neighbor_bins.discard(None)
        neighbor_bins.discard(s.bin_id)
        if len(neighbor_bins) > 1:
            ambiguous.append(s)
    return ambiguous


# ---------------------------------------------------------------------------
# PHASE 2d / 3b -- LLM ARBITRATION (Ollama qwen3-coder:30b)
# ---------------------------------------------------------------------------

def _ollama_generate(prompt: str, system: str) -> str:
    """
    Low-level Ollama call. Returns the model's response text or raises
    RuntimeError on failure.

    Uses streaming=False (single response JSON).
    """
    payload = json.dumps({
        "model":  OLLAMA_MODEL,
        "prompt": prompt,
        "system": system,
        "stream": False,
        "options": {
            "temperature": 0.1,   # low temp for deterministic structural decisions
            "num_predict": 512,
        },
    }).encode("ascii", errors="replace")

    req = urllib.request.Request(
        OLLAMA_URL,
        data    = payload,
        headers = {"Content-Type": "application/json"},
        method  = "POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=OLLAMA_TIMEOUT) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data.get("response", "").strip()
    except urllib.error.URLError as exc:
        raise RuntimeError("Ollama unreachable: %s" % exc) from exc


SEMANTIC_SYSTEM = (
    "You are a strict Python module boundary advisor. "
    "You receive a list of proposed output modules (bins), each with a name list, "
    "and one ambiguous symbol that has dependencies crossing bin boundaries. "
    "Reply ONLY with the exact bin number (integer) the symbol should belong to. "
    "No explanation. No prose. One integer on a single line."
)

CONFLICT_SYSTEM = (
    "You are a strict Python refactoring expert. "
    "You receive a Python code fragment that has a global-state ordering problem "
    "or a circular import after an automated module split. "
    "Produce a corrected version of the fragment. "
    "Output ONLY the corrected Python code, no markdown, no commentary."
)


def llm_arbitrate_symbol(symbol: Symbol, bins: List[Bin]) -> int:
    """
    Phase 2d: Ask qwen3-coder:30b which bin a cross-boundary symbol belongs to.
    Returns the winning bin_id.

    Falls back to the symbol's current bin_id if Ollama is unavailable.
    """
    bin_summaries = "\n".join(
        "Bin %d: %s" % (b.id, ", ".join(b.names[:10]))
        for b in bins
    )
    prompt = textwrap.dedent("""
        Ambiguous symbol: {name} ({kind})
        It is called by symbols in multiple bins.

        Available bins:
        {bins}

        Which bin number should '{name}' belong to?
        Reply with the bin number only.
    """).format(name=symbol.name, kind=symbol.kind, bins=bin_summaries).strip()

    try:
        response = _ollama_generate(prompt, SEMANTIC_SYSTEM)
        return int(response.split()[0])
    except (RuntimeError, ValueError):
        return symbol.bin_id   # fallback: keep current assignment


def llm_repair_conflict(code_fragment: str, problem_description: str) -> str:
    """
    Phase 3b: Ask qwen3-coder:30b to repair an ordering or circular-import
    conflict in a code fragment. Returns the repaired source code.

    Falls back to the original fragment unchanged if Ollama is unavailable.
    """
    prompt = textwrap.dedent("""
        Problem: {problem}

        Code fragment:
        {code}

        Produce the corrected Python code only.
    """).format(problem=problem_description, code=code_fragment).strip()

    try:
        return _ollama_generate(prompt, CONFLICT_SYSTEM)
    except RuntimeError:
        return code_fragment   # fallback: leave unchanged


# ---------------------------------------------------------------------------
# PHASE 3 -- GENERATION
# ---------------------------------------------------------------------------

def assign_filenames(bins: List[Bin], base_module_name: str) -> None:
    """
    Phase 3: Decide the output filename for each bin.

    Strategy:
        - The largest bin (most public API surface) becomes the base module.
        - All others are named after the dominant naming prefix of their symbols.
        - If two bins share the same prefix, append a numeric suffix.

    TODO: use LLM to suggest a semantically appropriate filename for
          bins whose symbols have no clear dominant prefix.
    """
    if not bins:
        return

    # Sort: largest bin becomes the base
    bins_by_size = sorted(bins, key=lambda b: b.line_count, reverse=True)
    bins_by_size[0].filename = base_module_name + ".py"

    used: Dict[str, int] = {}
    for b in bins_by_size[1:]:
        prefix = _dominant_prefix(b)
        if prefix in used:
            used[prefix] += 1
            fname = "%s_%s_%d.py" % (base_module_name, prefix, used[prefix])
        else:
            used[prefix] = 1
            fname = "%s_%s.py" % (base_module_name, prefix)
        b.filename = fname


def _dominant_prefix(b: Bin) -> str:
    """Return the most common naming prefix among symbols in a bin."""
    counter: Dict[str, int] = collections.Counter(
        s.prefix for s in b.symbols if s.prefix
    )
    return counter.most_common(1)[0][0] if counter else "helpers"


def validate_partition(bins: List[Bin], graph: Graph) -> List[str]:
    """
    Phase 3a: Static validation before writing any files.
    Returns a list of problem descriptions (empty = clean).

    Checks:
        - No circular imports between bins (if bin A imports bin B,
          bin B must not import bin A).
        - All references within the project are resolved.
        - No orphan symbols (symbols with no bin assignment).

    TODO: implement circular-import detection (build inter-bin dep graph
          and check for cycles with DFS).
    TODO: detect dangling references (calls to symbols that were lost).
    """
    problems: List[str] = []

    # Check for orphans
    for b in bins:
        for s in b.symbols:
            if s.bin_id is None:
                problems.append("Orphan symbol with no bin: %s" % s.name)

    # TODO: build inter-bin dependency graph and detect cycles

    return problems


def write_bin(b: Bin, source_lines: List[str], out_dir: Path,
              all_bins: List[Bin], dry_run: bool = True) -> None:
    """
    Phase 3c: Write one bin's symbols to its output file.

    Strategy (simple fallback, no libcst):
        1. Extract the original source lines for each symbol.
        2. Prepend a module docstring and the necessary import statements.
        3. Write out. No reformatting of the symbol bodies themselves.

    When libcst is available (TODO):
        - Use libcst.parse_module + RemoveUnusedImports + AddImportsVisitor
          for clean import management instead of the naive string approach.

    Args:
        b:           the Bin to write
        source_lines: original source split by line (0-indexed)
        out_dir:     directory to write into
        all_bins:    full list of bins (to compute cross-file imports)
        dry_run:     if True, print the plan but do not write files
    """
    out_path = out_dir / b.filename
    symbol_blocks: List[str] = []

    for s in sorted(b.symbols, key=lambda x: x.start_line):
        # Extract original lines (1-based line numbers, 0-based list index)
        block = "".join(source_lines[s.start_line - 1: s.end_line])
        symbol_blocks.append(block)

    # TODO: compute required imports (cross-bin and third-party)
    # cross_imports = _compute_cross_imports(b, all_bins)
    # import_header = _render_import_header(cross_imports)

    body = "\n\n".join(symbol_blocks)
    output = '"""\nAuto-generated module: %s\n"""\n\n' % (b.filename,) + body

    if dry_run:
        print("[DRY RUN] Would write %s (%d lines, %d symbols)" % (
            out_path, b.line_count, len(b.symbols)))
    else:
        out_path.write_text(output, encoding="ascii", errors="replace")
        print("Wrote %s" % out_path)


def rewrite_imports_in_project(project_root: Path, bins: List[Bin],
                               original_module: str, dry_run: bool) -> None:
    """
    Phase 3d: Walk all .py files under project_root and update any
    'from original_module import X' or 'import original_module; original_module.X'
    statements to point to the new split module file.

    TODO: implement using libcst AddImportsVisitor + RemoveImportsVisitor.
          A naive string-replace approach is shown below as a placeholder.
    """
    symbol_to_file: Dict[str, str] = {}
    for b in bins:
        module_name = b.filename.replace(".py", "")
        for s in b.symbols:
            symbol_to_file[s.name] = module_name

    for py_file in project_root.rglob("*.py"):
        text = py_file.read_text(encoding="utf-8", errors="replace")
        if original_module not in text:
            continue
        # TODO: proper AST/libcst rewrite instead of string substitution
        print("[TODO] Would rewrite imports in %s" % py_file)


def post_validate(out_dir: Path) -> List[str]:
    """
    Phase 3e: Compile-check every generated .py file.
    Returns a list of files that failed to compile.
    """
    failures: List[str] = []
    for py_file in out_dir.glob("*.py"):
        source = py_file.read_bytes()
        try:
            ast.parse(source.decode("utf-8", errors="replace"))
        except SyntaxError as exc:
            failures.append("%s: %s" % (py_file.name, exc))
    return failures


# ---------------------------------------------------------------------------
# ORCHESTRATOR
# ---------------------------------------------------------------------------

def refactor(source_path: Path, out_dir: Path, dry_run: bool = True) -> None:
    """
    Main entry point. Runs all three phases in sequence.

    Args:
        source_path: path to the large .py file to split
        out_dir:     directory where the new files will be written
        dry_run:     if True, analyse and plan but do not write or modify files
    """
    print("=== Phase 1: Analysis ===")
    source, tree = load_source(source_path)
    source_lines = source.splitlines(keepends=True)
    base_name    = source_path.stem

    symbols = extract_symbols(source, tree)
    print("  Symbols found: %d" % len(symbols))

    graph = build_dependency_graph(symbols)
    global_state = detect_global_state(symbols)
    print("  Global-state symbols: %d" % len(global_state))

    print("=== Phase 2: Partition ===")
    bins = heuristic_partition(symbols, graph, global_state)
    print("  Initial bins: %d" % len(bins))
    for b in bins:
        print("    %r" % b)

    ambiguous = find_ambiguous_symbols(symbols, graph, bins)
    print("  Ambiguous symbols: %d (sending to LLM)" % len(ambiguous))
    for s in ambiguous:
        new_bin_id = llm_arbitrate_symbol(s, bins)
        if new_bin_id != s.bin_id:
            print("    LLM moved '%s' to bin %d" % (s.name, new_bin_id))
            # TODO: physically move s to the new bin in the bins list

    print("=== Phase 3: Generation ===")
    assign_filenames(bins, base_name)

    problems = validate_partition(bins, graph)
    for p in problems:
        print("  [CONFLICT] %s" % p)
        # TODO: send conflicting fragment to llm_repair_conflict()

    if not dry_run:
        out_dir.mkdir(parents=True, exist_ok=True)

    for b in bins:
        write_bin(b, source_lines, out_dir, bins, dry_run=dry_run)

    if not dry_run:
        rewrite_imports_in_project(source_path.parent, bins, base_name, dry_run)
        failures = post_validate(out_dir)
        if failures:
            print("\n[ERROR] Compile failures after generation:")
            for f in failures:
                print("  " + f)
        else:
            print("\n[OK] All generated files compile cleanly.")

    # Summary report
    print("\n=== Summary ===")
    print("  Total symbols:   %d" % len(symbols))
    print("  Output files:    %d" % len(bins))
    for b in bins:
        flag = ""
        if b.is_too_small:
            flag = "  <-- BELOW MINIMUM (%d lines)" % LINE_MIN
        if b.is_too_large:
            flag = "  <-- ABOVE MAXIMUM (%d lines)" % LINE_MAX
        print("  %-40s %4d lines%s" % (b.filename or "?", b.line_count, flag))


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _usage() -> None:
    print(__doc__)
    print("Usage: python refactor_blueprint.py <source.py> [--out-dir DIR] [--apply]")
    print()
    print("  --out-dir DIR   where to write split files (default: ./split_<stem>)")
    print("  --apply         actually write files (default: dry-run)")


def main(argv: List[str]) -> int:
    if len(argv) < 2:
        _usage()
        return 1

    source_path = Path(argv[1])
    if not source_path.exists():
        print("ERROR: file not found: %s" % source_path)
        return 1

    out_dir  = Path("split_" + source_path.stem)
    dry_run  = True

    i = 2
    while i < len(argv):
        arg = argv[i]
        if arg == "--out-dir" and i + 1 < len(argv):
            out_dir = Path(argv[i + 1])
            i += 2
        elif arg == "--apply":
            dry_run = False
            i += 1
        else:
            print("Unknown argument: %s" % arg)
            _usage()
            return 1

    refactor(source_path, out_dir, dry_run=dry_run)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
