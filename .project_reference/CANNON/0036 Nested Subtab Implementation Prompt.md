BLUEPRINT: Nested Subtab Implementation Prompt

Use this template to request the addition of local subtabs inside any existing parent tab. It separates visual/positional rules, styling, and per-subtab content.
1. PARENT TAB CONTEXT

    Parent Tab Name: [e.g., Architecture Review, Settings, Data Inspector]

    Parent Label / Header: [e.g., "Architecture Review" in bold]

    Subtab Positioning: [e.g., Immediately below the parent label, anchored to the left, inside the parent container]

2. GLOBAL SUBTAB STYLING (Ear / Header)

    Ear Alignment: [e.g., Horizontal row, vertical stack]

    Active Ear Color: [e.g., Blue, #0055FF]

    Inactive Ear Color: [e.g., Green, #00AA00]

    Additional Ear Styling: [e.g., Rounded corners, underline animation, bold text on active]

3. SUBTAB DEFINITIONS

For each subtab you want, provide an entry following this structure.
Subtab [Number]: [Subtab Name]

    Unique ID: [e.g., tab-project-audit]

    Default State: [e.g., Active by default / Inactive]

3.1 UI Controls (Buttons, Inputs, Dropdowns):
(List every interactive element in this subtab)

    [Control Type] – [Label] – [Action / Behavior]

        Example: Button – Run Select Mode – Executes the selected audit mode

        Example: Checkbox – Require confirm before write – Toggles confirmation popup

        Example: Dropdown – Target by – Selects the target module for analysis

3.2 Primary Display Area:

    Type: [e.g., Large text log, AST tree viewer, Data table, Graph]

    Content Source: [e.g., Shows output of the active control, specifically only X results]

    Scrolling / Resizing: [e.g., Vertical scroll, fixed height, resizable]

3.3 Optional Metadata:

    Grouping / Layout: [e.g., Controls are arranged in a horizontal toolbar above the display area]

    Visibility Rule: [e.g., This subtab is hidden if the user lacks admin rights]

4. BEHAVIORAL RULES (Switching Logic)

    Switching Trigger: [e.g., Click on the ear / tab header]

    Content Swap: [e.g., The display area and controls refresh instantly; previous state persists if revisited]

    State Preservation: [e.g., Selected options in an inactive subtab are saved when switching away and back]

5. EXAMPLE MAPPING (Your Original Request)

To illustrate, here is how your specific Architecture Review request fits this blueprint:
Blueprint Field	Your Original Value
Parent Tab Name	Architecture Review
Parent Label	"Architecture Review" in bold
Subtab Positioning	Below the bold label
Active Ear Color	Blue
Inactive Ear Color	Green
Subtab 1	
Name	Run Selected Mode / Project Audit
Controls	Run select mode, Cancel, Run option mode, Get, Require confirm before write, Clear audit results, Save audit results in mode, Mode help, Project audit results, Include latest refactor report evidence, Copy audit results, Large module creation refactor protocol
Display Area	Large log text window (shows general audit results)
Subtab 2	
Name	Large Module AST Split Audit
Controls	Large module AST split audit inactive (status), Target by, Run validate to populate, Large modules (list), Copy path, Arrow buttons, Browse target, Run AST split audit, Copy split, Handoff for AI
Display Area	Large text window (shows ONLY AST split audit results)
How to use this blueprint

    Fill in the sections with your specific tab requirements.

    Present it to your developer or AI assistant as a single prompt.

    The blueprint ensures all visual, interactive, and behavioral details are captured, leaving no ambiguity about subtab placement, colors, controls, or content.

This template is UI-framework agnostic—whether you are building with React, Vue, Qt, or raw HTML/CSS, it translates cleanly into a concrete implementation task.
