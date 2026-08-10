this is very important tool versus project, 
we are auditing the project in Active project, 
not kanda_reasoner tool, 
what is happening here is that at moment casually 
kanda_reasoner is tool and project we are updating, 
so take very care not melt project audit to tool audit, 
audit just project with box logic, 
mcard logic (project is the card), brick wall , no leaking logic,
all logic shielded agains other logic boxes.



This is a critical architectural rule, especially because right now the physical paths happen to be identical:

KANDA TOOL:
E:\kanda_reasoner

ACTIVE PROJECT:
E:\kanda_reasoner

That coincidence must never cause the two logical roles to merge.

For the Engineering Audit / Diagnostics work, I will treat this as a self-hosting alias-collision case: same physical root, two completely separate logical identities.

Canonical rule

The audit target is always:

ACTIVE PROJECT

Never:

KANDA TOOL

The KANDA Tool is only the execution substrate that supplies the scanners, GUI, controllers, validators, and public contracts.

Conceptually:

KANDA TOOL
    │
    │ public audit capability
    ▼
ACTIVE PROJECT CARD
    │
    ├── project source
    ├── project configuration
    ├── project Freeze Memory
    ├── project validation evidence
    ├── project Diagnostics history
    └── project AI correction handoff

Not:

KANDA TOOL
    ├── audit itself automatically
    ├── use Tool-private state as Project state
    └── mix Tool and Project evidence
M-card rule

For this workflow, the selected Project is the M-card.

Every Engineering Review run must therefore be bound to an immutable Project-card identity containing at least:

project_identity
project_root
project_support_root
project_generation
project_source_fingerprint
project_configuration_fingerprint

That card travels through:

Complete Engineering Review
→ Diagnostics collection
→ capability coverage
→ correction dossiers
→ AI handoff
→ validation evidence

If the active Project changes while a run is executing:

old result
→ REJECTED AS STALE

It must never silently become evidence for the newly selected Project.

Tool versus Project firewall

For the next implementation I will enforce this exact separation:

TOOL_ROOT
Used only for:
- locating KANDA Python/runtime
- importing KANDA Tool modules
- locating Tool-owned validators
- locating public audit implementations

PROJECT_ROOT
Used only for:
- deciding what source is audited
- source fingerprints
- scope classification
- architecture scanning
- Ruff/BOM/Shadow targets
- Symbol Atlas Project analysis
- Project-specific diagnostics
- Project-specific Freeze lookup
- Project-specific evidence
- AI correction handoff

A scanner must never effectively do:

audit(tool_root)

merely because ToolRoot and ProjectRoot happen to resolve to the same directory today.

It must conceptually do:

audit(active_project_card.project_root)

with ToolRoot only providing the implementation that performs the audit.

No derivation across the wall

These will be prohibited:

derive Project root from Tool root
derive Project support root from Tool state
store Project audit state in Tool-private directories
use Tool Freeze state as Project Freeze state
use Tool identity as Project identity
reuse Tool mutable caches without Project-card binding
reach into another Box's private fields

Even in self-hosting.

The fact that:

ToolPath == ProjectPath

is allowed physically.

The fact that:

ToolRole == ProjectRole

is never allowed logically.

Box Logic

The Boxes remain:

KANDA Tool Runtime Box
    owns audit implementations

Project Selection Box
    owns which Project is active

Engineering Audit Box
    orchestrates Project engineering review

Engineering Diagnostics Box
    owns structured investigation and AI correction dossiers

EngineeringDiagnosticsStore
    owns Project-specific diagnostic persistence

Project Symbol Atlas Box
    owns Project symbol/owner intelligence

Project Freeze Memory Box
    owns Project frozen-feature state

AI Handoff Box
    owns transient Project correction artifact

Communication must be:

Box
→ narrow public immutable contract
→ Box

Never:

Box
→ private mutable state of another Box
Brick Wall requirement

Before a Complete Engineering Review starts, the run should prove something equivalent to:

ACTIVE PROJECT RESOLVED: PASS
PROJECT CARD CREATED: PASS
PROJECT ROOT BOUND: PASS
PROJECT SUPPORT ROOT BOUND: PASS

TOOL ROOT RESOLVED: PASS
TOOL ROLE: EXECUTION_PROVIDER_ONLY

TOOL / PROJECT LOGICAL SEPARATION: PASS

PROJECT AUDIT TARGET:
<selected project>

TOOL AUDIT TARGET:
NONE

PROJECT SELECTION GENERATION CAPTURED: PASS
PROJECT SOURCE FINGERPRINT CAPTURED: PASS
PROJECT CONFIGURATION FINGERPRINT CAPTURED: PASS

CROSS-PROJECT STATE LEAK: 0
TOOL-PRIVATE PROJECT STATE WRITE: 0
WRONG-ROOT WRITE: 0
PRIVATE BOX REACH-IN: 0

And at the end:

AUDITED PROJECT IDENTITY:
<same Project card>

PROJECT CHANGED DURING RUN:
NO

TOOL STATE MUTATED BY PROJECT AUDIT:
NO

OTHER PROJECT STATE MUTATED:
NO

PROJECT FREEZE MEMORY MUTATED:
NO

PROJECT SELECTION REGISTRY MUTATED:
NO
AI correction handoff ownership

The final artifact should also be explicitly Project-bound:

KANDA FULL ENGINEERING DIAGNOSTICS
AI CORRECTION HANDOFF

AUDIT TARGET ROLE:
ACTIVE PROJECT

PROJECT:
<selected project>

PROJECT ROOT:
<active project root>

PROJECT IDENTITY:
...

PROJECT SOURCE FINGERPRINT:
...

KANDA TOOL ROLE:
AUDIT EXECUTION PROVIDER ONLY

TOOL SOURCE INCLUDED AS PROJECT SOURCE:
ONLY IF THAT SOURCE BELONGS TO THE SELECTED PROJECT

That last statement matters enormously in the current self-hosted case.

Today, because the selected Project really is kanda_reasoner, its KANDA source is legitimately Project source.

Tomorrow, if you select:

E:\another_project

the exact same Engineering Review must audit:

E:\another_project

and must not suddenly start auditing E:\kanda_reasoner just because KANDA is the Tool executing the review.

Therefore, for the next correction

I will treat this as a non-negotiable invariant:

Complete Engineering Review
        ↓
ACTIVE PROJECT CARD
        ↓
audit ONLY that Project
        ↓
Project-specific Diagnostics
        ↓
Project-specific Architecture-grade correction dossiers
        ↓
Project-specific AI Correction Handoff

while:

KANDA Tool
= provider of capability
≠ audit target

unless KANDA Reasoner has itself been explicitly selected as the active Project—as happens today.

That distinction will be protected by Brick Wall + Box Logic + M-card + anti-leak + stale-Project rejection, rather than being left implicit because both roots currently happen to be E:\kanda_reasoner.
