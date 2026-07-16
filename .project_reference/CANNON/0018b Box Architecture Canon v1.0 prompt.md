UPDATED BOX ARCHITECTURE HANDOFF FOR NEXT AI

Purpose

This handoff explains the KANDA / PyArchitect architecture discipline called Box Architecture.

Read this before implementing, refactoring, patching, or modifying any feature.

Do not create code yet unless the user explicitly asks to implement after the Box Boundary Audit is clear.

Project context

Project:

KANDA Reasoner / PyArchitect

Common active project root:

E:\kanda_reasoner

The app is a Python / PySide6 desktop application with multiple GUI tabs, workflow validators, architecture validators, prompt-library tooling, engineering safety gates, storage policy tools, future visual navigation, and AI-assisted patch/freeze workflows.

Because the app is growing, every new feature must be created as an isolated logic box. The goal is to prevent code contamination, hidden coupling, circular dependencies, fragile GUI wiring, and unmaintainable spaghetti.

Core definition

Box Architecture is a contract-based modular architecture discipline.

A box is one isolated responsibility area.

Each box owns its own logic, hides its private internals, exposes a public contract, declares its dependencies, and communicates with other boxes only through approved routes.

The user metaphor is a toy house made of blocks:

If one block is removed, disabled, replaced, or refactored, the house may change shape. It may create a door or window. But the whole house should not collapse.

In software terms:

A removed or disabled feature should not crash unrelated features.

Professional equivalents

Box Architecture is the project term.

Professional architecture ideas behind it include:

* Modular Architecture
* Modular Monolith
* Component-Based Architecture
* Encapsulation
* Information Hiding
* Separation of Concerns
* Bounded Contexts
* Ports and Adapters
* Dependency Inversion
* Event-Driven Communication
* Plugin / Microkernel Architecture

Formal subtitle:

Box Architecture
A contract-based modular monolith discipline for isolated, replaceable logic blocks.

Core Law

Before any implementation, the AI must identify the primary box being changed.

No code change may begin until the box boundary is known.

Every implementation must answer:

1. What box owns this responsibility?
2. What files belong to this box?
3. What files are forbidden to touch?
4. What public contract does this box expose?
5. What inputs does this box accept?
6. What outputs does this box produce?
7. What other boxes does it depend on?
8. How does it communicate with other boxes?
9. What happens if this box is disabled or missing?
10. How will this box be validated independently?

If these answers are unclear, implementation must stop and the AI must ask for clarification.

Core box laws

Law 1: One Responsibility

A box owns one responsibility.

Good examples:

* Brain Navigator owns the rotating brain visual index.
* Tab Registry owns tab metadata.
* Navigation Controller owns tab switching by tab_id.
* Remember Box owns explanation-card display.
* Engineering Safety owns safety validation.

Bad example:

Brain Navigator renders the brain, stores prompt text, switches tabs directly, edits settings, and validates architecture.

That is a God Box.

Law 2: Public Contract, Private Internals

A box must expose a small public contract.

Other boxes may only use the public contract.

Private internals must not be imported or modified by other boxes.

Recommended Python convention:

Public:

* contract.py
* api.py
* **init**.py with explicit exports

Private:

* _internal_name.py
* internal/
* _data_loader.py
* _widget_impl.py

Law 3: No Private Reach-In

No box may import or call another box's private file, private method, private attribute, or internal state.

Forbidden:

from brain_navigator._hover_handler import calculate_hover
other_box._private_state = value
main_window.brain_navigator._web_view.setHtml(...)

Allowed:

from brain_navigator.contract import create_brain_navigator_widget

Law 4: Explicit Communication

Boxes must communicate only through approved routes:

* public contract call
* event / signal
* command
* registry
* controller
* mediator
* adapter
* bridge

Forbidden:

* random imports
* shared globals
* hidden mutable state
* direct private access
* tab-index magic
* circular imports

Law 5: State Belongs to One Box

Every piece of mutable state must have exactly one owner box.

Other boxes may request state through the public contract but may not mutate it directly.

Forbidden:

* two boxes writing the same global variable
* one box modifying another box's private list, dict, or model
* registry storing runtime state from many boxes

Law 6: Optional Boxes Need Fallbacks

If a box is optional, disabled, or replaceable, the app must have fallback behavior.

Examples:

* show "Brain Navigator unavailable" placeholder
* return empty mapping
* disable one button
* show simple index instead of animated brain
* skip feature but keep app running

Law 7: Registry Is a Phone Book, Not a Brain

A registry stores metadata, factories, IDs, labels, enabled flags, and contract locations.

A registry must not own business logic, GUI widget state, or behavior.

Good registry fields:

* tab_id
* label
* category
* builder
* enabled
* box_id
* contract path

Bad registry fields:

* live widget pointers
* current business state
* feature-specific logic
* long behavioral callbacks
* mutable cross-box state

Law 8: GUI Boxes Emit Intent

GUI boxes should own widgets, layout, visual behavior, and user interaction.

GUI boxes should not own domain logic.

A GUI box may emit:

* user_clicked_x
* open_tab_requested
* brain_region_hovered
* prompt_selected

A controller box should decide what to do next.

Law 9: Controllers Coordinate, They Do Not Own Domains

A controller receives events or commands and coordinates boxes through contracts.

A controller may:

* receive GUI signals
* call mapping box contract
* call navigation box contract
* update display box contract

A controller may not:

* store all business logic
* directly manipulate unrelated private widgets
* duplicate domain rules from other boxes

Law 10: One Patch Targets One Primary Box

Each implementation patch must name one primary box.

Small supporting touches are allowed only if declared in the Box Boundary Audit.

Allowed supporting touches:

* registry registration
* public contract update
* focused tests
* manifest update
* documentation
* adapter wiring

Forbidden:

* patching multiple unrelated boxes because it is convenient

Box sizes

Use box size to prevent overengineering.

Atom Box

Smallest isolated unit.

Usually:

* one function
* one class
* one file
* pure helper
* no cross-box dependencies

Examples:

* SlugConverter
* SafePathNormalizer
* LabelCleaner
* ColorToken

Requirements:

* docstring
* focused test when logic is nontrivial
* no box_manifest.json required

Module Box

A real feature or logic group.

Usually:

* one folder
* two to five files
* one public interface
* one responsibility
* may have dependencies through contracts

Examples:

* Brain Region Mapping
* Tab Navigation Controller
* Prompt Template Loader
* Source Debris Validator

Requirements:

* public contract
* private internals
* focused tests
* lightweight box_manifest.json recommended

Domain Box

Large feature composed of sub-boxes.

Usually:

* multiple files or folders
* explicit sub-boxes
* complete user-facing capability
* may include GUI, controller, mapping, validation, and resources

Examples:

* Brain Navigator
* Engineering Safety
* Prompt Library
* Architecture Review

Requirements:

* full box_manifest.json
* README
* public contract
* sub-box map
* focused tests
* boundary tests
* fallback behavior
* freeze gate

Box types

Each box must have one primary type.

GUI / View Box

Owns:

* widgets
* layout
* visual state
* user gestures
* Qt signals
* display rendering

Must not:

* own domain logic
* own persistence
* mutate registry
* import other box internals

Controller Box

Owns:

* orchestration
* routing
* user-intent handling
* command handling
* navigation flow

Must not:

* own GUI widgets
* store domain rules
* become a God Box

Registry Box

Owns:

* metadata
* IDs
* enabled flags
* factories
* contract locations
* discovery

Must not:

* store live widget state
* store business state
* perform feature behavior
* mutate unrelated boxes

Data Box

Owns:

* data structures
* mappings
* parsing
* validation
* transformation
* state model

Must not:

* import GUI
* directly call external APIs unless it is also a bridge or service box

Prompt Box

Owns:

* prompt templates
* prompt versions
* prompt composition
* prompt metadata

Must not:

* own GUI behavior
* directly call external AI APIs
* store unrelated app state

Validation Box

Owns:

* validation rules
* pass/fail criteria
* report generation
* test helpers

Must be able to run independently when possible.

Bridge / Adapter Box

Owns:

* external system communication
* file system calls
* OS integration
* API clients
* database access
* QWebEngine bridge
* WebChannel bridge

Must expose a safe public contract and mockable behavior.

Utility Box

Owns:

* pure helper functions
* constants
* formatting
* normalization

Should avoid dependencies on other boxes.

Box lifecycle

Every Module or Domain box should have a lifecycle state.

Draft

Designed or being implemented. Not frozen.

Active

Implemented and usable.

Frozen

Validated locally by the user and accepted as stable.

Deprecated

Still available but scheduled for replacement.

Disabled

Intentionally turned off. App must not crash.

Tombstone

Removed implementation, but historical note remains so future maintainers understand what existed and why it was removed.

Box contract rules

A box contract is the front door.

A contract defines what other boxes may use.

A contract may include:

* public functions
* public classes
* dataclasses
* commands
* events
* signals
* allowed payloads
* return values
* errors
* fallback behavior

A contract must not simply re-export all internals.

Bad contract:

from ._internal_a import *
from ._internal_b import *
from ._private_widget import *

Good contract:

def create_brain_navigator_widget(config: BrainNavigatorConfig) -> QWidget:
"""Create the public Brain Navigator widget."""

Contracts should be small.

When a contract changes incompatibly, the box version or contract version should be updated.

Communication decision tree

Use the smallest safe communication route.

Case 1: Box A needs a synchronous result from Box B

Use direct call through Box B's public contract.

Allowed:

from region_mapping.contract import resolve_region_target
target = resolve_region_target(region_id)

Forbidden:

from region_mapping._mapping_loader import REGION_MAP

Case 2: Box A only announces that something happened

Use event or Qt signal.

Example:

Brain Navigator emits:
brain_region_clicked(region_id)

No reply is expected.

Case 3: Box A requests an action with a result

Use a command.

Example:

open_tab(tab_id) -> bool

Commands should have one clear handler.

Case 4: Box A needs optional discovery

Use a registry.

Example:

registry.is_active("brain_navigator")
registry.get_contract("prompt_library")

Case 5: GUI triggers domain behavior

GUI emits intent.

Controller receives intent.

Controller calls domain contract.

Example:

Brain Navigator View emits brain_region_clicked(region_id)
Brain Navigation Controller receives it
Region Mapping resolves region_id to tab_id
Tab Navigation Controller opens tab_id
Remember Box displays explanation

Case 6: External system is involved

Use a bridge or adapter box.

Example:

GUI Box -> Controller Box -> Bridge Box -> External API/File/OS

GUI must not directly call external systems.

Events versus commands

Event

An event is a one-way notification.

It says:

Something happened.

Examples:

* brain_region_hovered
* brain_region_clicked
* tab_selected
* prompt_template_loaded

Events do not promise a return value.

Command

A command is a request for action.

It says:

Do this and tell me whether it worked.

Examples:

* open_tab(tab_id) -> bool
* load_prompt(prompt_id) -> PromptResult
* run_validation(box_id) -> ValidationResult

Commands should have one responsible handler.

Do not use events when a command is needed.

Do not use commands when a simple event is enough.

Dependency rules

A dependency is allowed only if:

1. it is declared
2. it uses the public contract
3. it does not create a cycle
4. it respects the dependency budget
5. it has fallback behavior if optional

A dependency is forbidden if:

* it imports private internals
* it mutates another box's state
* it creates a circular dependency
* it depends on GUI from a non-GUI box
* it bypasses a controller or bridge
* it assumes optional boxes are always available

Dependency budget guidance:

Atom box:

* prefer zero cross-box dependencies

Module box:

* prefer zero to two cross-box dependencies

Domain box:

* may depend on several boxes, but all must be declared and routed through contracts

If dependency count grows, consider splitting the box or adding a controller / mediator.

State rules

Every mutable state object must have one owner box.

Examples of state:

* selected tab
* current brain region
* selected prompt
* active project root
* validation result
* GUI theme state
* user settings
* runtime cache

Forbidden:

* shared mutable globals
* two boxes writing the same dict
* box A editing box B's private model
* registry storing everything because it is convenient
* hidden singleton state not declared in a contract

Preferred:

* state owned by one model/data box
* state exposed through read-only contract
* mutation through explicit commands
* GUI reflects state but does not own domain rules

Folder structure standards

Do not force a global /boxes folder if the project already has a mature layout.

Boundary clarity matters more than folder name.

Recommended Module Box layout:

box_name/
**init**.py
contract.py
box_manifest.json
README.md
_internal_logic.py
_internal_data.py
tests/
test_contract.py
test_boundary.py
test_contamination.py

Recommended Domain Box layout:

domain_box_name/
**init**.py
contract.py
box_manifest.json
README.md
_controller.py
_view.py
_state.py
sub_boxes/
sub_box_a/
sub_box_b/
tests/
test_contract.py
test_boundary.py
test_contamination.py
test_integration.py

KANDA layout rule:

Fit boxes into the existing source tree instead of creating an unrelated top-level layout.

Example:

kanda_reasoner_app/reasoner_tools_gui_shell/brain_navigator/
kanda_reasoner_app/reasoner_tools_gui_shell/remember_box/
kanda_reasoner_app/reasoner_tools_gui_shell/tab_navigation_controller.py

Box manifest standard

A full manifest is required for Domain boxes and recommended for Module boxes.

Atom boxes do not require a manifest unless they become reused across multiple boxes.

Example manifest:

{
"box_id": "brain_region_mapping",
"box_name": "Brain Region Mapping",
"box_type": "data",
"box_size": "module",
"version": "1.0.0",
"contract_version": "1.0",
"health_state": "draft",
"responsibility": "Maps brain structure IDs to tab IDs and analogy text.",
"owner_paths": [
"kanda_reasoner_app/reasoner_tools_gui_shell/brain_region_mapping/"
],
"public_contract": {
"interface_file": "contract.py",
"provides_functions": [
"resolve_brain_region_target"
],
"emits_events": [],
"accepts_commands": []
},
"private_internals": [
"_mapping_data.py",
"_mapping_loader.py"
],
"allowed_dependencies": [
"tab_registry"
],
"forbidden_dependencies": [
"main_window",
"engineering_safety",
"prompt_library",
"any_gui_box"
],
"communication_route": "direct_call_via_public_contract",
"fallback_behavior": "Unknown region returns a safe empty target object.",
"removal_policy": "optional",
"disable_safe": true,
"validation": {
"focused_tests": [
"tests/test_brain_region_mapping_contract.py"
],
"boundary_tests": [
"tests/test_brain_region_mapping_boundary.py"
]
}
}

Box Boundary Audit

Before writing code, the AI must output this audit.

Implementation must not begin until the human approves or the existing instruction clearly authorizes proceeding.

BOX BOUNDARY AUDIT

Patch target:
Primary box:
Box type:
Box size:
Lifecycle state:

Single responsibility:
Owner paths:
Files expected to change:

Files outside owner paths:
Reason for outside touch:
Allowed supporting touch? YES / NO

Public contract:
Private internals:
Inputs:
Outputs:

Dependencies:
Optional dependencies:
Forbidden dependencies:

Communication route:
Event/command/contract/registry/controller/bridge:

State ownership:
Does this box own mutable state? YES / NO
If YES, where is it stored?
Who may mutate it?

Fallback behavior:
Disable/removal behavior:

Risk of circular dependency:
Risk of registry leakage:
Risk of GUI/domain mixing:
Risk of private reach-in:

Focused tests:
Boundary tests:
Contamination tests:
Manual validation needed:

Freeze condition:

If any answer is unknown, mark it explicitly as unknown and do not invent.

Testing standard

A box is not stable until it can be tested independently.

Contract tests

Test the public contract only.

Do not import private files in contract tests.

If the test cannot use the public contract, the contract is incomplete.

Boundary tests

Test behavior when dependencies are:

* missing
* disabled
* empty
* returning None
* raising controlled errors

Contamination tests

Test that:

* no outside file imports private internals
* no circular dependency exists
* no forbidden dependency is present
* no GUI import appears inside pure data/model boxes
* no registry stores behavioral logic

Integration tests

Use only when validating communication between boxes.

Integration tests do not replace contract tests.

Disable and removal policy

Each Module or Domain box must declare a removal policy.

Required

The app cannot run without this box.

Removal requires migration first.

Optional

The app can run without this box.

Fallback is required.

Replaceable

Another implementation can provide the same contract.

The registry or controller chooses the active implementation.

Disabled behavior

If disabled, the app should:

* skip the feature
* show a placeholder
* return safe default
* disable related buttons
* log a clear reason
* keep unrelated boxes working

Freeze gate

A box or patch may be frozen only after validation.

Freeze requirements:

1. focused tests pass
2. relevant regression tests pass
3. py_compile passes for changed Python files
4. workflow validation passes if relevant
5. architecture validation passes if relevant
6. GUI visual confirmation when GUI is changed
7. no known box-boundary violation remains
8. user validates locally and approves freeze

No freeze without user validation.

Anti-patterns

These patterns are forbidden.

God Box

One box accumulates many unrelated responsibilities.

Invisible Wire

Two boxes communicate through hidden shared state.

Examples:

* mutable global
* hidden singleton
* class variable used by unrelated boxes
* registry used as mutable data dump

Reach-In

A box accesses another box's private internals.

Examples:

* importing _private_module
* calling _private_method
* editing private attributes

Circular Bridge

A mediator or controller hides a dependency cycle.

Leaking Registry

Registry stores live objects, behavior, or runtime state instead of metadata.

Cosmetic Interface

contract.py exists but simply re-exports all internals.

Temporal Coupling

Box A works only if Box B initializes first, but this dependency is undeclared.

GUI-Domain Mixing

A GUI box starts owning business rules or validation logic.

Event Bus Fog

Everything becomes an event, and program flow becomes invisible.

Use events only for notifications. Use commands for request-response.

Box Proliferation

Every tiny helper becomes a formal box, creating paperwork and slowing development.

Avoid formal box overhead for trivial atom helpers.

One-patch / one-primary-box workflow

Each patch must target one primary box.

Patch names should reflect the box.

Examples:

brain_navigator_box_scaffold
brain_region_mapping_contract
tab_navigation_controller_contract
remember_box_display_card

A patch may include supporting changes if declared:

* registry entry
* contract update
* adapter wiring
* focused tests
* documentation
* manifest

A patch must not silently modify unrelated boxes.

Brain Navigator example

Planned feature:

A first GUI tab shows a rotating interactive brain. Hovering a brain region shows a structure name. Clicking a structure opens the corresponding app tab and updates an explanation card.

Correct box split:

Brain Navigator Box

Type:

GUI / View

Owns:

* rotating brain
* hover visuals
* click visuals
* WebEngine wrapper

Does not own:

* tab switching
* tab internals
* prompt text
* validation logic

Outputs:

* brain_region_hovered(region_id)
* brain_region_clicked(region_id)

Brain Region Mapping Box

Type:

Data

Owns:

* brain structure to tab_id mapping
* analogy text

Input:

* region_id

Output:

* target tab_id
* brain structure name
* analogy title
* analogy text

Tab Navigation Controller Box

Type:

Controller

Owns:

* opening a tab by tab_id

Input:

* tab_id

Output:

* success/failure result

Remember Box

Type:

GUI / View

Owns:

* explanation card display

Input:

* brain structure name
* mapped tab label
* analogy text
* action label

Tab Registry Box

Type:

Registry

Owns:

* tab_id
* label
* category
* enabled
* builder
* tab kind

Does not own:

* tab business logic
* live widget state
* brain mapping text

Correct communication:

Brain Navigator emits brain_region_clicked(region_id)
Brain Navigation Controller receives event
Region Mapping resolves region_id to tab_id and analogy
Tab Navigation Controller opens tab_id
Remember Box displays analogy

Forbidden communication:

Brain Navigator directly calls notebook.setCurrentIndex(3)
Brain Navigator imports engineering_safety internals
Brain Navigator stores prompt library data
Tab Registry stores live widget objects and behavior

AI operating protocol

When this canon is loaded, the AI must follow this behavior.

Before implementation:

1. Identify the primary box.
2. Output the Box Boundary Audit.
3. Determine whether the task is one-box or multi-box.
4. State any supporting boxes that must be touched.
5. Ask for missing context if owner paths or contracts are unknown.

During implementation:

1. Patch one primary box.
2. Preserve public contracts unless intentionally changing them.
3. Do not import private internals from other boxes.
4. Avoid creating new cross-box dependencies.
5. Add focused tests.
6. Add boundary tests for optional/replaceable behavior.
7. Run available validation.
8. Deliver one ZIP or one focused output.
9. Wait for user validation.
10. Freeze only after user confirms clean validation.

Minimal Pre-Code Checklist

The AI must answer this before touching code:

1. Primary box:
2. Box type:
3. Box size:
4. Single responsibility:
5. Owner paths:
6. Public contract:
7. Private internals:
8. Inputs:
9. Outputs:
10. Dependencies:
11. Forbidden dependencies:
12. Communication route:
13. State ownership:
14. Fallback behavior:
15. Disable/removal behavior:
16. Tests to add or run:
17. Files outside box, if any:
18. Why outside touch is allowed:
19. Freeze criteria:
20. Human approval:

If the user says "go" after approving this audit, implementation may begin.

Relationship to KANDA patch and freeze discipline

Box Architecture controls source boundaries.

Pre-output contract gates control high-risk emitted artifacts, such as:

* PowerShell install blocks
* validation blocks
* patch delivery instructions
* freeze JSON
* freeze sidecar metadata
* validation evidence

Both must be obeyed.

When patching a box:

1. Identify the primary box.
2. Run Box Boundary Audit.
3. Preserve box boundaries.
4. Apply patch-delivery contract.
5. Validate locally.
6. Freeze only after clean user validation.

Final canon rule

Do not solve a local problem by contaminating another box.

Do not make a feature work by making the architecture weaker.

A good implementation should make the current feature work and make the next feature easier to add.

Final short definition

Box Architecture means building the app as isolated, contract-based logic boxes.

Each box owns one responsibility, exposes a public contract, hides private internals, declares dependencies, communicates through approved routes, validates independently, and can be changed or disabled without breaking unrelated boxes.
