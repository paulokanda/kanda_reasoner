KANDA REASONER — SHOW PROJECT TO AI SIZE, CONTENT, AND PORTABLE-SEPARATION HANDOFF

Project root:
E:\kanda_reasoner

Project Support root:
E:\kanda_reasoner_show_project_to_AI

Frozen feature:
freeze-20260729-show-project-and-portable-box-separation-canon-regenerated-evidence-semantics-correction

Frozen feature status:
frozen

Canonical Error Memory lesson:
lesson-show-project-generated-portable-archive-source-bloat-v1

1. PURPOSE OF THIS HANDOFF

This handoff exists to prevent the Show Project to AI folder from becoming unnecessarily large, slow to generate, or contaminated by Portable Distribution artifacts.

The central rule is:

SHOW PROJECT TO AI AND PORTABLE DISTRIBUTION ARE DIFFERENT BOXES.

They must never share creation ownership, output ownership, destination ownership, or lifecycle responsibility.

2. CANONICAL BOX LOGIC

SHOW PROJECT TO AI BOX

Owner:
reasoner_context_bundle and the handoff/export workflow

Trigger:
Create First and Second Prompt Files

Primary destination:
E:\kanda_reasoner_show_project_to_AI

Allowed output families:

* First Prompt files
* AI handoff ZIP
* source archive ZIP parts
* PNG asset ZIP parts
* compact Error Memory export
* full Error Memory ZIP
* source archive manifest
* routing and bundle manifests
* validation state
* Freeze Memory context
* startup and prompt-library ZIPs

Show Project may:

* inspect the selected project;
* classify source files;
* exclude generated release artifacts;
* create AI-readable manifests;
* create exact source archive parts;
* package PNG assets separately;
* record why generated archives were excluded;
* validate that its output does not contain Portable Distribution artifacts.

Show Project must never:

* create a Portable Distribution;
* rebuild a Portable Distribution;
* refresh a Portable Distribution;
* publish a Portable Distribution;
* move a Portable Distribution;
* delete a Portable Distribution;
* rename a Portable Distribution;
* request a Portable Distribution build;
* own a Portable Distribution;
* include a Portable Distribution in source archives;
* include a Portable Distribution in AI-readable manifests.

PORTABLE DISTRIBUTION BOX

Owner:
A separate productization or release workflow

Trigger:
An explicit user request to create a portable distribution

Dynamic output identity:

<project>-Windows-Portable.zip

Example:

KandaReasoner-Windows-Portable.zip

Destination:
Outside <project>_show_project_to_AI

The Portable Distribution workflow is independent from Show Project to AI.

The presence of an existing Portable ZIP inside the project root does not transfer ownership to Show Project.

Show Project may detect and exclude that file, but must not modify it.

3. ABSOLUTE NO-MIXTURE RULE

The following relationship is forbidden:

Show Project to AI
→ creates or owns
→ <project>-Windows-Portable.zip

The following relationship is allowed:

Independent release workflow
→ explicitly creates
→ <project>-Windows-Portable.zip

Show Project to AI
→ detects and excludes
→ <project>-Windows-Portable.zip

The portable filename remains a Portable Box artifact regardless of where it is accidentally located.

These must all be excluded:

KandaReasoner-Windows-Portable.zip

nested/KandaReasoner-Windows-Portable.zip

tests/fixtures/KandaReasoner-Windows-Portable.zip

A Portable Box filename must never be used as a legitimate ZIP-inclusion test fixture.

4. WHY THE PREVIOUS EXPORT BECAME GIGANTIC

The project root contained:

E:\kanda_reasoner\KandaReasoner-Windows-Portable.zip

Its approximate original size was:

469 MB

The old source exporter treated it as project source and created a dedicated source archive part containing that single nested ZIP.

The result was approximately:

446 MB of unnecessary source-archive output

The exporter also attempted to recompress an already compressed ZIP, saving almost no space while consuming substantial time.

The Portable ZIP added no useful AI-readable source context.

It was omitted from the active textual snapshot but still copied into the exact source archive.

This was incorrect.

5. EXPECTED NORMAL SIZE

After the correction, the validated KANDA Reasoner source archive was:

14,144,091 bytes

Approximately:

13.49 MiB

This is the expected scale for the current source archive, subject to normal source growth.

The source archive should remain in the tens-of-megabytes range unless the actual project source genuinely grows.

It must not suddenly grow by hundreds of megabytes because of:

* portable distributions;
* installers;
* release packages;
* generated distributions;
* already compressed archives;
* build outputs;
* transient release artifacts.

6. PNG ASSET SIZE

PNG assets are packaged separately from source archives.

The PNG archive can legitimately be much larger than the source archive because it contains application illustrations and reconstruction assets.

PNG assets must not be used to justify source-archive bloat.

The output families must remain separate:

source code and text
→ source archive parts

PNG assets
→ PNG asset parts

Portable distribution
→ separate release workflow, never Show Project output

Do not combine these families into a single source archive.

7. CANONICAL GENERATED-ARCHIVE CLASSIFIER

One canonical generated-archive classifier must be used by both:

* file manifest generation;
* source archive inventory generation.

Protected owner:

kanda_reasoner_app/reasoner_context_bundle/generated_archive_policy.py

The classifier must dynamically identify:

<project>-Windows-Portable.zip

It must also exclude project-prefixed root archives that clearly represent:

* portable builds;
* installers;
* distributions;
* release packages.

Portable exclusions should use:

reason_code:
generated_portable_distribution

The classifier must not depend only on the literal KANDA Reasoner filename.

It must work dynamically for other selected projects, such as:

eeg_kanda-Windows-Portable.zip

ExampleProject-Windows-Portable.zip

8. LEGITIMATE ZIP FILES MUST REMAIN SUPPORTED

Not every ZIP file inside a project is generated release output.

Differently named legitimate source fixtures and assets must remain includable.

Examples that may remain included:

tests/fixtures/ExampleProject-ArchiveFixture.zip

assets/sample_data.zip

test_data/example_payload.zip

The classifier must distinguish:

ExampleProject-Windows-Portable.zip
→ Portable Distribution, exclude

ExampleProject-ArchiveFixture.zip
→ legitimate fixture, preserve unless another project exclusion rule applies

9. UNKNOWN LARGE ARCHIVE FAIL-CLOSED RULE

An unknown large project-prefixed ZIP at the selected project root must not silently enter hashing and compression.

Before expensive processing, the exporter must detect suspicious archives when they are:

* located at the selected project root;
* project-prefixed;
* large;
* binary and not AI-readable;
* release-like or generated-artifact-like;
* not explicitly classified or allowlisted.

The export must then:

* exclude it through canonical policy; or
* stop immediately with a precise actionable error.

It must not spend many minutes recompressing an unknown large archive.

10. PROJECT EXCLUSION RULE ISOLATION

Synthetic validators must not inherit ambient user Project Exclusion Rules.

A validation fixture must inject explicit isolated ExclusionRules.

Otherwise ambient rules such as:

tests

fixtures

*.zip

may exclude a fixture’s parent folder before the generated-archive classifier is exercised.

Synthetic validation must prove:

* ambient exclusion settings cannot alter deterministic fixture results;
* the portable classifier is actually tested;
* a legitimate differently named nested ZIP remains included;
* a dynamic Portable filename remains excluded.

Live project validation may use the real project exclusion rules.

Synthetic regression fixtures must use isolated rules.

11. EVIDENCE AUTHORITY

Do not treat sample-capped exclusion logs as authoritative proof.

Fields such as:

excluded_path_samples

may contain only a limited sample of excluded paths.

A correctly excluded Portable ZIP may not appear in that sample.

The authoritative confirmation order is:

1. The live generated-archive classifier identifies the existing file as Portable Box output.

2. The AI-readable file manifest does not include the Portable path.

3. The source archive manifest does not include the Portable path.

4. The exact source archive ZIP members do not contain the Portable path.

5. The produced source-part set exactly matches the source manifest.

6. Every source-part size matches the manifest.

7. Every source-part SHA-256 matches the manifest.

8. Every source archive passes ZIP CRC validation.

An exclusion-reason record is useful diagnostic evidence when present.

Its absence from a sample-capped field must not create a false validation failure.

12. SECOND_PROMPT_FILES HYGIENE

The second_prompt_files folder should contain only governed handoff families.

Expected families include:

kanda_reasoner__ai_handoff_upload*.zip

kanda_reasoner__source_archive_partXX_of_YY.zip

kanda_reasoner__png_assets_partXX_of_YY.zip

kanda_reasoner__error_memory_full.zip

compact Error Memory files

source archive manifest

collector status

handoff readme

An optional AI handoff all-in-one ZIP may exist as a convenience archive.

It must not contain nested source archive ZIPs or Portable Distribution artifacts.

Loose Web AI JSON files should normally be removed after successful handoff ZIP publication when the workflow specifies that behavior.

The Project A&A local-AI working JSON may remain when required for local questions.

13. PORTABLE ZIP LOCATION

The best operational practice is to store portable releases outside the active project root.

A suitable independent location can be chosen by the release workflow, such as an external productization or release folder.

However, the current canon allows an existing Portable ZIP to remain in the live project root provided that:

* Show Project never modifies it;
* the classifier recognizes it;
* file manifests exclude it;
* source manifests exclude it;
* source archive ZIP members exclude it;
* Show Project output remains portable-free.

Moving or deleting an existing portable artifact is not authorized by the Show Project workflow.

14. REQUIRED REGENERATION VALIDATION

After a Show Project generation, confirmation must require:

REGENERATED_SUPPORT_PORTABLE_DISTRIBUTION_ABSENT: PASS

REGENERATED_STARTUP_PORTABLE_SEPARATION_CANON: PASS

REGENERATED_README_PORTABLE_SEPARATION_CANON: PASS

REGENERATED_LIVE_PORTABLE_POLICY_CLASSIFICATION: PASS

REGENERATED_FILE_MANIFEST_PORTABLE_EXCLUSION: PASS

REGENERATED_SOURCE_MANIFEST_PORTABLE_EXCLUSION: PASS

REGENERATED_SOURCE_PART_SET_EXACT: PASS

REGENERATED_SOURCE_ARCHIVE_PORTABLE_FREE: PASS

STATUS: IN_SYNC

The source archive byte total must also be reported.

A large increase must be investigated before Freeze.

15. SOURCE ARCHIVE AUDIT CHECKLIST

For every regenerated source archive:

* Load the source archive manifest.
* Enumerate all declared source parts.
* Confirm no undeclared source parts exist.
* Confirm no declared source part is missing.
* Compare each part’s byte size.
* Compare each part’s SHA-256.
* Open each ZIP and run CRC validation.
* Enumerate exact member names.
* Reject all dynamic Portable Distribution paths.
* Reject generated release artifacts.
* Confirm legitimate nested ZIP fixtures remain present when expected.
* Report total source archive bytes.
* Compare total size with the previous valid generation.

16. SIZE-REGRESSION WARNING THRESHOLD

A future AI should investigate when the source archive:

* grows by hundreds of megabytes without equivalent source growth;
* gains a source part containing only one large archive;
* contains another ZIP hundreds of megabytes in size;
* takes tens of minutes to generate;
* includes binary files absent from the active AI snapshot;
* attempts to recompress an already compressed archive;
* includes root-level release or distribution outputs.

Do not normalize or accept this behavior merely because the export eventually completes.

17. SAFE OPTIMIZATION ORDER

When Show Project generation becomes slow, investigate in this order:

1. Check for Portable Distribution ZIPs inside the project root.

2. Check source archive members for large nested ZIPs.

3. Compare current and previous source archive manifests.

4. Identify which exact files caused size growth.

5. Confirm PNG assets remain isolated in PNG archive parts.

6. Confirm generated release artifacts are classified before hashing or compression.

7. Confirm source archive reuse logic has not rebuilt unchanged content unnecessarily.

8. Only consider broader exporter redesign after proving the existing bounded policies are insufficient.

9. DO NOT “OPTIMIZE” BY REMOVING REQUIRED CONTEXT

Do not solve size problems by deleting or suppressing useful AI context.

Preserve:

* source code;
* prompt-library canon;
* routing manifests;
* validation state;
* compact Error Memory;
* full Error Memory archive;
* source archive manifest;
* required project documentation;
* legitimate source fixtures;
* required PNG reconstruction assets.

The goal is to remove generated release contamination, not weaken the AI handoff.

19. PROTECTED PATHS

Treat these as frozen-protected paths:

kanda_reasoner_app/reasoner_context_bundle/generated_archive_policy.py

kanda_reasoner_app/reasoner_context_bundle/source_tree_exporter_inventory.py

kanda_reasoner_app/reasoner_context_bundle/file_manifest_builder.py

kanda_reasoner_app/reasoner_context_bundle/handoff_zip_exporter_support.py

kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/12_generalized_project_canons/project_tool_boundary_startup_bridge.md

kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/12_generalized_project_canons/project_tool_boundary_canon.md

project_freeze_after_update/frozen_features_memory

Additional validated source involved:

kanda_reasoner_app/reasoner_context_bundle/source_tree_exporter_shared.py

tools/validate_show_project_generated_portable_archive_exclusion_v1.py

Do not modify these casually.

A future correction must:

* identify a demonstrated defect;
* inspect the frozen entry;
* inspect the active Error Memory lesson;
* preserve the Box separation;
* add focused regression evidence;
* regenerate Show Project output;
* confirm exact source archive members;
* Freeze only after STATUS: IN_SYNC.

20. FREEZE CANON

The active frozen entry is:

freeze-20260729-show-project-and-portable-box-separation-canon-regenerated-evidence-semantics-correction

Status:

frozen

Superseded by:

none

Any “planned next step” prose inside that frozen entry is historical intake text.

It must not be interpreted as pending work.

Project-specific Freeze Memory remains under:

<project>_show_project_to_AI/project_freeze_after_update/frozen_features_memory

Do not write project-specific frozen entries into project_freeze_ledger.

Freeze Preview remains read-only.

Confirm and Write requires explicit human confirmation.

21. ERROR MEMORY CANON

Canonical lesson:

lesson-show-project-generated-portable-archive-source-bloat-v1

The lesson must prevent:

* Portable ZIP inclusion as source;
* Show Project ownership of Portable generation;
* recompression of gigantic generated archives;
* reliance on sample-capped exclusion logs;
* synthetic-validator leakage from ambient exclusion rules;
* use of Portable filenames as legitimate inclusion fixtures.

Do not create duplicate Error Memory lessons for the same failure.

When a similar failure occurs, first check whether this lesson already owns it.

22. FAST FUTURE-AI DECISION RULE

When asked to maintain or repair Show Project to AI, apply this decision:

Is the file actual project source or a required reconstruction asset?

YES:
Include it in the correct governed family.

NO:
Continue classification.

Is the file a generated Portable, installer, distribution, release package, or other productization artifact?

YES:
Exclude it from Show Project.
Do not modify it.
Do not create it.
Do not move it.
Do not delete it.

NO:
Apply ordinary project exclusion and source-classification rules.

Is an unknown project-prefixed root ZIP very large?

YES:
Fail closed before hashing or compression.

NO:
Continue normal export.

23. EXPECTED HEALTHY FINAL STATE

A healthy current KANDA Reasoner generation should resemble:

AI handoff:
small, approximately hundreds of kilobytes

Full Error Memory:
small, approximately one megabyte

Source archive:
approximately 14 MB at the current project scale

PNG archive:
larger, because visual assets are separated there

Portable ZIP in Show Project:
zero

Portable ZIP in source archive:
zero

Portable ZIP in AI manifest:
zero

Show Project generation time:
reasonable and not dominated by recompressing a giant nested archive

Final markers:

STATUS: IN_SYNC

REGENERATED_SOURCE_ARCHIVE_PORTABLE_FREE: PASS

FREEZE_HINT_READY_RECORD_VERIFIED: PASS

24. NON-NEGOTIABLE SUMMARY

Never mix Show Project to AI with Portable Distribution.

Show Project creates AI context.

Portable creates a separately requested application distribution.

A Portable artifact may be detected and excluded by Show Project, but never created or owned by it.

Keep source archives small by excluding generated release artifacts before hashing and compression.

Validate exact manifests and ZIP members, not incomplete diagnostic samples.

Preserve legitimate source ZIP fixtures and required AI context.

Do not Freeze until the regenerated output proves that the Portable archive is absent from every Show Project output family.
