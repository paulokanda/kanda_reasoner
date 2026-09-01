# KANDA Reasoner Portable current governed build state

The current Portable builder identity is `kanda-reasoner-portable-timestamped-publication-name-v1r32`.

Completed hardening capabilities, in order:

1. `registry-boundary-gate`
2. `packaged-gui-smoke-isolation`
3. `governed-root-exact-rollback`
4. `runtime-path-hash-allowlist`
5. `exact-builder-member-governance`
6. `external-build-control-hash-binding`
7. `self-host-venv-build-interpreter`
8. `production-portable-authorization`
9. `spec-audit-policy-reconciliation`
10. `posix-zip-member-writer`
11. `packaged-gui-runtime-report-preservation`
12. `pyinstaller-submodule-import-preflight`
13. `selected-owner-fire-shield-isolation`
14. `packaged-worker-reentry-dispatch`
15. `clean-start-gui-regression-reset`
16. `tool-project-decoupled-portable-build`
17. `timestamped-publication-name`

v1r20 is a demonstrated-defect repair inside the existing governed-root exact
rollback capability. It does not add a new architecture stage.

The production v1r17 CREATE reached the governed-root backup phase and failed
before PyInstaller with:

`ValueError: ZIP does not support timestamps before 1980`

The rollback owner creates exact ZIP backups for every registry-derived
governed root before external build work. One protected filesystem file can
legitimately carry a modification timestamp older than the ZIP central
directory epoch even though its bytes and path are valid.

Python's standard `zipfile.ZipFile` API supports this exact case through
`strict_timestamps=False`. v1r20 enables that option only for governed-root
rollback backup archives. Python then clamps unrepresentable member timestamps
to 1980-01-01 while preserving file bytes, archive member paths, CRC checks,
baseline hashes, extraction verification, and exact rollback semantics.

The validator creates a disposable file with a pre-1980 timestamp, writes it
through the real governed-root backup owner, verifies the ZIP member year is
1980, and verifies the archived content is byte-identical.

The v1r17 Windows POSIX ZIP-member writer remains unchanged and frozen:
`System.IO.Compression` is loaded before
`System.IO.Compression.FileSystem`, final Portable ZIP members use `/`, and raw
backslash member rejection remains active.

Portable creation is Tool-owned and Project-selection agnostic. Build authority
comes from the builder's own `<kanda_reasoner>` source location, committed spec,
and `<kanda_reasoner>/.venv/Scripts/python.exe` using Python 3.12 x64 and
PyInstaller 6.21.0. The active Project may be external, self-hosted, or none; it
does not authorize or block Tool packaging.

The exact `portable/` builder contract is 31 files and 0 directories.
The runtime allowlist remains exactly 360 path/size/SHA-256-bound sources.
The seven external build-control authorities remain exact
path/role/size/SHA-256 bound.

The expected production artifact remains
`KandaReasoner-Windows-Portable.zip` in the user-selected destination folder.


## v1r20 packaged tab-switch crash hardening

The production clean-extraction smoke now keeps a token-bound runtime report outside the disposable smoke root so failure evidence survives. The shell records the lazy tab source before construction begins, and the Portable builder reports a nonzero packaged-process exit together with the last runtime event instead of collapsing the incident into a generic manual-denial message.

The PyInstaller specification also performs a fail-early import preflight for `routing_signal_scorer.ml_advisory_signal`. The Phase 12 facade now re-exports the two constants already required by that package initializer, eliminating the concrete collection-time ImportError observed in v1r18.


## v1r20 selected-owner Fire Shield isolation

The Project registry remains global authority for destination exclusion: a Portable
output or result path may not enter any registered Project, Project Support, or
Project transient owner root.

Snapshot, backup, immutability checks, and rollback are narrower by design. They
apply only to the Tool source, Tool Support, and Tool transient roots used by the
Portable operation. The currently selected Project never becomes the mutation or
rollback owner. Unrelated registered Projects may be edited, executed, watched,
or left open in an IDE without authorizing, vetoing, or being rolled back by the
Tool build.

Brick Wall invariant: registry knowledge does not grant mutation authority.

## v1r23 packaged-worker re-entry dispatch

The v1r20 selected-owner, rollback timestamp, PyInstaller import-preflight, and
packaged tab-switch evidence contracts remain authoritative and unchanged.

The new worker-dispatch capability repairs the packaged-runtime case where
`sys.executable` is the GUI executable rather than a Python interpreter. The
PyInstaller build now installs an allowlisted runtime hook before the GUI entry
point and includes the governed Ruff executable as a native worker dependency.
Audited Tool-owned `-m` and script workers execute headlessly; unknown Python
re-entry forms fail closed instead of constructing another KANDA Reasoner GUI.

The builder validates this contract immediately after PyInstaller, again after
clean ZIP extraction, and inside the packaged functional smoke. These checks use
a token-bound machine-readable worker report and therefore do not depend on
console output from the `console=False` executable.


## v1r25 clean-start GUI regression reset

The v1r23 packaged-worker re-entry dispatch remains authoritative. This revision
repairs Portable GUI regressions observed during the clean-extraction acceptance
run without patching generated Portable output.

The first packaged smoke launch now has no selected Project. The disposable
external smoke Project is injected only for the second scenario, after the
no-Project registry contract passes.

The shared tab header no longer forces blue/green Active Project foreground
colors. Active Project path fields are shrinkable and bounded to their own slot,
with the complete value available through the existing tooltip.

Lazy tool loading is re-entry guarded before Qt event processing, and one lazy
host may contain exactly one embedded tool. Embedded tool and nested Audit
Project containers ignore child size-hint pressure in both axes. Tab switching
restores the pre-switch top-level window size after lazy layout settlement.

Portable acceptance must prove: first launch Project NONE, one Audit Project
content instance, no header overlap, stable default palette text, stable shell
width/height across tab switches, and preserved v1r23 headless worker dispatch.


## v1r26 Tool/Project-decoupled Portable build

The Portable builder now treats KANDA Reasoner as the Tool being packaged, not as
a selected Project. Tool identity is derived from the builder's own source path.
No `current_project_id`, Project root equality, or `EXPLICIT_SELF_HOSTING` mode is
required to create the Tool Portable.

The Tool-owned Project registry is optional for build authorization. When present,
its historical external Project roots are used only as a fail-closed destination
firewall so the final ZIP cannot be written inside known Project, Project Support,
or Project transient roots. The observed active Project is receipt evidence only.

Governed-root snapshot, backup, immutability, and rollback scope is exactly the
Tool source, Tool Support, and Tool transient roots. The active external Project is
not snapshotted, backed up, restored, or otherwise made part of Portable creation.

The clean packaged first launch remains Project NONE. The second smoke scenario
uses only the isolated disposable Project environment. This keeps the distributable
Tool ready to receive any Project after launch while preserving normal PyCharm or
terminal development independently of KANDA Project-selection state.

## v1r32 current builder identity and S7B Tool/Project parity

The current governed Portable builder remains v1r32. The timestamped publication
capability is the current Portable identity; the v1r26 Tool/Project-decoupled
rules remain inherited architecture rather than the current revision label.

KSI-S7B aligns the production direct-build controls with that existing
architecture. Portable creation does not unload or clear the selected Project.
The selected Project is observed only, contributes no build authority, and
remains unchanged by the Tool build. The direct builder reuses the canonical
`portable/registry_boundary.py` owner for registered Project destination
exclusion and registry-change fail-closed checks.

The production PowerShell entrypoints derive Tool identity from their own
location and use `<kanda_reasoner>/.venv/Scripts/python.exe`. Machine-global
Python discovery and hard-coded drive-root Tool authority are not part of the
current build contract. The standalone Project-unload command remains an
explicit separate operation and is not a Portable build prerequisite.
