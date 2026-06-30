# Freeze Feature After Update Box

This KANDA Reasoner box creates and reads freeze-after-update state for the selected active project.

The selected project can be any project that KANDA Reasoner is working on. It may be KANDA Reasoner itself only in a self-hosting session. The tool identity and selected-project identity must remain separate.

New writes go to the selected project's external support root, not into the selected project source root:

```text
<project_drive>/<project_name>_show_project_to_AI/project_freeze_after_update/
```

The persistent project-specific memory lives in:

```text
<project_drive>/<project_name>_show_project_to_AI/project_freeze_after_update/frozen_features_memory/
```

Upload-ready freeze output files live in:

```text
<project_drive>/<project_name>_show_project_to_AI/project_freeze_after_update/files_to_send_ai/
```

KANDA Reasoner must not store per-project freeze history centrally in the reusable tool source, and must not merge the reusable KANDA Reasoner tool box with the selected project support box.
