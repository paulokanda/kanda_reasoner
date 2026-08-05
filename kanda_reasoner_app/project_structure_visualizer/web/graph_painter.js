(function () {
  "use strict";

  const nodePalette = {
    core: "#48c7ff",
    gui: "#ff9a45",
    ai: "#b98cff",
    validation: "#5fe09b",
    evidence: "#ffd65a",
    external: "#8d9bad"
  };
  const relationshipPalette = {
    contains: "#7892aa",
    imports: "#6fb8ff",
    calls: "#b98cff",
    inherits: "#ebf4ff",
    validates: "#5fe09b",
    invokes: "#ff9a45",
    protects: "#ffcc57",
    depends_on: "#8d9bad"
  };
  const nodeValues = {
    project: 12,
    package: 8,
    module: 5.5,
    class: 4.8,
    validator: 4.8,
    external: 4.5,
    function: 3.2
  };

  function metadata(record) {
    return record && record.metadata && typeof record.metadata === "object" ?
      record.metadata : {};
  }

  function create(flags) {
    function nodeColor(node) {
      if (flags.isSelected(node.id) || flags.isPathNode(node.id)) {
        return "#ffffff";
      }
      if (flags.isHovered(node.id)) {
        return "#dff6ff";
      }
      return nodePalette[node.category] || nodePalette.core;
    }

    function nodeValue(node) {
      const base = nodeValues[node.kind] || 4;
      if (node.kind !== "module" && node.kind !== "validator") {
        return base;
      }
      const percentile = Math.max(
        0,
        Math.min(1, Number(metadata(node).import_fan_in_percentile || 0))
      );
      return base * (1 + 0.65 * percentile);
    }

    function nodeLabel(node) {
      const nodeMetadata = metadata(node);
      const statuses = [
        node.frozen ? "Frozen" : "",
        node.protected ? "Protected" : "",
        node.external ? "External" : "",
        nodeMetadata.in_import_cycle ? "Import cycle" : "",
        Number(nodeMetadata.import_fan_in || 0) > 0 ?
          "Import fan-in: " + String(nodeMetadata.import_fan_in) : ""
      ].filter(Boolean);
      const suffix = statuses.length ? " | " + statuses.join(", ") : "";
      return String(node.label || node.id) + " | " +
        String(node.kind || "node") + suffix;
    }

    function linkColor(link) {
      if (flags.isPathEdge(link.id)) {
        return "#ffffff";
      }
      if (flags.isSelectedEdge(link)) {
        return "#9fe4ff";
      }
      if (metadata(link).in_import_cycle) {
        return "#ffb347";
      }
      return relationshipPalette[link.relationship] || "#91aac5";
    }

    function linkWidth(link) {
      if (flags.isPathEdge(link.id)) {
        return 2.8;
      }
      if (flags.isSelectedEdge(link)) {
        return 1.7;
      }
      if (metadata(link).in_import_cycle) {
        return 1.9;
      }
      return link.relationship === "contains" ? 0.45 : 0.9;
    }

    function linkOpacity(link) {
      if (flags.isPathEdge(link.id) || flags.isSelectedEdge(link)) {
        return 0.95;
      }
      if (metadata(link).in_import_cycle) {
        return 0.88;
      }
      return link.relationship === "contains" ? 0.24 : 0.58;
    }

    function arrowLength(link) {
      return link.relationship === "contains" ? 0 : 3.2;
    }

    function particleCount(link) {
      return flags.isPathEdge(link.id) ? 2 : 0;
    }

    return {
      nodeColor: nodeColor,
      nodeValue: nodeValue,
      nodeLabel: nodeLabel,
      linkColor: linkColor,
      linkWidth: linkWidth,
      linkOpacity: linkOpacity,
      arrowLength: arrowLength,
      particleCount: particleCount
    };
  }

  window.kandaGraphPainter = { create: create };
}());
