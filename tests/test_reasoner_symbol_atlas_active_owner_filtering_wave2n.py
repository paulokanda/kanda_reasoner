"""Public-contract regressions for Symbol Atlas active-owner filtering wave 2N."""

from __future__ import annotations

import tempfile
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from kanda_reasoner_app.reasoner_symbol_atlas.existing_code_finder import (
    ProjectSymbolAtlasExistingCodeFinderOptions,
    find_reasoner_symbol_atlas_existing_code,
)
from kanda_reasoner_app.reasoner_symbol_atlas.facade_owner_resolver import (
    ProjectSymbolAtlasFacadeOwnerOptions,
    resolve_reasoner_symbol_atlas_facade_owner,
)
from kanda_reasoner_app.reasoner_symbol_atlas.output_policy import (
    is_active_owner_candidate,
)
from kanda_reasoner_app.reasoner_symbol_atlas.schemas import (
    ProjectModuleRecord,
    ProjectSymbol,
    ProjectSymbolAtlasReport,
)


class ActiveOwnerFilteringWave2NTests(unittest.TestCase):
    """Prove inactive candidates cannot enter canonical owner ranking."""

    @staticmethod
    def _symbol(
        path: str,
        role: str = "canonical_owner",
        kind: str = "function",
        name: str = "TargetSymbol",
    ) -> ProjectSymbol:
        return ProjectSymbol(
            name=name,
            kind=kind,
            module=path.removesuffix(".py").replace("/", "."),
            path=path,
            line=10,
            owner_role=role,
        )

    @classmethod
    def _record(
        cls,
        path: str,
        role: str = "canonical_owner",
        module: str | None = None,
        is_test_file: bool = False,
        symbols: tuple[ProjectSymbol, ...] = (),
    ) -> ProjectModuleRecord:
        return ProjectModuleRecord(
            module=module or path.removesuffix(".py").replace("/", "."),
            path=path,
            owner_role=role,
            is_test_file=is_test_file,
            symbols=symbols,
        )

    @staticmethod
    def _merge_summary() -> SimpleNamespace:
        return SimpleNamespace(
            status="json_canonical",
            freshness_status="fresh",
        )

    def _resolve_facade(
        self,
        report: ProjectSymbolAtlasReport,
        target_path: str,
    ):
        with tempfile.TemporaryDirectory() as temp_dir:
            options = ProjectSymbolAtlasFacadeOwnerOptions(
                project_root=temp_dir,
                target_path=target_path,
                symbol_name="TargetSymbol",
            )
            with patch(
                "kanda_reasoner_app.reasoner_symbol_atlas.facade_owner_resolver."
                "merge_reasoner_symbol_atlas_live_and_json_evidence",
                return_value=(report, self._merge_summary()),
            ):
                return resolve_reasoner_symbol_atlas_facade_owner(options)

    def _find_symbol(
        self,
        report: ProjectSymbolAtlasReport,
        max_matches: int = 25,
    ):
        with tempfile.TemporaryDirectory() as temp_dir:
            options = ProjectSymbolAtlasExistingCodeFinderOptions(
                project_root=temp_dir,
                query_text="TargetSymbol",
                query_type="symbol",
                exact=True,
                max_matches=max_matches,
            )
            with patch(
                "kanda_reasoner_app.reasoner_symbol_atlas.existing_code_finder."
                "merge_reasoner_symbol_atlas_live_and_json_evidence",
                return_value=(report, self._merge_summary()),
            ):
                return find_reasoner_symbol_atlas_existing_code(options)

    def test_owner_policy_rejects_inactive_owner_classes(self) -> None:
        self.assertTrue(
            is_active_owner_candidate(
                "kanda_reasoner_app/domain/service.py",
                "canonical_owner",
            )
        )
        self.assertFalse(
            is_active_owner_candidate(
                ".project_reference/domain/service.py",
                "canonical_owner",
            )
        )
        self.assertFalse(
            is_active_owner_candidate(
                "kanda_reasoner_app/generated/service.py",
                "generated_or_stale",
            )
        )
        self.assertFalse(
            is_active_owner_candidate(
                "tests/test_service.py",
                "test_only",
                True,
            )
        )
        self.assertFalse(
            is_active_owner_candidate(
                "workbench/service.py",
                "canonical_owner",
            )
        )

    def test_existing_code_filters_before_result_limit(self) -> None:
        historical = self._symbol(".project_reference/a_owner.py")
        active = self._symbol("kanda_reasoner_app/z_owner.py")
        report = ProjectSymbolAtlasReport(
            project_root="unused",
            symbols=(historical, active),
        )

        result = self._find_symbol(report, max_matches=1)

        self.assertEqual((active,), result.symbol_matches)
        self.assertEqual((historical,), result.inactive_symbol_matches)
        self.assertEqual((active.path,), result.owner_paths)
        self.assertEqual((historical.path,), result.inactive_owner_paths)

    def test_facade_filters_inactive_candidates_before_ranking(self) -> None:
        import_symbol = ProjectSymbol(
            name="TargetSymbol",
            kind="import",
            path="kanda_reasoner_app/api.py",
            evidence=(
                "source: kanda_reasoner_app.domain.active_owner.TargetSymbol",
            ),
        )
        target = self._record(
            "kanda_reasoner_app/api.py",
            role="facade",
            module="kanda_reasoner_app.api",
            symbols=(import_symbol,),
        )
        active = self._record(
            "kanda_reasoner_app/domain/active_owner.py",
            module="kanda_reasoner_app.domain.active_owner",
            symbols=(self._symbol("kanda_reasoner_app/domain/active_owner.py"),),
        )
        historical = self._record(
            ".project_reference/domain/historical_owner.py",
            module="archive.historical_owner",
            symbols=(self._symbol(".project_reference/domain/historical_owner.py"),),
        )
        generated = self._record(
            "generated/generated_owner.py",
            role="generated_or_stale",
            module="generated.generated_owner",
            symbols=(
                self._symbol(
                    "generated/generated_owner.py",
                    role="generated_or_stale",
                ),
            ),
        )
        test_only = self._record(
            "tests/test_owner.py",
            role="test_only",
            module="tests.test_owner",
            is_test_file=True,
            symbols=(
                self._symbol(
                    "tests/test_owner.py",
                    role="test_only",
                ),
            ),
        )
        report = ProjectSymbolAtlasReport(
            project_root="unused",
            modules=(target, active, historical, generated, test_only),
            symbols=active.symbols + historical.symbols + generated.symbols + test_only.symbols,
        )

        decision = self._resolve_facade(report, target.path)

        self.assertEqual((active.path,), decision.owner_candidates)
        self.assertEqual(
            {historical.path, generated.path, test_only.path},
            set(decision.inactive_owner_candidates),
        )
        self.assertEqual(active.path, decision.likely_real_owner_path)

    def test_only_inactive_facade_owner_returns_no_likely_owner(self) -> None:
        target = self._record(
            "kanda_reasoner_app/api.py",
            role="facade",
            module="kanda_reasoner_app.api",
            symbols=(
                ProjectSymbol(
                    name="TargetSymbol",
                    kind="import",
                    path="kanda_reasoner_app/api.py",
                ),
            ),
        )
        historical = self._record(
            "_project_reference/domain/only_owner.py",
            module="archive.only_owner",
            symbols=(self._symbol("_project_reference/domain/only_owner.py"),),
        )
        report = ProjectSymbolAtlasReport(
            project_root="unused",
            modules=(target, historical),
            symbols=historical.symbols,
        )

        decision = self._resolve_facade(report, target.path)

        self.assertEqual((), decision.owner_candidates)
        self.assertEqual((historical.path,), decision.inactive_owner_candidates)
        self.assertEqual("", decision.likely_real_owner_path)

    def test_facade_result_preserves_inactive_evidence_separately(self) -> None:
        target = self._record(
            "kanda_reasoner_app/api.py",
            role="facade",
            module="kanda_reasoner_app.api",
            symbols=(
                ProjectSymbol(
                    name="TargetSymbol",
                    kind="import",
                    path="kanda_reasoner_app/api.py",
                ),
            ),
        )
        historical = self._record(
            ".project_reference/domain/old_owner.py",
            module="archive.old_owner",
            symbols=(self._symbol(".project_reference/domain/old_owner.py"),),
        )
        report = ProjectSymbolAtlasReport(
            project_root="unused",
            modules=(target, historical),
            symbols=historical.symbols,
        )

        decision = self._resolve_facade(report, target.path)

        self.assertEqual((historical.path,), decision.inactive_owner_candidates)
        self.assertIn(
            "Inactive owner candidates excluded before ranking: 1",
            decision.reasons,
        )
        self.assertEqual(
            [historical.path],
            decision.to_dict()["inactive_owner_candidates"],
        )

    def test_multiple_active_candidates_keep_role_precedence(self) -> None:
        target = self._record(
            "kanda_reasoner_app/api.py",
            role="facade",
            module="kanda_reasoner_app.api",
            symbols=(
                ProjectSymbol(
                    name="TargetSymbol",
                    kind="import",
                    path="kanda_reasoner_app/api.py",
                ),
            ),
        )
        helper = self._record(
            "kanda_reasoner_app/domain/_target_helper.py",
            role="private_helper",
            symbols=(self._symbol("kanda_reasoner_app/domain/_target_helper.py"),),
        )
        canonical = self._record(
            "kanda_reasoner_app/domain/target.py",
            role="canonical_owner",
            symbols=(self._symbol("kanda_reasoner_app/domain/target.py"),),
        )
        report = ProjectSymbolAtlasReport(
            project_root="unused",
            modules=(target, helper, canonical),
            symbols=helper.symbols + canonical.symbols,
        )

        decision = self._resolve_facade(report, target.path)

        self.assertEqual(canonical.path, decision.likely_real_owner_path)
        self.assertEqual(
            {helper.path, canonical.path},
            set(decision.owner_candidates),
        )

    def test_existing_code_result_serializes_inactive_matches(self) -> None:
        active = self._symbol("kanda_reasoner_app/domain/active_owner.py")
        historical = self._symbol(".project_reference/domain/old_owner.py")
        report = ProjectSymbolAtlasReport(
            project_root="unused",
            symbols=(historical, active),
        )

        result = self._find_symbol(report, max_matches=1)
        payload = result.to_dict()

        self.assertEqual("ready", result.status)
        self.assertIn(
            "Inactive owner candidates excluded before ranking: 1",
            result.reasons,
        )
        self.assertEqual(1, payload["symbol_match_count"])
        self.assertEqual(1, payload["inactive_symbol_match_count"])


if __name__ == "__main__":
    unittest.main()
