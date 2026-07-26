# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/__init__.py
"""Large File Refactor Planner support package for Architecture Review."""
from __future__ import annotations

from .ast_analysis import analyze_python_file
from .candidate_discovery import discover_candidates
from .docstring_planner import build_docstring_proposals
from .llm_arbitration import arbitrate_symbol_assignment, build_llm_arbitration_request
from .preview_writer import build_preview_bundle, validate_preview_bundle, write_preview_files
from .patch_zip_gate import build_patch_zip_creation_gate
from .project_patch_payload import create_project_patch_payload_zip
from .payload_apply_gate import build_payload_apply_gate, write_payload_apply_gate_manifest
from .import_rewrite_application_gate import (
    build_import_rewrite_application_gate,
    write_import_rewrite_application_gate_manifest,
)
from .human_confirmed_import_rewrite_contract import (
    build_human_confirmed_import_rewrite_contract,
    write_human_confirmed_import_rewrite_contract_manifest,
)
from .human_confirmed_apply_contract import (
    build_human_confirmed_apply_contract,
    write_human_confirmed_apply_contract_manifest,
)
from .final_guarded_source_apply_planning import (
    build_final_guarded_source_apply_plan,
    write_final_guarded_source_apply_plan_manifest,
)
from .source_apply_dry_run_validator import (
    build_source_apply_dry_run_validation,
    write_source_apply_dry_run_validation_manifest,
)
from .source_apply_preflight_backup_contract import (
    build_source_apply_preflight_backup_contract,
    write_source_apply_preflight_backup_contract_manifest,
)
from .guarded_source_apply_executor import (
    GUARDED_SOURCE_APPLY_EXECUTOR_TOKEN,
    build_guarded_source_apply_execution,
    write_guarded_source_apply_execution_manifest,
)
from .post_apply_validation import (
    POST_APPLY_VALIDATION_TOKEN,
    build_post_apply_validation,
    write_post_apply_validation_manifest,
)
from .source_apply_rollback_recovery import (
    SOURCE_APPLY_ROLLBACK_RECOVERY_TOKEN,
    build_source_apply_rollback_recovery,
    write_source_apply_rollback_recovery_manifest,
)
from .source_apply_multifile_recovery_evidence import (
    SOURCE_APPLY_MULTIFILE_RECOVERY_EVIDENCE_TOKEN,
    build_source_apply_multifile_recovery_evidence,
    write_source_apply_multifile_recovery_evidence_manifest,
)
from .models import FEATURE_ID, PlannerState
from .source_encoding_profile import build_source_encoding_profile
from .symbol_dependency_builder import build_symbol_dependency_report
from .workbench_dependency_readiness import build_workbench_dependency_readiness
from .workbench_plan_snapshot import (
    WorkbenchPlanSnapshot,
    build_workbench_plan_snapshot,
    load_workbench_plan_snapshot,
    write_workbench_plan_snapshot,
)
from .workbench_execution_basis import (
    build_workbench_execution_basis_set,
    execution_basis_is_fresh,
)
from .workbench_execution_feasibility import (
    evaluate_workbench_execution_feasibility,
)
from .workbench_refactor_baseline import (
    BehaviorBaselineEvidence,
    RefactorBaseline,
    build_refactor_baseline,
)
from .workbench_execution_contract import (
    WorkbenchExecutionContract,
    build_workbench_execution_contract,
    execution_contract_integrity_valid,
)
from .workbench_transaction_store import (
    WorkbenchTransactionStore,
    default_workbench_transaction_root,
)
from .workbench_refactor_transaction import (
    WorkbenchRefactorTransaction,
    detect_self_hosted_refactor,
    discover_workbench_recovery_pending,
    mark_workbench_transaction_recovery_pending,
    prepare_workbench_refactor_transaction,
    reserve_workbench_project_lane,
)

from .workbench_dynamic_python_risks import (
    DynamicPythonRiskReport,
    analyze_dynamic_python_risks,
)
from .workbench_transformation_recipe import (
    TransformationRecipe,
    build_transformation_recipe,
    transformation_recipe_integrity_valid,
)
from .workbench_sealed_payload import (
    WorkbenchSealedPayload,
    build_and_write_sealed_payload,
    verify_sealed_payload,
)
from .workbench_shadow_backend import (
    ControlledMirrorBackend,
    GitWorktreeBackend,
    choose_shadow_backend,
)
from .workbench_shadow_provenance import (
    ShadowProvenanceResult,
    prove_shadow_runtime_provenance,
)
from .workbench_shadow_validation import (
    ShadowValidationResult,
    validate_shadow_refactor,
)
from .workbench_journaled_apply_models import (
    JournaledApplyAuthorization,
    JournaledApplyResult,
    build_journaled_apply_authorization,
)
from .workbench_journaled_apply_executor import (
    execute_journaled_refactor_apply,
    resume_journaled_refactor_apply,
    finalize_journaled_refactor_transaction,
)
from .workbench_transaction_rollback import (
    JournaledRollbackResult,
    rollback_journaled_refactor_transaction,
)
from .workbench_refactor_receipt import (
    RefactorReceipt,
    build_and_write_refactor_receipt,
)
from .workbench_patch5_executor_proof import (
    ExecutorProofEvidence,
    find_patch5_executor_proof,
)

from .workbench_completion_review import (
    RefactorLargeModuleGate,
    SemanticDiffReview,
    TransactionSummary,
    WarningAcknowledgment,
    evaluate_refactor_large_module_gate,
)
from .workbench_completion_workflow import (
    CompletionEvidenceBundle,
    CompletionTransactionBundle,
    prepare_completion_evidence,
    prepare_completion_transaction,
    refresh_completion_review_state,
)

from .cst_real_preview_writer import build_and_write_real_preview
from .cst_docstring_inserter import insert_missing_docstrings_for_preview_blocks
from .cst_transform_fidelity import build_cst_transform_fidelity_report
from .helper_import_synthesizer import synthesize_helper_imports
from .real_preview_structural_validator import validate_real_preview_structure
from .workbench_preflight_backup_readiness import build_and_write_preflight_backup_readiness
from .workbench_source_payload_builder import build_and_write_source_apply_payload
from .workbench_guarded_source_apply import (
    execute_guarded_source_apply,
    expected_guarded_apply_token,
)
from .workbench_post_apply_validator import validate_and_write_post_apply
from .workbench_rollback_executor import (
    execute_workbench_rollback,
    expected_workbench_rollback_token,
)
from .workbench_behavior_validation import run_workbench_behavior_validation

from .workbench_import_rewrite_apply_readiness import (
    build_and_write_import_rewrite_apply_readiness,
    expected_import_rewrite_apply_token,
)

from .workbench_import_rewrite_apply_executor import (
    execute_guarded_import_rewrite_apply,
    expected_guarded_import_rewrite_apply_token,
    validate_import_rewrite_post_apply,
)
from .dependency_clusterer import build_dependency_clusters
from .split_planner import build_split_plan

from .workbench_import_rewrite_rollback_executor import (
    execute_import_rewrite_rollback,
    expected_import_rewrite_rollback_token,
)


from .advanced_import_rewrite_support import (
    build_advanced_import_rewrite_support,
    write_advanced_import_rewrite_support,
)

from .workbench_final_integration_hardening import (
    build_final_integration_hardening_report,
    write_final_integration_hardening_report,
)

from .batch_refactor_queue import (
    build_batch_refactor_queue,
    write_batch_refactor_queue,
)

from .visual_diff_ui import (
    build_visual_diff_report,
    write_visual_diff_artifacts,
)

from .behavior_test_presets import (
    build_behavior_test_presets,
    write_behavior_test_presets,
)

from .final_complete_workbench_freeze import (
    build_complete_workbench_freeze_report,
    write_complete_workbench_freeze_report,
)

__all__ = [
    "FEATURE_ID",
    "PlannerState",
    "analyze_python_file",
    "build_docstring_proposals",
    "build_llm_arbitration_request",
    "arbitrate_symbol_assignment",
    "build_preview_bundle",
    "validate_preview_bundle",
    "write_preview_files",
    "build_patch_zip_creation_gate",
    "create_project_patch_payload_zip",
    "build_payload_apply_gate",
    "write_payload_apply_gate_manifest",
    "build_import_rewrite_application_gate",
    "write_import_rewrite_application_gate_manifest",
    "build_human_confirmed_import_rewrite_contract",
    "write_human_confirmed_import_rewrite_contract_manifest",
    "build_human_confirmed_apply_contract",
    "write_human_confirmed_apply_contract_manifest",
    "build_final_guarded_source_apply_plan",
    "write_final_guarded_source_apply_plan_manifest",
    "build_source_apply_dry_run_validation",
    "write_source_apply_dry_run_validation_manifest",
    "build_source_apply_preflight_backup_contract",
    "write_source_apply_preflight_backup_contract_manifest",
    "GUARDED_SOURCE_APPLY_EXECUTOR_TOKEN",
    "build_guarded_source_apply_execution",
    "write_guarded_source_apply_execution_manifest",
    "POST_APPLY_VALIDATION_TOKEN",
    "build_post_apply_validation",
    "write_post_apply_validation_manifest",
    "SOURCE_APPLY_ROLLBACK_RECOVERY_TOKEN",
    "build_source_apply_rollback_recovery",
    "write_source_apply_rollback_recovery_manifest",
    "SOURCE_APPLY_MULTIFILE_RECOVERY_EVIDENCE_TOKEN",
    "build_source_apply_multifile_recovery_evidence",
    "write_source_apply_multifile_recovery_evidence_manifest",
    "build_source_encoding_profile",
    "build_symbol_dependency_report",
    "build_workbench_dependency_readiness",
    "WorkbenchPlanSnapshot",
    "build_workbench_plan_snapshot",
    "load_workbench_plan_snapshot",
    "write_workbench_plan_snapshot",
    "build_workbench_execution_basis_set",
    "execution_basis_is_fresh",
    "evaluate_workbench_execution_feasibility",
    "BehaviorBaselineEvidence",
    "RefactorBaseline",
    "build_refactor_baseline",
    "WorkbenchExecutionContract",
    "build_workbench_execution_contract",
    "execution_contract_integrity_valid",
    "WorkbenchTransactionStore",
    "default_workbench_transaction_root",
    "WorkbenchRefactorTransaction",
    "detect_self_hosted_refactor",
    "prepare_workbench_refactor_transaction",
    "reserve_workbench_project_lane",
    "mark_workbench_transaction_recovery_pending",
    "discover_workbench_recovery_pending",
    "DynamicPythonRiskReport",
    "analyze_dynamic_python_risks",
    "TransformationRecipe",
    "build_transformation_recipe",
    "transformation_recipe_integrity_valid",
    "WorkbenchSealedPayload",
    "build_and_write_sealed_payload",
    "verify_sealed_payload",
    "ControlledMirrorBackend",
    "GitWorktreeBackend",
    "choose_shadow_backend",
    "ShadowProvenanceResult",
    "prove_shadow_runtime_provenance",
    "ShadowValidationResult",
    "validate_shadow_refactor",
    "JournaledApplyAuthorization",
    "JournaledApplyResult",
    "build_journaled_apply_authorization",
    "execute_journaled_refactor_apply",
    "resume_journaled_refactor_apply",
    "finalize_journaled_refactor_transaction",
    "JournaledRollbackResult",
    "rollback_journaled_refactor_transaction",
    "RefactorReceipt",
    "build_and_write_refactor_receipt",
    "ExecutorProofEvidence",
    "find_patch5_executor_proof",
    "SemanticDiffReview",
    "WarningAcknowledgment",
    "TransactionSummary",
    "RefactorLargeModuleGate",
    "evaluate_refactor_large_module_gate",
    "CompletionEvidenceBundle",
    "CompletionTransactionBundle",
    "prepare_completion_evidence",
    "prepare_completion_transaction",
    "refresh_completion_review_state",
    "build_and_write_real_preview",
    "build_cst_transform_fidelity_report",
    "synthesize_helper_imports",
    "validate_real_preview_structure",
    "build_and_write_preflight_backup_readiness",
    "build_and_write_source_apply_payload",
    "execute_guarded_source_apply",
    "expected_guarded_apply_token",
    "validate_and_write_post_apply",
    "execute_workbench_rollback",
    "expected_workbench_rollback_token",
    "run_workbench_behavior_validation",
    "build_and_write_import_rewrite_apply_readiness",
    "expected_import_rewrite_apply_token",
    "build_dependency_clusters",
    "build_split_plan",
    "execute_import_rewrite_rollback",
    "expected_import_rewrite_rollback_token",
    "execute_guarded_import_rewrite_apply",
    "expected_guarded_import_rewrite_apply_token",
    "validate_import_rewrite_post_apply",
    "build_advanced_import_rewrite_support",
    "write_advanced_import_rewrite_support",
    "build_final_integration_hardening_report",
    "write_final_integration_hardening_report",
    "build_batch_refactor_queue",
    "write_batch_refactor_queue",
    "build_visual_diff_report",
    "write_visual_diff_artifacts",
    "build_behavior_test_presets",
    "write_behavior_test_presets",
    "build_complete_workbench_freeze_report",
    "write_complete_workbench_freeze_report",
    "discover_candidates",
]
# import_migration_preview is imported directly by the GUI train.
# preview_artifact_validation is imported directly by the GUI train.
# patch_zip_gate owns the patch ZIP creation gate train.
# project_patch_payload owns governed project patch payload ZIP creation.
# payload_apply_gate owns review-only future apply gating.
# import_rewrite_application_gate owns review-only future import rewrite gating.
# human_confirmed_import_rewrite_contract owns review-only confirmation contract evidence.
# human_confirmed_apply_contract owns review-only payload apply confirmation evidence.
# final_guarded_source_apply_planning owns planning-only final source-apply evidence.
# source_apply_dry_run_validator owns dry-run-only source-apply validation evidence.
# source_apply_preflight_backup_contract owns source-derived backup snapshot readiness evidence.
# guarded_source_apply_executor owns the first exact-token guarded source mutation executor.
# post_apply_validation owns post-apply hash and evidence checks.
# source_apply_rollback_recovery owns exact-token recovery from source-derived backup snapshots.
# source_apply_multifile_recovery_evidence owns non-mutating multi-file recovery evidence.
# cst_real_preview_writer owns preview-only real moved-code generation.
# real_preview_structural_validator owns structural validation of project-support moved-code Previews.
# workbench_preflight_backup_readiness owns daily-work backup readiness before future apply.
# workbench_source_payload_builder owns source-ready project-support payload staging without apply.
# workbench_guarded_source_apply owns exact-token source mutation from source-ready payloads.
# workbench_post_apply_validator owns structural post-apply validation evidence.
# workbench_rollback_executor owns exact-token rollback visibility and recovery execution.
# workbench_behavior_validation owns optional post-apply test-backed behavior evidence.

# import_migration_preview owns read-only deep import review before any import rewrite train.

# cst_symbol_source_extractor and cst_preview_rendering own stronger preview extraction fidelity.
# cst_docstring_inserter owns preview-only deterministic docstring insertion.
# helper_import_synthesizer owns preview-only helper import synthesis evidence.
# workbench_import_rewrite_apply_readiness owns no-write exact-token import rewrite apply gating.
# workbench_import_rewrite_rollback_executor owns exact-token import rewrite rollback visibility.
# workbench_final_integration_hardening owns read-only final Workbench integration gates.
# cst_transform_fidelity owns non-mutating transformation-fidelity evidence.
# advanced_import_rewrite_support owns no-write alias and multi-import rewrite support evidence.
# batch_refactor_queue owns no-write multi-file queue evidence before any batch execution train.
# visual_diff_ui owns read-only visual diff artifacts before any UI/apply execution train.
# behavior_test_presets owns read-only behavior-test preset discovery before optional test execution.
# final_complete_workbench_freeze owns read-only 25-step closure evidence.

# workbench_dynamic_python_risks owns static dynamic-language and Qt risk classification.
# workbench_transformation_recipe owns deterministic contract-to-mechanics translation.
# workbench_sealed_payload owns exact downstream artifact byte truth after seal.
# workbench_shadow_backend owns isolated worktree/mirror materialization without live writes.
# workbench_shadow_provenance proves runtime imports originate from the selected shadow root.
# workbench_shadow_validation owns layered shadow structural/API/topology/runtime/behavior evidence.

# workbench_completion_review owns semantic-first review and fail-closed final button gates.
# workbench_completion_workflow composes frozen Patch 1-3 public APIs into Patch 4 review evidence.

# workbench_source_mutation_primitives owns the one shared exact-byte physical file mutation primitive.
# workbench_journaled_apply_executor owns Patch 5 operation journaling, resume, and finalization.
# workbench_transaction_rollback owns reverse hash-verified rollback and drift conflicts.
# workbench_refactor_receipt owns durable machine-readable terminal transaction receipts.
# workbench_patch5_executor_proof reads canonical project freeze memory before GUI real-apply enablement.
