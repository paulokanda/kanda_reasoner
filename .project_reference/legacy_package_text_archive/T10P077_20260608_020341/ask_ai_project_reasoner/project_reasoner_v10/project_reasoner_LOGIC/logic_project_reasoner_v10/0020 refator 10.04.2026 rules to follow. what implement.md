the full end-to-end ordered roadmap down to “done.”
So here is the complete roadmap still to go, from the current stable state.

Right now, reasoner_retriever.py is already in late-stage shell form: retrieval seams are extracted and the origin mostly coordinates and delegates.

Complete remaining roadmap
1. Immediate repair
Add the missing snippet_retrieval import block in
E:\developer_tools\kanda_reasoner_app\project_reasoner_v10\reasoner_retriever.py
Re-run:
py_compile for origin and helpers
manifest validator
Confirm the unresolved references disappear in PyCharm.

This is the only clearly identified concrete defect still visible from the current origin file state.

2. Final cleanup pass for reasoner_retriever.py

After the missing import is fixed:

remove unused imports from the origin file
reformat __all__ into a multi-line canonical list
normalize blank lines and wrapper spacing
verify every wrapper has a matching import
verify no wrapper still delegates recursively by mistake
keep retrieve(...) in the origin file

This is now a cleanup/stabilization phase, not another decomposition phase. The current file already shows the right architectural shape.

3. Runtime smoke tests for retriever

After cleanup, test real retriever behavior with representative prompts:

startup question
explain-chain question
where-is question
which-calls question
runtime-heavy question
topomap explanation question
packaging metadata question
documentation intent question

Goal:

confirm wrappers resolve correctly
confirm no NameError
confirm no recursion
confirm returned bundles still contain file, symbol, and snippet evidence
4. Regression tests for retriever

Add or update tests for:

file retrieval helper
symbol retrieval helper
snippet retrieval helper
manifest validator schema
wrapper-import sanity
no recursive delegation
end-to-end retrieve(...) flow

This is important because most failures in this chat were:

broken wrapper signatures
missing imports
manifest drift
BOM/header issues
validator-clean but behavior-broken bundles
5. Final cleanup pass for ai_reasoner_main_window.py

That module is already basically done structurally, so the remaining work is small:

remove unused imports
normalize __all__ and spacing
confirm helper ownership boundaries stayed intact
keep it as a thin shell
6. Stabilization checkpoint

At this point, both major modules should be considered stable for this refactor wave:

ai_reasoner_main_window.py
reasoner_retriever.py

Then freeze those seams:

avoid further decomposition unless a real new seam appears
update docs/manifests only when necessary
prefer tests over more splitting
7. Next architecture target: v10_query_router.py

After retriever stabilization, audit:

E:\developer_tools\kanda_reasoner_app\project_reasoner_v10\v10_query_router.py

Reason:

intent ownership may overlap with reasoner_retriever_help\query_intents.py
now that retriever intent logic is modularized, router cleanup is safer

Tasks:

compare router intent heuristics with retriever intent heuristics
remove duplication
decide one clear ownership boundary
add tests for route consistency
8. Next architecture target: v10_prompt_builder.py

Then audit:

E:\developer_tools\kanda_reasoner_app\project_reasoner_v10\v10_prompt_builder.py

Tasks:

inspect duplication between prompt assembly and retrieval-bundle formatting
simplify prompt section composition
normalize prompt construction patterns
improve determinism and readability
add regression tests
9. End-to-end session-path audit

After router and prompt builder:

retriever
router
prompt builder
AI bridge/session path
main window orchestration

Goal:

verify handoff between stages
verify prompt receives the right retrieval bundle
verify answer flow is stable
eliminate duplicated logic across layers
10. Test and validation hardening

Then create a full validation pass that becomes standard for future work:

py_compile all touched modules
manifest validator
targeted unit tests
a few end-to-end scenario tests
PyCharm unresolved-reference sanity
BOM/header schema checks
11. Documentation and canon lock

Once stable:

update the canonical roadmap document
document safe-bundle rules
document manifest schema expectations
document origin-vs-helper ownership rules
document common failure modes found in this refactor
12. Only after all that: next large refactor target

Only then should the next large module be chosen.

Priority order I recommend:

v10_query_router.py
v10_prompt_builder.py
whichever module still mixes orchestration and domain heuristics after those two are stabilized
In one sentence

So the complete roadmap still to go is:

fix missing snippet imports in reasoner_retriever.py
do final retriever cleanup
do retriever runtime smoke tests
add retriever regression tests
do final main-window cleanup
stabilize both modules
refactor v10_query_router.py
refactor v10_prompt_builder.py
run end-to-end session-path audit
harden validation/test workflow
document the canon
only then pick the next large target

If you say continue, I will turn this into a stricter numbered execution plan with exact file-by-file order and stop conditions.

continue
Thought for 14s

Here is the stricter execution plan, in the exact order I would follow next time.

The plan starts from the current state where the retriever shell is already largely modularized, with file, symbol, and snippet logic extracted to helpers, and the remaining work is mostly stabilization, cleanup, validation, and then moving to the next architecture targets. The current origin file still clearly shows the public-shell pattern and the delegated seams.

Execution plan from here to stable completion
1. Repair the current retriever origin file

Target file
E:\developer_tools\kanda_reasoner_app\project_reasoner_v10\reasoner_retriever.py

Action

Add the missing import block from:
reasoner_retriever_help\snippet_retrieval.py
Ensure these names are imported:
build_runtime_anchor_snippets
extract_runtime_anchors_from_detail
find_anchor_line_in_file
read_snippet
resolve_existing_project_file_path
retrieve_snippets
score_file_snippet_candidate
score_runtime_anchor_for_question
score_symbol_snippet_candidate
snippet_radius_for_symbol

Why first
Because the wrappers already exist in the origin file, and unresolved references are the only clearly identified live defect still visible in the current source state.

Stop condition
Do not proceed until:

reasoner_retriever.py compiles
helper modules compile
manifest validator passes
unresolved references disappear in the IDE
2. Do a final cleanup pass on reasoner_retriever.py

Target file
E:\developer_tools\kanda_reasoner_app\project_reasoner_v10\reasoner_retriever.py

Action

Remove unused imports
Reformat the long single-line __all__
Normalize spacing between methods
Confirm wrapper signatures and return types are clean
Confirm wrappers correspond exactly to helper exports
Keep retrieve(...) in the origin file
Keep ProjectRetriever in the origin file
Do not create new helper files in this step

Why
At this stage the file is already in the correct structural role: public entry shell plus orchestration. More extraction now is lower value than cleanup.

Stop condition
Do not proceed until:

compile passes
validator passes
no new unresolved references appear
the origin file reads like a thin public shell
3. Smoke-test real retriever behavior

Targets

reasoner_retriever.py
its helper modules under:
E:\developer_tools\kanda_reasoner_app\project_reasoner_v10\reasoner_retriever_help

Action
Run representative retrieval prompts covering the main routing families:

startup flow
explain-chain flow
where-is flow
which-calls flow
runtime-heavy flow
topomap explanation flow
packaging metadata flow
documentation intent flow

What to verify

No NameError
No recursion loop
No missing helper imports
Returned RetrievalBundle contains expected file, symbol, and snippet evidence
Expanded callee logic still works
Section-priority routing still works

Stop condition
Do not proceed until all tested flows return sensible evidence and no runtime exceptions occur.

4. Add retriever regression coverage

Targets
Likely under:
E:\developer_tools\kanda_reasoner_app\project_reasoner_v10\tests

Action
Create or update tests for:

file_retrieval.py
symbol_retrieval.py
snippet_retrieval.py
reasoner_retriever_help.json manifest schema
import/wrapper sanity for reasoner_retriever.py
end-to-end retrieve(...) behavior

Highest-priority regressions to lock

malformed wrapper signatures
missing helper imports
helper stub recursion
validator-clean but behavior-broken state
BOM/header/manifest schema drift

Stop condition
Do not proceed until the retriever seam has regression coverage for both structure and behavior.

5. Final cleanup pass on ai_reasoner_main_window.py

Target file
E:\developer_tools\kanda_reasoner_app\project_reasoner_v10\ai_reasoner_main_window.py

Action

Remove unused imports
Normalize spacing and formatting
Re-check __all__
Confirm the shell/helper boundary is still correct
Avoid any new extraction unless a real seam appears

This module was already brought into a thin-shell structure earlier in the session, and the heavy architectural work there is effectively done.

Stop condition
Do not proceed until:

compile passes
manifest validator passes
no helper ownership drift is visible
6. Freeze the two major refactored shells

Targets

ai_reasoner_main_window.py
reasoner_retriever.py

Action
Declare both modules “shell-stable” for this refactor wave.

That means:

no more splitting unless a strong new seam appears
prioritize tests and bug fixes over more helper creation
prefer readability and correctness over additional decomposition

Stop condition
Proceed only after both modules are stable enough that new changes are small and local.

7. Audit v10_query_router.py

Target file
E:\developer_tools\kanda_reasoner_app\project_reasoner_v10\v10_query_router.py

Why next
Retriever intent logic now lives in dedicated helpers, so router cleanup becomes safer. The likely architectural issue now is overlap or duplicated intent heuristics between the router and reasoner_retriever_help\query_intents.py.

Action

Compare router routing logic to retriever intent predicates
Identify duplication
Decide ownership:
router decides route
retriever intent helper decides retrieval heuristics
Remove duplicated or drifting heuristics
Add tests for route consistency

Stop condition
Do not move on until intent ownership between router and retriever is clear and documented.

8. Audit v10_prompt_builder.py

Target file
E:\developer_tools\kanda_reasoner_app\project_reasoner_v10\v10_prompt_builder.py

Why after router
Once routing and retrieval are stabilized, prompt construction becomes the next likely duplication and complexity source.

Action

Audit prompt section composition
Clarify boundary between:
retrieval bundle content
route decision
prompt formatting
Remove repeated logic
Normalize prompt assembly style
Add regression tests for prompt output shape

Stop condition
Do not move on until prompt assembly is deterministic and free of obvious duplication.

9. Do an end-to-end session-path audit

Targets

router
retriever
prompt builder
AI bridge/session flow
main window orchestration

Action
Validate the full path:

question enters main window
router and/or retriever intent logic run
retrieval bundle is created
prompt is built
AI call path is invoked
answer is rendered

What to check

same question leads to stable route and bundle
no stage re-implements another stage’s job
no mismatched assumptions between bundle and prompt
UI shell still reflects actual pipeline state

Stop condition
Proceed only after the end-to-end path is consistent and repeatable.

10. Harden the validation workflow

Goal
Turn what we learned in this chat into the standard safety gate for future work.

Required validation sequence after any refactor bundle

py_compile touched files
manifest validator
targeted tests
end-to-end smoke scenario
IDE unresolved-reference check
BOM/header sanity check

Why
This chat surfaced repeated failure classes:

malformed wrapper signatures
missing imports
BOM corruption
manifest schema drift
validator-clean but behavior-broken bundles

Stop condition
This becomes the default workflow for all future refactor steps.

11. Document the canon

Action
Create or update a canonical internal note documenting:

origin-file responsibilities
helper-file responsibilities
safe-bundle rule
manifest schema
dependency graph expectations
header requirements
no-BOM rule
when to stop extracting and switch to cleanup/testing

Why
The next AI should not need to rediscover these rules.

Stop condition
Proceed only after the rules are written once in a stable place.

12. Choose the next large refactor target

Only after stages 1 through 11 are complete should the next large target be chosen.

Recommended priority

v10_query_router.py
v10_prompt_builder.py
whichever module still mixes orchestration and domain heuristics after those two are cleaned
File-by-file order

This is the strict practical order:

E:\developer_tools\kanda_reasoner_app\project_reasoner_v10\reasoner_retriever.py
E:\developer_tools\kanda_reasoner_app\project_reasoner_v10\reasoner_retriever_help\snippet_retrieval.py
E:\developer_tools\kanda_reasoner_app\project_reasoner_v10\reasoner_retriever_help\symbol_retrieval.py
E:\developer_tools\kanda_reasoner_app\project_reasoner_v10\reasoner_retriever_help\file_retrieval.py
E:\developer_tools\kanda_reasoner_app\project_reasoner_v10\reasoner_retriever_help.json
retriever tests
E:\developer_tools\kanda_reasoner_app\project_reasoner_v10\ai_reasoner_main_window.py
main-window tests or validation checks
E:\developer_tools\kanda_reasoner_app\project_reasoner_v10\v10_query_router.py
router tests
E:\developer_tools\kanda_reasoner_app\project_reasoner_v10\v10_prompt_builder.py
prompt-builder tests
end-to-end session flow
documentation/canon update
Safe-bundle policy from now on

Use a bundle only when:

one seam spans origin file + helper + manifest
the seam is tightly coupled
splitting it would leave a temporarily broken state

Do not bundle together:

two unrelated large seams
retriever and router refactors together
router and prompt builder together
Final state definition

The refactor wave is truly done only when all of these are true:

reasoner_retriever.py has no unresolved references
retriever helpers compile
manifests validate
retriever runtime smoke tests pass
retriever regressions exist
ai_reasoner_main_window.py is cleanup-complete
main window validates
router duplication is resolved
prompt builder duplication is resolved
end-to-end flow is stable
the canon is documented
Next-chat starting point

The best exact starting command for the next AI is:

repair missing snippet_retrieval imports in E:\developer_tools\kanda_reasoner_app\project_reasoner_v10\reasoner_retriever.py, then run full retriever cleanup and smoke validation

If you want, I can now turn this into a copy-paste master handoff prompt for the next session.


