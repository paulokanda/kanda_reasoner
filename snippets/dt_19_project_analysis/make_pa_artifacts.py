import io
import ast
import time
import codecs
from pathlib import Path
try:
    from radon.complexity import cc_visit
except Exception:
    cc_visit = None

ROOT = Path(__file__).resolve().parents[2]
OUT  = ROOT/"dev_tools"/"project_analysis"/"results_report"
OUT.mkdir(parents=True, exist_ok=True)

def read_text_safe(p: Path) -> str:
    try:
        b = p.read_bytes()
        if b.startswith(codecs.BOM_UTF8):
            b = b[len(codecs.BOM_UTF8):]
        return b.decode("utf-8", errors="ignore")
    except Exception:
        try:
            return p.read_text(encoding="cp1252", errors="ignore")
        except Exception:
            return ""

def iter_py(root: Path):
    for p in root.rglob("*.py"):
        yield p

# 1) method_details_<ts>.txt
ts = time.strftime("%Y%m%d_%H%M")
md_path = OUT / f"method_details_{ts}.txt"
buf = io.StringIO()
scanned = parsed = 0
for py in iter_py(ROOT):
    scanned += 1
    code = read_text_safe(py)
    if not code.strip():
        continue
    try:
        tree = ast.parse(code)
        parsed += 1
    except SyntaxError:
        continue
    classes = [n for n in tree.body if isinstance(n, ast.ClassDef)]
    funcs   = [n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
    if not classes and not funcs:
        continue
    buf.write(f"\n=== {py.as_posix()} ===\n")
    if funcs:
        buf.write("  [Functions]\n")
        for f in funcs:
            kind = "async def" if isinstance(f, ast.AsyncFunctionDef) else "def"
            argc = len(getattr(f, "args", object()).args) if hasattr(f, "args") else 0
            buf.write(f"    - {kind} {f.name}({argc} args)  @L{f.lineno}\n")
    for cls in classes:
        buf.write(f"  [Class] {cls.name}  @L{cls.lineno}\n")
        for n in cls.body:
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
                kind = "async def" if isinstance(n, ast.AsyncFunctionDef) else "def"
                argc = len(getattr(n, "args", object()).args) if hasattr(n, "args") else 0
                decos = []
                for d in getattr(n, "decorator_list", []) or []:
                    name = getattr(d, "id", None) or getattr(d, "attr", None)
                    if not name and hasattr(d, "func"):
                        name = getattr(d.func, "id", None) or getattr(d.func, "attr", None) or "decorator"
                    decos.append(name or "decorator")
                deco = f"  [{', '.join(decos)}]" if decos else ""
                buf.write(f"    - {kind} {n.name}({argc} args){deco}  @L{n.lineno}\n")

md_path.write_text(f"# Method/Class Details (generated {ts})\n# Scanned {scanned} files; parsed {parsed}\n" + buf.getvalue(), encoding="utf-8")
print(f"OK: {md_path}")

# 2) metrics_top100.txt (best effort with radon if present)
met_path = OUT / "metrics_top100.txt"
if cc_visit is None:
    met_path.write_text("radon not available; metrics skipped.\n", encoding="utf-8")
    print(f"OK: {met_path} (radon missing)")
else:
    rows = []
    for py in iter_py(ROOT):
        code = read_text_safe(py)
        if not code.strip():
            continue
        try:
            blocks = cc_visit(code)
        except Exception:
            continue
        for b in blocks:
            comp = getattr(b, "complexity", None)
            if comp is None: 
                continue
            name = getattr(b, "name", "")
            typ  = getattr(b, "type", "") or b.__class__.__name__
            line = getattr(b, "lineno", 0)
            rows.append((comp, typ, name, py.as_posix(), line))
    rows.sort(key=lambda t: t[0], reverse=True)
    top = rows[:100]
    with met_path.open("w", encoding="utf-8") as f:
        f.write("# Top 100 by Cyclomatic Complexity\n")
        f.write("# complexity | kind | name | file | line\n")
        for comp, typ, name, file, line in top:
            f.write(f"{comp:>4} | {typ:<7} | {name} | {file} | {line}\n")
    print(f"OK: {met_path} (entries={len(top)})")

