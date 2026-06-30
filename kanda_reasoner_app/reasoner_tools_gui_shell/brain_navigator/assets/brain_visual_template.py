# project-path: kanda_reasoner_app/reasoner_tools_gui_shell/brain_navigator/assets/brain_visual_template.py
"""HTML asset template for the visible Neural Architecture brain view."""
from __future__ import annotations
from html import escape
from .brain_mesh_data import get_brain_mesh_data_js
from .brain_visual_floating_window import (
    build_neural_architecture_floating_window_data_js,
)
from .brain_visual_floating_window_template import (
    build_floating_remember_window_css,
    build_floating_remember_window_runtime_js,
)
from .brain_visual_markers import build_neural_architecture_marker_data_js
from .brain_visual_spec import get_neural_architecture_visual_spec
__all__ = [
    "build_neural_architecture_asset_preview_html",
]
QWEBCHANNEL_SCRIPT_URL = "qrc:///qtwebchannel/qwebchannel.js"
THREE_JS_SCRIPT_URL = "https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"
def _render_title_html() -> str:
    """Render the frozen multiline title overlay."""
    spec = get_neural_architecture_visual_spec()
    return "\n".join(
        f"<div class=\"title-line title-line-{index}\">{escape(line)}</div>"
        for index, line in enumerate(spec.title_lines, start=1)
    )
def build_neural_architecture_asset_preview_html() -> str:
    """Build complete HTML for the Neural Architecture brain visual."""
    spec = get_neural_architecture_visual_spec()
    title_html = _render_title_html()
    footer_text = escape(spec.footer_text)
    mesh_data_js = get_brain_mesh_data_js()
    marker_data_js = build_neural_architecture_marker_data_js()
    floating_window_data_js = build_neural_architecture_floating_window_data_js()
    floating_window_css = build_floating_remember_window_css()
    floating_window_runtime_js = build_floating_remember_window_runtime_js()
    responsive_requirements = repr(list(spec.responsive_requirements))
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(spec.title_lines[0])}</title>
<script src="{QWEBCHANNEL_SCRIPT_URL}"></script>
<script src="{THREE_JS_SCRIPT_URL}"></script>
<style>
* {{ box-sizing: border-box; }}
html, body {{
    margin: 0;
    padding: 0;
    width: 100%;
    height: 100%;
    overflow: hidden;
    background: #e6e8ec;
    font-family: 'Courier New', monospace;
}}
#brain-stage {{
    position: relative;
    width: 100vw;
    height: 100vh;
    overflow: hidden;
    background: #e6e8ec;
}}
#brain-stage canvas {{
    position: absolute;
    inset: 0;
    z-index: 1;
    width: 100%;
    height: 100%;
    display: block;
}}
#hud-title {{
    position: absolute;
    top: 18px;
    left: 50%;
    transform: translateX(-50%);
    z-index: 10;
    text-align: center;
    pointer-events: none;
    white-space: nowrap;
    color: rgba(15, 35, 76, 0.94);
    letter-spacing: 4px;
    text-transform: uppercase;
}}
.title-line-1 {{ font-size: 18px; font-weight: 800; }}
.title-line-2 {{ font-size: 11px; margin-top: 5px; }}
.title-line-3 {{ font-size: 10px; margin-top: 5px; }}
.pulse-marker {{
    position: absolute;
    z-index: 20;
    width: 11px;
    height: 11px;
    border-radius: 999px;
    background: #082a72;
    border: 1px solid rgba(185, 215, 255, 0.9);
    box-shadow: 0 0 12px rgba(8, 42, 114, 0.72);
    transform: translate(-50%, -50%);
    animation: markerPulseSlow 2.8s ease-in-out infinite;
    cursor: pointer;
}}
.pulse-marker::after {{
    content: "";
    position: absolute;
    inset: -7px;
    border-radius: inherit;
    border: 1px solid rgba(8, 42, 114, 0.45);
    animation: markerRippleSlow 2.8s ease-out infinite;
}}
.pulse-marker:hover,
.pulse-marker.is-hovered {{
    background: #d9001b;
    box-shadow: 0 0 18px rgba(217, 0, 27, 0.92);
    animation: markerPulseFast 0.82s ease-in-out infinite;
}}
.pulse-marker:hover::after,
.pulse-marker.is-hovered::after {{
    border-color: rgba(217, 0, 27, 0.62);
    animation: markerRippleFast 0.82s ease-out infinite;
}}
@keyframes markerPulseSlow {{
    0%, 100% {{ transform: translate(-50%, -50%) scale(0.88); }}
    50% {{ transform: translate(-50%, -50%) scale(1.08); }}
}}
@keyframes markerRippleSlow {{
    0% {{ transform: scale(0.45); opacity: 0.7; }}
    100% {{ transform: scale(2.6); opacity: 0; }}
}}
@keyframes markerPulseFast {{
    0%, 100% {{ transform: translate(-50%, -50%) scale(0.92); }}
    50% {{ transform: translate(-50%, -50%) scale(1.26); }}
}}
@keyframes markerRippleFast {{
    0% {{ transform: scale(0.45); opacity: 0.95; }}
    100% {{ transform: scale(3.2); opacity: 0; }}
}}
#region-tip {{
    position: absolute;
    z-index: 30;
    display: none;
    padding: 6px 10px;
    border: 1.5px solid rgba(255, 132, 0, 0.95);
    border-radius: 8px;
    background: rgba(245, 247, 252, 0.94);
    color: rgba(0, 92, 255, 0.98);
    font-size: 10px;
    letter-spacing: 3px;
    text-transform: uppercase;
    font-weight: 700;
    pointer-events: none;
    white-space: nowrap;
    box-shadow: 0 3px 10px rgba(20, 35, 60, 0.14);
}}
{floating_window_css}
#footer-easter-egg {{
    position: absolute;
    left: 50%;
    bottom: 10px;
    transform: translateX(-50%);
    z-index: 10;
    color: rgba(0, 132, 255, 0.62);
    font-size: 10px;
    letter-spacing: 1.5px;
    pointer-events: none;
}}
</style>
</head>
<body>
<div id="brain-stage" data-visual-mode="neural_architecture_brain">
    <div id="hud-title" aria-label="Neural Architecture title">
{title_html}
    </div>
    <div id="region-tip"></div>
    <div id="floatingRegionWindow" role="dialog" aria-modal="false"></div>
    <div id="footer-easter-egg">{footer_text}</div>
</div>
<script>
{mesh_data_js}
{marker_data_js}
{floating_window_data_js}
const RESPONSIVE_REQUIREMENTS = {responsive_requirements};
let renderer = null;
let camera = null;
let projectedMarkers = [];
let brain = null;
let telPts = null;
let cerbPts = null;
let midPts = null;
let edgeLines = null;
let drag = false;
let wasDrag = false;
let pointerX = 0;
let pointerY = 0;
let downX = 0;
let downY = 0;
let animationTick = 0;
let lastFrameTime = 0;
const TARGET_FPS = 25;
const FRAME_INTERVAL_MS = 1000 / TARGET_FPS;
const BRAIN_REFERENCE_SCALE_BEFORE_FIT_PATCH = 1.70;
const BRAIN_RENDER_SCALE = BRAIN_REFERENCE_SCALE_BEFORE_FIT_PATCH * 0.70;
const BRAIN_GHOST_SPHERE_RADIUS = 1.34;
const TELENCEPHALON_COLOR = 0x005cff;
const CEREBELLUM_COLOR = 0x00aa40;
const MIDBRAIN_COLOR = 0xff8400;
let brainCenter = null;
let brainSize = null;
let markerSurfaceClouds = null;
function callBrainBridgeHover(regionId) {{
    if (window.brainNavigatorBridge && window.brainNavigatorBridge.onRegionHovered) {{
        window.brainNavigatorBridge.onRegionHovered(regionId);
    }}
}}
function callBrainBridgeClick(regionId) {{
    if (window.brainNavigatorBridge && window.brainNavigatorBridge.onRegionClicked) {{
        window.brainNavigatorBridge.onRegionClicked(String(regionId || "")); return true;
    }}
    return false;
}}
function retryPendingBrainNavigatorOpen() {{
    if (!window.pendingBrainNavigatorOpenRegionId) {{ return; }}
    if (callBrainBridgeClick(window.pendingBrainNavigatorOpenRegionId)) {{ window.pendingBrainNavigatorOpenRegionId = ""; }}
}}
function callBrainBridgeOpenModule(regionId) {{
    const delivered = callBrainBridgeClick(regionId);
    const statusElement = document.querySelector(".floating-remember-window-status");
    if (statusElement) {{ statusElement.textContent = delivered ? "Opening mapped module" : "Bridge connecting - click again"; }}
    if (!delivered) {{ window.pendingBrainNavigatorOpenRegionId = String(regionId || ""); window.setTimeout(function() {{ retryPendingBrainNavigatorOpen(); }}, 180); }}
    return delivered;
}}
function showRegionTip(label, clientX, clientY) {{
    const regionTip = document.getElementById("region-tip");
    if (!regionTip) {{ return; }}
    regionTip.textContent = label;
    regionTip.style.display = "block";
    regionTip.style.left = Math.min(clientX + 14, window.innerWidth - 260) + "px";
    regionTip.style.top = Math.max(8, clientY - 18) + "px";
}}
function hideRegionTip() {{
    const regionTip = document.getElementById("region-tip");
    if (!regionTip) {{ return; }}
    regionTip.style.display = "none";
}}
{floating_window_runtime_js}
function applyMarkerScreenPosition(markerElement, markerData) {{
    markerElement.style.left = markerData.x_percent + "%";
    markerElement.style.top = markerData.y_percent + "%";
}}
function applyProjectedMarkerScreenPosition(markerElement, screenPosition) {{
    markerElement.style.left = screenPosition.left + "px";
    markerElement.style.top = screenPosition.top + "px";
    markerElement.style.display = screenPosition.isVisible ? "block" : "none";
}}
function createNeuralArchitecturePulseMarker(markerData) {{
    const markerElement = document.createElement("button");
    markerElement.type = "button";
    markerElement.className = "pulse-marker";
    markerElement.dataset.regionId = markerData.region_id;
    markerElement.dataset.regionName = markerData.region_name;
    markerElement.setAttribute("aria-label", markerData.region_name);
    applyMarkerScreenPosition(markerElement, markerData);
    const anchorLocal = resolveMarkerSurfaceAnchorLocal(markerData);
    markerElement.addEventListener("mouseenter", function(event) {{
        markerElement.classList.add("is-hovered");
        showRegionTip(markerData.region_name, event.clientX, event.clientY);
        callBrainBridgeHover(markerData.region_id);
    }});
    markerElement.addEventListener("mousemove", function(event) {{
        showRegionTip(markerData.region_name, event.clientX, event.clientY);
    }});
    markerElement.addEventListener("mouseleave", function() {{
        markerElement.classList.remove("is-hovered");
        hideRegionTip();
    }});
    markerElement.addEventListener("click", function(event) {{
        event.preventDefault();
        event.stopPropagation();
        showFloatingRememberWindow(markerData, event.clientX, event.clientY);
    }});
    return {{
        element: markerElement,
        regionId: markerData.region_id,
        anchorLocal: anchorLocal,
        updateScreenPosition: function() {{
            if (anchorLocal && brain && camera) {{
                const screenPosition = projectBrainLocalPointToScreen(anchorLocal);
                applyProjectedMarkerScreenPosition(markerElement, screenPosition);
            }} else {{
                applyMarkerScreenPosition(markerElement, markerData);
            }}
        }},
    }};
}}
function createNeuralArchitecturePulseMarkers() {{
    const stage = document.getElementById("brain-stage");
    if (!stage) {{ return; }}
    if (projectedMarkers.length) {{ return; }}
    NEURAL_ARCHITECTURE_PULSE_MARKERS.forEach(function(markerData) {{
        const marker = createNeuralArchitecturePulseMarker(markerData);
        stage.appendChild(marker.element);
        projectedMarkers.push(marker);
    }});
    window.neuralArchitecturePulseMarkers = projectedMarkers;
}}
function updateProjectedMarkers() {{
    projectedMarkers.forEach(function(marker) {{
        if (marker && marker.updateScreenPosition) {{
            marker.updateScreenPosition();
        }}
    }});
}}
function stageSize() {{
    const stage = document.getElementById("brain-stage");
    return {{
        width: Math.max(1, stage ? stage.clientWidth : window.innerWidth),
        height: Math.max(1, stage ? stage.clientHeight : window.innerHeight),
    }};
}}
function makePositions(flat, scale) {{
    const out = new Float32Array(flat.length);
    for (let i = 0; i < flat.length; i++) {{ out[i] = flat[i] * scale; }}
    return out;
}}
function sampleFlatTriples(flat, keepRatio) {{
    if (keepRatio >= 0.999) {{ return flat; }}
    const out = [];
    const total = Math.floor(flat.length / 3);
    const step = Math.max(1, Math.round(1 / keepRatio));
    for (let i = 0; i < total; i++) {{
        if ((i % step) === 0) {{
            const j = i * 3;
            out.push(flat[j], flat[j + 1], flat[j + 2]);
        }}
    }}
    return out;
}}
function sampleLineSegments(flat, keepRatio) {{
    if (keepRatio >= 0.999) {{ return flat; }}
    const out = [];
    const totalSegs = Math.floor(flat.length / 6);
    const step = Math.max(1, Math.round(1 / keepRatio));
    for (let i = 0; i < totalSegs; i++) {{
        if ((i % step) === 0) {{
            const j = i * 6;
            out.push(flat[j], flat[j + 1], flat[j + 2], flat[j + 3], flat[j + 4], flat[j + 5]);
        }}
    }}
    return out;
}}
function buildPointRegion(flat, colorValue, pointSize, scale) {{ const geometry = new THREE.BufferGeometry(); geometry.setAttribute("position", new THREE.BufferAttribute(makePositions(flat, scale), 3)); const material = new THREE.PointsMaterial({{ color: colorValue, size: pointSize, sizeAttenuation: true, transparent: true, opacity: 0.95, depthWrite: false }}); return new THREE.Points(geometry, material); }}
function buildMeshLines(flat, scale) {{ const geometry = new THREE.BufferGeometry(); geometry.setAttribute("position", new THREE.BufferAttribute(makePositions(flat, scale), 3)); const material = new THREE.LineBasicMaterial({{ color: 0x000000, transparent: true, opacity: 0.30, depthWrite: false }}); return new THREE.LineSegments(geometry, material); }}
function vectorsFromFlat(flat, scale) {{ const out = []; for (let i = 0; i < flat.length; i += 3) {{ out.push(new THREE.Vector3(flat[i] * scale, flat[i + 1] * scale, flat[i + 2] * scale)); }} return out; }}
function buildMarkerSurfaceClouds(scale) {{ return {{ telencephalon: vectorsFromFlat(TEL_PTS, scale), cerebellum: vectorsFromFlat(CERB_PTS, scale), midbrain: vectorsFromFlat(MID_PTS, scale) }}; }}
function rawBrainPoint(nx, ny, nz) {{ return new THREE.Vector3(brainCenter.x + nx * brainSize.x * 0.5, brainCenter.y + ny * brainSize.y * 0.5, brainCenter.z + nz * brainSize.z * 0.5); }}
function nearestSurfacePoint(target, cloud, preferredSide) {{ let best = null; let bestD2 = Infinity; const side = preferredSide || 0; for (let i = 0; i < cloud.length; i++) {{ const p = cloud[i]; if (side !== 0) {{ const pSide = (p.x - brainCenter.x) < 0 ? -1 : 1; if (pSide !== side) {{ continue; }} }} const dx = p.x - target.x; const dy = p.y - target.y; const dz = p.z - target.z; const d2 = dx * dx + dy * dy + dz * dz; if (d2 < bestD2) {{ bestD2 = d2; best = p; }} }} if (!best && side !== 0) {{ return nearestSurfacePoint(target, cloud, 0); }} return best ? best.clone() : null; }}
function resolveMarkerSurfaceAnchorLocal(markerData) {{ if (!brainCenter || !brainSize || !markerSurfaceClouds) {{ return null; }} const cloudName = markerData.surface_cloud || "telencephalon"; const cloud = markerSurfaceClouds[cloudName] || markerSurfaceClouds.telencephalon; if (!cloud) {{ return null; }} const target = rawBrainPoint(markerData.anchor_x, markerData.anchor_y, markerData.anchor_z); const surfacePoint = nearestSurfacePoint(target, cloud, markerData.preferred_side || 0); if (!surfacePoint) {{ return null; }} const local = surfacePoint.sub(brainCenter); const lift = markerData.anchor_lift || 1.024; return local.multiplyScalar(lift); }}
function projectBrainLocalPointToScreen(anchorLocal) {{ const size = stageSize(); const point = anchorLocal.clone(); brain.localToWorld(point); point.project(camera); const left = (point.x * 0.5 + 0.5) * size.width; const top = (-point.y * 0.5 + 0.5) * size.height; const isVisible = point.z > -1.0 && point.z < 1.0 && left >= -32 && left <= size.width + 32 && top >= -32 && top <= size.height + 32; return {{ left: left, top: top, isVisible: isVisible }}; }}
function initializeNeuralArchitectureBrain() {{
    if (typeof THREE === "undefined") {{
        console.warn("Three.js unavailable; Neural Architecture brain renderer skipped.");
        createNeuralArchitecturePulseMarkers();
        return;
    }}
    const stage = document.getElementById("brain-stage");
    if (!stage) {{ return; }}
    const size = stageSize();
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0xe6e8ec);
    camera = new THREE.PerspectiveCamera(40, size.width / size.height, 0.05, 100);
    camera.position.set(0, 0.10, 4.05);
    renderer = new THREE.WebGLRenderer({{ antialias: true, alpha: false }});
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
    renderer.setSize(size.width, size.height);
    stage.insertBefore(renderer.domElement, stage.firstChild);
    const scale = BRAIN_RENDER_SCALE;
    brain = new THREE.Group();
    const brainContent = new THREE.Group();
    telPts = buildPointRegion(sampleFlatTriples(TEL_PTS, 0.78), TELENCEPHALON_COLOR, 0.020, scale);
    cerbPts = buildPointRegion(sampleFlatTriples(CERB_PTS, 0.90), CEREBELLUM_COLOR, 0.021, scale);
    midPts = buildPointRegion(sampleFlatTriples(MID_PTS, 1.00), MIDBRAIN_COLOR, 0.025, scale);
    edgeLines = buildMeshLines(sampleLineSegments(EDGE_PTS, 0.55), scale);
    brainContent.add(telPts);
    brainContent.add(cerbPts);
    brainContent.add(midPts);
    brainContent.add(edgeLines);
    const preCenterBounds = new THREE.Box3().setFromObject(brainContent);
    brainCenter = new THREE.Vector3();
    brainSize = new THREE.Vector3();
    preCenterBounds.getCenter(brainCenter);
    preCenterBounds.getSize(brainSize);
    markerSurfaceClouds = buildMarkerSurfaceClouds(scale);
    brainContent.position.sub(brainCenter);
    brain.add(brainContent);
    brain.rotation.set(0.08, -0.15, -0.05);
    scene.add(brain);
    const ghostMaterial = new THREE.MeshBasicMaterial({{
        color: 0x7e8796,
        transparent: true,
        opacity: 0.045,
        side: THREE.BackSide,
        depthWrite: false,
    }});
    scene.add(new THREE.Mesh(new THREE.SphereGeometry(BRAIN_GHOST_SPHERE_RADIUS, 28, 18), ghostMaterial));
    window.neuralArchitectureScene = scene;
    createNeuralArchitecturePulseMarkers();
    resizeNeuralArchitectureStage();
    attachBrainPointerHandlers();
    requestAnimationFrame(loopNeuralArchitectureBrain);
}}
function fitBrainToViewport() {{
    if (!camera) {{ return; }}
    const size = stageSize();
    const minSide = Math.min(size.width, size.height);
    let distance = 3.45;
    if (size.width < 1220 || size.height < 760 || minSide < 700) {{
        distance = 4.10;
    }}
    if (minSide < 560) {{
        distance = 4.65;
    }}
    camera.position.set(0, 0.10, distance);
    camera.lookAt(0, 0, 0);
    camera.updateProjectionMatrix();
}}
function resizeNeuralArchitectureStage() {{
    const stage = document.getElementById('brain-stage');
    const width = Math.max(1, stage ? stage.clientWidth : window.innerWidth);
    const height = Math.max(1, stage ? stage.clientHeight : window.innerHeight);
    if (renderer && renderer.setSize) {{
        renderer.setSize(width, height);
    }}
    if (camera) {{
        camera.aspect = width / height;
        camera.updateProjectionMatrix();
        fitBrainToViewport();
    }}
    updateProjectedMarkers();
}}
function attachBrainPointerHandlers() {{
    if (!renderer || !renderer.domElement || !brain) {{ return; }}
    const canvas = renderer.domElement;
    canvas.addEventListener("mousedown", function(event) {{
        drag = true;
        wasDrag = false;
        pointerX = event.clientX;
        pointerY = event.clientY;
        downX = event.clientX;
        downY = event.clientY;
        hideRegionTip();
    }});
    window.addEventListener("mouseup", function() {{ drag = false; }});
    window.addEventListener("mouseleave", function() {{ drag = false; hideRegionTip(); }});
    window.addEventListener("mousemove", function(event) {{
        if (!drag || !brain) {{ return; }}
        const dx0 = event.clientX - downX;
        const dy0 = event.clientY - downY;
        if ((dx0 * dx0 + dy0 * dy0) > 9) {{ wasDrag = true; }}
        brain.rotation.y += (event.clientX - pointerX) * 0.008;
        brain.rotation.x += (event.clientY - pointerY) * 0.008;
        pointerX = event.clientX;
        pointerY = event.clientY;
    }});
}}
function loopNeuralArchitectureBrain(now) {{
    requestAnimationFrame(loopNeuralArchitectureBrain);
    if (!renderer || !camera || !window.neuralArchitectureScene || !brain) {{ return; }}
    if (!lastFrameTime) {{ lastFrameTime = now; return; }}
    const elapsed = now - lastFrameTime;
    if (elapsed < FRAME_INTERVAL_MS) {{ return; }}
    const safeElapsed = Math.min(elapsed, 100);
    animationTick += 0.007 * (safeElapsed / 16.6667);
    lastFrameTime = now - (elapsed % FRAME_INTERVAL_MS);
    if (!drag) {{
        brain.rotation.y = animationTick * 0.22 - 0.15;
        brain.rotation.x = Math.sin(animationTick * 0.22) * 0.045 + 0.08;
    }}
    if (telPts && telPts.material) {{ telPts.material.opacity = 0.91 + 0.06 * Math.abs(Math.sin(animationTick * 0.85)); }}
    if (cerbPts && cerbPts.material) {{ cerbPts.material.opacity = 0.91 + 0.06 * Math.abs(Math.sin(animationTick * 0.75 + 1.4)); }}
    if (midPts && midPts.material) {{ midPts.material.opacity = 0.91 + 0.06 * Math.abs(Math.sin(animationTick * 0.95 + 2.1)); }}
    updateProjectedMarkers();
    renderer.render(window.neuralArchitectureScene, camera);
}}
initializeNeuralArchitectureBrain();
window.addEventListener("resize", resizeNeuralArchitectureStage);
window.addEventListener("orientationchange", resizeNeuralArchitectureStage);
document.addEventListener("keydown", function(event) {{
    if (event.key === "Escape") {{
        hideFloatingRememberWindow();
    }}
}});
document.addEventListener("click", function(event) {{
    const floatingWindow = document.getElementById("floatingRegionWindow");
    if (!floatingWindow || floatingWindow.style.display === "none") {{ return; }}
    if (!floatingWindow.contains(event.target) && !event.target.classList.contains("pulse-marker")) {{
        hideFloatingRememberWindow();
    }}
}});
</script>
</body>
</html>
"""
