KANDA REASONER — DYNAMIC PORTABLE DISTRIBUTION CREATION HANDOFF

Project example:
E:\kanda_reasoner

Project Support example:
E:\kanda_reasoner_show_project_to_AI

Required portable destination:
E:<dynamic-project-name>-Windows-Portable.zip

Example:
E:\kanda_reasoner-Windows-Portable.zip

The exact capitalization or display name may use the project’s existing canonical product-name resolver when one exists. The output must still be placed at the root of the same drive as the selected project, outside both the project folder and Project Support folder.

1. PURPOSE

This handoff explains how to create a dynamic Windows Portable Distribution without contaminating:

* the active project source;
* the Show Project to AI folder;
* source archive parts;
* AI-readable handoff manifests;
* Freeze Memory;
* Error Memory exports;
* Project Support outputs.

The non-negotiable principle is:

PORTABLE DISTRIBUTION AND SHOW PROJECT TO AI ARE DIFFERENT BOXES.

Portable creation belongs to an independent productization or release workflow.

Show Project to AI must never create, rebuild, refresh, move, delete, publish, or own a Portable Distribution.

2. EXPLICIT USER REQUEST REQUIRED

A Portable Distribution may be created only after an explicit user request.

Valid examples:

* Create the Windows Portable version of this project.
* Build the portable ZIP.
* Generate <project>-Windows-Portable.zip.

The Portable workflow must not start merely because:

* Show Project to AI was generated;
* source archives were created;
* Freeze was performed;
* validation passed;
* the application started;
* a Portable ZIP is missing;
* a previous Portable ZIP is outdated;
* project source changed;
* the user clicked Create First and Second Prompt Files.

No automatic Portable build is allowed.

3. CANONICAL BOX OWNERSHIP

PORTABLE DISTRIBUTION BOX

Owner:
Independent productization or release workflow

Trigger:
Explicit human request

Input:
Selected active project source

Build staging:
A transient folder outside the project source and outside Project Support

Final output:
The root of the same drive that contains the selected project

Output identity: <project>-Windows-Portable.zip

SHOW PROJECT TO AI BOX

Owner:
reasoner_context_bundle and handoff exporter

Trigger:
Create First and Second Prompt Files

Destination: <project>_show_project_to_AI

Allowed output families:

* AI handoff ZIPs
* source archive parts
* PNG asset parts
* Error Memory exports
* manifests
* validation state
* startup context
* Freeze Memory context

Portable output is not an allowed Show Project output family.

4. DYNAMIC PATH RESOLUTION

Never hardcode E:\ unless the selected project is actually on E:.

Resolve paths dynamically from the selected project root.

Canonical variables:

ProjectRoot:
The selected active project folder.

DriveRoot:
The filesystem root containing ProjectRoot.

ProjectFolderName:
The final folder component of ProjectRoot.

CanonicalProductName:
The project’s configured product name when a governed product-name owner exists.

PortableName: <CanonicalProductName-or-ProjectFolderName>-Windows-Portable.zip

PortableOutput: <DriveRoot><PortableName>

Example 1:

ProjectRoot:
E:\kanda_reasoner

DriveRoot:
E:\

ProjectFolderName:
kanda_reasoner

PortableOutput:
E:\kanda_reasoner-Windows-Portable.zip

Example 2:

ProjectRoot:
D:\eeg_kanda

DriveRoot:
D:\

ProjectFolderName:
eeg_kanda

PortableOutput:
D:\eeg_kanda-Windows-Portable.zip

When the project has a governed display or product name such as KandaReasoner, that canonical owner may produce:

E:\KandaReasoner-Windows-Portable.zip

Do not invent a new naming transformation inside the release helper. Reuse the existing canonical product-name resolver when available. Otherwise, use the exact project folder leaf.

5. REQUIRED DESTINATION BOUNDARY

The final Portable ZIP must be located:

* on the same drive as the selected project;
* at that drive’s root;
* outside the active project folder;
* outside the Project Support folder;
* outside <project>_show_project_to_AI;
* outside first_prompt_files;
* outside second_prompt_files;
* outside source archive staging;
* outside Freeze Memory;
* outside Error Memory;
* outside the application package being archived.

For:

E:\kanda_reasoner

Valid:

E:\kanda_reasoner-Windows-Portable.zip

Invalid:

E:\kanda_reasoner\kanda_reasoner-Windows-Portable.zip

Invalid:

E:\kanda_reasoner_show_project_to_AI\kanda_reasoner-Windows-Portable.zip

Invalid:

E:\kanda_reasoner_show_project_to_AI\second_prompt_files\kanda_reasoner-Windows-Portable.zip

Invalid:

E:\kanda_reasoner\dist\kanda_reasoner-Windows-Portable.zip

Invalid:

E:\kanda_reasoner_delete_after_daily_work\kanda_reasoner-Windows-Portable.zip as the final published artifact

The transient root may be used for build staging, but not as the final published destination.

6. TRANSIENT BUILD STAGING

Build the Portable package in a temporary release workspace outside the active project.

Recommended dynamic staging root:

<DriveRoot><ProjectFolderName>_delete_after_daily_work\portable_build<run-identity>

Example:

E:\kanda_reasoner_delete_after_daily_work\portable_build\20260729_023000

The staging folder may contain:

* copied application files;
* bundled Python runtime;
* dependencies;
* launchers;
* temporary manifests;
* checksums;
* assembly output;
* temporary ZIP output;
* validation logs.

The staging folder must not be:

* the selected project root;
* Project Support;
* the Show Project folder;
* a source archive folder;
* a Freeze Memory folder.

The portable workflow may clean only the transient staging folder it owns.

It must never clean or modify:

* the active project source;
* <project>_show_project_to_AI;
* an existing Portable ZIP without explicit replacement approval;
* unrelated files at the drive root.

7. SOURCE INPUT BOUNDARY

The Portable builder may read required files from the selected project.

It must not write build products back into the project source.

The project source is input-only during Portable assembly, except for changes separately requested and governed as project development.

The Portable workflow must not leave inside ProjectRoot:

* build folders;
* dist folders;
* packaged runtimes;
* dependency caches;
* temporary ZIP files;
* generated executables;
* copied DLL collections;
* portable launchers;
* release manifests;
* installer output.

All generated release material belongs in transient staging or the final drive-root ZIP.

8. SHOW PROJECT CONTAMINATION PREVENTION

Before building, resolve:

ProjectRoot

ProjectSupportRoot: <DriveRoot><ProjectFolderName>_show_project_to_AI

PortableOutput

TransientBuildRoot

Require all four paths to be distinct.

The following conditions must be enforced:

PortableOutput is not inside ProjectRoot.

PortableOutput is not inside ProjectSupportRoot.

TransientBuildRoot is not inside ProjectRoot.

TransientBuildRoot is not inside ProjectSupportRoot.

ProjectSupportRoot is not copied into the Portable package unless a separate explicit product requirement identifies a specific runtime asset inside it.

The default rule is:

DO NOT INCLUDE <project>_show_project_to_AI IN THE PORTABLE DISTRIBUTION.

Project Support contains AI handoff, source reconstruction, Error Memory, and Freeze artifacts. These are development and governance outputs, not normal portable-application runtime content.

9. FILES THAT MUST NOT ENTER THE PORTABLE ZIP

Exclude development and handoff artifacts unless a specific product contract explicitly requires one.

Default exclusions include:

* <project>_show_project_to_AI
* first_prompt_files
* second_prompt_files
* source archive ZIP parts
* PNG reconstruction archive parts
* AI handoff ZIPs
* Error Memory full exports
* compact Error Memory exports
* Freeze Hint intake
* frozen feature handoff exports
* temporary patch staging
* patch bootstrap folders
* previous Portable ZIPs
* release ZIPs
* installer packages
* build caches
* test caches
* virtual environments not used as the governed portable runtime
* .git
* IDE caches
* **pycache**
* temporary logs
* secrets
* API keys
* local credential files
* environment-variable exports
* patient or private user data
* user-specific absolute-path configuration

The portable package must contain only what is required to run the application on the supported target system.

10. SHOW PROJECT MUST NOT BE CALLED

The Portable workflow must not invoke:

* Create First and Second Prompt Files;
* Show Project source archive generation;
* Show Project PNG archive generation;
* AI handoff generation;
* Error Memory export;
* Freeze Memory writing.

Likewise, Show Project must not invoke the Portable builder.

These workflows may inspect the same active project, but they must not call or own each other.

11. PORTABLE BUILD INPUT MANIFEST

Before assembly, create a release-specific input manifest inside transient staging.

The manifest should record:

* selected ProjectRoot;
* resolved DriveRoot;
* canonical project or product name;
* PortableOutput;
* transient build root;
* build timestamp;
* governed Python runtime identity;
* included runtime files;
* excluded development files;
* source commit or source fingerprint when available;
* builder version;
* explicit user-request evidence;
* whether an existing output was present;
* replacement disposition.

Do not place this release manifest inside Show Project.

A sanitized copy may be included inside the Portable package when useful for provenance.

12. EXISTING OUTPUT COLLISION

When the final output already exists:

<DriveRoot><project>-Windows-Portable.zip

Do not silently overwrite it.

Use one of these governed behaviors:

A. Fail closed and ask for explicit replacement approval.

B. Preserve the existing package and create a timestamped candidate only when the user explicitly requested versioned output.

C. Replace it only after explicit user authorization and successful validation of the new candidate.

Default behavior:

EXISTING PORTABLE OUTPUT → FAIL CLOSED

Do not delete the existing ZIP before the new candidate is complete and validated.

13. ATOMIC PUBLICATION

Never write the final ZIP directly as a partially built archive.

Build to a temporary candidate path outside ProjectRoot and Project Support.

Example:

E:\kanda_reasoner_delete_after_daily_work\portable_build<run>\kanda_reasoner-Windows-Portable.zip.partial

After assembly:

1. Validate ZIP integrity.
2. Validate expected root structure.
3. Validate required launcher files.
4. Validate absence of Show Project artifacts.
5. Validate absence of secrets.
6. Calculate SHA-256.
7. Confirm final destination boundary.
8. Publish through an atomic move or replace operation.

Only after all checks pass should the final file appear at:

E:\kanda_reasoner-Windows-Portable.zip

14. ARCHIVE ROOT CONTRACT

The Portable ZIP should have one predictable internal root folder unless the application’s existing portable contract specifies otherwise.

Recommended internal root:

<CanonicalProductName>-Windows-Portable/

Example:

KandaReasoner-Windows-Portable/

The ZIP should not dump hundreds of files directly at archive root unless that structure is already canonical and validated.

Expected general layout:

<project>-Windows-Portable/
launcher
application
runtime
resources
licenses
README
release manifest

Do not include another Portable ZIP inside the Portable ZIP.

Do not include the selected project root as an unnecessary extra parent hierarchy such as:

E/
kanda_reasoner/
...

Do not encode absolute Windows paths into ZIP member names.

15. ZIP PATH SAFETY

Reject ZIP members that:

* begin with /;
* begin with a drive letter;
* contain ../ traversal;
* contain unsafe absolute paths;
* escape the internal portable root;
* duplicate another archive member;
* differ only by unsafe path normalization;
* contain symlink escapes;
* create recursive archive inclusion.

The final Portable ZIP must not contain itself.

16. PORTABLE RUNTIME VALIDATION

Before publication, validate at minimum:

* ZIP opens successfully.
* ZIP CRC passes.
* Expected internal root exists.
* Required launcher exists.
* Required runtime exists.
* Required application entry point exists.
* Required resources exist.
* No duplicate ZIP members exist.
* No unsafe member paths exist.
* No Show Project folder exists inside the ZIP.
* No AI handoff ZIP exists inside the ZIP.
* No source archive parts exist inside the ZIP.
* No previous Portable ZIP exists inside the ZIP.
* No secrets or credentials are included.
* No source-only transient files are included.
* SHA-256 is calculated.
* Final size is reported.

When feasible, extract into a clean temporary folder and run a smoke test using the packaged launcher.

17. REQUIRED BOX-SEPARATION VALIDATION MARKERS

A successful Portable build should report markers equivalent to:

PORTABLE EXPLICIT USER REQUEST: PASS

PORTABLE OWNER SEPARATION: PASS

PORTABLE PROJECT ROOT READ-ONLY: PASS

PORTABLE OUTPUT SAME DRIVE ROOT: PASS

PORTABLE OUTPUT OUTSIDE PROJECT ROOT: PASS

PORTABLE OUTPUT OUTSIDE PROJECT SUPPORT: PASS

PORTABLE TRANSIENT STAGING OUTSIDE PROJECT: PASS

PORTABLE TRANSIENT STAGING OUTSIDE PROJECT SUPPORT: PASS

SHOW PROJECT WORKFLOW NOT INVOKED: PASS

SHOW PROJECT ARTIFACTS EXCLUDED: PASS

PORTABLE SELF-INCLUSION BLOCKED: PASS

PORTABLE ZIP INTEGRITY: PASS

PORTABLE ZIP PATH SAFETY: PASS

PORTABLE REQUIRED RUNTIME: PASS

PORTABLE LAUNCHER SMOKE TEST: PASS

PORTABLE SHA256: <hash>

PORTABLE OUTPUT: <absolute drive-root path>

STATUS: PORTABLE READY

18. REQUIRED NEGATIVE REGRESSION TESTS

A focused validator must prove rejection of these cases:

Portable output under ProjectRoot.

Portable output under <project>_show_project_to_AI.

Portable staging under ProjectRoot.

Portable staging under Project Support.

Show Project exporter invoking the Portable builder.

Portable builder invoking Show Project.

Portable ZIP containing second_prompt_files.

Portable ZIP containing source archive parts.

Portable ZIP containing an existing Portable ZIP.

Portable ZIP containing itself.

Portable build starting without explicit user request.

Silent overwrite of an existing drive-root Portable ZIP.

Unsafe ZIP paths.

Secrets or environment-key files entering the package.

19. DYNAMIC MULTI-PROJECT SUPPORT

The workflow must not be hardcoded only for KANDA Reasoner.

It should resolve dynamically:

E:\kanda_reasoner
→ E:\kanda_reasoner-Windows-Portable.zip

E:\eeg_kanda
→ E:\eeg_kanda-Windows-Portable.zip

D:\ExampleProject
→ D:\ExampleProject-Windows-Portable.zip

The selected Project owns the portable application content.

KANDA Reasoner may provide reusable productization tooling, but must not confuse:

* the Tool project;
* the selected Project;
* the Show Project support folder;
* the Portable Distribution output.

When the selected project is eeg_kanda:

Project source:
E:\eeg_kanda

Tool:
E:\kanda_reasoner

Show Project:
E:\eeg_kanda_show_project_to_AI

Portable output:
E:\eeg_kanda-Windows-Portable.zip

Do not create:

E:\kanda_reasoner-Windows-Portable.zip

unless KANDA Reasoner itself is the explicitly selected project being productized.

20. TOOL VERSUS PROJECT BOUNDARY

The selected active Project determines:

* content to package;
* product identity;
* runtime requirements;
* validation requirements;
* final Portable output name.

KANDA Reasoner as a Tool may provide:

* reusable builder logic;
* path resolution;
* archive safety;
* validation;
* reporting.

The Tool must not become the packaged Project by mistake.

Always show and validate:

Selected ProjectRoot

ToolRoot

ProjectSupportRoot

PortableOutput

TransientBuildRoot

These identities must be printed before the build starts.

21. PRODUCT NAME RESOLUTION

Use this precedence:

1. Explicit project product name from a governed project configuration.
2. Existing canonical portable product-name resolver.
3. Selected project folder leaf.

Do not infer a product name from:

* the Tool folder;
* the Show Project folder;
* a previous unrelated ZIP;
* a display label from another selected project;
* an AI guess.

The final filename must be deterministic.

22. SAME-DRIVE ROOT REQUIREMENT

The Portable output must use the root of the drive containing the selected project.

Resolve it from ProjectRoot.

Examples:

Project:
E:\kanda_reasoner

Portable:
E:\kanda_reasoner-Windows-Portable.zip

Project:
D:\eeg_kanda

Portable:
D:\eeg_kanda-Windows-Portable.zip

Do not redirect to:

* Downloads;
* Desktop;
* the system temporary folder;
* C:\ when the project is on E:;
* Project Support;
* the active project;
* a hardcoded developer-specific folder.

23. PORTABLE BUILD MUST NOT ALTER SHOW PROJECT

Record the state of Project Support before and after the Portable build.

At minimum, confirm:

* no new files created;
* no files modified;
* no files deleted;
* no source parts rebuilt;
* no PNG parts rebuilt;
* no AI handoff ZIP refreshed;
* no collector run started;
* no Freeze intake changed;
* no Error Memory export changed.

A content inventory or hash snapshot may be used for this validation.

Required marker:

SHOW PROJECT SUPPORT UNCHANGED BY PORTABLE BUILD: PASS

24. SHOW PROJECT MUST CONTINUE EXCLUDING PORTABLE OUTPUT

Even though the Portable ZIP is correctly created outside ProjectRoot, the Show Project classifier must retain its portable exclusion rule.

This protects against:

* accidental copying into ProjectRoot;
* a user moving the ZIP;
* a release helper temporarily placing it under source;
* future path mistakes;
* nested Portable contamination.

The two controls are complementary:

Portable builder:
Publishes outside ProjectRoot and Project Support.

Show Project:
Detects and excludes Portable artifacts if misplaced.

25. ERROR MEMORY AND FREEZE

Portable creation must have its own feature identity and validation evidence.

Do not append Portable build evidence to the frozen Show Project feature as though they were one feature.

The existing frozen Show Project rule remains:

Show Project never creates or refreshes <project>-Windows-Portable.zip.

A future Portable builder feature may be frozen separately after:

* explicit user request;
* package implementation;
* local validation;
* smoke testing;
* drive-root publication;
* proof that Show Project remained unchanged.

Do not create a new Error Memory lesson unless an actual new failure occurs and no existing lesson owns it.

26. NO AUTOMATIC PORTABLE REFRESH

After the first Portable build, future source changes must not automatically rebuild it.

A later rebuild requires another explicit user request.

The workflow may report:

A Portable package exists and may be older than current source.

It must not independently decide to refresh it.

27. SAFE CLEANUP

After successful publication, the Portable workflow may remove only:

* its own transient build folder;
* its own temporary candidate ZIP;
* its own temporary logs;
* its own temporary extraction folder.

It must not remove:

* ProjectRoot;
* Project Support;
* Show Project outputs;
* previous Portable packages without approval;
* source archives;
* PNG archives;
* Freeze Memory;
* Error Memory;
* unrelated drive-root files.

Cleanup failures should be reported but must not corrupt the published Portable ZIP.

28. REQUIRED FINAL REPORT

The final result should report:

Selected project: <absolute ProjectRoot>

Tool root:
<absolute ToolRoot or N/A>

Project Support: <absolute ProjectSupportRoot>

Portable product name: <dynamic product name>

Portable output: <absolute DriveRoot path>

Portable ZIP size: <byte count and readable size>

Portable ZIP SHA-256: <hash>

ZIP member count: <count>

Runtime smoke test:
PASS or FAIL

Show Project support unchanged:
PASS or FAIL

Project source unchanged:
PASS or FAIL

Portable explicit-request evidence:
PASS

Final status:
PORTABLE READY or PORTABLE BUILD FAILED

29. FAST DECISION RULE FOR FUTURE AI

Before creating a Portable ZIP, ask internally:

Did the user explicitly request a Portable build?

NO:
Do not build.

YES:
Continue.

What is the selected active ProjectRoot?

Resolve it exactly.

What drive contains the selected project?

Use that drive root.

What is the canonical product name?

Use project configuration or project folder leaf.

Where is Project Support?

Resolve <project>_show_project_to_AI and keep it untouched.

Where should staging occur?

Use the project drive’s governed transient root outside ProjectRoot and Project Support.

Where should final output occur?

<DriveRoot><project>-Windows-Portable.zip

Does an existing output already exist?

Fail closed unless explicit replacement authorization exists.

Did the final package contain Show Project artifacts?

YES:
Reject the build.

Did the build modify Show Project?

YES:
Reject the build and restore only through governed recovery.

Did all validation pass?

YES:
Atomically publish to drive root.

30. NON-NEGOTIABLE SUMMARY

Create Portable distributions only after an explicit user request.

Derive the Portable identity dynamically from the selected active project.

Build outside the active project.

Build outside Project Support.

Publish at the root of the same drive as the selected project.

Never write the final Portable ZIP inside ProjectRoot.

Never write it inside <project>_show_project_to_AI.

Never invoke Show Project during a Portable build.

Never allow Show Project to invoke the Portable builder.

Never package Show Project artifacts into the Portable ZIP.

Never silently overwrite an existing Portable ZIP.

Validate ZIP integrity, runtime, path safety, source immutability, and Show Project immutability before publication.

Portable Distribution and Show Project to AI must remain permanently separate Boxes.
