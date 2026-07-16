Updated saved memory
Thought for 5s

Use this as the handoff for next time:

We are continuing the GUI-first roadmap until step 32.
The intention is not to keep growing CLI tooling as the product path. CLI/scripts are only support and testing helpers. The real user path must be through the GUI.

What we intended overall

We are making kanda_reasoner_app better at understanding Python projects by adding and using only two high-value new static-context data families:

packaging_metadata
documentation_intent

These must be:

collected by reasoner_context_collector
written into the main JSON
loaded by project_reasoner_v10
used by retriever/prompt builder
exposed in the GUI

What has already been done

Core static-context wave completed:

added config support for packaging_metadata and documentation_intent
integrated both into collector_main.py
created:
packaging_metadata_parser.py
collector_packaging_metadata.py
documentation_intent_parser.py
collector_documentation_intent.py
updated:
v10_index_loader.py
v10_retriever.py
v10_prompt_builder.py
cleaned import ownership / canonical package paths
created and fixed static-context test suite runner
got the full static-context test suite passing
created real-project smoke + assertion scripts for E:\eeg_kernel_ai_neural_data_analysis
improved documentation parser to avoid junk/cache/generated summary text as project-purpose summary

Recent GUI-first work completed

Step 19 finished:
Created read-only GUI inspector:

project_reasoner_v10\v10_static_context_inspector_widget.py

Step 20 finished:
Created dialog owner that consumes JsonProjectIndex:

project_reasoner_v10\v10_static_context_dialog.py

Step 21 finished:
Integrated the dialog into the real GUI owner:

project_reasoner_v10\v10_main_window.py

This included:

import of StaticContextDialog
creation of self.static_context_button
placement of the button in the Project JSON area
signal wiring
show_static_context_dialog() method

Step 22 finished:
Improved the inspector with a human-friendly Summary tab while preserving raw JSON tabs.

Step 23 mostly finished:
Improved Summary readability and delivered a complete updated module for the inspector.

Current roadmap state

We are starting/continuing step 24.

Step 24 intention:

create a dedicated compact evidence preview for static context
keep Summary and raw JSON tabs unchanged
add an Evidence tab to the inspector
populate it with compact previews of:
packaging files
packaging evidence
documentation files
documentation evidence

What has already been done for step 24

Created:

project_reasoner_v10\v10_static_context_evidence_formatter.py

This formatter already exists and is intended to provide:

build_static_context_evidence_preview(...)

What still needs to be done next

Resume exactly here:

Update:
E:\developer_tools\kanda_reasoner_app\project_reasoner_v10\v10_static_context_inspector_widget.py
Add import:
from .v10_static_context_evidence_formatter import build_static_context_evidence_preview
Add a read-only _evidence_view
Add a new tab:
"Evidence"
In set_static_context(...), populate _evidence_view using:
build_static_context_evidence_preview(packaging_metadata=..., documentation_intent=...)

After step 24 is complete, continue the roadmap like this:

Step 25:
Improve retrieval/readability around the new static-context sections.

Step 26:
Improve prompt interpretation around conflicts between docs/packaging and code truth.

Step 27:
Start profile system work (generic_python, architecture_heavy_python, qt_python).

Step 28:
Continue profile detection/use.

Step 29:
Continue profile-specific enrichment.

Step 30:
Expose profile detection/override in GUI.

Step 31:
Integrate static-context viewing more fully into GUI workflow.

Step 32:
Finish full GUI-first flow:

choose project in GUI
run/load analysis in GUI
inspect static context in GUI
ask AI in GUI using packaging + docs + code

Important constraints to keep

Work step by step
Use the exact format the user requested:
module to create/update
code above implementation
code below implementation
code to implement
final snippet
terminal test
One code change at a time, unless the user explicitly asks for a complete module update
Keep updating the user with:
“Starting step X”
what is being done in that step
“Finish step X”
GUI-first, not CLI-first

Important note

The small fake fixture repos are intentional and should be kept.
They are for deterministic tests.
E:\eeg_kernel_ai_neural_data_analysis is for real-project smoke/integration validation, not a replacement for fixtures.


