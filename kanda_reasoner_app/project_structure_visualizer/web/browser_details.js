(function () {
  "use strict";

  function escapeHtml(value) {
    return String(value == null ? "" : value)
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#39;");
  }

  function metadata(node) {
    return node && node.metadata && typeof node.metadata === "object" ?
      node.metadata : {};
  }

  function overviewHtml() {
    const graph = window.__KANDA_GRAPH_SNAPSHOT__ || {};
    const statistics = graph.statistics || {};
    const findings = statistics.structure_findings || {};
    const reviewCandidates = Array.isArray(
      findings.high_import_fan_in_without_visible_validation
    ) ? findings.high_import_fan_in_without_visible_validation : [];
    return "<h2>Structural findings</h2>" +
      "<dl>" +
      "<dt>Import-cycle components</dt><dd>" +
      escapeHtml(findings.cyclic_component_count || 0) + "</dd>" +
      "<dt>Modules in import cycles</dt><dd>" +
      escapeHtml(findings.cyclic_node_count || 0) + "</dd>" +
      "<dt>Low-confidence relationships</dt><dd>" +
      escapeHtml(findings.low_confidence_edge_count || 0) + "</dd>" +
      "<dt>Review candidates</dt><dd>" +
      escapeHtml(reviewCandidates.length) + "</dd>" +
      "</dl>" +
      "<p class=\"muted\">Signals describe only the rendered snapshot. " +
      "They do not claim whole-project completeness or a quality score.</p>";
  }

  function update(container, node) {
    if (!container) {
      return;
    }
    if (!node) {
      container.innerHTML = overviewHtml();
      return;
    }
    const nodeMetadata = metadata(node);
    const statusText = [
      node.frozen ? "Frozen" : "",
      node.protected ? "Protected" : "",
      node.external ? "External" : "",
      nodeMetadata.in_import_cycle ? "Import cycle" : ""
    ].filter(Boolean).join(", ") || "Normal";
    container.innerHTML =
      "<h2>" + escapeHtml(node.label) + "</h2>" +
      "<dl>" +
      "<dt>Type</dt><dd>" + escapeHtml(node.kind) + "</dd>" +
      "<dt>Category</dt><dd>" + escapeHtml(node.category) + "</dd>" +
      "<dt>Path</dt><dd>" +
      escapeHtml(node.relative_path || "Not applicable") + "</dd>" +
      "<dt>Incoming relationships</dt><dd>" +
      escapeHtml(node.incoming_count) + "</dd>" +
      "<dt>Outgoing relationships</dt><dd>" +
      escapeHtml(node.outgoing_count) + "</dd>" +
      "<dt>Import fan-in</dt><dd>" +
      escapeHtml(nodeMetadata.import_fan_in || 0) + "</dd>" +
      "<dt>Import fan-out</dt><dd>" +
      escapeHtml(nodeMetadata.import_fan_out || 0) + "</dd>" +
      "<dt>Import cycle</dt><dd>" +
      escapeHtml(nodeMetadata.import_cycle_component_id || "No") + "</dd>" +
      "<dt>Visible validation links</dt><dd>" +
      escapeHtml(nodeMetadata.visible_validation_link_count || 0) + "</dd>" +
      "<dt>Status</dt><dd>" + escapeHtml(statusText) + "</dd>" +
      "</dl>" +
      "<p class=\"muted\">" + escapeHtml(node.summary || "") + "</p>";
  }

  window.kandaBrowserDetails = { update: update };
}());
