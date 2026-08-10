#!/usr/bin/env python3
# project-path: kanda_prompt_workspace/prompt_tools/sync_startup_routing_kernel_pack.py
r"""
sync_startup_routing_kernel_pack.py

Generate a one-ZIP startup prompt request kernel pack from canonical KANDA prompt files.

Phase 7A v2 folder model:
- Script lives in:   kanda_prompt_workspace/prompt_tools/
- Source map lives:  kanda_prompt_workspace/prompt_tools/STARTUP_ROUTING_KERNEL_SOURCES.json
- Delivery lives in: <project_drive>:/<project_name>_show_project_to_AI/first_prompt_files/
  (the previous legacy delivery folder is deprecated for normal generated startup delivery.)

Safety model:
- Canonical prompt files are read-only inputs.
- Generated startup files are separated Markdown files inside a ZIP.
- The ZIPs and tell_AI_read_before_all.md file are convenience delivery artifacts for ChatGPT/LLM startup sessions.
- The ZIP also carries a generated active-project freeze context so AI sees frozen-feature obligations at startup.
- No canonical source file is modified by this script.

Typical use from the kanda_prompt_workspace root:
    python .\prompt_tools\sync_startup_routing_kernel_pack.py
    python .\prompt_tools\sync_startup_routing_kernel_pack.py --check
    python .\prompt_tools\sync_startup_routing_kernel_pack.py --sync --yes
    python .\prompt_tools\sync_startup_routing_kernel_pack.py --ensure-sync --yes

If no mode is supplied, the script defaults to --check.
This makes IDE/run-button launches safe and read-only instead of raising an argparse error.

Recommended routine use:
    python .\prompt_tools\sync_startup_routing_kernel_pack.py --ensure-sync --yes

The --ensure-sync mode checks first, regenerates only when needed, and checks again.
The --sync mode regenerates and then runs a post-sync check.
"""


from __future__ import annotations

import sys

from startup_kernel.boot_text import (
    make_boot_command_text,
)
from startup_kernel.cli import command_check, command_ensure_sync, confirm_sync, main, parse_args
from startup_kernel.constants import *
from startup_kernel.core_helpers import (
    clean_delivery_folder,
    collect_status,
    date_certificate,
    default_first_prompt_output_dir,
    detect_workspace_root,
    generated_header,
    load_source_map,
    now_utc,
    read_text_utf8,
    resolve_source,
    sha256_bytes,
    sha256_file,
)
from startup_kernel.maintenance_text import make_modify_startup_delivery_protocol
from startup_kernel.paste_readme_text import make_paste_after_uploading_file, make_readme
from startup_kernel.prompt_library_zip import (
    iter_prompt_library_payload_files,
    make_prompt_library_zip,
    prompt_library_source_fingerprint,
    validate_prompt_library_zip_contract,
)
from startup_kernel.read_order import (
    add_read_order_block,
    make_startup_artifact_read_order_notice,
    strip_startup_artifact_read_order_block,
)
from startup_kernel.start_here_text import make_start_here_file
from startup_kernel.startup_source_map import SourceEntry
from startup_kernel.zip_contract import (
    read_manifest_from_zip,
    validate_generated_zip_contract,
)
from startup_kernel.zip_delivery import (
    find_delivery_zip,
    make_zip,
)

__all__ = [
    "SourceEntry",
    "add_read_order_block",
    "clean_delivery_folder",
    "collect_status",
    "command_check",
    "command_ensure_sync",
    "confirm_sync",
    "date_certificate",
    "default_first_prompt_output_dir",
    "detect_workspace_root",
    "find_delivery_zip",
    "generated_header",
    "iter_prompt_library_payload_files",
    "load_source_map",
    "make_boot_command_text",
    "make_modify_startup_delivery_protocol",
    "make_paste_after_uploading_file",
    "make_prompt_library_zip",
    "make_readme",
    "make_start_here_file",
    "make_startup_artifact_read_order_notice",
    "make_zip",
    "main",
    "now_utc",
    "parse_args",
    "prompt_library_source_fingerprint",
    "read_manifest_from_zip",
    "read_text_utf8",
    "resolve_source",
    "sha256_bytes",
    "sha256_file",
    "strip_startup_artifact_read_order_block",
    "validate_generated_zip_contract",
    "validate_prompt_library_zip_contract",
]


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
