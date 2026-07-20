# Prompt Routing Draft — Clean Names v2

This draft uses final intuitive prompt IDs and 12 use-based groups.

## Groups

### Session Start and Navigation (`01_session_start_and_navigation`)
Start a session, load the base stack, and establish AI-human operating context.

- `daily_reasoner_startup_loader` — Daily Reasoner Startup Loader
- `daily_session_start_prompt` — Daily Session Start Prompt
- `daily_startup_loader_template` — Daily Startup Loader Template
- `general_prompt_stack_load_order` — General Prompt Stack Load Order
- `project_startup_canon_template` — Project Startup Canon Template
- `reasoner_startup_canon` — Reasoner Startup Canon
- `session_start_upload_checklist` — Session Start Upload Checklist
- `ai_human_partnership_session_start` — AI-Human Partnership Session Start

### Prompt Routing and Indexing (`02_prompt_routing_and_indexing`)
Map human intent to the correct prompt, route, overlay, or companion stack.

- `project_overlay_selector` — Project Overlay Selector
- `prompt_navigation_index` — Prompt Navigation Index
- `prompt_substitution_map` — Prompt Substitution Map

### Governance, Freeze, and Handoff (`03_governance_freeze_and_handoff`)
Freeze validated work, write handoffs, and preserve governance state.

- `workflow_handoff_template` — End-of-Chat Governance Update Template
- `workflow_handoff_template` — Active Governance Freeze Update
- `professional_engineering_governance_template` — Professional Engineering Governance Template
- `workflow_handoff_template` — Current Workflow Handoff Template
- `workflow_handoff_template` — Reasoner Professional Engineering Governance
- `workflow_handoff_template` — Workflow Handoff Template

### Box Architecture and Boundaries (`04_box_architecture_and_boundaries`)
Declare active box, ownership boundaries, public contracts, and cross-box validation.

- `stateful_control_regression_canon` — Stateful Control Regression Canon
- `box_architecture_canon` — Box Architecture Canon
- `project_folder_organization_canon` — Project Folder Organization Canon

### Patch Delivery and Validation (`05_patch_delivery_and_validation`)
Build installable patches, validate evidence, track patch status, and protect rollback.

- `bundle_gated_development_workflow` — Bundle-Gated Development Workflow
- `implementation_and_delivery_protocol` — Implementation and Delivery Protocol
- `implementation_roadmap_builder` — Implementation Roadmap Builder

### Refactor and Architecture Hardening (`06_refactor_and_architecture_hardening`)
Split large modules, triage architecture, and harden system design.

- `architecture_hardening_triage_protocol` — Architecture Hardening Triage Protocol
- `architecture_hardening_triage_template` — Architecture Hardening Triage Template
- `large_module_refactor_protocol` — Large Module Refactor Protocol
- `large_module_refactor_template` — Large Module Refactor Template

### Prompt Authoring and Audit (`07_prompt_authoring_and_audit`)
Audit, update, generalize, reconcile, and maintain prompt canons.

- `prompt_audit_canon` — Prompt Audit Canon
- `project_specific_prompt_generalization` — Project-Specific Prompt Generalization
- `prompt_canon_reconciliation_protocol` — Prompt Canon Reconciliation Protocol

### Python Engineering Core (`08_python_engineering_core`)
Core Python design, architecture, refactoring, patterns, and engineering judgement.

- `python_clean_architecture` — Python Clean Architecture
- `python_clean_code` — Python Clean Code
- `python_design_patterns` — Python Design Patterns
- `python_domain_driven_design` — Python Domain-Driven Design
- `python_enterprise_architecture` — Python Enterprise Architecture
- `python_high_performance` — Python High Performance
- `python_legacy_code_workflow` — Python Legacy Code Workflow
- `peopleware_team_boundary` — Peopleware Team Boundary
- `practical_field_handbook_template` — Practical Field Handbook Template
- `python_pragmatic_programmer` — Python Pragmatic Programmer
- `python_refactoring` — Python Refactoring
- `software_engineering_books_master` — Software Engineering Books Master

### Python Quality, Security, and Observability (`09_python_quality_security_observability`)
Testing, security, observability, resilience, validation, documentation, and quality gates.

- `tab4_docstring_quality_roadmap` — Tab 4 Docstring Quality Roadmap
- `python_documentation_developer_experience` — Python Documentation and Developer Experience
- `python_observability_logging_metrics_tracing` — Python Observability Logging Metrics and Tracing
- `python_resilience_error_handling` — Python Resilience and Error Handling
- `python_security_threat_prevention` — Python Security and Threat Prevention
- `python_testing_pytest` — Python Testing with Pytest
- `python_validation_serialisation_type_safety` — Python Validation, Serialisation, and Type Safety

### Python API, Data, Async, and Config (`10_python_api_data_async_config`)
APIs, databases, async/distributed design, configuration, and feature flags.

- `python_api_design` — Python API Design
- `python_async_parallel_distributed` — Python Async, Parallel, and Distributed Computing
- `python_configuration_feature_flags` — Python Configuration and Feature Flags
- `python_database_design_optimisation` — Python Database Design and Optimisation

### Productization and Release Readiness (`11_productization_and_release_readiness`)
Productization, infrastructure, lifecycle, deployment, operations, and SRE.

- `professional_ai_assisted_engineering_framework` — Professional AI-Assisted Engineering Framework
- `professional_infrastructure_roadmap` — Professional Infrastructure Roadmap
- `productization_readiness_roadmap` — Productization Readiness Roadmap
- `kubernetes_deployment_operations` — Kubernetes Deployment and Operations
- `python_lifecycle_versioning_deprecation` — Python Lifecycle, Versioning, and Deprecation
- `python_site_reliability_engineering` — Python Site Reliability Engineering

### Generalized Project Canons (`12_generalized_project_canons`)
Reusable architecture canons generalized from project-specific systems.

- `data_transform_pipeline_invariants` — Data Transform Pipeline Invariants
- `desktop_help_document_layout_canon` - Desktop Help Document Layout Canon
- `domain_decision_table_template` — Domain Decision Table Template
- `plugin_package_import_canon` — Plugin Package Import Canon
- `shared_visual_render_engine_canon` — Shared Visual Render Engine Canon
- `transform_resolver_architecture_contract` — Transform Resolver Architecture Contract

Retired routing aliases are resolved through `prompt_substitution_map`; do not add them back to the active list.

## Wave 4B Class 04 active owners

- KPR-04-001 box_architecture_canon
- KPR-04-002 kanda_box_shielding_canon
- KPR-04-003 project_folder_organization_canon
- KPR-04-004 stateful_control_regression_canon
- KPR-04-006 boundary_first_repair_protocol
- KPR-04-007 reserved as a deprecated redirect with no active route.

### `web_ai_large_module_refactor_exchange_protocol`

- Prompt code: `KPR-06-001`
- Load when: an exact Planner package needs bounded external architecture review.
- Do not load for: target-specific AST repair, direct source implementation, delivery mechanics, or freeze writing.
- Companions: `large_module_refactor_protocol`, `web_ai_planning_response_bundle_blueprint`, `brick_wall_comprehensive_quality_gate`.

### `web_ai_planning_response_bundle_blueprint`

- Prompt code: `KPR-06-002`
- Load when: an already-reasoned planning payload must be packaged for Imported Web AI Version intake.
- Do not load for: architecture reasoning, direct source implementation, or final freeze authority.
- Companions: `web_ai_large_module_refactor_exchange_protocol`, current Class 05 delivery owners.

### `web_ai_ast_split_risk_repair_protocol`

- Prompt code: `KPR-06-003`
- Load when: exact target source and current AST evidence require target-specific repair or a SAFE structural split.
- Do not load for: generic Planner review, universal module-size law, or final freeze writing.
- Companions: `large_module_refactor_protocol`, `python_refactoring`, `project_tool_boundary_canon`.

## Wave 8A Class 12 human-process and handbook specialists

### `peopleware_team_boundary` — Peopleware Team Boundary

- **Prompt code:** `KPR-12-007`
- **File:** `ACTIVE_PROMPTS/12_generalized_project_canons/peopleware_team_boundary.md`
- **Load when:** a software-delivery problem may be primarily human, organizational, workload, communication, or collaboration related.
- **Do not load for:** solo code mechanics, medical diagnosis, covert monitoring, personnel ranking, or implementation authorization.
- **Companions:** `prompt_navigation_index`; `project_tool_boundary_canon` when project identity matters.

### `practical_field_handbook_template` — Practical Field Handbook Template

- **Prompt code:** `KPR-12-008`
- **File:** `ACTIVE_PROMPTS/12_generalized_project_canons/practical_field_handbook_template.md`
- **Load when:** a supplied or reliably identified source must become a practical audience-specific handbook.
- **Do not load for:** invented source-faithful detail, substitute reproduction of a copyrighted work, or direct source implementation.
- **Companions:** `prompt_navigation_index`; current evidence sources when current claims require verification.
