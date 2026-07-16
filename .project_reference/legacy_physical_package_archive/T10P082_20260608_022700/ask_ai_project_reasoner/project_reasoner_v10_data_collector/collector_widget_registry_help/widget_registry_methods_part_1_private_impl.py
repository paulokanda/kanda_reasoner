"""Private method implementations for collector_widget_registry."""

from __future__ import annotations

__all__ = []

def _bind_root_globals(root_globals):
    globals().update(root_globals)

def _wrg__current_source_symbol_impl(self) -> str:
    names = [name for _kind, name in self._scope_stack if name]
    return ".".join(names) if names else "<module>"

def _wrg__current_class_name_impl(self) -> str:
    for kind, name in reversed(self._scope_stack):
        if kind == "class":
            return name
    return ""

def _wrg__current_method_name_impl(self) -> str:
    for kind, name in reversed(self._scope_stack):
        if kind in FUNCTION_SCOPE_KINDS:
            return name
    return ""

def _wrg__push_scope_impl(self, kind: str, name: str) -> None:
    self._scope_stack.append((kind, name))

def _wrg__pop_scope_impl(self) -> None:
    if self._scope_stack:
        self._scope_stack.pop()

def _wrg_visit_ClassDef_impl(self, node: ast.ClassDef) -> None:
    self._push_scope("class", node.name)
    self.generic_visit(node)
    self._pop_scope()

def _wrg_visit_FunctionDef_impl(self, node: ast.FunctionDef) -> None:
    self._push_scope("function", node.name)
    self.generic_visit(node)
    self._pop_scope()

def _wrg_visit_AsyncFunctionDef_impl(self, node: ast.AsyncFunctionDef) -> None:
    self._push_scope("async_function", node.name)
    self.generic_visit(node)
    self._pop_scope()

def _wrg_visit_Assign_impl(self, node: ast.Assign) -> None:
    widget_call = node.value if isinstance(node.value, ast.Call) else None
    if widget_call is not None:
        widget_type = _get_widget_type_from_call(widget_call)
        if widget_type:
            target_ref = self._first_supported_target_ref(node.targets)
            if target_ref:
                self._register_assigned_widget(
                    target_ref=target_ref,
                    widget_type=widget_type,
                    call_node=widget_call,
                    assign_node=node,
                    creation_style="assignment_constructor",
                )

    self.generic_visit(node)

def _wrg_visit_AnnAssign_impl(self, node: ast.AnnAssign) -> None:
    widget_call = node.value if isinstance(node.value, ast.Call) else None
    if widget_call is not None:
        widget_type = _get_widget_type_from_call(widget_call)
        if widget_type:
            target_ref = _expr_to_ref(node.target)
            if target_ref:
                self._register_assigned_widget(
                    target_ref=target_ref,
                    widget_type=widget_type,
                    call_node=widget_call,
                    assign_node=node,
                    creation_style="annotated_assignment_constructor",
                )

    self.generic_visit(node)

def _wrg_visit_Call_impl(self, node: ast.Call) -> None:
    self._handle_widget_property_call(node)
    self._handle_layout_call(node)
    self.generic_visit(node)

def _wrg__register_assigned_widget_impl(
    self,
    target_ref: str,
    widget_type: str,
    call_node: ast.Call,
    assign_node: ast.AST,
    creation_style: str,
) -> str:
    variable_name = _variable_name_from_ref(target_ref)
    source_symbol = self._current_source_symbol()
    class_name = self._current_class_name()
    method_name = self._current_method_name()
    widget_id = _build_widget_id(
        source_file=self.source_file,
        source_symbol=source_symbol,
        variable_name=variable_name,
        widget_type=widget_type,
        line=getattr(assign_node, "lineno", 0) or 0,
        col=getattr(assign_node, "col_offset", 0) or 0,
    )

    display_text = _extract_constructor_display_text(widget_type, call_node)
    parent_ref = _extract_constructor_parent_ref(widget_type, call_node)

    record = {
        "widget_id": widget_id,
        "widget_type": widget_type,
        "variable_name": variable_name,
        "widget_ref": target_ref,
        "display_text": display_text,
        "placeholder_text": "",
        "tooltip_text": "",
        "object_name": "",
        "items": [],
        "header_labels": [],
        "tab_texts": [],
        "source_file": self.source_file,
        "source_symbol": source_symbol,
        "class_name": class_name,
        "method_name": method_name,
        "line": getattr(assign_node, "lineno", None),
        "end_line": getattr(assign_node, "end_lineno", getattr(assign_node, "lineno", None)),
        "col": getattr(assign_node, "col_offset", None),
        "parent_layout": "",
        "layout_kind": "",
        "layout_position": {},
        "container_widget": parent_ref,
        "creation_style": creation_style,
        "connections": [],
        "layout_records": [],
        "confidence": 1.0,
    }

    existing = self.registry.get(widget_id)
    if existing:
        record = existing
        if display_text and not existing.get("display_text"):
            record["display_text"] = display_text
        if parent_ref and not existing.get("container_widget"):
            record["container_widget"] = parent_ref
    else:
        self.registry[widget_id] = record

    self._index_widget_ref(source_symbol, target_ref, widget_id)
    if variable_name:
        self._index_widget_var(variable_name, widget_id)

    return widget_id

def _wrg__register_inline_widget_impl(
    self,
    widget_call: ast.Call,
    parent_layout: str = "",
    layout_kind: str = "",
    layout_position: dict[str, Any] | None = None,
    creation_style: str = "inline_constructor",
) -> str:
    widget_type = _get_widget_type_from_call(widget_call)
    if not widget_type:
        return ""

    source_symbol = self._current_source_symbol()
    class_name = self._current_class_name()
    method_name = self._current_method_name()
    line = getattr(widget_call, "lineno", 0) or 0
    col = getattr(widget_call, "col_offset", 0) or 0

    widget_id = _build_widget_id(
        source_file=self.source_file,
        source_symbol=source_symbol,
        variable_name="",
        widget_type=widget_type,
        line=line,
        col=col,
    )

    if widget_id not in self.registry:
        self.registry[widget_id] = {
            "widget_id": widget_id,
            "widget_type": widget_type,
            "variable_name": "",
            "widget_ref": "",
            "display_text": _extract_constructor_display_text(widget_type, widget_call),
            "placeholder_text": "",
            "tooltip_text": "",
            "object_name": "",
            "items": [],
            "header_labels": [],
            "tab_texts": [],
            "source_file": self.source_file,
            "source_symbol": source_symbol,
            "class_name": class_name,
            "method_name": method_name,
            "line": line,
            "end_line": getattr(widget_call, "end_lineno", line),
            "col": col,
            "parent_layout": parent_layout,
            "layout_kind": layout_kind,
            "layout_position": layout_position or {},
            "container_widget": _extract_constructor_parent_ref(widget_type, widget_call),
            "creation_style": creation_style,
            "connections": [],
            "layout_records": [],
            "confidence": 0.90,
        }

    if parent_layout or layout_kind or layout_position:
        self._append_layout_record(
            widget_id=widget_id,
            parent_layout=parent_layout,
            layout_kind=layout_kind,
            layout_position=layout_position or {},
            line=line,
        )

    return widget_id

def _wrg__handle_widget_property_call_impl(self, node: ast.Call) -> None:
    if not isinstance(node.func, ast.Attribute):
        return

    method_name = _safe_str(node.func.attr)
    target_ref = _expr_to_ref(node.func.value)
    widget_id = self._resolve_widget_id(target_ref)

    if not widget_id:
        return

    record = self.registry.get(widget_id)
    if not record:
        return

    if method_name in TEXT_SETTER_TO_FIELD:
        text_value = _node_to_text(_first_arg(node))
        if text_value:
            record[TEXT_SETTER_TO_FIELD[method_name]] = text_value
        return

    if method_name in SINGLE_ITEM_SETTER_TO_FIELD:
        item_value = _node_to_text(_first_arg(node))
        if item_value:
            target_field = SINGLE_ITEM_SETTER_TO_FIELD[method_name]
            current_items = list(record.get(target_field, []))
            current_items.append(item_value)
            record[target_field] = current_items
        return

    if method_name in LIST_SETTER_TO_FIELD:
        values = _node_to_text_list(_first_arg(node))
        if values:
            record[LIST_SETTER_TO_FIELD[method_name]] = values
        return

    if method_name == "setTabText":
        if len(node.args) >= 2:
            tab_index = _node_to_number(node.args[0])
            tab_text = _node_to_text(node.args[1])
            if tab_text:
                current_tab_texts = list(record.get("tab_texts", []))
                current_tab_texts.append(
                    {
                        "index": tab_index,
                        "text": tab_text,
                        "line": getattr(node, "lineno", None),
                    }
                )
                record["tab_texts"] = current_tab_texts
        return

def _wrg__handle_layout_call_impl(self, node: ast.Call) -> None:
    if not isinstance(node.func, ast.Attribute):
        return

    method_name = _safe_str(node.func.attr)
    if method_name not in LAYOUT_METHODS:
        return

    layout_ref = _expr_to_ref(node.func.value)

    if method_name == "addWidget":
        self._handle_add_widget(node, layout_ref)
        return

    if method_name == "addRow":
        self._handle_add_row(node, layout_ref)
        return

    if method_name == "addTab":
        self._handle_add_tab(node, layout_ref)
        return

def _wrg__handle_add_widget_impl(self, node: ast.Call, layout_ref: str) -> None:
    if not node.args:
        return

    widget_id = self._resolve_or_create_widget_from_expr(
        node.args[0],
        parent_layout=layout_ref,
        layout_kind="layout_add_widget",
        layout_position=_extract_layout_position_from_add_widget(node),
    )
    if not widget_id:
        return

    self._append_layout_record(
        widget_id=widget_id,
        parent_layout=layout_ref,
        layout_kind="layout_add_widget",
        layout_position=_extract_layout_position_from_add_widget(node),
        line=getattr(node, "lineno", None),
    )

def _wrg__handle_add_row_impl(self, node: ast.Call, layout_ref: str) -> None:
    if len(node.args) < 2:
        return

    label_expr = node.args[0]
    field_expr = node.args[1]

    label_widget_id = self._resolve_or_create_widget_from_expr(
        label_expr,
        parent_layout=layout_ref,
        layout_kind="form_row_label",
        layout_position={"role": "label"},
    )
    field_widget_id = self._resolve_or_create_widget_from_expr(
        field_expr,
        parent_layout=layout_ref,
        layout_kind="form_row_field",
        layout_position={"role": "field"},
    )

    if label_widget_id:
        self._append_layout_record(
            widget_id=label_widget_id,
            parent_layout=layout_ref,
            layout_kind="form_row_label",
            layout_position={"role": "label"},
            line=getattr(node, "lineno", None),
        )

    if field_widget_id:
        self._append_layout_record(
            widget_id=field_widget_id,
            parent_layout=layout_ref,
            layout_kind="form_row_field",
            layout_position={"role": "field"},
            line=getattr(node, "lineno", None),
        )

def _wrg__handle_add_tab_impl(self, node: ast.Call, layout_ref: str) -> None:
    if len(node.args) < 2:
        return

    widget_expr = node.args[0]
    tab_text = _node_to_text(node.args[1])

    widget_id = self._resolve_or_create_widget_from_expr(
        widget_expr,
        parent_layout=layout_ref,
        layout_kind="tab_page",
        layout_position={"tab_text": tab_text},
    )
    if not widget_id:
        return

    self._append_layout_record(
        widget_id=widget_id,
        parent_layout=layout_ref,
        layout_kind="tab_page",
        layout_position={"tab_text": tab_text},
        line=getattr(node, "lineno", None),
    )

    record = self.registry.get(widget_id, {})
    current_tab_texts = list(record.get("tab_texts", []))
    current_tab_texts.append(
        {
            "index": None,
            "text": tab_text,
            "line": getattr(node, "lineno", None),
        }
    )
    record["tab_texts"] = current_tab_texts

def _wrg__append_layout_record_impl(
    self,
    widget_id: str,
    parent_layout: str,
    layout_kind: str,
    layout_position: dict[str, Any],
    line: int | None,
) -> None:
    record = self.registry.get(widget_id)
    if not record:
        return

    if parent_layout and not record.get("parent_layout"):
        record["parent_layout"] = parent_layout

    if layout_kind and not record.get("layout_kind"):
        record["layout_kind"] = layout_kind

    if layout_position and not record.get("layout_position"):
        record["layout_position"] = layout_position

    current_layout_records = list(record.get("layout_records", []))
    current_layout_records.append(
        {
            "parent_layout": parent_layout,
            "layout_kind": layout_kind,
            "layout_position": layout_position,
            "line": line,
        }
    )
    record["layout_records"] = current_layout_records

def _wrg__index_widget_ref_impl(self, source_symbol: str, target_ref: str, widget_id: str) -> None:
    if source_symbol not in self._scope_ref_index:
        self._scope_ref_index[source_symbol] = {}
    self._scope_ref_index[source_symbol][target_ref] = widget_id
    self._file_ref_index[target_ref] = widget_id

def _wrg__index_widget_var_impl(self, variable_name: str, widget_id: str) -> None:
    if variable_name not in self._file_var_index:
        self._file_var_index[variable_name] = []
    if widget_id not in self._file_var_index[variable_name]:
        self._file_var_index[variable_name].append(widget_id)

def _wrg__resolve_widget_id_impl(self, target_ref: str) -> str:
    if not target_ref:
        return ""

    source_symbol = self._current_source_symbol()
    scope_map = self._scope_ref_index.get(source_symbol, {})
    if target_ref in scope_map:
        return scope_map[target_ref]

    if target_ref in self._file_ref_index:
        return self._file_ref_index[target_ref]

    variable_name = _variable_name_from_ref(target_ref)
    if variable_name:
        matches = self._file_var_index.get(variable_name, [])
        if len(matches) == 1:
            return matches[0]

    return ""

def _wrg__resolve_or_create_widget_from_expr_impl(
    self,
    expr: ast.AST,
    parent_layout: str,
    layout_kind: str,
    layout_position: dict[str, Any],
) -> str:
    ref = _expr_to_ref(expr)
    widget_id = self._resolve_widget_id(ref)
    if widget_id:
        return widget_id

    if isinstance(expr, ast.Call):
        widget_type = _get_widget_type_from_call(expr)
        if widget_type:
            return self._register_inline_widget(
                widget_call=expr,
                parent_layout=parent_layout,
                layout_kind=layout_kind,
                layout_position=layout_position,
                creation_style="inline_constructor",
            )

    return ""
