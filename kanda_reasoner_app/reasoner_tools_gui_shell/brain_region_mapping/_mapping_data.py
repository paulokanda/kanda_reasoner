# project-path: kanda_reasoner_app/reasoner_tools_gui_shell/brain_region_mapping/_mapping_data.py
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
        "target_tab_label": "Audit Project",
        "analogy_title": "Executive planning and architecture",
        "analogy_text": (
            "The frontal lobe is associated with planning and executive "
            "control, like Audit Project organizes architecture, workflow, "
            "and engineering-safety review in one governed workspace."
        ),
        "tooltip_text": "Frontal lobe -> Audit Project",
        "category": "Core Review",
    },
    {
        "region_id": "broca_area",
        "region_name": "Broca Area (language area)",
        "target_tab_id": "project_qa",
        "target_tab_label": "Local AI",
        "analogy_title": "Language production and clear answers",
        "analogy_text": (
            "Broca Area is associated with expressive language, like Local AI "
            "turns project context into clear explanations, answers, and "
            "implementation guidance."
        ),
        "tooltip_text": "Broca Area -> Local AI",
        "category": "Project Tools",
    },
    {
        "region_id": "parietal_lobe",
        "region_name": "Parietal lobe",
        "target_tab_id": "architecture_review",
        "target_tab_label": "Audit Project",
        "analogy_title": "Integration and workflow coordination",
        "analogy_text": (
            "The parietal lobe integrates information across space and "
            "sensation, like the Workflow Review child tab inside Audit "
            "Project coordinates how project tasks connect and execute."
        ),
        "tooltip_text": "Parietal lobe -> Audit Project > Workflow Review",
        "category": "Core Review",
    },
    {
        "region_id": "brainstem_midbrain",
        "region_name": "Brainstem / Midbrain region",
        "target_tab_id": "architecture_review",
        "target_tab_label": "Audit Project",
        "analogy_title": "Survival layer and safety control",
        "analogy_text": (
            "The brainstem and midbrain protect core survival functions, like "
            "Audit Project groups Architecture Review and Engineering Safety "
            "before fragile changes are made."
        ),
        "tooltip_text": "Brainstem / Midbrain -> Audit Project",
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
        "region_id": "visual_association_cortex",
        "region_name": "Visual association cortex",
        "target_tab_id": "project_structure_3d",
        "target_tab_label": "Project Structure 3D",
        "analogy_title": "Spatial integration and structural mapping",
        "analogy_text": (
            "Visual association cortex integrates visual patterns into a "
            "coherent spatial model, like Project Structure 3D helps the "
            "user understand packages, modules, and relationships as one "
            "interactive read-only map."
        ),
        "tooltip_text": "Visual association cortex -> Project Structure 3D",
        "category": "Project Tools",
    },
    {
        "region_id": "central_sulcus",
        "region_name": "Central sulcus",
        "target_tab_id": "project_web_ai",
        "target_tab_label": "Web AI",
        "analogy_title": "Boundary between project context and web reasoning",
        "analogy_text": (
            "The central sulcus separates major functional cortical areas, "
            "like Web AI preserves a controlled boundary between the "
            "active Project context and external Web AI advice."
        ),
        "tooltip_text": "Central sulcus -> Web AI",
        "category": "Project Tools",
    },
    {
        "region_id": "cerebellum",
        "region_name": "Cerebellum",
        "target_tab_id": "config_web_ai",
        "target_tab_label": "Config AI",
        "analogy_title": "Calibration and coordinated settings",
        "analogy_text": (
            "The cerebellum calibrates and fine-tunes movement, like Config AI "
            "centralizes the gateway, model, endpoint, and credential settings "
            "used by the AI tabs."
        ),
        "tooltip_text": "Cerebellum -> Config AI",
        "category": "Configuration",
    },
    {
        "region_id": "temporal_lobe",
        "region_name": "Temporal lobe",
        "target_tab_id": "project_qa",
        "target_tab_label": "Local AI",
        "analogy_title": "Meaning, memory, and language",
        "analogy_text": (
            "The temporal lobe supports memory, meaning, and language, like "
            "Local AI interprets the project and answers questions about it."
        ),
        "tooltip_text": "Temporal lobe -> Local AI",
        "category": "Project Tools",
    },
    {
        "region_id": "temporal_lobe_error_memory",
        "region_name": "Temporal lobe Error Memory node",
        "target_tab_id": "error_memory",
        "target_tab_label": "Error Memory",
        "analogy_title": "Failure memory and learned prevention",
        "analogy_text": (
            "The temporal lobe supports memory and meaning, like Error Memory "
            "keeps project-specific lessons from failures so repeated mistakes "
            "can be recognized, corrected, and prevented."
        ),
        "tooltip_text": "Temporal lobe Error Memory node -> Error Memory",
        "category": "Project Memory",
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
