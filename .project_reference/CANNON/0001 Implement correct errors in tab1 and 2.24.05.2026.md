Below is the report to give the next AI.

```text
NEXT SESSION HANDOFF FOR AI
Project: Project Reasoner / developer_tools
Phase status: Complete JSON + split JSON web-AI readiness is frozen.

============================================================
0. FROZEN CONTEXT - DO NOT REDESIGN THIS PHASE
============================================================

The previous phase is frozen and validated.

Frozen as correct:
1. developer_tools__complete.json now contains the additive web-AI awareness layer.
2. developer_tools__complete_local_AI.json inherited the same required web-AI awareness sections.
3. web_ai_readme exists and tells AI which JSON sections to inspect for each question type.
4. JSON Splitter emits developer_tools__complete__web_ai_route_manifest.json.
5. Splitter route manifest maps question types to chunks.
6. Splitter tail-preservation bug was fixed.
7. Split/reassemble validation passed losslessly.
8. Real validation questions were answered successfully from split/complete JSON evidence.

Important validated final splitter result:
- payload_hash_failure_count: 0
- source_hash_ok: True
- reconstructed_hash_ok: True
- source_partition_ok: True
- source_slice_integrity_ok: True
- strict_coverage_ok: True
- route_manifest.ok: True

Do not reopen or redesign complete JSON logic unless a new failing validation proves a new bug.

The next phase is not about complete JSON.
The next phase is about making:
1. First step: check / correct architecture
2. Second step: check / correct workflow

better at exposing important project errors across many projects.

============================================================
1. WHAT FIRST STEP: CHECK / CORRECT ARCHITECTURE SHOULD EXPOSE
============================================================

Goal:
The architecture checker should audit source-code structure, ownership, box boundaries, symbol safety, and project maintainability. It should identify errors that are not solved merely by having a good complete JSON.

The checker should expose these categories:

1. Duplicate public symbols

Detect:
- Same class/function/constant name defined in multiple files.
- Same public API exported from multiple modules.
- Same helper name repeated across boxes.
- Ambiguous "canonical" definition.
- Duplicate symbols where no primary owner is clear.

Why important:
Even if web_ai_symbol_index and primary_definition_index help AI navigate duplicates, the source project may still contain real duplicate/shadowing problems.

Examples of error messages:
- Duplicate public symbol: PromptBuilder found in multiple files.
- Duplicate helper: build_x found in collector and splitter boxes.
- Ambiguous owner: same public function exported by two boxes.

2. Symbol shadowing

Detect:
- Local variable shadows imported function/class.
- Function shadows module name.
- Test helper shadows production helper.
- Constant shadows imported constant.
- Public name shadows built-in or project-level symbol.
- Alias import hides true owner.

Why important:
Shadowing can create subtle runtime bugs and makes AI reasoning less reliable.

Examples:
- from x import build_prompt, then local def build_prompt(...)
- variable named json, Path, list, dict, file, id, input, etc.
- test function or fixture hides production function.

3. Wrong owner box

Detect:
- Collector logic inside splitter.
- Splitter logic inside collector.
- GUI logic inside core/business module.
- Local-AI logic modifying canonical web-AI JSON.
- Prompt builder logic inside AI bridge.
- Retriever logic inside GUI.
- Validation logic inside production runtime path when it should be audit-only.

Why important:
The project uses box isolation. Each box should own only its own responsibility.

Architecture checker should identify owner mismatch such as:
- This file belongs to JSON Splitter but imports collector internals.
- This collector helper writes local-AI working JSON.
- This GUI file owns business logic that should be in a helper module.

4. Cross-box boundary violations

Detect:
- Core logic imports GUI libraries.
- Collector imports splitter internals.
- Splitter imports collector internals.
- AI bridge imports GUI window classes.
- Validation/audit modules modify production output.
- Tests import private GUI runtime state instead of public contracts.
- Helper modules reach into unrelated boxes.

Important boundaries:
- Collector creates canonical complete JSON.
- Local-AI copy manager manages developer_tools__complete_local_AI.json.
- Local-AI enrichment modifies only local-AI JSON.
- JSON Splitter splits already-generated JSON and emits route manifest.
- Prompt Builder builds prompts.
- Retriever retrieves evidence.
- AI Bridge talks to local AI and applies grounding.
- GUI wires buttons and displays state.

5. Circular imports

Detect:
- A imports B, B imports A.
- Package __init__.py imports heavy modules that import the package back.
- GUI imports helper that imports GUI again.
- Splitter imports validator that imports splitter GUI.
- Collector main imports modules that import collector main.

Why important:
Circular imports cause intermittent failures, especially in GUI startup and unit tests.

6. Side effects on import

Detect:
- Module starts GUI on import.
- Module reads/writes JSON on import.
- Module runs collector on import.
- Module starts local AI model on import.
- Module opens files or mutates global state on import.
- Module modifies sys.path globally on import.

Allowed:
- Pure constants.
- Pure function/class definitions.
- Safe lightweight metadata.

7. Mixed responsibility files

Detect:
- One file owns GUI + collector + splitter + validation.
- One file owns prompt building + AI bridge + retrieval.
- One file owns production logic + test fixtures.
- One file owns canonical JSON generation + local-AI enrichment.
- One file owns many unrelated workflow steps.

Architecture checker should flag:
- File has too many responsibility domains.
- File should be split into helper modules.
- File violates single-box ownership.

8. Stale / deprecated variants

Detect:
- Multiple old splitter versions.
- Old collector variants.
- Deprecated prompt builder variants.
- Obsolete test runners.
- Old generated helper files still importable.
- Legacy files with names like v1, v2, old, backup, copy, temp, scratch.

Do not delete automatically.
Report:
- Active owner candidate.
- Deprecated candidates.
- Risk if AI edits wrong file.

9. Misplaced tests

Detect:
- Test file outside expected tests folder.
- Test imports wrong production owner.
- Test protects old/deprecated file instead of active file.
- Test name implies one feature but imports another.
- Test helper duplicates production logic.
- Test file is included as production entry point.

10. Missing tests for critical owners

Detect:
- Important production file has no linked tests.
- Critical feature has no test protection.
- Recently changed owner box lacks focused test.
- Public symbol has no test coverage.
- Splitter/collector/prompt builder logic lacks regression tests.

Use:
- web_ai_test_protection_index
- web_ai_file_responsibility_index
- test_links
- files payload

11. Unsafe path and platform assumptions

Detect:
- Hardcoded absolute paths when not expected.
- Windows path mixed incorrectly with POSIX path.
- Raw string path issues.
- Unix-only commands in project code.
- Path separator assumptions.
- File encoding not explicit.
- Non-ASCII output in Python modules where project requires ASCII.

12. Canonical vs working-copy boundary errors

Detect:
- Local-AI experiment writes to developer_tools__complete.json.
- Collector writes directly to developer_tools__complete_local_AI.json.
- Splitter modifies input JSON.
- Enrichment modifies canonical web-AI JSON.
- Validation CLI writes files when it should be read-only.

Correct contract:
- Step 4 collector -> developer_tools__complete.json
- copy_manager -> developer_tools__complete_local_AI.json
- local-AI enrichment -> developer_tools__complete_local_AI.json only
- splitter -> split output folder only
- validators -> read-only

13. Generated artifact contract errors

Detect:
- Manifest schema mismatch.
- Missing BUNDLE_MANIFEST file.
- Bundle manifest outside _project_reference/BUNDLE_MANIFEST.
- Split output missing route manifest.
- Split output route manifest not referenced by upload index.
- Complete JSON missing required web-AI sections.
- Local-AI JSON stale relative to canonical.
- Manifest file name convention mismatch.

14. Public API instability

Detect:
- Public functions/classes renamed without compatibility.
- __all__ exports private or deprecated symbols.
- Public symbol removed but tests/workflows still reference it.
- Entry point changed without workflow update.
- New helper not exported when needed.
- Unwanted export creates duplicate-public-symbol noise.

15. Dead code and unreachable files

Detect:
- File never imported, referenced, or used by workflow.
- Function/class never referenced.
- GUI button refers to no function.
- Workflow step points to missing file.
- Test only covers deprecated file.

16. Inconsistent source-of-truth

Detect:
- README says one owner, source code says another.
- Workflow metadata says one step, GUI uses another.
- JSON route says one entry point, GUI uses another.
- Test protection index says one test, actual imports say none.
- File responsibility index and source docstring disagree.

17. Error handling architecture problems

Detect:
- Broad except hides real error.
- Failing validator returns PASS.
- GUI catches error but does not display useful message.
- Audit command fails without nonzero exit code.
- Splitter continues after missing required file.
- Local-AI answer silently falls back without warning.

18. Import heaviness / slow startup

Detect:
- GUI startup imports local AI model.
- Architecture checker imports full GUI.
- Tests import PySide6 unnecessarily.
- Validator imports heavy runtime modules.
- Pure helpers depend on GUI libraries.

19. Bundle safety issues

Detect:
- Bundle missing manifest.
- Bundle includes unrelated files.
- Bundle overwrites files outside intended box.
- Bundle mixes multiple concerns.
- Bundle weakens tests.
- Bundle modifies generated JSON manually.
- Bundle removes compatibility fields.

20. Project-wide "AI confusion" risks

Detect:
- Several files claim same responsibility.
- Many versions of same tool exist without active/deprecated labels.
- Entry point cannot be determined.
- Tests protect unclear target.
- Owner box cannot be inferred.
- Symbol has many duplicates and no primary definition.

============================================================
2. WHAT SECOND STEP: CHECK / CORRECT WORKFLOW SHOULD EXPOSE
============================================================

Goal:
The workflow checker should audit whether project steps, GUI buttons, commands, files, outputs, and dependencies match the intended user workflow.

It should find stale or broken workflows, not just source-code architecture.

The checker should expose these categories:

1. Workflow step points to missing file

Detect:
- GUI step references a module that no longer exists.
- Button command points to removed file.
- Documentation references old path.
- Workflow metadata has stale path.

Example:
- Step 4 says collector is in old path but active collector moved.
- JSON splitter workflow points to old splitter version.

2. Workflow step points to deprecated file

Detect:
- Step uses old splitter variant.
- Step uses old collector runner.
- Step opens old GUI.
- Step calls deprecated helper.

Report:
- Current referenced file.
- Better active owner candidate.
- Reason the current file appears deprecated.

3. Button-to-action mismatch

Detect:
- GUI button label says one action but calls another.
- "Refresh Local-AI Copy" calls ensure instead of refresh.
- "Split JSON" uses wrong input path.
- "Load JSON" does not update current loaded-track label.
- "Ask Local AI" bypasses the retriever.

4. Step order dependency errors

Correct sequence should be:

1. Check/correct architecture.
2. Check/correct workflow.
3. Other preparation steps.
4. Collect project structure -> developer_tools__complete.json.
5. Refresh/copy local-AI JSON if needed.
6. Split JSON.
7. Ask AI about project.

Workflow checker should detect:
- Splitter runs before collector.
- Local-AI copy is not refreshed after canonical regeneration.
- Ask-AI tab uses stale JSON.
- Validation runs before output exists.
- Web-AI route manifest missing after split.

5. Input/output contract mismatch

Detect:
- Step produces file A but next step expects file B.
- Collector outputs developer_tools__complete.json but splitter expects another filename.
- Splitter creates developer_tools_split_manifest.json but validator searches only *__split_manifest.json.
- Local-AI path expects developer_tools__complete_local_AI.json but GUI loaded canonical JSON.
- Upload index references route manifest not present.

6. Output folder naming mismatch

Detect:
- Code expects json_split.
- GUI writes json_splitted.
- Validator searches for one manifest pattern but actual manifest uses another.
- Route manifest naming differs by source base name.
- Documentation says dev_tools_docs/json_split but app uses dev_tools_docs/json_splitted.

7. Stale generated artifact workflow

Detect:
- Complete JSON older than source files.
- Local-AI JSON older than canonical JSON.
- Split chunks older than complete JSON.
- Route manifest older than split manifest.
- Upload index older than route manifest.
- Test protection index stale after new tests.

8. Missing validation step in workflow

Workflow should expose missing validation checkpoints:

After Step 4 collector:
- Run complete JSON audit.

After local-AI refresh:
- Run local-AI complete JSON audit.

After splitter:
- Run split/reassemble validation.

After web-AI route manifest:
- Confirm route manifest present and has routes.

If workflow lacks these checks, it should report:
- Validation missing from workflow.
- Validation available but not wired to GUI.
- Validation exists but not documented.

9. Placeholder command misuse

Detect:
- Documentation tells user to run <SPLIT_OUTPUT_FOLDER> literally.
- Command contains placeholder but no explanation.
- PowerShell commands use angle brackets.
- Paths not quoted.
- Backticks missing or unsafe.
- Command examples incompatible with Windows PowerShell.

10. GUI state label mismatch

Detect:
- Loaded JSON label does not distinguish canonical vs local-AI vs other.
- Step 7 Ask AI tab does not show current JSON path.
- Splitter does not show current input JSON.
- Local-AI copy buttons do not show stale/fresh state.
- Validation result not visible after command.

11. Workflow not reflecting dual JSON track

Correct rule:
- canonical JSON = web-AI export
- local-AI JSON = working copy for local AI enrichment

Workflow checker should expose:
- Local-AI path writing to canonical.
- Canonical path overwritten by local-AI enrichment.
- GUI does not label which track is loaded.
- Refresh local-AI copy missing after canonical regeneration.
- Local-AI stale state not reported.

12. Workflow not reflecting route manifest

Detect:
- Splitter output includes route manifest but upload instructions ignore it.
- Upload index does not reference route manifest.
- Web-AI prompt does not tell AI to open route manifest first.
- Split chunks uploaded without route guide.
- Route manifest not copied into expected output package.

13. Workflow not reflecting new web-AI readme

Detect:
- Complete JSON has web_ai_readme but prompt ignores it.
- Split route manifest has question routes but workflow still tells AI to search chunks manually.
- Upload instructions do not mention web_ai_readme.
- AI question workflow does not use question_routes.

14. Missing "which file should AI inspect" workflow

Detect:
- Web-AI flow lacks a deterministic route:
  - symbol question -> symbol route
  - file responsibility -> responsibility route
  - tests -> test protection route
  - entry points -> entry point route
  - citations -> stable evidence route

15. Broken local-AI Ask flow

Detect:
- Ask Local AI uses stale prompt.
- Ask Local AI does not use selected JSON.
- Ask Local AI bypasses evidence pack.
- Ask Local AI rejects grounded answer due to outdated forbidden path rule.
- Streaming answer appears then gets replaced by false INSUFFICIENT_EVIDENCE.
- Deterministic answer path crashes due to renamed private helper.
- Focus snippets path crashes due to renamed private helper.

Previously seen examples:
- score_file_locator_candidate vs _score_file_locator_candidate
- select_focus_snippets_from_prompt vs _select_focus_snippets_from_prompt
- PromptBuilder answer appeared then was replaced by INSUFFICIENT_EVIDENCE

16. Workflow step does not expose enough logs

Detect:
- Step fails but GUI only says failed.
- No path of input/output file shown.
- No manifest path printed.
- No validation command printed.
- No stale/fresh hash shown.
- No route manifest status shown.

17. Workflow step cannot be rerun idempotently

Detect:
- Rerunning collector corrupts outputs.
- Rerunning local-AI refresh overwrites local-only enrichment without warning.
- Rerunning splitter leaves stale old chunks mixed with new chunks.
- Rerunning validator picks wrong manifest.
- Rerunning GUI action duplicates state.

18. Workflow references old validation logic

Detect:
- Workflow uses old split validator that does not understand route manifest.
- Workflow uses old audit that does not check web-AI sections.
- Workflow uses old JSON copy status that does not detect stale local-AI JSON.
- Workflow uses old splitter that can drop tail entries.

19. Missing rollback / fail-safe workflow

Detect:
- If collector fails, workflow should preserve previous complete JSON.
- If splitter fails, workflow should preserve previous valid split folder or clearly mark output invalid.
- If local-AI refresh fails, local-AI JSON should not be half-written.
- If validation fails, workflow should not mark output as ready.

20. Workflow documentation drift

Detect:
- Prompt says update prompt, but code owns the behavior.
- Documentation says collector creates local-AI JSON, but copy_manager owns it.
- Documentation says splitter is optional, but upload flow requires route manifest.
- Documentation says "complete JSON is final" but source files are final truth for implementation.

21. Missing cross-project generalization

The user wants Step 1 and Step 2 to audit various projects, not only this project.

Workflow checker should generalize to detect:
- Missing entry point.
- Missing generated artifact contract.
- Missing route/index/manifest if project uses split context.
- Missing test protection map.
- Missing ownership map.
- Stale generated outputs.
- Stale local working copy.
- Deprecated variant still referenced.
- GUI button and workflow mismatch.

============================================================
3. ERRORS ALREADY COVERED BY CURRENT FROZEN PHASE
============================================================

Do not spend the next phase re-solving these unless validation fails again:

1. Complete JSON missing web-AI sections.
2. Local-AI JSON missing web-AI sections.
3. Web AI not knowing which section to inspect.
4. Split chunks lacking route manifest.
5. Splitter dropping tail entries during chunk merge.
6. Split/reassemble validation failure from dropped tail chunks.
7. Route manifest missing or invalid after split.
8. Web AI unable to answer PromptBuilder responsibility from JSON.

These are fixed and validated.

============================================================
4. ERRORS NOT YET COVERED
============================================================

The next phase should assume these may still exist:

1. Duplicate public symbols in source code.
2. Shadowed functions/classes/constants.
3. Wrong owner box for helpers.
4. Cross-box imports.
5. Circular imports.
6. GUI/core boundary violations.
7. Stale/deprecated file variants.
8. Misplaced tests.
9. Missing tests for critical files.
10. Workflow steps pointing to old files.
11. GUI buttons wired to old actions.
12. Output path naming mismatch.
13. Stale generated artifacts.
14. Local-AI copy stale or overwritten incorrectly.
15. Route manifest ignored by upload workflow.
16. Old splitter variants still referenced.
17. Reassembly GUI path not revalidated.
18. Local-AI retriever not prioritizing new indexes.
19. No one-command full pipeline validator.
20. No broad question benchmark suite.

============================================================
5. PROPOSED NEXT ROADMAP
============================================================

Next session should not restart complete JSON work.

Recommended roadmap:

1. Run "First step: check / correct architecture" on current project.
2. Collect all reported architecture errors.
3. Classify each error into:
   - duplicate/shadowing
   - owner-box violation
   - cross-box import
   - stale/deprecated file
   - missing test protection
   - GUI/core boundary violation
   - generated artifact contract violation
4. Decide which categories are already detected well and which need better detectors.
5. Create a focused architecture-checker improvement roadmap.

Then:

6. Run "Second step: check / correct workflow" on current project.
7. Collect all reported workflow errors.
8. Classify each error into:
   - stale path
   - wrong step order
   - wrong input/output contract
   - GUI button/action mismatch
   - stale generated artifact
   - validation missing from workflow
   - placeholder command issue
   - route manifest/upload workflow mismatch
9. Decide which categories are already detected well and which need better detectors.
10. Create a focused workflow-checker improvement roadmap.

Implementation rule:
Do not patch many detectors at once.
Create one narrow gate per detector category.

Suggested first detector gates:

Architecture:
1. duplicate_public_symbol_detector_gate
2. shadowed_symbol_detector_gate
3. box_owner_boundary_detector_gate
4. deprecated_variant_detector_gate
5. test_protection_gap_detector_gate

Workflow:
1. workflow_file_path_existence_gate
2. workflow_step_io_contract_gate
3. workflow_generated_artifact_freshness_gate
4. workflow_dual_json_track_gate
5. workflow_split_route_manifest_gate

============================================================
6. SAFETY RULE FOR NEXT AI
============================================================

Do not interpret "frozen complete JSON phase" as "whole project is clean."

Correct status:

complete JSON + split JSON web-AI readiness:
FROZEN AND VALIDATED

architecture checker:
NEXT PHASE, NOT FROZEN

workflow checker:
NEXT PHASE, NOT FROZEN

The next work is to make Step 1 and Step 2 better at exposing the remaining architecture and workflow errors across projects.
```

in this handoff report you inserted all important error to be audited  by 1 and 2?

Yes — the handoff report includes the main important error families that Step 1 and Step 2 should audit.
But I would phrase it like this for the next AI:
The report is intentionally comprehensive at the category level, not exhaustive at the individual-rule level.It lists the important classes of errors that Step 1 and Step 2 should learn to expose across projects.Next session should convert these categories into concrete detector gates, one by one.
So the answer is:
Yes, it includes the important audit targets for:1. First step: check / correct architecture2. Second step: check / correct workflow
The most important groups included are:
Architecture Step 1:- duplicate public symbols- symbol shadowing- wrong owner box- cross-box boundary violations- circular imports- side effects on import- mixed responsibility files- stale/deprecated variants- misplaced tests- missing tests for critical owners- unsafe path/platform assumptions- canonical vs local-AI working-copy boundary errors- generated artifact contract errors- public API instability- dead code/unreachable files- inconsistent source-of-truth- error handling architecture problems- heavy imports / slow startup risks- unsafe bundle composition- AI-confusion risks
Workflow Step 2:- workflow step points to missing file- workflow step points to deprecated file- button-to-action mismatch- wrong step order- input/output contract mismatch- output folder naming mismatch- stale generated artifacts- missing validation step- placeholder command misuse- GUI state label mismatch- dual JSON track mistakes- route manifest ignored by upload workflow- web_ai_readme ignored by workflow- missing deterministic route for AI question types- broken local-AI Ask flow- insufficient logs- non-idempotent reruns- old validation logic still referenced- missing fail-safe/rollback behavior- workflow documentation drift- lack of cross-project generalization
What it does not yet do is define exact implementation logic for every detector. That is the next roadmap step.
The next AI should treat the report as:
A complete audit taxonomy for Step 1 and Step 2.Not yet a completed detector implementation.
Best next action next session:
Take this taxonomy and build a numbered roadmap:
1 detector gate per category or subcategory.
Start with highest-risk architecture detectors:
- duplicate_public_symbol_detector- shadowed_symbol_detector
- - box_owner_boundary_detector- deprecated_variant_detector- 
- test_protection_gap_detectorThen workflow detectors:- 
- workflow_file_path_existence_gate- workflow_step_io_contract_gate-
- workflow_generated_artifact_freshness_gate- workflow_dual_json_track_gate-
- workflow_split_route_manifest_gate


You are continuing a Project Reasoner / developer_tools audit project.

Context:
The previous phase is frozen and validated. Do not redesign it unless a new validation failure proves a bug.

Frozen phase:
- developer_tools__complete.json now contains the additive web-AI awareness layer.
- developer_tools__complete_local_AI.json inherited the same required web-AI awareness sections.
- web_ai_readme exists and routes AI question types to the correct JSON sections.
- JSON Splitter emits developer_tools__complete__web_ai_route_manifest.json.
- Splitter route manifest maps question types to chunks.
- Splitter tail-preservation bug was fixed by replacing unsafe chunks[-1].extend(chunks.pop()) with merge_excess_tail_chunks(...).
- Split/reassemble validation passed losslessly.
- Real web-AI validation questions were answered successfully from split/complete JSON evidence.

Validated final splitter state:
- payload_hash_failure_count: 0
- source_hash_ok: True
- reconstructed_hash_ok: True
- source_partition_ok: True
- source_slice_integrity_ok: True
- strict_coverage_ok: True
- route_manifest.ok: True

Current task:
We are planning the next phase. This phase is not about complete JSON anymore.
The next phase is to improve:

1. First step: check / correct architecture
2. Second step: check / correct workflow

The goal is to make these two steps detect important project errors across many projects, not only this current developer_tools project.

Existing proposed audit taxonomy:

ARCHITECTURE STEP 1 SHOULD EXPOSE:
1. Duplicate public symbols
2. Symbol shadowing
3. Wrong owner box
4. Cross-box boundary violations
5. Circular imports
6. Side effects on import
7. Mixed responsibility files
8. Stale or deprecated variants
9. Misplaced tests
10. Missing tests for critical owners
11. Unsafe path and platform assumptions
12. Canonical vs working-copy boundary errors
13. Generated artifact contract errors
14. Public API instability
15. Dead code and unreachable files
16. Inconsistent source-of-truth
17. Error handling architecture problems
18. Import heaviness / slow startup risks
19. Bundle safety issues
20. Project-wide AI confusion risks

WORKFLOW STEP 2 SHOULD EXPOSE:
1. Workflow step points to missing file
2. Workflow step points to deprecated file
3. Button-to-action mismatch
4. Wrong step order
5. Input/output contract mismatch
6. Output folder naming mismatch
7. Stale generated artifacts
8. Missing validation step in workflow
9. Placeholder command misuse
10. GUI state label mismatch
11. Dual JSON track workflow mistakes
12. Route manifest ignored by upload workflow
13. web_ai_readme ignored by workflow
14. Missing deterministic route for AI question types
15. Broken local-AI Ask flow
16. Workflow step does not expose enough logs
17. Workflow step cannot be rerun idempotently
18. Workflow references old validation logic
19. Missing rollback / fail-safe workflow
20. Workflow documentation drift
21. Missing cross-project generalization

Already covered by frozen phase:
- Complete JSON missing web-AI sections
- Local-AI JSON missing web-AI sections
- Web AI not knowing which section to inspect
- Split chunks lacking route manifest
- Splitter dropping tail entries during chunk merge
- Split/reassemble validation failure from dropped tail chunks
- Route manifest missing or invalid after split
- Web AI unable to answer PromptBuilder responsibility from JSON

Not yet covered:
- Source-code shadowing itself
- Architecture ownership violations
- Workflow metadata staleness
- GUI reassembly button hardening
- One-command full pipeline validation
- Local-AI retriever prioritizing new indexes
- Old/deprecated splitter cleanup
- Broad benchmark suite

Question for you:
Review this audit taxonomy critically.

1. Is any important architecture error category missing from Step 1?
2. Is any important workflow error category missing from Step 2?
3. Are any categories redundant and should be merged?
4. Which detector gates should be built first, in risk-priority order?
5. For each missing category you identify, explain:
   - why it matters,
   - which project files or JSON sections might reveal it,
   - what a good detector should report,
   - whether it belongs to Step 1 architecture or Step 2 workflow.

Important constraints:
- Do not restart or redesign the frozen complete JSON / splitter readiness phase.
- Treat source code as implementation truth.
- Treat developer_tools__complete.json as canonical web-AI export truth.
- Treat developer_tools__complete_local_AI.json as local-AI working evidence only.
- Do not propose broad rewrites.
- Recommend one narrow detector gate per concern.
- Preserve box isolation.
- Prefer additive audit/reporting first before correction.


second opinion:

12:57 AM

This is a rich audit taxonomy question. Let me reason carefully from what I can observe in your actual JSON structure (from the chunks I already inspected) before making recommendations.
Critical Review of the Audit Taxonomy
1. Missing Architecture Categories (Step 1)

The existing 20 categories are solid but have these genuine gaps:
A1-21: Symbol collision across box boundaries (not just shadowing)

Different from #2 (symbol shadowing). Shadowing is when a local name hides an outer name within a file. This is when two different boxes export the same public symbol name, so import order determines which one wins silently.

    Why it matters: In your project, should_skip, write_text, iter_python_files appear in multiple files (visible in the symbol_index). Web AI and local AI both get ambiguous resolution. Runtime behavior depends on which module was imported first.
    Files/JSON: symbol_index (check for duplicate symbol names across different files), import_graph.
    Detector should report: {symbol, file_a, file_b, box_a, box_b} — "two boxes export the same public name."
    Step: Architecture Step 1.

A1-22: Implicit coupling through shared mutable globals or module-level state

Different from #6 (side effects on import). Side effects on import = something executes at import time. This is when two modules both read/write a shared module-level variable, creating hidden coupling the import graph does not show.

    Why it matters: EEG session state, reference dropdowns, and montage identity are exactly the kind of state that gets silently shared. Your attribute_state_map (chunk 7) exists precisely to detect this, but it is not currently cross-referenced against box ownership.
    Files/JSON: attribute_state_map, object_ownership, semantic_roles.
    Detector should report: {attribute, owning_file, accessing_file, box_owning, box_accessing} — "attribute defined in Box A is mutated by Box B without a declared interface."
    Step: Architecture Step 1.

A1-23: Inconsistent error handling contract across box boundary

Different from #17 (error handling architecture problems). #17 catches missing try/except and bare raises. This catches inconsistent contracts: Box A raises ValueError, Box B catches Exception, Box C returns None silently — so errors disappear across boundaries without being logged or surfaced.

    Why it matters: Your limitations section already flags 16 parse-failing files. The error handling contract across the montage/reference pipeline is invisible to web AI.
    Files/JSON: call_edges (trace exception propagation), symbol_index (find raise/return-None patterns), module_summary_index.
    Detector should report: {boundary_call, caller_expects, callee_raises, mismatch_type}.
    Step: Architecture Step 1.

A1-24: Test file asserts implementation detail instead of contract

Different from #9 (misplaced tests) and #10 (missing tests). This is when a test exists and is placed correctly but tests internal state rather than the public contract — making it brittle to safe refactors and giving false confidence.

    Why it matters: Your tools/architecture/check_* files are numerous (200+). Some may assert internal attribute values rather than observable behavior, which means an architecture refactor will break tests even when behavior is correct.
    Files/JSON: Files corpus (test files), symbol_index (detect ._private access in test assertions).
    Detector should report: {test_file, tested_symbol, access_type: internal|public, risk: brittle}.
    Step: Architecture Step 1.

A1-25: Missing __all__ on public-facing modules (uncontrolled public surface)

Related to #14 (public API instability) but distinct. Without __all__, every name in a module is implicitly public. A refactor that adds a helper function accidentally exports it.

    Why it matters: Your project has 1,251 Python files and 6,318 symbols. Without __all__ control, the public surface is undefined. Box boundary enforcement becomes impossible.
    Files/JSON: Files corpus (check for __all__ presence), module_summary_index.
    Detector should report: {file, box, has_all: false, exposed_symbol_count: N, risk: "uncontrolled surface"}.
    Step: Architecture Step 1.

2. Missing Workflow Categories (Step 2)

The existing 21 workflow categories are good but miss:
A2-22: Workflow assumes file encoding / platform line endings

Distinct from #11 (unsafe path assumptions). #11 is about path separators. This is about UTF-8 vs UTF-16, CRLF vs LF, BOM presence. Your limitations section already caught this: _project_reference/txt_md/requirements_anterior.txt: decoded with utf-16 after NUL-byte detection. A workflow that processes this file assuming UTF-8 will silently corrupt data.

    Why it matters: One encoding mismatch can corrupt a whole requirements parse, which then silently produces wrong dependency metadata in the canonical JSON.
    Files/JSON: limitations.packaging_metadata.warnings, collection_config, file corpus (encoding declarations).
    Detector should report: {file, detected_encoding, assumed_encoding, workflow_step, risk: data_corruption}.
    Step: Workflow Step 2.

A2-23: Workflow step silently succeeds with empty output

A step runs, exits 0, produces an output file — but the file is empty or contains a stub. Downstream steps consume it without error, producing wrong results.

    Why it matters: Your splitter produces part_count: 28 chunks. If the collector silently emits an empty files list (root_skeleton shows files: []), the splitter happily splits an empty corpus and all web-AI answers are wrong.
    Files/JSON: Manifest root_skeleton (empty lists), project_summary counters (zero values that should be nonzero), limitations.files_corpus.
    Detector should report: {workflow_step, output_file, expected_min_entries, actual_entries, verdict: empty_output}.
    Step: Workflow Step 2.

A2-24: Workflow dependency version skew between declared and installed

The workflow declares dependencies in requirements.txt (e.g. mne>=1.6) but the actually installed version differs. Collector results depend on which version of MNE is installed.

    Why it matters: If the installed version changes behavior silently (e.g., a new MNE release changes signal handling), the collector produces different output without any flag in the JSON.
    Files/JSON: packaging_metadata.declared_dependencies, limitations, collector runtime environment (not currently captured).
    Detector should report: {package, declared_constraint, installed_version, compatible: bool}.
    Step: Workflow Step 2. (Also relevant to architecture if a version skew causes import-time failures.)

A2-25: Workflow produces output to wrong relative path (path root drift)

The workflow is designed to write outputs relative to project root, but if run from a different working directory, outputs land in the wrong place. Downstream steps read stale files from the correct path instead of the new output.

    Why it matters: Your manifest records an absolute Windows path (E:\eeg_kernel_ai_neural_data_analysis\...). If the project is run from a subdirectory or CI uses a different root, the canonical JSON is written to the wrong location and the splitter reads a stale version.
    Files/JSON: collector_info.root_path, manifest source_file (absolute path vs relative), collection_config.
    Detector should report: {expected_output_path, actual_cwd, resolved_path, match: bool}.
    Step: Workflow Step 2.

3. Redundancy Analysis — Categories to Merge
Pair	Verdict
#2 Symbol shadowing + A1-21 (cross-box name collision)	Keep separate. Shadowing is within-file scope; cross-box collision is across-module public API. Different detector logic.
#6 Side effects on import + A1-22 (shared mutable globals)	Keep separate. Side effects = code runs at import; shared globals = state coupling. A file can have one without the other.
#8 Stale/deprecated variants + #16 Inconsistent source-of-truth	Merge these. A stale variant is an inconsistent source-of-truth. Detector: find files where two variants exist for the same responsibility and flag which is canonical.
#12 Canonical vs working-copy boundary + #13 Generated artifact contract	Keep separate. #12 is about which file is authoritative; #13 is about what the generated file must contain.
#9 Misplaced tests + #10 Missing tests	Keep separate but run together in one gate. They share the same input (file corpus + symbol index) but report different problems.
Step 2 #1 (missing file) + #2 (deprecated file)	Merge. Both reduce to "workflow step references a file that is not the current canonical version." One gate, two sub-checks.
Step 2 #13 (web_ai_readme ignored) + #14 (missing deterministic route)	Merge. If the readme is ignored, routes are missing. One gate covering both.

Net after merging: 18 architecture categories, 19 workflow categories.
4. Detector Gates — Risk-Priority Build Order

Priority is based on: blast radius (how many downstream things fail if this is wrong) × detectability (easy to write a reliable gate) × already-known evidence in your JSON.
Phase 1 — Build First (Blocking / High Blast Radius)
Priority	Gate	Why first
1	A2-23: Silent empty output	Your root_skeleton.files: [] is already suspicious. If the files corpus is silently empty, every downstream answer is wrong. Easy to check: len(files) == 0 is a one-line detector.
2	A1-21: Cross-box public symbol collision	symbol_index already exists with 6,318 entries. Detecting duplicates is a dict-grouping operation. High value, low effort. Already partially visible in your data (should_skip appears in multiple files).
3	A1-25: Missing __all__ on public modules	Files corpus exists. Grep for __all__. Report uncontrolled surface per box. High value for box boundary enforcement which is your stated architecture goal.
4	Merged #8+#16: Stale variant / inconsistent source-of-truth	Your project has 200+ check_* architecture scripts. Many are versioned variants (_v2, _repair, _revised). This is the highest-risk area for AI confusion and for developers making changes to the wrong file.
5	A2-25: Path root drift	Absolute paths are already in your manifest. Detector is trivial: compare collector_info.root_path with os.getcwd() at workflow runtime. Prevents silent stale-file reads.
Phase 2 — Build Next (High Value, Moderate Effort)
Priority	Gate	Why second
6	#5 Circular imports	import_graph already exists in chunk 3. Topological sort + cycle detection is a standard algorithm. Circular imports cause subtle import-order bugs in PySide6 apps specifically.
7	#4 Cross-box boundary violations	object_ownership + semantic_roles already exist. Gate: find call_edges where from_box != to_box and the call target is not in the declared public API of the target box.
8	A1-22: Shared mutable globals	attribute_state_map already exists. Gate: find attributes mutated in a different box than the one that defined them.
9	A2-22: Encoding / line-ending drift	Already flagged in limitations. Gate: validate encoding of all files referenced in packaging_file_patterns and doc patterns before the collector runs.
10	A1-23: Inconsistent error contract	Requires scanning call_edges for raise/return-None mismatches at boundaries. Moderate effort but critical for montage/reference pipeline correctness.
Phase 3 — Build Later (Important but Lower Urgency)
Priority	Gate
11	#6 Side effects on import
12	#14 Public API instability
13	A1-24: Test asserting internals
14	A2-24: Dependency version skew
15	#15 Dead code / unreachable files
16–19	Remaining Step 2 workflow metadata gates
5. Summary Table of All Missing Categories
ID	Name	Step	Priority	Evidence already in JSON
A1-21	Cross-box public symbol collision	Architecture	1	symbol_index (duplicate names visible)
A1-22	Shared mutable globals across boxes	Architecture	2	attribute_state_map, object_ownership
A1-23	Inconsistent error contract at boundaries	Architecture	2	call_edges, symbol_index
A1-24	Test asserting implementation internals	Architecture	3	Files corpus (test files)
A1-25	Missing __all__ / uncontrolled public surface	Architecture	1	Files corpus
A2-22	Encoding / line-ending drift	Workflow	2	limitations.packaging_metadata.warnings
A2-23	Workflow step silently produces empty output	Workflow	1	root_skeleton.files: [], project_summary counters
A2-24	Declared vs installed dependency version skew	Workflow	3	packaging_metadata.declared_dependencies
A2-25	Path root drift (absolute vs runtime cwd)	Workflow	1	collector_info.root_path, manifest source_file
Merge #8+#16	Stale variant / inconsistent source-of-truth	Architecture	1	module_summary_index, files corpus (_v2, _repair patterns)
Merge Step2 #1+#2	Workflow references missing or deprecated file	Workflow	2	Files corpus + declared_workflows
Merge Step2 #13+#14	web_ai_readme ignored / route missing	Workflow	2	Route manifest
One-Line Build Recommendation

Build gates in this order: A2-23 → A1-21 → A2-25 → Merge(#8+#16) → A1-25 → circular imports → boundary violations → A1-22 → A2-22 → A1-23. Each gate is a narrow, additive detector that reports without correcting. Build the report layer before any correction layer.
