# KANDA Reasoner Portable — Continuation Instruction

Read `KANDA_REASONER_PORTABLE_CREATION_CANONICAL_HANDOFF_2026-07-30.md` before proposing or changing any Portable logic.

The validated baseline is Portable Creator v1r11:

* Feature ID: `kanda-reasoner-portable-builder-install-v1r11`
* Validated release: `E:\KandaReasoner-Windows-Portable.zip`
* SHA-256: `1664bea434c2c7d98fe494e2a0c6061b73ffc52647e9845268f31c8b854b2a46`
* Final status: `STATUS: PORTABLE READY AND VALIDATED`

Do not redesign the workflow from zero. Preserve the validated five-phase release state machine:

1. Validate the delivery package.
2. Install the creator transactionally.
3. Validate the installed creator with compact identity JSON.
4. Build, hydrate physical runtime dependencies, cleanly extract, launch twice, test important features, close naturally, and publish atomically.
5. Independently validate the final published ZIP.

Treat `KandaReasonerWindows.spec` as the packaging authority. Use the governed Python 3.12 interpreter and exact PyInstaller 6.21.0. Keep all build work under `E:\kanda_reasoner_delete_after_daily_work`.

Portable creation must remain independent from Show Project, Freeze, and Error Memory.

Do not rely only on PyInstaller completion, ZIP integrity, or main-window launch. Validate the physical-runtime manifest and test Validate Project, Manage Workflows, Insert Missing Docstrings, Project Structure 3D, Show Project, Audit Project, Freeze, Config Web AI, and other changed or important tabs from a clean extraction.

Do not claim success until the workflow prints:

`PHASE 05 FINAL PORTABLE VALIDATION: PASS`

and:

`STATUS: PORTABLE READY AND VALIDATED`

When a failure occurs, inspect `portable_result.json`, `portable_creator_transcript.txt`, and `FINAL_VALIDATION.txt`. Repair only the exact owning layer, preserve previously passed contracts, and resume from the last reliable marker.
