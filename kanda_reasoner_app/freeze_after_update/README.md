# Freeze Feature After Update Box

This KANDA Reasoner box creates and reads project-local freeze-after-update state.

It writes only inside the selected project:

```text
<any_project>/project_freeze_after_update/
```

The project-local box contains persistent memory in `frozen_features_memory/` and upload-ready output files in `files_to_send_ai/`.

KANDA Reasoner must not store per-project freeze history centrally.
