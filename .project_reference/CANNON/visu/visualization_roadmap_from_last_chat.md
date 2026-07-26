Roadmap — Read-Only 3D Project Structure Visualizer

Suggested feature identity:

project-structure-3d-visualizer-v1

The feature should remain a human visualization layer over existing project-analysis data. It should not become a new project scanner, intelligence engine, source-of-truth graph, or editing system.
Phase 1 — Governance and scope

    Define the feature boundary

    The visualizer may:

        display project structure;

        display packages, modules, classes and selected functions;

        display imports, calls, inheritance and validation relationships;

        search, filter, isolate and focus nodes;

        send node-selection events back to PySide6;

        export a screenshot.

    It may not:

        modify source files;

        create imports or relationships;

        move files;

        edit graph nodes;

        persist user changes to project architecture;

        execute shell commands;

        invoke Apply;

        modify Error Memory or Freeze Memory;

        treat JavaScript as filesystem authority.

    Audit frozen protected paths

    Before implementation, inspect the active Project frozen-feature memory.

    The visualizer should avoid modifying protected retrieval, Local AI, Project Web AI, Apply, Error Memory and Freeze owners unless strictly necessary.

    Choose the canonical data source

    Reuse existing KANDA project-analysis outputs where possible:

        files;

        packages;

        symbols;

        imports;

        call relationships;

        validation coverage;

        frozen/protected status;

        architecture boxes;

        project boundaries.

    Do not build a second scanner merely for the visualizer.

    Define the first release scope

    Version 1 should visualize:

        project;

        packages;

        Python modules;

        classes;

        important functions;

        imports;

        inheritance;

        selected call relationships;

        validators;

        frozen/protected files.

    Avoid adding every local variable, method call and generated artifact in the first release.

Phase 2 — User experience design

    Choose the main layout

    Recommended PySide6 page structure:

┌──────────────────────────────────────────────────────────────┐
│ Project Structure 3D                                        │
├─────────────────┬──────────────────────────────┬─────────────┤
│ Controls        │                              │ Details     │
│                 │       3D graph viewport      │             │
│ Search          │                              │ Node info   │
│ View mode       │                              │ Relations   │
│ Filters         │                              │ Path        │
│ Legend          │                              │ Status      │
│                 │                              │             │
├─────────────────┴──────────────────────────────┴─────────────┤
│ Status / node count / active filters / selected project      │
└──────────────────────────────────────────────────────────────┘

    Create three visualization modes

    Architecture mode

    Show:

        Project root;

        major packages;

        major subsystems;

        external dependencies;

        architectural boxes.

    Structure mode

    Show:

        packages;

        modules;

        classes;

        selected public functions.

    Focus mode

    Show only:

        selected node;

        direct parents and children;

        imports;

        callers;

        callees;

        validators;

        frozen/protected relationships.

    Define the visual language

    Suggested node shapes:

        Project: large translucent boundary;

        package: translucent box or clustered shell;

        module: rounded cube;

        class: hexagonal node;

        function: sphere;

        validator: outlined diamond;

        external dependency: desaturated sphere;

        frozen file: gold halo;

        selected node: bright outline and subtle bloom.

    Define color semantics

    Use one stable color meaning:

        blue: core/runtime;

        purple: AI-related;

        orange: user interface;

        green: validation and safety;

        yellow: retrieval and evidence;

        cyan: selected Project;

        red: error, risk or forbidden dependency;

        gray: external dependency;

        gold: frozen or protected.

    Define edge semantics

        import: thin solid edge;

        function call: curved edge;

        inheritance: directional bright edge;

        GUI invocation: orange edge;

        data flow: animated particles when selected;

        validation coverage: green dashed edge;

        frozen protection: gold outline or relationship;

        external dependency: gray low-opacity edge.

    Design navigation interactions

Required interactions:

    mouse wheel zoom;

    orbit with drag;

    pan;

    hover tooltip;

    click node;

    double-click to focus;

    click empty space to clear selection;

    keyboard Escape to leave focus mode;

    search and center;

    fit graph;

    reset camera;

    return to overview.

Phase 3 — Graph data contract

    Create one immutable graph snapshot schema

Suggested top-level structure:

schema_version
project_identity
generated_at
source_provenance
nodes
edges
clusters
legend
layout
statistics

    Define the node contract

Each node should contain:

id
label
kind
relative_path
qualified_name
package
parent_id
category
size_metric
complexity_metric
incoming_count
outgoing_count
frozen
protected
external
risk_level
summary
position
metadata

    Define the edge contract

Each edge should contain:

id
source
target
relationship
directed
weight
label
evidence
validation_status
metadata

    Use stable identifiers

Node IDs must remain stable between runs.

Recommended identity patterns:

project:<project-slug>
package:<relative-package>
module:<relative-file-path>
class:<relative-file-path>:<qualified-class>
function:<relative-file-path>:<qualified-function>
external:<dependency-name>

    Include provenance

Each relationship should identify its source:

    source inspection;

    Symbol Atlas;

    import analysis;

    call-site analysis;

    architecture review;

    validation evidence;

    frozen-feature memory.

The renderer should never imply that an inferred edge is certain when its evidence is weak.

    Define relation confidence

Suggested values:

confirmed
derived
inferred
documentation_only
unresolved

Use opacity or edge style to distinguish confidence.
Phase 4 — Python graph snapshot builder

    Create a dedicated read-only graph snapshot owner

Suggested responsibility:

project_structure_visualizer/
    graph_snapshot_builder.py
    graph_schema.py
    graph_filters.py
    graph_layout_cache.py

This owner should consume existing KANDA outputs and produce renderer-ready JSON.

    Do not rescan project source unnecessarily

Preferred flow:

Existing project analysis
        ↓
Canonical graph snapshot builder
        ↓
Immutable graph JSON
        ↓
3D renderer

Direct source inspection should only fill demonstrated gaps that existing analysis cannot provide.

    Normalize packages and modules

The builder should:

    map files to packages;

    create parent-child hierarchy;

    avoid duplicate package nodes;

    exclude generated evidence and temporary folders;

    exclude .project_reference, archives, oldies and backups;

    separate external dependencies from Project-owned files.

    Select important functions

Do not show every function initially.

Possible inclusion criteria:

    public function;

    entry-point function;

    high incoming-call count;

    high outgoing-call count;

    validator target;

    architecture owner;

    frozen protected function;

    selected search result.

    Create graph-density limits

Establish hard bounds, for example:

Architecture mode: 100–300 nodes
Structure mode: 500–1,500 nodes
Focused mode: 20–200 nodes
Absolute render ceiling: configurable

Large Projects should open at package/module level rather than trying to render all symbols.

    Add graph statistics

Compute:

    total nodes;

    total edges;

    package count;

    module count;

    class count;

    function count;

    isolated nodes;

    strongly connected groups;

    external dependency count;

    protected-node count.

Phase 5 — Stable 3D layout

    Generate the first layout in JavaScript

Let 3d-force-graph generate the initial positions using:

    charge force;

    link distance;

    collision force;

    package-cluster attraction;

    category-region attraction.

    Create semantic spatial regions

Give major categories preferred regions:

Core/runtime        center
GUI                 upper-left
AI/reasoner         upper-right
Validation          lower-right
Evidence/retrieval  lower-left
External systems    outer orbit

    Freeze positions after stabilization

Once the simulation cools:

    capture node coordinates;

    send coordinates to Python;

    store them in a generated visualization cache;

    reuse them next time.

The cache is a visualization artifact, not architectural truth.

    Use deterministic layout seeds

The same unchanged project should reopen with substantially the same map.

This is essential for user familiarity.

    Handle graph changes incrementally

When new nodes appear:

    preserve known node coordinates;

    place new nodes near their package or parent;

    run a short localized simulation;

    avoid reorganizing the whole project.

    Provide a “Recalculate layout” action

This should be explicit and separate from normal opening.

The button may clear only the generated visualization-coordinate cache.
Phase 6 — Local web renderer

    Bundle all JavaScript locally

Bundle pinned versions of:

    Three.js;

    3d-force-graph;

    required controls;

    local renderer JavaScript;

    local renderer CSS.

Do not depend on a CDN during normal operation.

    Create a minimal local HTML shell

Suggested files:

project_structure_visualizer/web/
    index.html
    graph_renderer.js
    graph_theme.css
    vendor/
        three.min.js
        3d-force-graph.min.js

    Build the graph renderer

Renderer responsibilities:

    accept immutable graph JSON;

    create node objects;

    create edge objects;

    apply colors and shapes;

    handle camera controls;

    show tooltips;

    highlight selection;

    isolate paths;

    update filters;

    emit selection events to Python.

    Create custom node geometry

Use Three.js geometries:

    cube or rounded box for files;

    sphere for functions;

    octahedron or hexagonal form for classes;

    translucent box for packages;

    ring or halo for frozen nodes.

    Add restrained visual effects

Recommended:

    mild bloom on selected node;

    soft fog;

    subtle background gradient;

    low-opacity package boundaries;

    directional particles only for active paths;

    antialiasing;

    smooth camera interpolation.

Avoid constant particle animation across every edge.

    Add level-of-detail behavior

Depending on camera distance:

    far: package labels only;

    medium: module labels;

    close: class and function labels;

    selected: always show label.

    Add collision prevention

Use collision forces or bounding radii so:

    boxes do not overlap;

    large package clusters remain readable;

    labels are not embedded inside nodes.

Phase 7 — PySide6 integration

    Create the visualizer widget

Suggested owner:

ProjectStructure3DWidget

It should contain:

    toolbar;

    left filter panel;

    QWebEngineView;

    right details panel;

    bottom status bar.

    Create a dedicated controller

Suggested responsibilities:

ProjectStructure3DController

It should:

    resolve selected Project identity;

    request a graph snapshot;

    validate snapshot schema;

    load graph into the web view;

    manage search and filters;

    receive selected-node events;

    populate the details panel;

    control camera commands;

    manage graph-cache lifecycle.

    Use QWebChannel for narrow communication

Expose only explicit slots, for example:

on_node_selected(node_id)
on_edge_selected(edge_id)
on_background_selected()
on_layout_stabilized(position_snapshot)
on_renderer_ready()
on_renderer_error(message)

    Do not expose generic Python objects

Do not expose:

    filesystem objects;

    shell helpers;

    project writers;

    Apply controllers;

    validation controllers;

    Error Memory;

    Freeze writers;

    credential stores.

    Validate every JavaScript-originated ID

Python must verify that:

    node ID exists in the active graph snapshot;

    edge ID exists;

    the selected Project identity has not changed;

    the graph generation is still current.

    Add stale-generation protection

Every graph load should receive a unique generation ID.

Events from an obsolete web page or previous Project must become safe no-ops.

    Handle Project switching

On selected Project change:

    invalidate current snapshot;

    clear node details;

    clear graph search;

    cancel pending generation;

    load the new Project snapshot;

    reject late events from the previous graph.

Phase 8 — Controls and exploration features

    Implement search

Search should support:

    filename;

    package;

    class;

    function;

    relative path;

    architecture box;

    frozen feature;

    external dependency.

    Implement relationship filters

Toggle:

    imports;

    calls;

    inheritance;

    GUI invocations;

    validation coverage;

    frozen/protected relationships;

    external dependencies.

    Implement node-type filters

Toggle:

    packages;

    modules;

    classes;

    functions;

    validators;

    external dependencies.

    Implement isolate selected

Show only:

    selected node;

    direct neighbors;

    optional depth 1–3;

    relationship types chosen by the user.

    Implement dependency-path display

User selects:

    source node;

    target node;

    relationship types.

KANDA displays a read-only path between them when available.

    Implement package expand and collapse

Default:

    packages collapsed in Architecture mode;

    modules revealed on package selection;

    symbols revealed only on explicit expansion.

    Implement focus history

Add:

    Back;

    Forward;

    Overview.

This should behave like visual navigation history, not graph editing.

    Implement details sidebar

Display:

    node name;

    type;

    relative path;

    parent package;

    summary;

    incoming relationship count;

    outgoing relationship count;

    validators;

    frozen/protected status;

    architecture box;

    source provenance.

    Add a legend panel

The legend should explain:

    node shapes;

    colors;

    edge styles;

    confidence levels;

    frozen/protected markers.

Phase 9 — Performance and responsiveness

    Build snapshots outside the GUI thread

Project analysis and graph assembly should run in a worker thread.

PySide6 GUI updates must remain on the GUI thread.

    Add cancellation

Cancel graph generation when:

    Project changes;

    page closes;

    user requests refresh;

    a newer graph request supersedes the current one.

    Cache generated snapshots

Cache key should include:

Project identity
Project source fingerprint
Graph schema version
Filter/profile version
Layout version

    Use progressive loading

Recommended sequence:

    display packages;

    display modules;

    display relationships;

    progressively reveal detailed symbols.

    Throttle expensive interactions

Throttle:

    hover events;

    camera-position updates;

    layout-position snapshots;

    resize events;

    rapid filter changes.

    Add renderer health diagnostics

Record without sensitive content:

    renderer initialized;

    snapshot node count;

    snapshot edge count;

    load duration;

    layout duration;

    WebGL availability;

    JavaScript errors;

    stale event rejection.

Phase 10 — Safety and trust boundaries

    Keep graph data immutable in JavaScript

JavaScript may maintain temporary visual state, but Python remains the owner of the graph snapshot.

    Block external navigation

The embedded browser should reject:

    arbitrary HTTP navigation;

    external links;

    file URLs outside bundled assets;

    popup windows;

    downloads.

    Use local assets only

Normal operation must not require internet access.

    Block JavaScript filesystem access

The page should receive graph JSON through controlled injection or QWebChannel, never through unrestricted file browsing.

    Sanitize labels and metadata

Escape:

    HTML;

    JavaScript strings;

    filenames;

    summaries;

    tooltip content.

    Respect Tool versus Project boundaries

The graph must clearly distinguish:

    reusable Tool-owned modules;

    selected Project-owned modules;

    external Project Support artifacts;

    generated visualization artifacts.

    Exclude secrets and unsupported files

Never send to the renderer:

    API keys;

    .env contents;

    credential files;

    raw patient data;

    binary file content;

    unredacted sensitive logs.

Phase 11 — Validation strategy

    Create schema validation tests

Validate:

    unique node IDs;

    unique edge IDs;

    all edge endpoints exist;

    valid relationship types;

    valid node types;

    valid project identity;

    no forbidden absolute paths;

    no external Support source leakage.

    Create snapshot-builder tests

Test:

    packages;

    files;

    classes;

    functions;

    imports;

    inheritance;

    validators;

    frozen nodes;

    exclusions;

    deterministic ordering.

    Create renderer contract tests

Test:

    graph loads;

    node count matches;

    edge count matches;

    node selection event;

    background selection;

    filter application;

    focus mode;

    layout stabilization;

    renderer error reporting.

    Create real Qt tests

Instantiate the real PySide6 page and verify:

    QWebEngineView loads;

    controls are visible;

    graph-ready signal arrives;

    Project switching rejects stale events;

    page destruction does not trigger deleted-widget callbacks;

    GUI remains responsive during graph creation.

    Create safety tests

Prove:

    no write API;

    no shell API;

    no Apply authority;

    no external URL loading;

    no Project Support source ingestion;

    no .project_reference archive ingestion;

    no credentials in graph JSON;

    no absolute path leakage unless explicitly approved.

    Create visual regression fixtures

Maintain small deterministic test projects:

    simple package tree;

    circular imports;

    inheritance hierarchy;

    validation relationships;

    frozen nodes;

    external dependencies;

    large graph stress fixture.

    Create performance acceptance tests

Suggested targets:

300 nodes / 600 edges: instant interactive load
1,000 nodes / 3,000 edges: smooth interaction
3,000 nodes: progressive or clustered mode required
GUI thread blocking: unacceptable

Phase 12 — Delivery sequence

    Deliver v1A: static architecture prototype

Include:

    local HTML renderer;

    hardcoded fixture graph;

    camera controls;

    node colors and shapes;

    PySide6 embedding;

    node-selection callback.

No live Project data yet.

    Deliver v1B: real read-only snapshot

Add:

    existing Project data ingestion;

    packages;

    modules;

    imports;

    details panel;

    search;

    filters.

    Deliver v1C: semantic relationships

Add:

    classes;

    selected functions;

    inheritance;

    calls;

    validators;

    frozen/protected status.

    Deliver v1D: stable layout and focus paths

Add:

    position caching;

    semantic zones;

    isolate selected;

    dependency path;

    expand/collapse;

    navigation history.

    Deliver v1E: polish and optimization

Add:

    bloom;

    fog;

    refined typography;

    adaptive labels;

    animations;

    screenshot export;

    large-graph safeguards;

    accessibility settings.

Phase 13 — Acceptance criteria

    Functional acceptance

The user can:

    open the 3D graph;

    understand major project areas;

    orbit and zoom smoothly;

    search for a file or symbol;

    click it;

    see its relationships;

    isolate its neighborhood;

    return to overview;

    identify frozen and validated areas.

    Read-only acceptance

The feature cannot:

    edit graph structure;

    modify source;

    run shell commands;

    invoke Apply;

    write Error Memory;

    write Freeze Memory;

    modify architectural relationships.

    Visual acceptance

The graph should:

    avoid immediate hairball appearance;

    have stable positions;

    use understandable colors;

    use restrained animation;

    preserve readable labels;

    distinguish packages, files, classes and functions;

    remain attractive in both overview and focus modes.

    Performance acceptance

    GUI remains responsive;

    Project switching is safe;

    renderer failures are contained;

    large Projects automatically begin at a higher abstraction level;

    loading a graph does not require internet access.

    Governance acceptance

    no frozen protected behavior is regressed;

    existing analysis remains canonical;

    the visualizer is a consumer, not a competing source of truth;

    validation evidence passes;

    live PySide6 test passes;

    Freeze Preview is reviewed;

    final Freeze requires explicit human Confirm and Write.

Recommended first implementation slice

The safest first patch should include only:

New read-only Project Structure 3D page
Local QWebEngineView renderer
Locally bundled 3d-force-graph assets
Fixture graph
Orbit, zoom and pan
Node selection
PySide6 details panel
No live analyzer integration yet
No layout persistence yet
No advanced relationships
No modifications to existing intelligence engines

That proves the visual approach and interaction quality before coupling it to KANDA’s real project-analysis data.
