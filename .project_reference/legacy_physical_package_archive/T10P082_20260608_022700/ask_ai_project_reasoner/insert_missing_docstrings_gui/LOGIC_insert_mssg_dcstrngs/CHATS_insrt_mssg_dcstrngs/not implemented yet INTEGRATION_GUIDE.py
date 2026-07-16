"""
HOW TO WIRE THE AI GENERATOR INTO insert_missing_docstrings.py
================================================================

This file documents exactly what to change in the existing worker script.
No existing logic is removed — the AI generator is additive.

STEP 1 — Add imports at the top of insert_missing_docstrings.py
---------------------------------------------------------------
Add these three imports after the existing stdlib imports:

    from ai_config import AIConfig
    from context_builder import (
        build_class_context,
        build_function_context,
        build_module_context,
    )
    from ai_docstring_generator import AIDocstringGenerator


STEP 2 — Thread the generator through collect_changes()
-------------------------------------------------------
Change the signature of collect_changes() and collect_missing_docstring_insertions()
to accept an optional generator:

    def collect_changes(
        root: Path,
        *,
        include_module: bool,
        include_classes: bool,
        include_functions: bool,
        include_init: bool,
        include_relaxed_paths: bool,
        include_tests: bool,
        generator: AIDocstringGenerator | None = None,   # <-- ADD
    ) -> tuple[dict[Path, tuple[str, bool]], list[str]]:

    def collect_missing_docstring_insertions(
        root: Path,
        path: Path,
        include_module: bool,
        include_classes: bool,
        include_functions: bool,
        include_init: bool,
        manifest: dict | None,
        generator: AIDocstringGenerator | None = None,   # <-- ADD
    ) -> tuple[list[tuple[int, list[str]]], list[str], str, bool]:


STEP 3 — Replace build_*_docstring() calls with context-aware calls
--------------------------------------------------------------------
Inside collect_missing_docstring_insertions(), replace the three builder calls:

BEFORE (module docstring):
    module_doc = build_module_docstring(path, module_id, tree, root, manifest)

AFTER:
    if generator is not None:
        from context_builder import build_module_context
        ctx = build_module_context(path, module_id, tree, lines)
        module_doc = '"""' + generator.generate(ctx) + '"""'
    else:
        module_doc = build_module_docstring(path, module_id, tree, root, manifest)

------

BEFORE (class docstring):
    payload = wrap_docstring_lines(build_class_docstring(node), indent) + [indent]

AFTER:
    if generator is not None:
        from context_builder import build_class_context
        ctx = build_class_context(node, tree, module_id, lines)
        raw_body = generator.generate(ctx)
        full_doc = '"""' + raw_body + '"""'
    else:
        full_doc = build_class_docstring(node)
    payload = wrap_docstring_lines(full_doc, indent) + [indent]

------

BEFORE (function docstring):
    payload = wrap_docstring_lines(build_function_docstring(node), indent) + [indent]

AFTER:
    if generator is not None:
        from context_builder import build_function_context
        ctx = build_function_context(node, tree, module_id, lines)
        raw_body = generator.generate(ctx)
        full_doc = '"""' + raw_body + '"""'
    else:
        full_doc = build_function_docstring(node)
    payload = wrap_docstring_lines(full_doc, indent) + [indent]


STEP 4 — Expose --ai flag in run() and main()
---------------------------------------------
In run(), add:

    def run(
        root: Path,
        mode: str,
        *,
        include_module: bool = True,
        include_classes: bool = True,
        include_functions: bool = True,
        include_init: bool = False,
        include_relaxed_paths: bool = False,
        include_tests: bool = False,
        ai_config_path: str | None = None,   # <-- ADD
    ) -> int:
        generator: AIDocstringGenerator | None = None
        if ai_config_path is not None:
            cfg = AIConfig.from_json(ai_config_path) if ai_config_path != "default" \
                  else AIConfig.default()
            generator = AIDocstringGenerator(config=cfg, project_root=root,
                                             on_fallback=lambda n, r: print(f"FALLBACK {n}: {r}"))

        changes, skipped_messages = collect_changes(
            root, ..., generator=generator
        )

        if generator is not None:
            generator.flush_cache()

In build_parser(), add:

    parser.add_argument(
        "--ai",
        metavar="CONFIG",
        nargs="?",
        const="default",
        help="Enable AI docstring generation. Optionally pass path to ai_config.json.",
    )

In main(), pass through:

    return run(root, mode, ..., ai_config_path=args.ai)


STEP 5 — Pass generator through in collect_changes()
-----------------------------------------------------
Inside the collect_changes() loop body, forward the generator:

    insertions, skipped, current, had_bom = collect_missing_docstring_insertions(
        root, path,
        include_module=include_module,
        include_classes=include_classes,
        include_functions=include_functions,
        include_init=include_init,
        manifest=manifest,
        generator=generator,   # <-- ADD
    )


FILE LAYOUT AFTER INTEGRATION
==============================

Place all four files in the same directory:

    your_tool/
    ├── insert_missing_docstrings.py        (existing, patched per above)
    ├── insert_missing_docstrings_gui.py    (existing, add AI settings panel later)
    ├── mode_options_hlp.py                 (existing, unchanged)
    ├── ai_config.py                        (NEW)
    ├── context_builder.py                  (NEW)
    └── ai_docstring_generator.py           (NEW)


QUICK TEST (no GUI)
===================

1. Make sure Ollama is running:
       ollama serve
       ollama pull codellama:13b

2. Run scan first to see what would be generated:
       python insert_missing_docstrings.py --root /path/to/project --scan --ai

3. Preview the actual docstrings without writing:
       python insert_missing_docstrings.py --root /path/to/project --diff --ai

4. Write when satisfied:
       python insert_missing_docstrings.py --root /path/to/project --write --ai

5. Use a custom config (faster model, different timeout):
       python insert_missing_docstrings.py --root /path/to/project --diff --ai ai_config.json

EXAMPLE ai_config.json
=======================
{
  "base_url": "http://localhost:11434/v1",
  "model": "qwen2.5-coder:7b",
  "timeout_seconds": 20.0,
  "max_tokens": 512,
  "temperature": 0.05,
  "fallback_to_heuristic": true,
  "workers": 4,
  "cache_enabled": true,
  "cache_path": ".docstring_cache.json",
  "docstring_style": "numpy"
}

Recommended local models (quality vs speed tradeoff):
  • Best quality  : deepseek-coder:33b, codellama:34b
  • Balanced      : qwen2.5-coder:14b, codellama:13b   (DEFAULT)
  • Fastest       : qwen2.5-coder:7b, starcoder2:7b
"""
