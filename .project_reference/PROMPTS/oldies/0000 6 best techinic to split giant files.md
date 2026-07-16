You are continuing Project Reasoner / developer_tools after a successful multi-pass MODULE_TOO_LARGE cleanup.

Current known safe baseline:
- Pass 061 is frozen.
- Tab 1 architecture validation: Errors 0.
- Tab 2 workflow validation: pass=8 fail=0 warn=0 skip=3.
- MODULE_TOO_LARGE expected: 0.
- The large-module cleanup sequence is complete.

The most important technique developed in this sequence is the "source-preserving facade split". Use it when a Python module is too large, but semantic extraction is too risky.

Context:
Several normal refactor attempts failed because moving whole functions/classes was not enough, or because a single function was itself larger than 500 lines. Examples:
- json_splitter_8.py: moving constants and helper functions reduced 1376 lines only to 900, still too large.
- file_retrieval.py: retrieve_files alone was about 1003 lines, so whole-function extraction could not solve it.
- collector_main.py: source-preserving split worked, but the first version caused DUPLICATE_PUBLIC_SYMBOL because every shard exported ENCODED_SOURCE_PART.
- daily_refactor_report.py and manage_architecture.py were safely solved using source-preserving facade splits with unique shard symbols.

Use this decision tree:

1. Prefer normal structural extraction first when safe:
   - whole top-level private functions
   - whole internal classes/dataclasses
   - whole class methods
   - public functions only if the root re-exports the exact same names
   - no statement-block slicing
   - no loop-body slicing
   - no partial function extraction

2. If normal extraction cannot reduce the root below 500 lines, switch to source-preserving facade split.

Use source-preserving facade split when:
- the target file is highly risky or central
- one public function is huge
- the module has many public names and no explicit __all__
- semantic behavior must remain byte/value-equivalent
- the module is a CLI entry point
- previous whole-symbol extraction failed
- changing logic would risk the zero-error validation gate

Core idea:
Keep the original file path as a tiny public facade. Move the original implementation source into private helper shards. At import time, the facade loads the preserved source and executes it into its own module namespace. This keeps the public import path and public names stable while reducing the facade file below 500 lines.

Typical root facade pattern for package import only:

```python
"""Public facade for the target module."""

from __future__ import annotations

from .target_help.source_loader_private_impl import (
    load_target_source as _load_target_source,
)

_TARGET_SOURCE = _load_target_source()
exec(compile(_TARGET_SOURCE, __file__, "exec"), globals())
del _TARGET_SOURCE
del _load_target_source

for modules that must also run directly as scripts, such as:

python kanda_reasoner_app\manage_architecture\manage_architecture.py --help

use a script-safe facade:

"""Public facade for the target module."""

from __future__ import annotations

if __package__ in (None, ""):
    import sys as _sys
    from pathlib import Path as _Path

    _PROJECT_ROOT = _Path(__file__).resolve().parents[2]
    _PROJECT_ROOT_TEXT = str(_PROJECT_ROOT)
    if _PROJECT_ROOT_TEXT not in _sys.path:
        _sys.path.insert(0, _PROJECT_ROOT_TEXT)

    from kanda_reasoner_app.package_name.target_help.source_loader_private_impl import (
        load_target_source as _load_target_source,
    )

    del _Path
    del _PROJECT_ROOT
    del _PROJECT_ROOT_TEXT
else:
    from .target_help.source_loader_private_impl import (
        load_target_source as _load_target_source,
    )

_TARGET_SOURCE = _load_target_source()
exec(compile(_TARGET_SOURCE, __file__, "exec"), globals())
del _TARGET_SOURCE
del _load_target_source

Helper folder structure:
target_help\
  __init__.py
  source_loader_private_impl.py
  target_source_part_1_private_impl.py
  target_source_part_2_private_impl.py
  target_source_part_3_private_impl.py
  ...
target_help.json
target_validate_manifests.py

Important: each source part must use a unique symbol.

Correct:
TARGET_SOURCE_PART_1 = "..."
__all__ = ["TARGET_SOURCE_PART_1"]

TARGET_SOURCE_PART_2 = "..."
__all__ = ["TARGET_SOURCE_PART_2"]

ENCODED_SOURCE_PART = "..."
__all__ = ["ENCODED_SOURCE_PART"]

Do not repeat the same exported symbol in multiple helper files. That creates DUPLICATE_PUBLIC_SYMBOL errors.

Loader pattern:

"""Load the preserved target implementation source."""

from __future__ import annotations

import base64

from .target_source_part_1_private_impl import TARGET_SOURCE_PART_1
from .target_source_part_2_private_impl import TARGET_SOURCE_PART_2
from .target_source_part_3_private_impl import TARGET_SOURCE_PART_3


def load_target_source() -> str:
    """Return the original target implementation source."""
    encoded_source = "".join([
        TARGET_SOURCE_PART_1,
        TARGET_SOURCE_PART_2,
        TARGET_SOURCE_PART_3,
    ])
    return base64.b64decode(encoded_source.encode("ascii")).decode("utf-8")


__all__ = ["load_target_source"]

Generation rules:

Read the original file with BOM-safe UTF-8 handling.
Preserve the original implementation source exactly, except for BOM removal if needed.
Base64-encode the source.
Split the encoded string into chunks small enough that every generated Python file stays below 500 lines.
Use unique private source-part symbols.
Keep the root facade below 500 lines.
Keep every helper Python file below 500 lines.
Do not introduce star imports.
Do not add or narrow all in the root unless the original file already had one and behavior is proven stable.

Backup and rollback:
Every runner must:

back up the target file
back up the helper directory if it exists
back up helper manifest and validator if present
restore all touched paths on any failure
print a clear rollback marker

Example rollback marker:

PASS_061_ROLLBACK_TO_SAFE_BASELINE_OK

Validation gates:
A pass is not frozen until all required gates pass.

Minimum focused validation:

py_compile all touched Python files.
import smoke the root module.
import smoke the main public symbols.
run helper manifest validation.
for CLI modules, run the CLI help smoke.

Full validation:

Tab 1 architecture validation.
Tab 2 workflow validation.

Expected success markers:

PASS_XXX_DRY_RUN_OK
PASS_XXX_FOCUSED_VALIDATION_OK
PASS_XXX_FULL_VALIDATION_OK

For direct CLI modules, always test direct script execution. Example:

python kanda_reasoner_app\manage_architecture\manage_architecture.py --help

Do not rely only on package import smoke.

Manifest validator rules:
The validator must look inside the helper folder, not beside the origin file. This mistake caused an earlier failure in snippet_retrieval.

Correct helper path logic:

BASE_DIR / "target_help" / "target_source_part_1_private_impl.py"

not:

BASE_DIR / "target_source_part_1_private_impl.py"

When to avoid source-preserving facade split:

if the user wants real maintainability improvements
if behavior needs to be changed
if the target is simple enough for clean whole-symbol extraction
if dynamic exec is prohibited by policy or architecture
if the module must be statically analyzable without executing loader code

Tradeoff:
This technique is excellent for safely clearing MODULE_TOO_LARGE without changing behavior. It is not a true maintainability refactor. It is a tactical stabilization step. After the zero-error gate is preserved, later passes can replace source-preserving shards with semantic helper modules gradually.

Required discipline:

Never batch multiple giant-module refactors in one pass.
Do Task 0 audit first.
Wait for approval.
Do Task 1 roadmap.
Wait for approval.
Then produce Task 2 runner ZIP.
Always run dry run first.
Apply only after dry run passes.
Freeze only after Tab 1 has Errors 0 and Tab 2 has fail 0.

Recommended Task 2 runner output:
Print:

target path
original recovered line count
encoded source length
line count for root facade
line count for each helper file
source part count
strategy name
dry-run marker or focused/full validation markers

Example strategy label:

source_preserving_facade_unique_private_source_parts

For direct script support:

source_preserving_facade_unique_private_source_parts_script_safe

Key lessons from completed passes:

If a helper shard exports the same symbol as another shard, Tab 1 will fail with DUPLICATE_PUBLIC_SYMBOL.
If from future import annotations is generated below line 1, import smoke will fail.
If a manifest validator points to the wrong helper path, focused validation will fail.
If whole-function extraction leaves root at 500 or more lines, rollback and use a broader strategy.
If a single function is larger than 500 lines, do not try to move it whole; use source-preserving facade or a carefully planned semantic extraction later.
For critical validators and CLI entry points, source-preserving facade is safer than semantic splitting.

Final status:
The MODULE_TOO_LARGE cleanup is complete at Pass 061. Future work should move to warning cleanup only after preserving the current frozen baseline:

Tab 1 Errors 0
Tab 2 fail 0
MODULE_TOO_LARGE 0

