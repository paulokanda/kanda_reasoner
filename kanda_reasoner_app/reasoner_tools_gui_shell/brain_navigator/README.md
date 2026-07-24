# Brain Navigator Box

Status: visible Neural Architecture brain with safe fallback index available

## Responsibility

The Brain Navigator box owns the first-tab brain homepage experience. It
currently provides a safe fallback index that maps brain structures to app tools
and a lazy Qt WebChannel bridge scaffold for the future rotating web brain.

The fallback remains intentionally simple: it uses normal Qt widgets only, does not load QWebEngine, and does not import the future brain mesh asset.

## Public contract

Public imports must go through:

```text
kanda_reasoner_app.reasoner_tools_gui_shell.brain_navigator.contract
```

Current public symbols:

```text
BRAIN_NAVIGATOR_BOX_ID
BRAIN_NAVIGATOR_TAB_ID
BRAIN_NAVIGATOR_TAB_LABEL
BrainNavigatorContractSummary
get_brain_navigator_contract_summary
create_brain_navigator_tab
create_brain_web_bridge
build_brain_web_channel_bootstrap_script
normalize_brain_region_id
get_brain_web_bridge_summary
```

`create_brain_navigator_tab` lazily imports the fallback widget factory so
importing the public contract does not require PySide6 or QWebEngine.

`create_brain_web_bridge` lazily creates the internal QObject and QWebChannel
bridge for future web content. The bridge emits intent only and does not switch
tabs directly.

## Visible fallback behavior

The fallback first tab shows:

```text
Brain Navigator title
brain-structure to app-tool index
Remember Box explanation card
Open tool button
```

Selecting a brain structure updates the Remember Box card. Pressing Open Tool
requests navigation by stable `tab_id` through an injected callback. The Brain
Navigator does not call `setCurrentIndex` and does not know notebook indexes.

## Brain Web Bridge behavior

The bridge exposes JavaScript-callable slots:

```text
onRegionHovered(region_id)
onRegionClicked(region_id)
onBrainClicked()
```

The bridge emits Qt signals:

```text
regionHovered(region_id)
regionClicked(region_id)
```

The no-argument `onBrainClicked()` slot is a legacy compatibility path for the
uploaded demo brain page. Future web brain content should call the region-aware
slots.

## Forbidden responsibilities

The Brain Navigator box must not own:

```text
tab switching internals
tab registry internals
prompt library logic
engineering safety logic
workflow review logic
architecture review logic
other tab internals
```

## Current dependencies

Allowed public-contract dependencies:

```text
Brain Region Mapping Box
Remember Box
Tab Navigation Controller callback injected by the GUI shell
Qt WebChannel bridge internals loaded lazily only when requested
```

Forbidden dependencies in the public contract:

```text
main_window internals
tool_specs internals
QWebEngine
other tab internals
```

## Future sub-boxes

Planned next boxes:

```text
Brain Asset Box
Fancy Index Box
Web Brain View Box
```

## Freeze condition

This bridge scaffold is freezeable when:

```text
focused bridge tests pass
fallback and first-tab regression tests pass
py_compile passes for changed files
workflow validation remains clean
architecture validation remains clean
manual GUI confirmation is performed before visual behavior is frozen
```

## Patch 7 - WebView scaffold dry-run

The Brain Navigator now includes an internal WebView scaffold sub-box. This is
not wired into the visible first tab yet. The visible fallback index remains the
active GUI path until the WebView is manually validated.

The scaffold can build a local HTML test surface with brain-region buttons, load
it into a QWebEngineView, attach the Brain Web Bridge through QWebChannel, and
emit region intent through onRegionHovered(region_id) and onRegionClicked(region_id).

The scaffold does not switch tabs, import MainWindow, inspect the tab registry,
or mutate any other tab.


## Patch 8 - Brain asset extraction

Patch 8 extracts the uploaded Neural Architecture brain prototype into inert,
project-owned Brain Navigator assets. The extracted asset is not wired into the
visible first tab yet. The visible fallback index remains the active GUI path.

New asset files:

```text
assets/brain_mesh_data.py
assets/brain_visual_spec.py
assets/brain_visual_template.py
```

The mesh data asset preserves the rebuilt `male_brain.glb` metadata from the
uploaded prototype:

```text
source vertices: 2605
source faces: 4850
surface dots: 9255
visible edges: 3724
```

The frozen future title is:

```text
Neural Architecture
of
Knowledge and Architecture Navigator for Developer Assistance (KANDA)
```

The frozen footer text is:

```text
What is the airspeed velocity of an unladen swallow?
```

The visual asset also freezes the marker behavior for later patches:

```text
dark blue slow pulsing circle by default
ripple waves from each circle
live red fast pulse on hover
hover label appears only over the marker
left click opens a floating explanation window
click outside or Escape closes the floating window
```

Responsive layout is now a hard requirement. The future brain must fit the available tab space, preserve aspect ratio, avoid clipping, and update renderer,
camera, and projected marker positions when the window is resized. The asset
preview template includes the expected resize contract:

```text
window.addEventListener("resize", resizeNeuralArchitectureStage)
renderer.setSize(width, height)
camera.aspect = width / height
camera.updateProjectionMatrix()
updateProjectedMarkers()
```

Patch 8 does not switch tabs, does not import MainWindow, does not inspect the
tab registry, and does not replace the fallback Brain Navigator tab.


## Patch 9 - Isolated Neural Architecture WebView preview

Patch 9 adds a manual preview-only WebView path for the extracted Neural
Architecture visual asset. The preview loads the project-owned asset HTML into a
QWebEngineView, attaches the Brain Web Bridge through QWebChannel, and keeps the
visible fallback index as the default first-tab GUI path.

New internal preview file:

```text
_neural_architecture_preview.py
```

New public lazy contract functions:

```text
build_neural_architecture_preview_html
create_neural_architecture_preview
get_neural_architecture_preview_summary
```

The preview is manual only and not wired into the visible first tab. It is used
to validate that the extracted brain asset page can be loaded safely before any
default GUI replacement.

The preview preserves the responsive requirement:

```text
window.addEventListener("resize", resizeNeuralArchitectureStage)
renderer.setSize(width, height)
camera.aspect = width / height
camera.updateProjectionMatrix()
updateProjectedMarkers()
```

The preview does not switch tabs, does not import MainWindow, does not inspect
the tab registry, and does not replace the fallback Brain Navigator tab.

Manual preview launcher:

```text
workbench/manual_preview/run_neural_architecture_preview.ps1
```


## Patch 10 - Responsive pulse marker layer

Patch 10 adds a manual-preview-only pulse marker layer on top of the extracted
Neural Architecture brain asset. The visible Brain Navigator fallback tab remains
the safe default.

Marker behavior:

- default state: small dark blue slow pulsing circle
- ripple waves radiate from each circle
- hover state: live red faster pulse
- hover shows only the neuroanatomic label
- hover emits `onRegionHovered(region_id)` through the Brain Web Bridge
- left click emits `onRegionClicked(region_id)` through the Brain Web Bridge
- floating Remember Box windows are intentionally deferred to the next patch

Responsive behavior:

- marker anchors use normalized stage percentages
- `updateProjectedMarkers()` reapplies marker positions after resize
- markers remain preview-only and do not switch tabs directly

Patch 10 does not replace the visible first tab, does not import `main_window`,
does not call `setCurrentIndex`, and does not inspect tab internals.



## Patch 11 - Visible Neural Architecture default tab

Patch 11 promotes the Neural Architecture WebView to the normal visible Brain
Navigator tab. The page should no longer show the text-heavy fallback index by
default. The visible page title is now rendered inside the brain visual as:

```text
Neural Architecture
of
Knowledge and Architecture Navigator for Developer Assistance (KANDA)
```

The fallback index remains available only if WebEngine or the brain visual cannot
be created. That fallback still does not load QWebEngine and still does not call
`setCurrentIndex`.

The visible default brain view uses the extracted mesh asset, the responsive
Three.js renderer, the pulse-marker layer, the QWebChannel bridge, and the
footer Easter egg. It must fit the available tab space and update renderer,
camera, and markers on resize.

Patch 11 does not add floating Remember Box windows yet and does not switch tabs
from inside the WebView.

## Patch 12 - Floating Remember Box window layer

Patch 12 adds click-open floating Remember Box windows to the visible Neural
Architecture brain. A left click on a pulse marker opens a professional floating
window near the marker.

Each floating window shows:

```text
brain structure label
mapped module label
analogy title
purpose text
module-opening action status
```

The floating Remember Box window closes when the user clicks outside it or
presses Escape. Opening a second marker replaces the visible explanation.

Patch 12 intentionally does not switch tabs, does not open modules, does not
call setCurrentIndex, and does not import MainWindow or other tab internals. The
Open Module wiring remains deferred to the next patch so this layer can be
validated independently.

## Patch 13 - Visual fit and neuroanatomic marker correction

Patch 13 adjusts the visible Neural Architecture brain after manual visual
feedback. The brain render scale is reduced to 70 percent of the previous
visual scale so the whole brain fits inside the tab without clipping. The
occipital lobe receives a yellow posterior-superior highlight while the
cerebellum remains green and separated from the posterior telencephalon.

The pulse marker anchors are repositioned according to the current rendered
model orientation and lateral neuroanatomic relationships: frontal/anterior,
central sulcus between frontal and parietal, lateral sulcus above temporal,
occipital posterior-superior, and cerebellum posterior-inferior on the
separate lobulated structure. This patch does not add module opening, does not
switch tabs, and does not import `main_window`.


## Patch 14 - Restored colors and mesh-anchored anatomy markers

Patch 14 corrects the previous anatomy assumption. In this mesh, x is
hemisphere side, y is superior-inferior, and z is anterior-posterior. The patch
therefore stops treating the screen left-right axis as the anterior-posterior
axis.

The visual scale from Patch 13 is kept because the brain size fits correctly.
The incorrect yellow occipital overlay is removed and the original mesh colors
are restored: telencephalon blue, cerebellum green, and midbrain/brainstem
orange.

Pulse markers now use anatomical 3D anchors. At runtime each anchor is snapped
to the corresponding mesh surface cloud and then projected into screen space on
every animation frame. This means the markers are snapped to the mesh and
projected every frame, so they rotate with the brain instead of staying fixed as
2D overlay percentages.

This patch does not add module opening, does not switch tabs, and does not
import `main_window`, `tool_specs`, or other tab internals.


## Patch 15 - Mesh-anchor marker refinement

Patch 15 keeps the corrected 70 percent brain fit and the mesh-anchored marker
system, but refines several anatomical anchors after manual GUI review.

Refinements:

```text
frontal_lobe -> moved to a frontopolar, most-anterior position
parietal_lobe -> lowered from the crown to a more central superior cerebrum position
brainstem_midbrain -> lowered into the middle of the trunk-like structure
occipital_lobe -> lowered on the posterior cerebrum above the cerebellum
cerebellum -> lowered and centered toward the vermis between the two cerebellar lobules
cerebellar_folia -> lowered onto the cerebellar mass itself
```

Patch 15 preserves the no-navigation boundary. It does not open modules, switch
tabs directly, import MainWindow, or alter the floating-window navigation state.


## Patch 16 - Floating Fancy Index open-module action

Patch 16 promotes the click-open floating explanation surface into a small
professional Fancy Index. Marker click still opens the floating index, but it
no longer opens a module immediately.

The floating index now contains an explicit Open module action. Pressing that
button emits the marker region id through the Brain Web Bridge. The Python-side
visible tab adapter resolves the region through the public Brain Region Mapping
contract and calls the injected stable-tab callback.

Boundary rules preserved:

```text
WebView knows region ids only
WebView does not know tab ids or tab indexes
Brain Navigator does not call setCurrentIndex
MainWindow and tool_specs internals are not imported
unknown or unmapped regions fail safely without navigation
```


## Patch 17 - Open module button hardening

Patch 17 keeps the floating Fancy Index behavior but hardens the Open module
control so it is not just a visual label. The action is rendered as an explicit
button with pointer events, title, aria label, active/hover styling, and a small
bridge-connection retry path.

Behavior:

```text
marker click -> opens floating Fancy Index only
Open module button click -> requests mapped tab navigation through the bridge
bridge not ready -> button status changes to bridge connecting and retries once
known region -> Python adapter resolves target tab through Brain Region Mapping
unknown region -> no-op safe failure
```

Patch 17 preserves the Box Architecture route: the WebView emits only the region
ID, Python resolves the target through the public mapping contract, and tab
opening still uses only the injected stable-tab callback.


## Patch 18 - Open module bridge lifetime hardening

Patch 18 fixes the runtime path where the floating Fancy Index appears but the
Open module button does not reach Python. The HTML button remains unchanged; the
hardening is on the Python WebChannel lifetime boundary.

The visible Neural Architecture tab now keeps a strong reference to the preview
bundle, and the preview widget/WebView keep strong references to the
QWebChannel bridge bundle. This prevents the QObject bridge from being garbage
collected after the factory returns.

This patch still uses only the injected stable-tab callback and the Brain Region
Mapping public contract. It does not import MainWindow, inspect tab widgets, or
call setCurrentIndex directly.

## Patch 19 - Final Brain Navigator freeze snapshot

Patch 19 is a polish and freeze-snapshot patch. It does not change the working
runtime behavior from the previous bridge-lifetime fix. It records the validated
Brain Navigator interaction chain as a public snapshot:

```text
normal app opens the Neural Architecture brain tab
brain keeps the corrected 70 percent fit scale
markers stay mesh-anchored and rotate with the model
marker click opens the floating Fancy Index only
Open module emits region intent through QWebChannel
Python resolves the region through the public Brain Region Mapping contract
navigation uses only the injected stable-tab callback
```

The final flow remains inside the Box Architecture boundary: no direct numeric
tab switching, no MainWindow import, no tool_specs reach-in, and no WebView
knowledge of tab indexes. The safe Qt fallback index remains available only if
WebEngine or visual creation fails.

## Floating window lifecycle and readability correction

The floating brain-region information window is transient page state. It now
closes automatically whenever the Brain Navigator page is hidden, including
manual tab changes and successful Open module navigation. The close request is
owned by the Brain Navigator preview wrapper and calls only the page-local
`hideFloatingRememberWindow()` JavaScript helper. It does not connect to
MainWindow, inspect tab indexes, or add an application-scoped signal owner.

The floating window now uses a readable Windows-first system font stack and
larger text sizes for the title, mapped module, explanation, status, route, and
action label. Brain geometry, marker coordinates, catalog mappings, colors, and
QWebChannel routing remain unchanged.
