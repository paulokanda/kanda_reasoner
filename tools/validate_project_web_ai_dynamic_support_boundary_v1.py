# project-path: tools/validate_project_web_ai_dynamic_support_boundary_v1.py
"""Validate dynamic Project Support identity for Project Web AI."""

from __future__ import annotations

import argparse
import py_compile
import tempfile
from pathlib import Path

from kanda_reasoner_app.project_support_boundary import (
    resolve_project_tool_boundary_identity,
)
from kanda_reasoner_app.reasoner_engine.project_web_ai_agent_protocol import (
    agent_system_contract,
    parse_agent_tool_request,
)
from kanda_reasoner_app.reasoner_engine.project_web_ai_boundary_context import (
    ProjectAgentBoundaryContext,
    ProjectAgentBoundaryError,
)
from kanda_reasoner_app.reasoner_engine.project_web_ai_read_tools import (
    ProjectReadToolBroker,
    ProjectReadToolError,
)
from kanda_reasoner_app.web_ai_provider_contracts import (
    ProjectWebAIRequestIdentity,
)

FEATURE_ID = "project-web-ai-dynamic-support-boundary-v1"
TOUCHED = (
    "kanda_reasoner_app/reasoner_engine/project_web_ai_boundary_context.py",
    "kanda_reasoner_app/reasoner_engine/project_web_ai_agent_protocol.py",
    "kanda_reasoner_app/reasoner_engine/project_web_ai_read_tools.py",
    "kanda_reasoner_app/reasoner_engine/project_web_ai_agent_runtime.py",
    "kanda_reasoner_app/reasoner_engine/project_web_ai_workers.py",
    "kanda_reasoner_app/reasoner_engine/project_web_ai_bridge.py",
    "tools/validate_project_web_ai_read_only_agent_v1.py",
    "tools/validate_project_web_ai_dynamic_support_boundary_v1.py",
)


def require(condition: object, marker: str) -> None:
    """Raise one focused assertion or print its marker."""
    if not condition:
        raise AssertionError(marker)
    print(marker + ": PASS")


def request_identity(root: Path, request_id: str, epoch: int = 1) -> ProjectWebAIRequestIdentity:
    """Return one exact request identity bound to a disposable Project."""
    identity = resolve_project_tool_boundary_identity(root)
    return ProjectWebAIRequestIdentity(
        request_id=request_id,
        session_id="session-" + str(epoch),
        project_id=identity.active_project_id,
        project_slug=identity.active_project_slug,
        project_root_fingerprint=identity.active_project_root_fingerprint,
        support_root=str(identity.active_project_support_root),
        snapshot_id="snapshot-" + str(epoch),
        context_hash="context-" + str(epoch),
        gateway_id="fixture",
        model_id="fixture-model",
        privacy_approval_id="approval-" + str(epoch),
        created_at_utc="2026-07-23T00:00:00+00:00",
        project_epoch=epoch,
    )


def validate_dynamic_roots() -> None:
    """Prove separate source/support folders and dynamic Project switching."""
    with tempfile.TemporaryDirectory(prefix="kanda_dynamic_support_") as temp:
        base = Path(temp)
        first = base / "alpha_project"
        second = base / "beta_project"
        first.mkdir()
        second.mkdir()
        (first / "alpha.py").write_text("VALUE = 'alpha'\n", encoding="utf-8")
        (second / "beta.py").write_text("VALUE = 'beta'\n", encoding="utf-8")

        first_request = request_identity(first, "request-a", epoch=4)
        second_request = request_identity(second, "request-b", epoch=5)
        first_boundary = ProjectAgentBoundaryContext.from_request(
            first, first_request
        )
        second_boundary = ProjectAgentBoundaryContext.from_request(
            second, second_request
        )
        first_payload = first_boundary.tool_payload()
        second_payload = second_boundary.tool_payload()

        require(
            first_payload["active_project_folder_name"] == "alpha_project"
            and first_payload["project_support_folder_name"]
            == "alpha_project_show_project_to_AI",
            "DYNAMIC_PROJECT_SUPPORT_FOLDER_NAME",
        )
        require(
            second_payload["active_project_folder_name"] == "beta_project"
            and second_payload["project_support_folder_name"]
            == "beta_project_show_project_to_AI",
            "PROJECT_SWITCH_REDERIVES_SUPPORT_ROOT",
        )
        require(
            first_payload["project_support_relationship"]
            == "SEPARATE_EXTERNAL_FOLDER"
            and first_payload["logical_prefix_is_physical_child"] is False,
            "PROJECT_AND_SUPPORT_ARE_SEPARATE_FOLDERS",
        )
        require(
            first_payload["second_prompt_files"]
            == "<PROJECT_SUPPORT_ROOT>\\second_prompt_files",
            "SECOND_PROMPT_FILES_UNDER_EXTERNAL_SUPPORT_ROOT",
        )
        require(
            first_payload["dynamic_support_contract"]
            == "<project_drive>:\\<project_name>_show_project_to_AI",
            "DYNAMIC_DRIVE_AND_PROJECT_NAME_CONTRACT",
        )
        forbidden = set(first_payload["forbidden_nested_forms"])
        require(
            "<PROJECT_ROOT>\\show_project_to_AI" in forbidden
            and "<PROJECT_ROOT>\\alpha_project_show_project_to_AI" in forbidden,
            "NESTED_PROJECT_SUPPORT_FORMS_FORBIDDEN",
        )

        first_broker = ProjectReadToolBroker(
            first, boundary=first_boundary
        )
        boundary_result = first_broker.execute(
            "describe_project_boundaries", {}
        ).payload
        require(
            boundary_result["project_support_read_authority"] is False
            and boundary_result["project_source_read_authority"] is True,
            "PROJECT_SUPPORT_DESCRIPTION_WITHOUT_READ_AUTHORITY",
        )
        require(
            first_broker.execute(
                "read_project_file", {"path": "alpha.py"}
            ).payload["path"]
            == "alpha.py",
            "ACTIVE_PROJECT_SOURCE_READ_PRESERVED",
        )

        try:
            ProjectReadToolBroker(second, boundary=first_boundary)
        except ProjectReadToolError:
            print("STALE_PROJECT_BOUNDARY_REJECTED_AFTER_SWITCH: PASS")
        else:
            raise AssertionError("STALE_PROJECT_BOUNDARY_REJECTED_AFTER_SWITCH")

        wrong_support = ProjectWebAIRequestIdentity(
            **{
                **first_request.__dict__,
                "support_root": str(second_request.support_root),
            }
        )
        try:
            ProjectAgentBoundaryContext.from_request(first, wrong_support)
        except ProjectAgentBoundaryError:
            print("SUPPORT_ROOT_IDENTITY_MISMATCH_FAILS_CLOSED: PASS")
        else:
            raise AssertionError("SUPPORT_ROOT_IDENTITY_MISMATCH_FAILS_CLOSED")


def validate_prompt_and_protocol(root: Path) -> None:
    """Validate authoritative path semantics in agent and normal-chat prompts."""
    request = request_identity(root, "request-self", epoch=7)
    boundary = ProjectAgentBoundaryContext.from_request(root, request)
    contract = agent_system_contract(boundary)
    require(
        "The active Project source and Project Support are two separate folders"
        in contract,
        "AGENT_CONTRACT_SEPARATE_FOLDER_LANGUAGE",
    )
    require(
        "Manifest paths beginning with show_project_to_AI/ are stable logical"
        in contract,
        "LOGICAL_MANIFEST_PREFIX_NOT_PHYSICAL_CHILD",
    )
    require(
        "Project switch invalidates it" in contract
        and "Project epoch: 7" in contract,
        "MCARD_PARADIGM_IDENTITY_GENERATION_REUSED",
    )
    parsed = parse_agent_tool_request(
        "KANDA_PROJECT_TOOL_REQUEST_BEGIN\n"
        '{"tool":"describe_project_boundaries","arguments":{}}\n'
        "KANDA_PROJECT_TOOL_REQUEST_END"
    )
    require(
        parsed is not None and parsed.tool == "describe_project_boundaries",
        "BOUNDARY_DESCRIPTION_TOOL_PROTOCOL",
    )

    bridge = (
        root
        / "kanda_reasoner_app/reasoner_engine/project_web_ai_bridge.py"
    ).read_text(encoding="utf-8")
    require(
        "<project_drive>:\\\\<project_name>_show_project_to_AI" in bridge
        and "logical evidence prefixes" in bridge,
        "NORMAL_CHAT_TRUSTED_BOUNDARY_CORRECTED",
    )
    worker = (
        root
        / "kanda_reasoner_app/reasoner_engine/project_web_ai_workers.py"
    ).read_text(encoding="utf-8")
    runtime = (
        root
        / "kanda_reasoner_app/reasoner_engine/project_web_ai_agent_runtime.py"
    ).read_text(encoding="utf-8")
    require(
        "request_identity=identity" in worker
        and "ProjectAgentBoundaryContext.from_request" in runtime,
        "REQUEST_EPOCH_SNAPSHOT_BOUNDARY_BOUND",
    )
    require(
        "write_authority" in runtime
        and '"boundary_identity_bound": True' in runtime,
        "BRICK_WALL_TOOL_PROJECT_IDENTITY_GATE",
    )


def validate_source_contract(root: Path) -> None:
    """Compile touched modules and enforce bounded ownership surfaces."""
    for relative in TOUCHED:
        path = root / relative
        py_compile.compile(str(path), doraise=True)
        require(
            len(path.read_text(encoding="utf-8").splitlines()) <= 500,
            "TOUCHED_SOURCE_MODULES_MAX_500_LINES " + relative,
        )
    broker = (root / TOUCHED[2]).read_text(encoding="utf-8")
    boundary = (root / TOUCHED[0]).read_text(encoding="utf-8")
    forbidden = ("subprocess", "os.system", "Popen(", "write_bytes(")
    require(
        not any(token in broker or token in boundary for token in forbidden),
        "BOUNDARY_FIX_ADDS_NO_WRITE_OR_SHELL_AUTHORITY",
    )
    require(
        "project_support_read_authority\": False" in boundary
        and "read_project_support" not in broker,
        "PROJECT_SUPPORT_CONTENT_REMAINS_UNEXPOSED",
    )
    print("PYTHON_COMPILE: PASS")
    print("TOUCHED_SOURCE_MODULES_MAX_500_LINES: PASS")


def main() -> int:
    """Run all focused dynamic boundary validations."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    validate_source_contract(root)
    validate_dynamic_roots()
    validate_prompt_and_protocol(root)
    print("MCARD_APPLICABILITY: NOT_APPLICABLE")
    print("MCARD_PARADIGM_REUSE: IDENTITY_AND_GENERATION_ONLY")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
