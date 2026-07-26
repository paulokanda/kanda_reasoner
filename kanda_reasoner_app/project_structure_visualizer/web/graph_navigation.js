(function () {
  "use strict";

  const PATH_RELATIONSHIPS = new Set([
    "imports", "calls", "inherits", "validates", "invokes", "protects", "depends_on"
  ]);

  function normalizedQuery(value) {
    return String(value || "").trim().toLowerCase();
  }

  function create(initialGraph) {
    const state = {
      graph: initialGraph,
      nodesById: new Map(),
      childrenById: new Map(),
      edges: [],
      selectedId: "",
      collapsed: new Set(),
      focusMode: "all",
      focusNodes: new Set(),
      pathNodes: new Set(),
      pathEdges: new Set(),
      history: [],
      historyIndex: -1
    };

    function rebuildIndexes(graph) {
      state.graph = graph;
      state.nodesById = new Map();
      state.childrenById = new Map();
      state.edges = Array.isArray(graph.edges) ? graph.edges.slice() : [];
      (Array.isArray(graph.nodes) ? graph.nodes : []).forEach(function (node) {
        state.nodesById.set(node.id, node);
        const parentId = String(node.parent_id || "");
        if (parentId) {
          if (!state.childrenById.has(parentId)) {
            state.childrenById.set(parentId, []);
          }
          state.childrenById.get(parentId).push(node.id);
        }
      });
      state.collapsed = new Set(Array.from(state.collapsed).filter(function (id) {
        return state.nodesById.has(id);
      }));
      state.history = state.history.filter(function (id) {
        return state.nodesById.has(id);
      });
      state.historyIndex = Math.min(state.historyIndex, state.history.length - 1);
      if (!state.nodesById.has(state.selectedId)) {
        state.selectedId = "";
      }
      clearPath();
      state.focusMode = "all";
      state.focusNodes.clear();
    }

    function clearPath() {
      state.pathNodes.clear();
      state.pathEdges.clear();
    }

    function ancestorsOf(nodeId) {
      const result = [];
      const visited = new Set();
      let current = state.nodesById.get(nodeId);
      while (current) {
        const parentId = String(current.parent_id || "");
        if (!parentId || visited.has(parentId)) {
          break;
        }
        visited.add(parentId);
        result.push(parentId);
        current = state.nodesById.get(parentId);
      }
      return result;
    }

    function revealNode(nodeId) {
      ancestorsOf(nodeId).forEach(function (parentId) {
        state.collapsed.delete(parentId);
      });
    }

    function recordHistory(nodeId) {
      if (!nodeId) {
        return;
      }
      if (state.history[state.historyIndex] === nodeId) {
        return;
      }
      state.history = state.history.slice(0, state.historyIndex + 1);
      state.history.push(nodeId);
      if (state.history.length > 80) {
        state.history.shift();
      }
      state.historyIndex = state.history.length - 1;
    }

    function select(nodeId, record) {
      const normalized = String(nodeId || "");
      if (!state.nodesById.has(normalized)) {
        return { ok: false, message: "Selected node is unavailable." };
      }
      revealNode(normalized);
      state.selectedId = normalized;
      if (record !== false) {
        recordHistory(normalized);
      }
      return {
        ok: true,
        nodeId: normalized,
        message: "Focused " + state.nodesById.get(normalized).label + "."
      };
    }

    function isHiddenByCollapse(nodeId) {
      return ancestorsOf(nodeId).some(function (parentId) {
        return state.collapsed.has(parentId);
      });
    }

    function addAncestors(targetSet) {
      Array.from(targetSet).forEach(function (nodeId) {
        ancestorsOf(nodeId).forEach(function (parentId) {
          targetSet.add(parentId);
        });
      });
    }

    function visibleGraph() {
      let allowed = new Set(Array.from(state.nodesById.keys()).filter(function (nodeId) {
        return !isHiddenByCollapse(nodeId);
      }));
      if (state.focusMode !== "all") {
        const focused = new Set(state.focusNodes);
        addAncestors(focused);
        allowed = new Set(Array.from(allowed).filter(function (nodeId) {
          return focused.has(nodeId);
        }));
      }
      const nodes = Array.from(state.nodesById.values()).filter(function (node) {
        return allowed.has(node.id);
      });
      const edges = state.edges.filter(function (edge) {
        return allowed.has(edge.source) && allowed.has(edge.target);
      });
      return { nodes: nodes, edges: edges };
    }

    function isolateSelected(depth) {
      if (!state.selectedId) {
        return { ok: false, message: "Select a node before isolating it." };
      }
      const maximumDepth = Math.max(1, Math.min(3, Number(depth) || 1));
      const visited = new Set([state.selectedId]);
      let frontier = new Set([state.selectedId]);
      for (let level = 0; level < maximumDepth; level += 1) {
        const next = new Set();
        state.edges.forEach(function (edge) {
          if (frontier.has(edge.source) && !visited.has(edge.target)) {
            visited.add(edge.target);
            next.add(edge.target);
          }
          if (frontier.has(edge.target) && !visited.has(edge.source)) {
            visited.add(edge.source);
            next.add(edge.source);
          }
        });
        (state.childrenById.get(state.selectedId) || []).forEach(function (childId) {
          visited.add(childId);
        });
        frontier = next;
      }
      state.focusMode = "neighborhood";
      state.focusNodes = visited;
      clearPath();
      return {
        ok: true,
        nodeId: state.selectedId,
        message: "Isolated the selected node and depth " + maximumDepth + " neighborhood."
      };
    }

    function showOverview() {
      state.focusMode = "all";
      state.focusNodes.clear();
      clearPath();
      state.selectedId = "";
      return { ok: true, overview: true, message: "Returned to graph overview." };
    }

    function toggleSelectedExpansion() {
      if (!state.selectedId) {
        return { ok: false, message: "Select a package or module first." };
      }
      const children = state.childrenById.get(state.selectedId) || [];
      if (!children.length) {
        return { ok: false, message: "The selected node has no expandable children." };
      }
      if (state.collapsed.has(state.selectedId)) {
        state.collapsed.delete(state.selectedId);
        return { ok: true, expanded: true, nodeId: state.selectedId, message: "Expanded selected node." };
      }
      state.collapsed.add(state.selectedId);
      return { ok: true, expanded: false, nodeId: state.selectedId, message: "Collapsed selected node." };
    }

    function matchingNode(query) {
      const normalized = normalizedQuery(query);
      if (!normalized) {
        return null;
      }
      return Array.from(state.nodesById.values()).find(function (candidate) {
        return [candidate.label, candidate.id, candidate.relative_path, candidate.qualified_name]
          .join(" ").toLowerCase().includes(normalized);
      }) || null;
    }

    function adjacency(directed, includeContains) {
      const result = new Map();
      function add(source, target, edge) {
        if (!result.has(source)) {
          result.set(source, []);
        }
        result.get(source).push({ target: target, edge: edge });
      }
      state.edges.forEach(function (edge) {
        if (!includeContains && !PATH_RELATIONSHIPS.has(edge.relationship)) {
          return;
        }
        add(edge.source, edge.target, edge);
        if (!directed) {
          add(edge.target, edge.source, edge);
        }
      });
      return result;
    }

    function shortestPath(sourceId, targetId, directed, includeContains) {
      const graph = adjacency(directed, includeContains);
      const queue = [sourceId];
      const previous = new Map([[sourceId, null]]);
      while (queue.length) {
        const current = queue.shift();
        if (current === targetId) {
          break;
        }
        (graph.get(current) || []).forEach(function (step) {
          if (!previous.has(step.target)) {
            previous.set(step.target, { node: current, edge: step.edge });
            queue.push(step.target);
          }
        });
      }
      if (!previous.has(targetId)) {
        return null;
      }
      const nodeIds = [targetId];
      const edgeIds = [];
      let cursor = targetId;
      while (cursor !== sourceId) {
        const step = previous.get(cursor);
        if (!step) {
          return null;
        }
        edgeIds.push(step.edge.id);
        cursor = step.node;
        nodeIds.push(cursor);
      }
      nodeIds.reverse();
      edgeIds.reverse();
      return { nodeIds: nodeIds, edgeIds: edgeIds };
    }

    function tracePathToQuery(query) {
      if (!state.selectedId) {
        return { ok: false, message: "Select the source node before tracing a path." };
      }
      const target = matchingNode(query);
      if (!target) {
        return { ok: false, message: "No path target matched the search text." };
      }
      let path = shortestPath(state.selectedId, target.id, true, false);
      if (!path) {
        path = shortestPath(state.selectedId, target.id, false, false);
      }
      if (!path) {
        path = shortestPath(state.selectedId, target.id, false, true);
      }
      if (!path) {
        return { ok: false, message: "No relationship path was found." };
      }
      state.pathNodes = new Set(path.nodeIds);
      state.pathEdges = new Set(path.edgeIds);
      state.focusMode = "path";
      state.focusNodes = new Set(path.nodeIds);
      select(target.id, true);
      return {
        ok: true,
        nodeId: target.id,
        pathLength: path.edgeIds.length,
        message: "Displayed a " + path.edgeIds.length + "-edge path to " + target.label + "."
      };
    }

    function goBack() {
      if (state.historyIndex <= 0) {
        return { ok: false, message: "No earlier focus is available." };
      }
      state.historyIndex -= 1;
      state.focusMode = "all";
      state.focusNodes.clear();
      clearPath();
      return select(state.history[state.historyIndex], false);
    }

    function goForward() {
      if (state.historyIndex < 0 || state.historyIndex >= state.history.length - 1) {
        return { ok: false, message: "No later focus is available." };
      }
      state.historyIndex += 1;
      state.focusMode = "all";
      state.focusNodes.clear();
      clearPath();
      return select(state.history[state.historyIndex], false);
    }

    function capabilities() {
      return {
        canBack: state.historyIndex > 0,
        canForward: state.historyIndex >= 0 && state.historyIndex < state.history.length - 1,
        selectedId: state.selectedId,
        focusMode: state.focusMode,
        collapsedCount: state.collapsed.size
      };
    }

    rebuildIndexes(initialGraph || { nodes: [], edges: [] });
    return {
      setGraph: rebuildIndexes,
      select: select,
      selectedId: function () { return state.selectedId; },
      matchingNode: matchingNode,
      visibleGraph: visibleGraph,
      isolateSelected: isolateSelected,
      showOverview: showOverview,
      toggleSelectedExpansion: toggleSelectedExpansion,
      tracePathToQuery: tracePathToQuery,
      goBack: goBack,
      goForward: goForward,
      isPathNode: function (nodeId) { return state.pathNodes.has(nodeId); },
      isPathEdge: function (edgeId) { return state.pathEdges.has(edgeId); },
      capabilities: capabilities,
      revealNode: revealNode
    };
  }

  window.kandaGraphNavigation = { create: create };
}());
