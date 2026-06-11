"""
Whenever you need a button (or any trigger) to toggle a group of UI or plot elements on and off,
you can follow the same pattern. Below is a breakdown of the key ingredients and the sequence of actions,
illustrated on our Amplitude‐Map example. After that, you’ll find a generic ASCII pipeline you can reuse
for any set of components.


1. Maintain a Boolean “Visible” Flag

Every toggleable feature needs a piece of state, usually a self.visible or self.enabled boolean.
In our case:

# Initialized in __init__:
self.red_line_visible = False

This flag tells us, before we do anything, whether we should be in the ON branch or the OFF branch.

- Step 2: Create and wire the toggle button -Wiring the Button

In a factory method, instantiate your button and connect it to the toggle handler.
Create the button once and hook its clicked signal to your toggle method:


def create_toggle_button(self):
    btn = AnimatedShadowButton(text="Amplitude Map (µV)", …)
    btn.clicked.connect(self.toggle_red_line_and_maps)
    return btn

No logic lives here—just the connection.

- Step 3: Toggle method skeleton - The Toggle Method
Write a single method that flips the flag, branches into ON or OFF logic, and then redraws.
This is the heart. It does three things in sequence:

    Flip the flag

    Branch into ON or OFF logic

    Redraw or refresh

def toggle_red_line_and_maps(self):
    # 1. Flip the state
    self.red_line_visible = not self.red_line_visible

    # 2a. ON branch: prepare and show everything
    if self.red_line_visible:
        …  # create or reveal each element, reset trackers, update plot

    # 2b. OFF branch: hide and clean up everything
    else:
        …  # hide or remove each element, reset trackers

    # 3. Always redraw at the end
    self.visualizer.fig.canvas.draw_idle()


3a. ON Branch

Inside the if self.red_line_visible: block:

    Initialize any missing elements (axes, lines, windows)

    Reset any “last-seen” or caching flags so updates run fresh

    Show each element (e.g. axis.set_visible(True))

    Trigger an update routine to position/redraw every part

For our map:

if self.red_line_visible:
    if self.vline is None:
        self.vline = self.visualizer.ax.axvline(…)         # create red line
        self.connect_events()
    if not self.topomap_ax:
        self.initialize_topomap()                           # create map axes

    self.topomap_ax.set_visible(True)                      # show axes
    self.topomap_ax.set_title("Topographic Map")

    # Force full rebuild:
    self._last_topomap_time = None
    self._last_cbar_vmin    = None
    self._last_cbar_vmax    = None
    self.topomap_cbar       = None
    self.topomap_cbar_ax    = None

    # Position everything for the current time
    self.update_vline(self.vline.get_xdata()[0])

    # Show floating pro_filters
    if not self.floating_window:
        self._create_floating_window()
    else:
        self.floating_window.show()

3b. OFF Branch

Inside the else: block:

    Hide each element (set_visible(False))

    Remove any artists or windows you no longer need (.remove(), deleteLater())

    Clear any lists or trackers so memory can be freed

    Optionally, reset flags if you call this programmatically


else:
    if self.vline:
        self.vline.set_visible(False)

    if self.topomap_ax:
        self.topomap_ax.set_visible(False)

    # Hide and delete colorbar
    if self.topomap_cbar:
        self.topomap_cbar.remove()
        self.topomap_cbar = None
    if self.topomap_cbar_ax:
        self.topomap_cbar_ax.remove()
        self.topomap_cbar_ax = None

    # Hide floating window
    if self.floating_window:
        self.floating_window.hide()

    # Remove blue labels
    for txt in getattr(self.visualizer, 'amplitude_texts', []):
        safe_remove_artist(txt)
    self.visualizer.amplitude_texts = []


4. Putting It All Together: Reusable ASCII Pipeline
Below is a template you can adapt any time you need to toggle N components in sync:

[User clicks Toggle Button]
              ↓
      toggle_method():
              ↓
       self.visible = not self.visible
              ↓
   ┌──────────┴───────────┐
   │                      │
   ▼                      ▼
[ON branch]          [OFF branch]
   │                      │
   │─ initialize missing  │─ hide each component
   │  elements (if any)   │  (set_visible(False))
   │                      │
   │─ reset cache flags   │─ remove/destroy
   │  (e.g. last_time,    │  artists/windows
   │   last_colorbar)     │
   │                      │
   │─ make components     │─ clear lists/refs
   │  visible again       │  (so GC can free)
   │                      │
   │─ run update/redraw   │─ reset state flags
   │  routine             │  (if needed)
   │                      │
   └──────────┬───────────┘
              │
              ▼
    redraw canvas (draw_idle)

Key points to carry to any new toggle:

    State flag (self.visible) drives branching

    Initialization vs. reuse (create only once)

    Cache resets so updates truly rerun

    Symmetric cleanup (hide + remove)

    One canvas redraw at the very end

With that pattern in mind, whenever you show me a new button and a list of elements to toggle,
I can reproduce the same logic: flip the flag, branch, initialize or hide, reset caches,
call update, and redraw.


#### - Generalization - ####

- Step 1: Define a visibility flag -

In your class __init__, add a boolean attribute that tracks the ON/OFF state of the feature.

self.feature_visible = False

- Step 2: Create and wire the toggle button -

In a factory method, instantiate your button and connect it to the toggle handler.

def create_toggle_button(self):
    btn = SomeButton("Toggle Feature")
    btn.clicked.connect(self.toggle_feature)
    return btn

- Step 3: Toggle method skeleton -

Write a single method that flips the flag, branches into ON or OFF logic, and then redraws.

def toggle_feature(self):
    # 3.1 Flip the state
    self.feature_visible = not self.feature_visible

    # 3.2 Branch
    if self.feature_visible:
        # … ON branch …
    else:
        # … OFF branch …

    # 3.3 Redraw at end
    self.canvas.draw_idle()

- Step 4: ON branch – initialize, reset, show, update -

Inside the if self.feature_visible: block:

# 4.1 Create missing elements only once
if self.elem is None:
    self.elem = create_element()

# 4.2 Reset any caching flags so updates always run
self._last_update_time = None
self.cached_obj       = None

# 4.3 Make elements visible
self.elem.set_visible(True)

# 4.4 Call your update routine to position/redraw
self.update_feature(self.current_parameter)

- Step 5: OFF branch – hide, remove, clear -

Inside the else: block:

# 5.1 Hide each element
if self.elem:
    self.elem.set_visible(False)

# 5.2 Remove or destroy artists/windows
if self.elem_artist:
    self.elem_artist.remove()
    self.elem_artist = None

# 5.3 Clear lists or trackers
self.elem_list = []

- Step 6: Final canvas redraw -

After the ON/OFF branches, always call:

self.canvas.draw_idle()

- Step 7: ASCII pipeline overview -

[User clicks Toggle Button]
              ↓
      toggle_feature()
              ↓
       self.feature_visible = not self.feature_visible
              ↓
   ┌──────────┴───────────┐
   │                      │
   ▼                      ▼
[ON branch]          [OFF branch]
   │                      │
   │─ 4.1 init elems      │─ 5.1 hide elems
   │─ 4.2 reset caches    │─ 5.2 remove artists
   │─ 4.3 show elems      │─ 5.3 clear trackers
   │─ 4.4 update feature  │
   └──────────┬───────────┘
              │
              ▼
     6. redraw canvas

 If you provide:

    The names (or types) of the UI/plot components you want to toggle

    Any “last seen” or cache flags you’re using

    The update routine (e.g. update_feature(...)) that draws or positions them

    Whether you need any cleanup (e.g. .remove(), deleteLater())

I can template out the exact toggle_feature() method for you—complete
with numbered steps, ####-style comments, and an ASCII pipeline.
Just send me those details and I’ll build your specific on/off logic.

"""

