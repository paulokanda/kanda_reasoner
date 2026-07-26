(function () {
  "use strict";

  const host = document.getElementById("graph3dHost");
  const root = document.getElementById("visualizerRoot");
  const status = document.getElementById("sceneStatus");
  const browserDetails = document.getElementById("browserDetailsBody");
  const vendor = window.__KANDA_VENDOR_MANIFEST__ || {};
  const state = {
    graph: window.__KANDA_GRAPH_SNAPSHOT__,
    generationId: String(window.__KANDA_GRAPH_GENERATION__ || ""),
    embedded: Boolean(window.__KANDA_EMBEDDED__),
    navigation: null,
    selectedId: "",
    hoveredId: "",
    bridge: null,
    engine: null,
    renderedNodes: new Map(),
    resizeObserver: null,
    fitTimers: [],
    viewportReady: false,
    viewportWidth: 0,
    viewportHeight: 0,
    activationGeneration: ""
  };

  state.navigation = window.kandaGraphNavigation.create(state.graph);
  if (state.embedded) {
    root.classList.add("embedded");
  }

  function edgeEndpointId(value) {
    if (value && typeof value === "object") {
      return String(value.id || "");
    }
    return String(value || "");
  }

  const painter = window.kandaGraphPainter.create({
    isSelected: function (nodeId) { return String(nodeId) === state.selectedId; },
    isHovered: function (nodeId) { return String(nodeId) === state.hoveredId; },
    isPathNode: function (nodeId) { return state.navigation.isPathNode(String(nodeId)); },
    isPathEdge: function (edgeId) { return state.navigation.isPathEdge(String(edgeId)); },
    isSelectedEdge: function (edge) {
      if (!state.selectedId) {
        return false;
      }
      return edgeEndpointId(edge.source) === state.selectedId ||
        edgeEndpointId(edge.target) === state.selectedId;
    }
  });

  function notifyBridge(methodName, args) {
    if (window.kandaQtBridge) {
      window.kandaQtBridge.notify(methodName, args);
    }
  }

  function connectQtBridge() {
    if (!state.embedded || !window.kandaQtBridge) {
      return false;
    }
    return window.kandaQtBridge.connect(
      state.generationId,
      function (bridge) {
        state.bridge = bridge;
        notifyBridge("onRendererReady", [state.generationId]);
      },
      function (message) {
        status.textContent = "Renderer bridge error";
        notifyBridge("onRendererError", [state.generationId, message]);
      }
    );
  }

  function updateBrowserDetails(node) {
    if (!state.embedded && window.kandaBrowserDetails) {
      window.kandaBrowserDetails.update(browserDetails, node);
    }
  }

  function publishSelection(node) {
    updateBrowserDetails(node);
    if (node) {
      notifyBridge("onNodeSelected", [state.generationId, node.id]);
    } else {
      notifyBridge("onBackgroundSelected", [state.generationId]);
    }
  }

  function sourceNode(nodeId) {
    return (state.graph.nodes || []).find(function (candidate) {
      return candidate.id === nodeId;
    }) || null;
  }

  function visibleStatus() {
    const visible = state.navigation.visibleGraph();
    const capabilities = state.navigation.capabilities();
    status.textContent = visible.nodes.length + " visible nodes | " +
      visible.edges.length + " visible edges | " + capabilities.focusMode +
      " | local 3d-force-graph " + String(vendor.package_version || "unknown");
  }

  function cloneNode(node) {
    const position = Array.isArray(node.position) ? node.position : [0, 0, 0];
    const x = Number(position[0]) || 0;
    const y = Number(position[1]) || 0;
    const z = Number(position[2]) || 0;
    return Object.assign({}, node, {
      x: x, y: y, z: z,
      fx: x, fy: y, fz: z
    });
  }

  function cloneLink(edge) {
    return Object.assign({}, edge, {
      source: String(edge.source || ""),
      target: String(edge.target || "")
    });
  }

  function resizeRenderer() {
    const rect = host.getBoundingClientRect();
    const width = Math.floor(rect.width);
    const height = Math.floor(rect.height);
    const wasReady = state.viewportReady;
    if (!state.engine || width < 32 || height < 32) {
      state.viewportReady = false;
      return { ready: false, width: width, height: height, recovered: false };
    }
    state.engine.width(width).height(height);
    state.viewportReady = true;
    state.viewportWidth = width;
    state.viewportHeight = height;
    return { ready: true, width: width, height: height, recovered: !wasReady };
  }

  function ensureRenderer() {
    if (state.engine) {
      return state.engine;
    }
    if (typeof window.ForceGraph3D !== "function") {
      throw new Error("Pinned local 3d-force-graph did not expose ForceGraph3D.");
    }
    state.engine = new window.ForceGraph3D(host, {
      controlType: "orbit",
      rendererConfig: { antialias: true, alpha: true }
    });
    state.engine
      .backgroundColor("rgba(0,0,0,0)")
      .showNavInfo(false)
      .nodeId("id")
      .nodeColor(painter.nodeColor)
      .nodeVal(painter.nodeValue)
      .nodeLabel(painter.nodeLabel)
      .nodeOpacity(0.88)
      .linkSource("source")
      .linkTarget("target")
      .linkColor(painter.linkColor)
      .linkWidth(painter.linkWidth)
      .linkOpacity(painter.linkOpacity)
      .linkDirectionalArrowLength(painter.arrowLength)
      .linkDirectionalArrowRelPos(1)
      .linkDirectionalParticles(painter.particleCount)
      .linkDirectionalParticleWidth(2.2)
      .warmupTicks(0)
      .cooldownTicks(1)
      .cooldownTime(250)
      .onNodeHover(function (node) {
        state.hoveredId = node ? String(node.id) : "";
        state.engine.refresh();
      })
      .onNodeClick(function (node) {
        if (node) {
          focusNodeById(String(node.id), true);
        }
      })
      .onBackgroundClick(function () {
        state.navigation.showOverview();
        state.selectedId = "";
        publishSelection(null);
        refreshVisibleGraph();
      });
    resizeRenderer();
    if (typeof window.ResizeObserver === "function") {
      state.resizeObserver = new window.ResizeObserver(function () {
        activateViewport(false);
      });
      state.resizeObserver.observe(host);
    } else {
      window.addEventListener("resize", function () { activateViewport(false); });
    }
    return state.engine;
  }

  function refreshVisibleGraph() {
    const engine = ensureRenderer();
    const visible = state.navigation.visibleGraph();
    const nodes = visible.nodes.map(cloneNode);
    const links = visible.edges.map(cloneLink);
    state.renderedNodes = new Map(nodes.map(function (node) {
      return [String(node.id), node];
    }));
    engine.graphData({ nodes: nodes, links: links });
    engine.refresh();
    visibleStatus();
    return { nodes: nodes, links: links };
  }

  function selectNodeById(nodeId, recordHistory) {
    const normalized = String(nodeId || "");
    const result = state.navigation.select(normalized, recordHistory !== false);
    if (!result.ok) {
      return result;
    }
    state.selectedId = normalized;
    publishSelection(sourceNode(normalized));
    refreshVisibleGraph();
    return result;
  }

  function focusNodeById(nodeId, recordHistory) {
    const result = selectNodeById(nodeId, recordHistory);
    if (!result.ok) {
      return result;
    }
    const node = state.renderedNodes.get(String(nodeId));
    if (!node || !state.engine) {
      return result;
    }
    const distance = 150;
    const norm = Math.hypot(node.x, node.y, node.z);
    let camera;
    if (norm > 0.001) {
      const ratio = 1 + distance / norm;
      camera = { x: node.x * ratio, y: node.y * ratio, z: node.z * ratio };
    } else {
      camera = { x: 0, y: 0, z: distance };
    }
    state.engine.cameraPosition(camera, node, 550);
    return result;
  }

  function fitGraph() {
    ensureRenderer();
    state.fitTimers.forEach(window.clearTimeout);
    state.fitTimers = [80, 320, 900].map(function (delay, index) {
      return window.setTimeout(function () {
        if (state.engine && state.viewportReady) {
          state.engine.resumeAnimation();
          state.engine.refresh();
          state.engine.zoomToFit(index === 1 ? 350 : 0, 48);
        }
      }, delay);
    });
    return { ok: true, message: "Fit the visible graph." };
  }

  function resetCamera() {
    const result = state.navigation.showOverview();
    state.selectedId = "";
    publishSelection(null);
    refreshVisibleGraph();
    fitGraph();
    return result;
  }

  function focusByQuery(query) {
    const node = state.navigation.matchingNode(query);
    if (!node) {
      return false;
    }
    return Boolean(focusNodeById(node.id, true).ok);
  }

  function applyNavigationResult(result, focusSelection) {
    if (!result || !result.ok) {
      return result || { ok: false, message: "Navigation action failed." };
    }
    if (result.overview) {
      state.selectedId = "";
      publishSelection(null);
      refreshVisibleGraph();
      fitGraph();
      return result;
    }
    if (result.nodeId) {
      state.selectedId = String(result.nodeId);
      publishSelection(sourceNode(state.selectedId));
    }
    refreshVisibleGraph();
    if (focusSelection && result.nodeId) {
      focusNodeById(result.nodeId, false);
    }
    return result;
  }

  function isolateSelected() {
    return applyNavigationResult(state.navigation.isolateSelected(1), false);
  }

  function showOverview() {
    return applyNavigationResult(state.navigation.showOverview(), false);
  }

  function toggleSelectedExpansion() {
    return applyNavigationResult(state.navigation.toggleSelectedExpansion(), false);
  }

  function tracePathToQuery(query) {
    return applyNavigationResult(state.navigation.tracePathToQuery(query), true);
  }

  function goBack() {
    return applyNavigationResult(state.navigation.goBack(), true);
  }

  function goForward() {
    return applyNavigationResult(state.navigation.goForward(), true);
  }

  function navigationState() {
    const visible = state.navigation.visibleGraph();
    const capabilities = state.navigation.capabilities();
    return {
      selectedId: capabilities.selectedId,
      focusMode: capabilities.focusMode,
      collapsedCount: capabilities.collapsedCount,
      canBack: capabilities.canBack,
      canForward: capabilities.canForward,
      visibleNodeCount: visible.nodes.length,
      visibleEdgeCount: visible.edges.length,
      pathNodeCount: visible.nodes.filter(function (node) {
        return state.navigation.isPathNode(node.id);
      }).length,
      pathEdgeCount: visible.edges.filter(function (edge) {
        return state.navigation.isPathEdge(edge.id);
      }).length
    };
  }


  function rendererDiagnostics() {
    const rect = host.getBoundingClientRect();
    const renderer = state.engine && state.engine.renderer();
    const canvas = renderer && renderer.domElement;
    const data = state.engine ? state.engine.graphData() : { nodes: [], links: [] };
    const scene = state.engine && state.engine.scene();
    return {
      ok: true, ready: state.viewportReady, generationId: state.generationId,
      hostWidth: Math.floor(rect.width), hostHeight: Math.floor(rect.height),
      canvasWidth: canvas ? canvas.width : 0, canvasHeight: canvas ? canvas.height : 0,
      graphNodeCount: (data.nodes || []).length, graphEdgeCount: (data.links || []).length,
      sceneChildCount: scene && scene.children ? scene.children.length : 0
    };
  }

  function activateViewport(forceFit) {
    const engine = ensureRenderer();
    const dimensions = resizeRenderer();
    if (!dimensions.ready) {
      return Object.assign(rendererDiagnostics(), { ok: false, retry: true });
    }
    engine.resumeAnimation();
    engine.refresh();
    if (forceFit || dimensions.recovered || state.activationGeneration !== state.generationId) {
      state.activationGeneration = state.generationId;
      fitGraph();
    }
    return Object.assign(rendererDiagnostics(), { retry: false });
  }

  function rendererIdentity() {
    return {
      provider: "3d-force-graph",
      version: String(vendor.package_version || ""),
      local: true,
      assetSha256: String(vendor.asset_sha256 || ""),
      renderer: "WebGL"
    };
  }

  function hasWebGLRenderer() {
    if (!state.engine || typeof state.engine.renderer !== "function") {
      return false;
    }
    const renderer = state.engine.renderer();
    return Boolean(renderer && renderer.domElement && renderer.getContext());
  }

  function setGraph(graph, generationId) {
    if (!graph || !Array.isArray(graph.nodes) || !Array.isArray(graph.edges)) {
      notifyBridge("onRendererError", [
        String(generationId || ""),
        "Renderer received an invalid graph snapshot."
      ]);
      return false;
    }
    state.graph = graph;
    state.generationId = String(generationId || "");
    state.navigation.setGraph(graph);
    state.selectedId = state.navigation.selectedId();
    state.hoveredId = "";
    refreshVisibleGraph();
    updateBrowserDetails(null);
    activateViewport(true);
    notifyBridge("onRendererReady", [state.generationId]);
    return true;
  }

  function bindBrowserControls() {
    const controls = document.getElementById("browserNavigation");
    if (!controls || state.embedded) {
      return;
    }
    controls.addEventListener("click", function (event) {
      const button = event.target.closest("button[data-command]");
      if (!button) {
        return;
      }
      const query = document.getElementById("browserPathQuery");
      const methods = {
        back: goBack,
        forward: goForward,
        overview: showOverview,
        isolate: isolateSelected,
        expand: toggleSelectedExpansion,
        path: function () { return tracePathToQuery(query ? query.value : ""); }
      };
      const method = methods[button.getAttribute("data-command")];
      if (method) {
        const result = method();
        status.textContent = result && result.message ?
          result.message : "Navigation updated.";
      }
    });
  }

  window.kandaProjectGraph = {
    ensureBridge: connectQtBridge,
    fitGraph: fitGraph,
    resetCamera: resetCamera,
    focusByQuery: focusByQuery,
    isolateSelected: isolateSelected,
    showOverview: showOverview,
    toggleSelectedExpansion: toggleSelectedExpansion,
    tracePathToQuery: tracePathToQuery,
    goBack: goBack,
    goForward: goForward,
    navigationState: navigationState,
    rendererIdentity: rendererIdentity,
    hasWebGLRenderer: hasWebGLRenderer,
    rendererDiagnostics: rendererDiagnostics,
    activateViewport: activateViewport,
    setGraph: setGraph
  };

  document.addEventListener("visibilitychange", function () {
    if (!document.hidden) {
      activateViewport(true);
    }
  });

  window.addEventListener("keydown", function (event) {
    if (event.key === "Escape") {
      showOverview();
    } else if (event.altKey && event.key === "ArrowLeft") {
      goBack();
    } else if (event.altKey && event.key === "ArrowRight") {
      goForward();
    }
  });

  try {
    bindBrowserControls();
    ensureRenderer();
    setGraph(state.graph, state.generationId);
    connectQtBridge();
  } catch (error) {
    status.textContent = "Local WebGL renderer error";
    notifyBridge("onRendererError", [
      state.generationId,
      error instanceof Error ? error.message : String(error)
    ]);
    throw error;
  }
}());
