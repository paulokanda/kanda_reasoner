# Audit Report: Router Prompt System & ZIP Delivery Failure Pattern

**Subject:** Recurring failure to (a) stage delivered ZIPs to `<drive>:\<project>_delete_after_daily_work` and (b) deliver a valid `KANDA_FREEZE_HINT.json` / freeze-form JSON.
**Scope:** Architecture, prompts, implementation, validation, and process. No ML integration work included, per the stated boundary.

---

## 1. Diagnosis — Why the Recurring Error Happens

The two failures are downstream symptoms of the **same root cause**: ZIP delivery is currently treated as a *generic text-generation event* governed by instructions sitting far away (in startup files loaded once, at session start), instead of being treated as a **distinct governed action with its own mandatory, machine-checkable gate that fires at the moment of output**.

Concretely, five compounding weaknesses:

1. **Distance between rule and action.** The staging-folder rule and the freeze-hint rule live in startup documents (`07_daily_patch_delivery_guardrails.md`, `09_active_project_freeze_context.md`) read once at the top of a long session. By the time a ZIP is actually built and presented — possibly thousands of tokens later — there is no automatic re-trigger that pulls those rules back into active attention. The assistant is relying on memory of instructions, not on enforcement.

2. **No artifact-level contract check.** Nothing inspects the ZIP itself before presentation. The assistant *narrates* that `KANDA_FREEZE_HINT.json` is included, but no code verifies it exists at ZIP root, is valid JSON, and contains the mandatory schema fields. A claim ("I included it") is not the same as a verified fact.

3. **Freeze hint and freeze-form JSON are generated independently (or one is skipped).** Because there is no single canonical source feeding both the in-ZIP sidecar and the chat-visible freeze-form JSON, they can diverge or one can be omitted entirely without anything noticing.

4. **No fail-closed behavior.** The current design allows a ZIP link to be delivered even when delivery obligations are unmet. There's no rule that says "if the contract can't be verified, withhold the ZIP." Soft obligations get silently dropped under task load; only hard gates survive.

5. **Installer logic is hand-written per patch.** Because the PowerShell installer is composed fresh each time rather than instantiated from one canonical, tested template, drift is easy: a `Downloads`-first search pattern, a missing staging-folder creation step, or wrong terminal hygiene can creep back in without anyone noticing, because there is no shared template to regress-test.

In short: **the obligations are documented but not enforced.** Documentation degrades under context load; enforcement does not.

---

## 2. Architecture-Level Fix

Treat **"deliver a patch ZIP"** as its own governed route in the router (your Q15), not a generic Routed-Work output. That route should have a structure like:

```
ZIP_DELIVERY_ROUTE
 ├── 1. Build payload (existing logic)
 ├── 2. Generate KANDA_FREEZE_HINT.json from canonical source
 ├── 3. Generate freeze-form JSON from the SAME canonical source
 ├── 4. Assemble ZIP (payload/ + root-level KANDA_FREEZE_HINT.json)
 ├── 5. Run zip_contract_validator.py against the assembled ZIP  <-- HARD GATE
 ├── 6. Run installer_template_check (no hand-written installer) <-- HARD GATE
 ├── 7. If 5 or 6 fail → STOP, report failure, do NOT present ZIP link
 └── 8. If pass → emit ZIP link + install block + freeze-form JSON + checklist
```

Key architectural decisions, answering your numbered questions directly:

- **Q1/Q8 (fail-closed on missing hint):** Yes. Make ZIP presentation *structurally* depend on a passing contract check. Not a reminder — a precondition.
- **Q2 (validator before presentation):** Yes. `zip_contract_validator.py` should be a real script invoked in the pipeline, not a mental checklist.
- **Q3 (single canonical installer template):** Yes. One template, parameterized by `$PROJECT_NAME`/`$PROJECT_ROOT`/payload folder name. Hand-authoring per patch is exactly how the Downloads/Desktop fallback regression re-enters.
- **Q4 (tests reject Downloads/Desktop fallback):** Yes, as a static test on the template itself (template is checked into the repo and linted), so a bad edit to the template fails CI rather than failing silently in a delivered patch.
- **Q5 (single source for hint + freeze-form JSON):** Yes. Both must be rendered from one `freeze_payload` object so they cannot diverge. This directly fixes the "placeholder feature title / empty validated_files" failure — there is no second hand-typed copy to drift.
- **Q9 (shrink startup instructions to an always-active delivery contract):** Yes, but as a *supplement* to enforcement, not a substitute. A short, unmissable contract block reduces reliance on the long startup load surviving in working memory; the validator script is what actually prevents the failure if the block is missed anyway.
- **Q10 (separate `patch_release_manifest.json`):** Yes — recommended. It should bundle both the install obligations (staging path, drive-root expectation) and freeze obligations (hint schema, validation evidence) in one place that `zip_contract_validator.py` reads, so install and freeze rules can't drift independently of each other either.
- **Q11 (root-level metadata excluded from payload copy, tested):** Yes — this is a correctness property of the installer template and should have a dedicated unit test (extract → assert `KANDA_FREEZE_HINT.json` is NOT in the installed project tree).
- **Q12 (freeze GUI explains rejection):** Yes — strongly recommended for diagnosability. A freeze GUI that says "rejected: missing `validation_evidence_summary`" is far better than a silent placeholder draft, and removes ambiguity about whether the *assistant* or the *freeze tool* caused the failure.
- **Q13 (regression tests with malformed hints):** Yes — this is the only way to know the freeze form's rejection behavior keeps working as the schema evolves.

---

## 3. Prompt-Level Fix

Two changes to the prompt/startup layer:

**A. Add a short, always-active "Delivery Contract" block**, distinct from the long startup pack, that is re-surfaced specifically at ZIP-emission time rather than only at session start. Something like:

```
ZIP_DELIVERY_CONTRACT (must pass before any ZIP link is shown):
[ ] Compact Windows-safe basename
[ ] Installer generated from canonical template (not hand-written)
[ ] Installer stages from drive root -> <drive>:\<project>_delete_after_daily_work
[ ] Installer deletes root-drive ZIP copy after staging
[ ] Root-level KANDA_FREEZE_HINT.json present and schema-complete, OR explicit
    "non-freezeable, reason: ___" statement
[ ] Freeze-form JSON block included in the chat response, generated from the
    same source as the hint
[ ] Validation evidence includes "VALIDATION OK: <feature_id>" (+ "STATUS: IN_SYNC"
    if startup sync touched)
[ ] zip_contract_validator.py run, result = PASS
ANY UNCHECKED ITEM => DO NOT EMIT ZIP LINK. Report what is missing instead.
```

This block should be **injected by the router itself** whenever it detects ZIP-link generation, PowerShell install blocks, or freeze evidence in the upcoming response — i.e., the router becomes the trigger, not session memory (your Q7). This is the single highest-leverage prompt fix: it converts a "remember to do this" instruction into a "this gate runs every time" instruction.

**B. Make the override sections (prompt-library creation, freeze GUI changes, startup delivery maintenance) explicitly reference the ZIP_DELIVERY_CONTRACT** whenever their output path ends in a patch ZIP, so the two governance layers compose instead of operating in parallel and silently dropping one of them.

---

## 4. Python Implementation Fix

Minimal concrete components:

**`zip_contract_validator.py`** — run against the assembled ZIP before it is ever presented:

```python
import json
import zipfile
import sys

MANDATORY_FREEZE_FIELDS = [
    "schema_version", "kind", "patch_name", "feature_id", "feature_title",
    "primary_box", "box_type", "validated_files", "generated_files",
    "protected_paths", "do_not_regress_rules", "validation_evidence_summary",
    "known_warnings", "planned_next_step", "notes",
]

class ZipContractError(Exception):
    pass

def validate_zip(zip_path: str, expect_freeze_hint: bool = True) -> dict:
    """Validates structural + freeze-hint contract of a patch ZIP.
    Raises ZipContractError on any violation. Returns a report dict on success.
    """
    report = {"zip_path": zip_path, "checks": []}

    with zipfile.ZipFile(zip_path) as zf:
        names = zf.namelist()

        # 1. Windows-safe basename check happens on the filename, not in-zip.

        # 2. Root-level hint presence
        root_hint_candidates = [n for n in names if n == "KANDA_FREEZE_HINT.json"]
        if expect_freeze_hint:
            if not root_hint_candidates:
                raise ZipContractError(
                    "Missing root-level KANDA_FREEZE_HINT.json "
                    "(or patch was not declared non-freezeable)."
                )
            raw = zf.read("KANDA_FREEZE_HINT.json")
            try:
                hint = json.loads(raw)
            except json.JSONDecodeError as e:
                raise ZipContractError(f"KANDA_FREEZE_HINT.json is not valid JSON: {e}")

            missing = [f for f in MANDATORY_FREEZE_FIELDS if f not in hint]
            if missing:
                raise ZipContractError(
                    f"KANDA_FREEZE_HINT.json missing mandatory fields: {missing}"
                )

            if not hint.get("validated_files"):
                raise ZipContractError("validated_files is empty.")
            if not hint.get("validation_evidence_summary"):
                raise ZipContractError("validation_evidence_summary is empty.")
            if hint.get("feature_title", "").strip().lower() in (
                "", "placeholder", "tbd", "untitled feature"
            ):
                raise ZipContractError("feature_title is placeholder/empty.")

            report["freeze_hint"] = hint

        # 3. Hint must NOT also exist inside payload root (prevents accidental
        #    install of delivery metadata as a source file).
        payload_dirs = {n.split("/")[0] for n in names if "/" in n}
        for d in payload_dirs:
            if f"{d}/KANDA_FREEZE_HINT.json" in names:
                raise ZipContractError(
                    f"KANDA_FREEZE_HINT.json duplicated inside payload folder '{d}/' "
                    "— must exist only at ZIP root."
                )

    report["checks"].append("PASS")
    return report


if __name__ == "__main__":
    path = sys.argv[1]
    try:
        result = validate_zip(path)
        print("ZIP CONTRACT: PASS")
        print(json.dumps(result, indent=2, default=str))
    except ZipContractError as e:
        print(f"ZIP CONTRACT: FAIL — {e}")
        sys.exit(1)
```

**Single source for hint + freeze-form JSON** — build both from one function so they can't diverge:

```python
def build_freeze_payload(feature_id, feature_title, primary_box, box_type,
                          validated_files, generated_files, protected_paths,
                          do_not_regress_rules, validation_evidence_summary,
                          known_warnings, planned_next_step, notes,
                          patch_name, schema_version="1.0"):
    return {
        "schema_version": schema_version,
        "kind": "freeze_intake",
        "patch_name": patch_name,
        "feature_id": feature_id,
        "feature_title": feature_title,
        "primary_box": primary_box,
        "box_type": box_type,
        "validated_files": validated_files,
        "generated_files": generated_files,
        "protected_paths": protected_paths,
        "do_not_regress_rules": do_not_regress_rules,
        "validation_evidence_summary": validation_evidence_summary,
        "known_warnings": known_warnings,
        "planned_next_step": planned_next_step,
        "notes": notes,
    }

# Both of these are then just renders of the same dict:
#  - written into KANDA_FREEZE_HINT.json at ZIP root
#  - dumped as the chat-visible freeze-form JSON block
```

**Canonical installer template** — one parameterized PowerShell template (not reproduced here in full to keep this report focused) with placeholders for `$PROJECT_NAME` and a fixed, tested staging algorithm:

```powershell
$ProjectRoot = "<resolved at generation time>"
$DriveRoot = (Get-Item $ProjectRoot).PSDrive.Root
$StagingDir = Join-Path $DriveRoot "<PROJECT_NAME>_delete_after_daily_work"
if (-not (Test-Path $StagingDir)) { New-Item -ItemType Directory -Path $StagingDir | Out-Null }

$ZipAtRoot = Join-Path $DriveRoot "<ZIP_BASENAME>.zip"
if (-not (Test-Path $ZipAtRoot)) {
    Write-Host "ZIP not found at $ZipAtRoot. Place it there first."
    exit 1
}
Move-Item $ZipAtRoot (Join-Path $StagingDir "<ZIP_BASENAME>.zip") -Force
$StagedZip = Join-Path $StagingDir "<ZIP_BASENAME>.zip"
Expand-Archive -Path $StagedZip -DestinationPath $StagingDir -Force
# install only payload/, never KANDA_FREEZE_HINT.json
Copy-Item (Join-Path $StagingDir "<PAYLOAD_FOLDER>\*") $ProjectRoot -Recurse -Force
Remove-Item $StagedZip -Force
Start-Sleep -Seconds 5
Clear-Host
```

This template should be a checked-in file, not something composed fresh in chat each time — that is what makes it testable (Q3, Q4).

---

## 5. Validation / Test Strategy

| Test | Purpose |
|---|---|
| `test_validator_rejects_missing_hint.py` | ZIP with no root-level hint → `ZipContractError` |
| `test_validator_rejects_malformed_json.py` | Hint present but invalid JSON → rejected |
| `test_validator_rejects_missing_fields.py` | Hint missing any of the 14 mandatory fields → rejected, names the field(s) |
| `test_validator_rejects_placeholder_title.py` | `feature_title` in a placeholder denylist → rejected |
| `test_validator_rejects_empty_validated_files.py` | Empty list → rejected |
| `test_validator_rejects_duplicate_hint_in_payload.py` | Hint duplicated inside payload folder → rejected |
| `test_installer_template_no_downloads_desktop.py` | Static check: template source contains no `Downloads`/`Desktop` path strings |
| `test_installer_excludes_root_metadata.py` | Simulated install run → `KANDA_FREEZE_HINT.json` is absent from the installed project tree |
| `test_installer_creates_staging_dir_if_missing.py` | Staging dir auto-created |
| `test_installer_deletes_root_zip_after_staging.py` | Root-drive ZIP copy removed post-stage |
| `test_freeze_payload_single_source_consistency.py` | Hint JSON and freeze-form JSON produced in the same delivery are byte-for-byte equal (after parsing) |
| `test_freeze_gui_explains_rejection.py` | GUI/CLI surfaces the *specific* validator failure message, not a generic placeholder draft |

CI should run these on every change to the validator, the template, or the freeze schema — this is what prevents the next schema/template edit from silently reopening the same hole.

---

## 6. Final-Answer Checklist (for every future ZIP delivery)

Before presenting a ZIP link, install block, or freeze evidence, the response must confirm, explicitly and in this order:

```
[ ] ZIP basename is Windows-safe and compact
[ ] Installer generated from canonical template (version: ___)
[ ] Installer stages ZIP at <drive>:\<project>_delete_after_daily_work
[ ] Root-drive ZIP copy deleted after staging (in script logic)
[ ] Root-level KANDA_FREEZE_HINT.json present, OR explicit non-freezeable statement given
[ ] zip_contract_validator.py executed against the ZIP — result: PASS / FAIL
[ ] If FAIL: ZIP link withheld, failure reason stated, no patch presented
[ ] Freeze-form JSON included in this response (marker-wrapped, valid JSON only)
[ ] Freeze-form JSON generated from same source object as KANDA_FREEZE_HINT.json
[ ] Validation evidence includes "VALIDATION OK: <feature_id>"
[ ] "STATUS: IN_SYNC" included if startup-delivery sync was touched
```

This checklist should be the *last* thing rendered in any ZIP-delivery response, with each line marked, not implied.

---

## 7. Risks of Overcomplicating the Router

- **Fast Path drag:** If the new ZIP_DELIVERY_CONTRACT gate is wired into the router as a blanket rule, it risks firing on *any* mention of a ZIP or PowerShell snippet, even trivial unrelated ones, slowing down ordinary Fast Path work. Mitigate by scoping the trigger narrowly to "this response is about to emit an installable patch ZIP link," not "this response mentions ZIP."
- **Schema rigidity vs. evolving feature types:** A hard-coded mandatory-fields list will need updates as freeze intake schema evolves; if the validator and schema drift apart, you reintroduce exactly the divergence problem you're trying to solve. Keep the mandatory-fields list itself generated from (or tested against) the same schema source the freeze GUI uses.
- **False sense of safety from "checklist theater":** A checklist with checkmarks but no underlying script execution is exactly the failure mode you already have (the assistant claiming inclusion without verification). The checklist must report the *actual* validator exit code, not a self-assessed checkbox.
- **Maintenance burden on the canonical installer template:** Centralizing the installer is good for consistency but creates a single point of failure — a bad edit to the template breaks every future delivery. This is exactly why it needs its own static tests (Section 5), checked in like any other source file.
- **Over-governing genuinely non-freezeable patches:** Not all patches are freeze-ready. The contract should explicitly support — not penalize — a clearly stated "non-freezeable, reason: ___" path, or assistants will be incentivized to fabricate a freeze hint just to satisfy the gate.

---

## 8. Minimal Next Patch Plan

To stop this specific failure from recurring, in priority order:

1. **Write `zip_contract_validator.py`** (Section 4) and wire it as a hard precondition: no ZIP link is emitted unless this script reports PASS against the assembled ZIP.
2. **Write `build_freeze_payload()`** as the single source feeding both `KANDA_FREEZE_HINT.json` and the chat-visible freeze-form JSON. Remove any path that lets these be authored independently.
3. **Extract the PowerShell installer into one canonical template file**, parameterized, checked into the repo, with the static "no Downloads/Desktop" test in place immediately.
4. **Add the router trigger**: detect "response will contain a ZIP link / install block / freeze evidence" and inject the `ZIP_DELIVERY_CONTRACT` checklist at that point, not only at session start.
5. **Add the regression test suite** from Section 5, focused first on the two tests that map directly to the two recurring failures: missing/duplicated hint, and Downloads/Desktop fallback in the template.
6. **Update `07_daily_patch_delivery_guardrails.md` and `09_active_project_freeze_context.md`** to point at the new validator/template/checklist as the authoritative mechanism, rather than restating the obligations in prose only.

Everything else in this audit (freeze GUI rejection messaging, `patch_release_manifest.json`, broader regression coverage) is valuable but secondary to these six items — those six are what directly close the gap that caused the `ml_adv000_router_canon_v1_patch.zip` failure.
