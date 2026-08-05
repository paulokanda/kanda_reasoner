Good news: this codebase already computes more than I initially thought — it's just not being presented as a quality signal. Here's what's actually there, and what I'd add.

What already exists (confirmed in the code)
Fan-in/fan-out per node — apply_relationship_counts() in graph_snapshot_primitives.py already populates incoming_count and outgoing_count on every node. Right now this only shows up as plain text in the click-to-inspect side panel (details_presenter.py → browser_details.js). It's never used visually — no node is sized or colored by it. That's a real, computed coupling metric sitting unused.
Test-protection edges — graph_protection_status.py builds validates/protects relationships from web_ai_test_protection_index and Freeze evidence. This means the graph already knows which modules have linked tests and which don't. That's arguably a better "is this well-structured" signal than anything topological — a module with high fan-in and zero validates edges is a genuinely risky spot in the codebase, not just an ugly-looking hub.
Confidence levels on edges (confirmed/derived/inferred/unresolved) — already in the schema. Low-confidence import edges could themselves be a signal of static-analysis ambiguity worth flagging.
What's genuinely absent: cycle detection. I searched the whole package (Python and JS) for "cycle"/"cyclic"/"circular" — nothing. No graph-theoretic cycle check exists anywhere in this pipeline.
Confirmed architecture mismatch, corrected

The tab uses matplotlib + PySide6 (confirmed earlier), but the 3D renderer here is different — web/vendor/3d-force-graph...js shows this visualizer embeds three.js + d3-force + ngraph physics for the actual 3D layout, run inside the QWebEngineView. So the force-directed physics engine (ngraph) is already present as a dependency. That matters because ngraph and d3-force both have straightforward extension points for exactly the kind of analysis we're discussing (node degree already drives some physics behavior in force simulations).

What I'd actually build, in priority order

1. Surface fan-in/fan-out visually — this is nearly free. The data exists; it just needs to reach graph_painter.js/the renderer as node size or color. A node with incoming_count far above the package average is your god-object signal, visible at a glance instead of buried in a side panel you only see after clicking. This is the single highest-value, lowest-effort change.

2. Add cycle detection as a new Python module. Something like graph_cycle_detector.py sitting alongside graph_snapshot_builder.py: run Tarjan's or Johnson's algorithm over the imports/calls edges, tag every node that participates in a cycle with metadata.in_cycle = true, and add a cycle_count to statistics. Cheap to compute (edge count here is capped at _MAX_IMPORT_EDGES = 2400, so this is a small graph by algorithmic standards), and cycles are one of the few structural findings that are almost never a false positive — if A→B→C→A, that's worth a human's attention every time.

3. Cross-reference coupling with test protection. Since validates edges already exist, a derived metric — "modules with incoming_count in the top quartile AND zero incoming validates edges" — would be a genuinely defensible "risk hotspot" list, not a vague aesthetic judgment. This is specific to what this codebase already tracks and wouldn't require new evidence collection, just a join between two things that already exist.

4. A new summary sheet, not just visual encoding. Given the statistics block in the snapshot already reports node_count/edge_count/module_count, I'd add a structure_findings section: cycle count and list, top-N nodes by fan-in, count of low-confidence (inferred/unresolved) edges, and count of untested high-fan-in modules. That turns "look at the pretty graph and judge for yourself" into an actual read-out, while still keeping the 3D view as the way to see where those findings live spatially.

5. What I would not do: invent a single "quality score." Coupling, cycles, and test coverage are different failure modes with different remediation paths — collapsing them into one number would throw away exactly the diagnostic specificity that makes this useful. Keep them as separate, labeled findings tied to concrete graph elements the person can click on.

Want me to write the graph_cycle_detector.py module against this codebase's actual conventions (matching the make_node/make_edge helper style in graph_snapshot_primitives.py), or start with the visual fan-in/fan-out encoding in graph_painter.js since that's the smaller, faster win?

