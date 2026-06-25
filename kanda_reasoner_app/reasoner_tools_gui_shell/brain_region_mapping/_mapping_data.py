"""Private mapping data for the Brain Region Mapping box.

This module intentionally contains data only. It does not import GUI modules,
tab widgets, the main window, or the tab registry. Focused tests compare these
stable tab identifiers with the registry from outside the box boundary.
"""

from __future__ import annotations

from typing import Final

RAW_BRAIN_REGION_TARGETS: Final[tuple[dict[str, str], ...]] = (
    {
        "region_id": "frontal_lobe",
        "region_name": "Frontal lobe",
        "target_tab_id": "architecture_review",
        "target_tab_label": "Architecture Review",
        "analogy_title": "Executive planning and architecture",
        "analogy_text": (
            "The frontal lobe is associated with planning and executive "
            "control, like Architecture Review organizes the project at the "
            "highest structural level."
        ),
        "tooltip_text": "Frontal lobe -> Architecture Review",
        "category": "Core Review",
    },
    {
        "region_id": "broca_area",
        "region_name": "Broca Area (language area)",
        "target_tab_id": "project_qa",
        "target_tab_label": "Project Q&A",
        "analogy_title": "Language production and clear answers",
        "analogy_text": (
            "Broca Area is associated with expressive language, like Project "
            "Q&A turns project context into clear explanations, answers, and "
            "implementation guidance."
        ),
        "tooltip_text": "Broca Area -> Project Q&A",
        "category": "Project Tools",
    },
    {
        "region_id": "parietal_lobe",
        "region_name": "Parietal lobe",
        "target_tab_id": "workflow_review",
        "target_tab_label": "Workflow Review",
        "analogy_title": "Integration and workflow coordination",
        "analogy_text": (
            "The parietal lobe integrates information across space and "
            "sensation, like Workflow Review coordinates how project tasks "
            "connect and execute."
        ),
        "tooltip_text": "Parietal lobe -> Workflow Review",
        "category": "Core Review",
    },
    {
        "region_id": "brainstem_midbrain",
        "region_name": "Brainstem / Midbrain region",
        "target_tab_id": "engineering_safety",
        "target_tab_label": "Engineering Safety",
        "analogy_title": "Survival layer and safety control",
        "analogy_text": (
            "The brainstem and midbrain protect core survival functions, like "
            "Engineering Safety protects the app from unsafe architecture and "
            "implementation mistakes."
        ),
        "tooltip_text": "Brainstem / Midbrain -> Engineering Safety",
        "category": "Core Review",
    },
    {
        "region_id": "cerebellar_folia",
        "region_name": "Cerebellar folia",
        "target_tab_id": "docstring_assistant",
        "target_tab_label": "Docstring Assistant",
        "analogy_title": "Fine detail and precision documentation",
        "analogy_text": (
            "Cerebellar folia are fine folded structures, like Docstring "
            "Assistant works at the fine-detail level of module, class, and "
            "function documentation."
        ),
        "tooltip_text": "Cerebellar folia -> Docstring Assistant",
        "category": "Project Tools",
    },
    {
        "region_id": "occipital_lobe",
        "region_name": "Occipital lobe",
        "target_tab_id": "project_structure_map",
        "target_tab_label": "Show Project to AI",
        "analogy_title": "Seeing the whole project",
        "analogy_text": (
            "The occipital lobe processes vision, like Show Project to AI "
            "helps the user see the project layout and source organization."
        ),
        "tooltip_text": "Occipital lobe -> Show Project to AI",
        "category": "Project Tools",
    },
    {
        "region_id": "central_sulcus",
        "region_name": "Central sulcus",
        "target_tab_id": "project_structure_map",
        "target_tab_label": "Show Project to AI",
        "analogy_title": "Boundary between source and AI handoff",
        "analogy_text": (
            "The central sulcus separates major functional cortical areas, "
            "like Show Project to AI now owns the boundary between source files "
            "and external AI handoff packages."
        ),
        "tooltip_text": "Central sulcus -> Show Project to AI",
        "category": "Project Tools",
    },
    {
        "region_id": "cerebellum",
        "region_name": "Cerebellum",
        "target_tab_id": "refactor_report",
        "target_tab_label": "Refactor Report",
        "analogy_title": "Correction and refinement",
        "analogy_text": (
            "The cerebellum fine-tunes movement and correction, like Refactor "
            "Report fine-tunes project health by identifying what should be "
            "improved."
        ),
        "tooltip_text": "Cerebellum -> Refactor Report",
        "category": "Project Tools",
    },
    {
        "region_id": "temporal_lobe",
        "region_name": "Temporal lobe",
        "target_tab_id": "project_qa",
        "target_tab_label": "Project Q&A",
        "analogy_title": "Meaning, memory, and language",
        "analogy_text": (
            "The temporal lobe supports memory, meaning, and language, like "
            "Project Q&A interprets the project and answers questions about it."
        ),
        "tooltip_text": "Temporal lobe -> Project Q&A",
        "category": "Project Tools",
    },
    {
        "region_id": "hippocampus",
        "region_name": "Hippocampus",
        "target_tab_id": "freeze_feature_after_update",
        "target_tab_label": "Freeze Feature After Update",
        "analogy_title": "Memory consolidation and protected recall",
        "analogy_text": (
            "The hippocampus helps consolidate experiences into durable memory, "
            "like Freeze Feature After Update records validated features into "
            "project-local freeze memory so future AI sessions can remember and "
            "protect them."
        ),
        "tooltip_text": "Hippocampus -> Freeze Feature After Update",
        "category": "Project Memory",
    },
    {
        "region_id": "lateral_sulcus",
        "region_name": "Lateral sulcus / Sylvian fissure",
        "target_tab_id": "exclusion_rules",
        "target_tab_label": "Exclusion Rules",
        "analogy_title": "Functional boundary and separation rules",
        "analogy_text": (
            "The lateral sulcus is a major boundary between cortical regions, "
            "like Exclusion Rules defines what should stay separated from "
            "analysis or packaging."
        ),
        "tooltip_text": "Lateral sulcus -> Exclusion Rules",
        "category": "Configuration",
    },
    {
        "region_id": "longitudinal_fissure",
        "region_name": "Longitudinal fissure",
        "target_tab_id": "prompt_library",
        "target_tab_label": "Prompt Library",
        "analogy_title": "Central organization of knowledge",
        "analogy_text": (
            "The longitudinal fissure organizes the two hemispheres around a "
            "clear central divide, like Prompt Library organizes reusable "
            "prompt knowledge into a structured system."
        ),
        "tooltip_text": "Longitudinal fissure -> Prompt Library",
        "category": "Configuration",
    },
)
