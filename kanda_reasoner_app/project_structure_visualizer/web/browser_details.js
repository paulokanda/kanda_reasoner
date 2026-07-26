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

  function update(container, node) {
    if (!container) {
      return;
    }
    if (!node) {
      container.textContent = "No node selected.";
      return;
    }
    const statusText = [
      node.frozen ? "Frozen" : "",
      node.protected ? "Protected" : "",
      node.external ? "External" : ""
    ].filter(Boolean).join(", ") || "Normal";
    container.innerHTML =
      "<h2>" + escapeHtml(node.label) + "</h2>" +
      "<dl>" +
      "<dt>Type</dt><dd>" + escapeHtml(node.kind) + "</dd>" +
      "<dt>Category</dt><dd>" + escapeHtml(node.category) + "</dd>" +
      "<dt>Path</dt><dd>" +
      escapeHtml(node.relative_path || "Not applicable") + "</dd>" +
      "<dt>Incoming</dt><dd>" + escapeHtml(node.incoming_count) + "</dd>" +
      "<dt>Outgoing</dt><dd>" + escapeHtml(node.outgoing_count) + "</dd>" +
      "<dt>Status</dt><dd>" + escapeHtml(statusText) + "</dd>" +
      "</dl>" +
      "<p class=\"muted\">" + escapeHtml(node.summary || "") + "</p>";
  }

  window.kandaBrowserDetails = { update: update };
}());
