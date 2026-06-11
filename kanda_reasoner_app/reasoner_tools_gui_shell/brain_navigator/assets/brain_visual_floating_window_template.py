"""Floating Remember Box CSS and JavaScript template fragments."""

from __future__ import annotations

__all__ = [
    "build_floating_remember_window_css",
    "build_floating_remember_window_runtime_js",
]


def build_floating_remember_window_css() -> str:
    """Return CSS for the Neural Architecture floating Fancy Index."""

    return """#floatingRegionWindow {
    position: absolute;
    z-index: 40;
    display: none;
    max-width: min(460px, 88vw);
    padding: 17px 19px 16px 19px;
    border: 1.5px solid rgba(255, 132, 0, 0.95);
    border-radius: 14px;
    background: rgba(245, 247, 252, 0.97);
    color: #10244d;
    box-shadow: 0 16px 40px rgba(20, 35, 60, 0.24);
    backdrop-filter: blur(7px);
    font-family: 'Courier New', monospace;
    pointer-events: auto;
}
.floating-remember-window-kicker {
    color: rgba(0, 92, 255, 0.98);
    font-size: 9px;
    letter-spacing: 3px;
    text-transform: uppercase;
    font-weight: 800;
}
.floating-remember-window-title {
    margin-top: 6px;
    color: #0a1d45;
    font-size: 15px;
    line-height: 1.25;
    font-weight: 800;
}
.floating-remember-window-module {
    margin-top: 8px;
    color: #0f3478;
    font-size: 11px;
    line-height: 1.35;
    font-weight: 700;
}
.floating-remember-window-purpose {
    margin-top: 10px;
    color: #182c55;
    font-size: 11px;
    line-height: 1.45;
}
.floating-remember-window-status {
    margin-top: 12px;
    display: inline-block;
    padding: 5px 8px;
    border: 1px solid rgba(0, 132, 255, 0.28);
    border-radius: 999px;
    color: rgba(0, 92, 255, 0.85);
    background: rgba(0, 132, 255, 0.08);
    font-size: 9px;
    letter-spacing: 1px;
    text-transform: uppercase;
}

.floating-remember-window-actions {
    margin-top: 14px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 10px;
}
.floating-remember-window-action {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-width: 128px;
    cursor: pointer;
    user-select: none;
    border: 1px solid rgba(255, 132, 0, 0.82);
    border-radius: 999px;
    padding: 7px 12px;
    color: #ffffff;
    background: linear-gradient(135deg, rgba(255, 132, 0, 0.96), rgba(0, 92, 255, 0.92));
    font-family: 'Courier New', monospace;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    box-shadow: 0 8px 18px rgba(20, 40, 90, 0.20);
}
.floating-remember-window-action:hover {
    filter: brightness(1.08);
    transform: translateY(-1px);
}
.floating-remember-window-action:active {
    filter: brightness(0.98);
    transform: translateY(0px);
}
.floating-remember-window-route {
    color: rgba(15, 52, 120, 0.78);
    font-size: 9px;
    line-height: 1.35;
    text-transform: uppercase;
    letter-spacing: 1px;
}
"""


def build_floating_remember_window_runtime_js() -> str:
    """Return JavaScript helpers for click-open floating Remember Boxes."""

    return """function escapeFloatingWindowHtml(value) {
    return String(value || "")
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/\"/g, "&quot;")
        .replace(/'/g, "&#39;");
}
function findFloatingRememberWindowData(regionId) {
    return NEURAL_ARCHITECTURE_FLOATING_WINDOWS.find(function(windowData) {
        return windowData.region_id === regionId;
    });
}
function hideFloatingRememberWindow() {
    const floatingWindow = document.getElementById("floatingRegionWindow");
    if (!floatingWindow) { return; }
    floatingWindow.style.display = "none";
    floatingWindow.innerHTML = "";
}
function positionFloatingRememberWindow(floatingWindow, clientX, clientY) {
    const margin = 14;
    floatingWindow.style.left = "0px";
    floatingWindow.style.top = "0px";
    floatingWindow.style.display = "block";
    const width = floatingWindow.offsetWidth || 420;
    const height = floatingWindow.offsetHeight || 220;
    const preferredLeft = clientX + 20;
    const preferredTop = clientY - 24;
    const left = Math.max(margin, Math.min(preferredLeft, window.innerWidth - width - margin));
    const top = Math.max(margin, Math.min(preferredTop, window.innerHeight - height - margin));
    floatingWindow.style.left = left + "px";
    floatingWindow.style.top = top + "px";
}
function showFloatingRememberWindow(markerData, clientX, clientY) {
    const floatingWindow = document.getElementById("floatingRegionWindow");
    if (!floatingWindow) { return; }
    const windowData = findFloatingRememberWindowData(markerData.region_id) || {
        region_name: markerData.region_name,
        target_tab_label: "No mapped module",
        analogy_title: "No mapping available",
        purpose_text: "This marker has no floating explanation payload yet.",
        action_state: "No module action available.",
        action_label: "Open module",
    };
    floatingWindow.innerHTML = [
        '<div class="floating-remember-window-kicker">Brain structure</div>',
        '<div class="floating-remember-window-title">' + escapeFloatingWindowHtml(windowData.region_name) + '</div>',
        '<div class="floating-remember-window-module">Mapped module: ' + escapeFloatingWindowHtml(windowData.target_tab_label) + '</div>',
        '<div class="floating-remember-window-purpose"><strong>' + escapeFloatingWindowHtml(windowData.analogy_title) + '</strong><br>' + escapeFloatingWindowHtml(windowData.purpose_text) + '</div>',
        '<div class="floating-remember-window-status">' + escapeFloatingWindowHtml(windowData.action_state) + '</div>',
        '<div class="floating-remember-window-actions">',
        '<button type="button" class="floating-remember-window-action" title="Open mapped module" aria-label="Open mapped module" data-region-id="' + escapeFloatingWindowHtml(windowData.region_id) + '">' + escapeFloatingWindowHtml(windowData.action_label || "Open module") + '</button>',
        '<div class="floating-remember-window-route">Stable tab-id route<br>via injected controller</div>',
        '</div>',
    ].join("");
    const actionButton = floatingWindow.querySelector(".floating-remember-window-action");
    if (actionButton) {
        actionButton.addEventListener("click", function(event) {
            event.preventDefault();
            event.stopPropagation();
            const delivered = callBrainBridgeOpenModule(windowData.region_id);
            actionButton.dataset.lastDeliveryState = delivered ? "delivered" : "bridge_pending";
        });
    }
    positionFloatingRememberWindow(floatingWindow, clientX, clientY);
}
"""
