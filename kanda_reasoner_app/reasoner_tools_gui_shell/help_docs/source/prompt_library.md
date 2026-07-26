# Prompt Library

First-Time User Tutorial

Prompt Library is a read-only dashboard for finding, reviewing, and copying the current governed KANDA prompts.

![Prompt Library canonical vault](../assets/drawings/prompt_library_opener_canonical_vault.png)

Image note:

- Subject: A curated prompt library organized as protected cards, books, and drawers.
- Asset path: `assets/drawings/prompt_library_opener_canonical_vault.png`.
- Alt text: Three colleagues browse organized prompt cards around a glowing reference book in a warm KANDA study.
- Caption: Prompt Library helps you find and reuse current prompts without turning the browser into an editor or runtime.
- Artwork status: `primary_contextual_prompt_library_raster`.

## What Prompt Library Means

Prompt Library presents the current active prompt collection in a visual, read-only dashboard.

**In plain English:** It is a governed bookshelf. You may browse prompts, read them, copy one prompt, copy a complete group stack, and open the source folder. You do not edit or run prompts from this tab.

## What This Tab Does

Prompt Library lets you:

1. load the current canonical prompt workspace;
2. use the legacy package library only as compatibility fallback;
3. see one cube for each current prompt group;
4. open a group in a floating window;
5. review prompt titles and metadata;
6. preview the full prompt text;
7. copy the selected prompt;
8. copy the full group stack in defined order;
9. open the selected prompt's file location;
10. reload the canonical library;
11. read status and source information.

## What This Tab Does Not Do

Prompt Library does not:

- edit prompt text;
- create prompts;
- delete prompts;
- execute prompts;
- send prompts to an AI;
- change prompt governance;
- activate deprecated prompts;
- rewrite prompt metadata;
- decide routing;
- bypass lifecycle rules.

<div class="callout callout-note">
<div class="callout-icon">1</div>
<div><strong>Use Prompt Library to find, learn, preview, and copy.</strong> Authoring, lifecycle changes, validation, and governance remain owned by their existing source workflows.</div>
</div>

## Canonical Workspace and Legacy Fallback

The tab prefers the governed canonical workspace:

`kanda_prompt_workspace/prompt_library`

When that workspace contains `ACTIVE_PROMPTS`, it becomes the source of the dashboard.

When the canonical workspace is unavailable, the tab may use the package-owned Prompt Library as a legacy compatibility fallback.

The status line clearly reports which source was loaded.

### Canonical workspace

The status message includes:

`canonical workspace`

### Legacy fallback

The status message includes:

`legacy compatibility fallback`

The fallback keeps the tab usable, but it should not be mistaken for the preferred governed source.

## Current Prompts Only

The canonical scan is limited to `ACTIVE_PROMPTS`.

The loader hides entries whose metadata status is:

- archived;
- deprecated;
- inactive;
- retired;
- superseded.

It also hides entries with:

`load_type=never`

README files and folder-assimilation notes are not treated as prompts.

<div class="callout callout-warning">
<div class="callout-icon">!</div>
<div><strong>Hidden does not mean deleted.</strong> Retired or deprecated prompt files may still exist in governed storage, but they are intentionally absent from the current dashboard.</div>
</div>

## Reload Canonical Library

Click **Reload Canonical Library** when:

- active prompt files changed;
- prompt metadata changed;
- the group catalog changed;
- the canonical workspace became available;
- the dashboard looks stale.

Reload performs a fresh read of current groups and current prompts.

It does not edit any prompt file.

## The Group Cube Dashboard

![Prompt Library active group cubes](../assets/drawings/prompt_library_active_group_cubes.png)

Image note:

- Subject: Current active prompt groups represented as distinct organized cubes.
- Asset path: `assets/drawings/prompt_library_active_group_cubes.png`.
- Alt text: Three colleagues inspect colorful active prompt-group cubes while retired, archived, and deprecated collections remain stored separately.
- Caption: Each dashboard cube represents one current Prompt Library group.
- Artwork status: `primary_contextual_prompt_library_raster`.

Each visible cube represents one current group from the group catalog.

A group has:

- group identifier;
- display name;
- description;
- color role;
- ordered prompt identifiers;
- copy-stack setting;
- floating-window setting.

The dashboard also shows the number of current prompts matched to each group.

### Why groups matter

Groups keep prompts together by purpose or workflow.

The group catalog defines the intended prompt order.

That order matters when copying a complete stack.

### Opening a group

Activate a cube to open its floating read-only group window.

The main status line changes to:

`Opened group window: <group name>`

## The Group Window

![Prompt Library group browser](../assets/drawings/prompt_library_group_browser.png)

Image note:

- Subject: Reviewing one prompt group with prompt list, metadata, preview, and copying actions.
- Asset path: `assets/drawings/prompt_library_group_browser.png`.
- Alt text: Three colleagues review a read-only prompt binder, metadata card, selected prompt, and full group stack in a warm library.
- Caption: Select a prompt to read its metadata and full text before copying it.
- Artwork status: `primary_contextual_prompt_library_raster`.

The group window contains:

- group heading;
- group description;
- Copy Selected Prompt;
- Copy Full Group Stack;
- Open File Location;
- Close;
- prompt list;
- metadata panel;
- full text preview;
- status message.

## Prompt List

The left list shows the current prompts assigned to the selected group.

The displayed title comes from metadata when possible.

When no metadata title is available, the filename becomes a readable title.

Selecting a prompt updates both the metadata panel and the full text preview.

## Metadata Panel

The metadata panel may show:

- Group;
- Title;
- Category;
- Relative path;
- Metadata filename;
- prompt ID;
- version;
- status;
- load type;
- project-agnostic state;
- explainer;
- how-it-works description.

Metadata helps you understand what the prompt is and whether it is appropriate before copying it.

## Full Text Preview

The preview panel displays the selected prompt's complete text.

The preview is read-only.

Review the prompt before copying it.

Pay attention to:

- stated purpose;
- required context;
- input assumptions;
- output expectations;
- order requirements;
- safety boundaries;
- references to other prompts;
- project-specific versus project-agnostic language.

## Copy Selected Prompt

Click **Copy Selected Prompt** to copy the full text of the currently selected prompt to the system clipboard.

The status line reports:

`Copied prompt text: <relative path>`

This action copies text only.

It does not run the prompt or send it anywhere.

## Copy Full Group Stack

Click **Copy Full Group Stack** to copy every current prompt in the group in group-defined order.

The stack builder:

1. follows the group's ordered prompt IDs;
2. includes current matching prompts;
3. separates prompts clearly;
4. preserves the intended group sequence.

The status line reports:

`Copied full group stack: <group name>`

Use the full stack only when the target workflow expects the complete group.

Do not assume that every task needs every prompt in a group.

## Open File Location

Click **Open File Location** to open the selected prompt's parent folder in the operating-system file browser.

This helps you locate the governed source file and related metadata.

The button opens a folder.

It does not open an editor or grant permission to modify governed prompts.

## Status Messages

The main dashboard status reports:

- number of current groups;
- number of current prompts;
- canonical workspace or fallback source;
- source path;
- hidden deprecated and retired entries;
- opened group window;
- missing group catalog.

The group window status reports:

- prompt count;
- selected copy action;
- full-stack copy action;
- no matching prompts;
- missing prompt folder.

Read status messages before assuming a prompt is absent or the library failed.

## Missing Groups or Prompts

### No prompt groups found

The dashboard reports the expected canonical catalog location.

Check whether:

- the canonical workspace exists;
- the group catalog exists;
- its JSON is valid;
- the correct source root is active.

### Group has no matching prompts

The group window reports that no prompt files matched the group's prompt IDs.

This may mean:

- prompt IDs are stale;
- prompts moved;
- prompts are hidden by lifecycle metadata;
- the group catalog needs reconciliation;
- the source is the compatibility fallback.

## Group Reconciliation

For canonical groups, the loader reconciles the catalog with current prompt files.

It:

- removes stale prompt IDs;
- prevents duplicate IDs;
- preserves catalog order for current matches;
- appends current prompts missing from the registry;
- adds current folder groups not yet listed in the catalog.

This keeps the dashboard aligned with current `ACTIVE_PROMPTS` without turning the GUI into a new prompt-authoring owner.

## Read-Only Governance Boundary

![Prompt Library read-only safety boundary](../assets/drawings/prompt_library_read_only_boundary.png)

Image note:

- Subject: Prompt browsing and copying remain separate from protected governance and canonical records.
- Asset path: `assets/drawings/prompt_library_read_only_boundary.png`.
- Alt text: Three colleagues browse prompt cards while canonical prompts, governance, ownership, and audit records remain behind a glowing read-only safety boundary.
- Caption: Prompt Library can browse, preview, and copy. It cannot rewrite governance or canonical prompt records.
- Artwork status: `primary_contextual_prompt_library_raster`.

Prompt Library is a browser, not an authoring authority.

It may:

- find;
- display;
- preview;
- copy;
- open a file location.

It may not:

- edit canonical prompts;
- change lifecycle state;
- approve prompt releases;
- alter ownership;
- change routing;
- bypass validation;
- execute a prompt automatically.

**In plain English:** The library helps you choose a book. It does not rewrite the master copy or decide how the book is governed.

## What Success Looks Like

A successful first session has:

1. current groups visible;
2. status showing the correct source;
3. one group window opened;
4. prompt list populated;
5. metadata visible;
6. full text preview visible;
7. selected prompt copied successfully;
8. full group stack copied in expected order;
9. source folder opened when needed;
10. no prompt files modified.

## Common Mistakes

### Assuming every stored prompt is visible

The dashboard intentionally hides non-current lifecycle states.

### Mistaking fallback data for canonical workspace

Read the source status.

### Copying a full group when one prompt is enough

Use the smallest correct prompt set for the task.

### Copying without reading metadata

The prompt may have a specific purpose, order, or context requirement.

### Treating Open File Location as edit permission

It only opens the folder.

### Expecting the tab to run a prompt

The tab copies text only.

### Expecting Reload to modify the library

Reload only rereads current source files and catalogs.

## If Something Goes Wrong

### The dashboard is empty

Check the status message and expected group catalog path.

### A prompt is missing

Check:

- lifecycle status;
- load type;
- ACTIVE_PROMPTS location;
- group prompt IDs;
- canonical versus fallback source;
- metadata validity.

### Copy Selected Prompt does nothing

Select a prompt in the list first.

### Copy Full Group Stack reports no prompts

The group currently has no matched current prompts.

### Open File Location warns that the folder is missing

The selected prompt path may be stale or unavailable.

### The dashboard looks outdated

Click Reload Canonical Library.

## First-Time Checklist

Before using the library:

- [ ] Source status read
- [ ] Canonical workspace preferred
- [ ] Current groups visible
- [ ] Hidden lifecycle behavior understood
- [ ] Read-only boundary understood

Before copying one prompt:

- [ ] Correct group opened
- [ ] Correct prompt selected
- [ ] Metadata reviewed
- [ ] Full text reviewed
- [ ] Task requires only this prompt

Before copying a group stack:

- [ ] Complete group is actually required
- [ ] Group description reviewed
- [ ] Prompt order understood
- [ ] Target workflow accepts the stack
- [ ] No hidden retired prompt expected

After copying:

- [ ] Clipboard action confirmed by status
- [ ] Prompt not assumed to be executed
- [ ] Source files remain unchanged
- [ ] Governance remains with the owning workflow

## Final Rule

**Use Prompt Library to find, understand, and copy current governed prompts, but keep authoring, lifecycle changes, routing, validation, and execution in their existing owning workflows.**
