# project-path: kanda_reasoner_app/engineering_diagnostics_gui/diagnostic_table_model.py
"""Transient indexed Qt model builder for Engineering Diagnostics findings."""

from __future__ import annotations

from typing import Any

from .models import DiagnosticFindingView

__all__ = ["create_finding_table_model_class"]


def create_finding_table_model_class(
    abstract_table_model: type,
    model_index: type,
    qt: Any,
    columns: tuple[tuple[str, str], ...],
) -> type:
    """Build the Qt table model without importing PySide6 at package import time."""

    class FindingTableModel(abstract_table_model):
        def __init__(self) -> None:
            super().__init__()
            self.rows: tuple[DiagnosticFindingView, ...] = ()
            self._filter_keys: tuple[
                tuple[str, str, str, str, str, str, str, str], ...
            ] = ()
            self._visible_rows: tuple[int, ...] | None = None
            self._filters = (
                "all", "all", "all", "all", "all", "all", "all", ""
            )
            self._sort_column = -1
            self._sort_descending = False

        def rowCount(self, parent=None) -> int:  # noqa: N802
            current = parent if parent is not None else model_index()
            if current.isValid():
                return 0
            return len(self.rows) if self._visible_rows is None else len(self._visible_rows)

        def columnCount(self, parent=None) -> int:  # noqa: N802
            current = parent if parent is not None else model_index()
            return 0 if current.isValid() else len(columns)

        def data(self, index, role=None):
            active_role = qt.DisplayRole if role is None else role
            if not index.isValid() or active_role not in (qt.DisplayRole, qt.ToolTipRole):
                return None
            view = self.row_view(index.row())
            if view is None:
                return None
            field = columns[index.column()][0]
            value = getattr(view, field, None)
            if value is None:
                value = getattr(view.record, field, "")
            return str(value if value is not None else "")

        def headerData(self, section, orientation, role=None):  # noqa: N802
            active_role = qt.DisplayRole if role is None else role
            if active_role != qt.DisplayRole:
                return None
            if orientation == qt.Horizontal:
                return columns[section][1]
            return str(section + 1)

        @staticmethod
        def _filter_key(
            view: DiagnosticFindingView,
        ) -> tuple[str, str, str, str, str, str, str, str]:
            record = view.record
            text = "\n".join(
                (
                    record.code,
                    record.relative_path,
                    record.message,
                    record.category,
                    view.scope_classification,
                    view.frozen_status,
                    view.governing_freeze_ids,
                    view.owner_status,
                    view.owner_confidence,
                    view.canonical_owner,
                    view.group_kind,
                    view.group_label,
                    view.group_confidence,
                    view.decision_state,
                    view.remediation_action_class,
                    (
                        view.remediation_intent.likely_correction
                        if view.remediation_intent is not None
                        else ""
                    ),
                    " ".join(group.label for group in view.groups),
                    " ".join(view.enrichment.owner.active_candidates),
                    " ".join(view.enrichment.owner.historical_candidates),
                )
            ).lower()
            return (
                record.severity.lower(),
                view.lifecycle_state.lower(),
                view.decision_state.lower(),
                view.scope_classification.lower(),
                view.frozen_status.lower(),
                view.owner_status.lower(),
                view.group_kind.lower(),
                text,
            )

        def _rebuild_visible(self) -> tuple[int, ...] | None:
            severity, lifecycle, decision, scope, frozen, owner, group, text = self._filters
            filtering = (
                severity != "all"
                or lifecycle != "all"
                or decision != "all"
                or scope != "all"
                or frozen != "all"
                or owner != "all"
                or group != "all"
                or bool(text)
            )
            accepted: list[int] | range = range(len(self.rows))
            if filtering:
                accepted = []
                for index, key in enumerate(self._filter_keys):
                    (
                        row_severity,
                        row_lifecycle,
                        row_decision,
                        row_scope,
                        row_frozen,
                        row_owner,
                        row_group,
                        search_text,
                    ) = key
                    if severity != "all" and row_severity != severity:
                        continue
                    if lifecycle != "all" and row_lifecycle != lifecycle:
                        continue
                    if decision != "all" and row_decision != decision:
                        continue
                    if scope != "all" and row_scope != scope:
                        continue
                    if frozen != "all" and row_frozen != frozen:
                        continue
                    if owner != "all" and row_owner != owner:
                        continue
                    if group != "all" and row_group != group:
                        continue
                    if text and text not in search_text:
                        continue
                    accepted.append(index)
            if self._sort_column >= 0:
                field = columns[self._sort_column][0]
                accepted = sorted(
                    accepted,
                    key=lambda index: str(
                        getattr(self.rows[index], field, None)
                        or getattr(self.rows[index].record, field, "")
                    ).lower(),
                    reverse=self._sort_descending,
                )
            if not filtering and self._sort_column < 0:
                return None
            return tuple(accepted)

        def set_rows(self, rows: tuple[DiagnosticFindingView, ...]) -> None:
            self.beginResetModel()
            self.rows = tuple(rows)
            self._filter_keys = tuple(self._filter_key(view) for view in self.rows)
            self._visible_rows = self._rebuild_visible()
            self.endResetModel()

        def set_filters(
            self,
            severity: str,
            lifecycle: str,
            *args: str,
        ) -> None:
            """Set current filters while preserving prior wave call signatures."""
            scope = "all"
            frozen = "all"
            owner = "all"
            group = "all"
            decision = "all"
            text = ""
            if len(args) == 1:
                text = args[0]
            elif len(args) == 3:
                scope, frozen, text = args
            elif len(args) == 4:
                scope, frozen, owner, text = args
            elif len(args) == 5:
                scope, frozen, owner, group, text = args
            elif len(args) == 6:
                scope, frozen, owner, group, decision, text = args
            elif args:
                raise TypeError("Unsupported Engineering Diagnostics filter signature.")
            normalized = (
                severity.strip().lower() or "all",
                lifecycle.strip().lower() or "all",
                decision.strip().lower() or "all",
                scope.strip().lower() or "all",
                frozen.strip().lower() or "all",
                owner.strip().lower() or "all",
                group.strip().lower() or "all",
                text.strip().lower(),
            )
            if normalized == self._filters:
                return
            self.beginResetModel()
            self._filters = normalized
            self._visible_rows = self._rebuild_visible()
            self.endResetModel()

        def sort(self, column, order=None) -> None:
            if column < 0 or column >= len(columns):
                return
            active_order = qt.AscendingOrder if order is None else order
            self.beginResetModel()
            self._sort_column = int(column)
            self._sort_descending = active_order == qt.DescendingOrder
            self._visible_rows = self._rebuild_visible()
            self.endResetModel()

        def row_view(self, display_row: int) -> DiagnosticFindingView | None:
            if display_row < 0:
                return None
            source_row = display_row
            if self._visible_rows is not None:
                if display_row >= len(self._visible_rows):
                    return None
                source_row = self._visible_rows[display_row]
            if source_row >= len(self.rows):
                return None
            return self.rows[source_row]

    return FindingTableModel
