# Project Freeze After Update

This folder is a project-local closed box used by KANDA Reasoner.

It belongs to this project only. KANDA Reasoner reads this folder when you use
the **Freeze Feature After Update** tab, then it writes fresh AI-send files into
`files_to_send_ai/`.

Do not move this folder into KANDA Reasoner. Do not merge it with another
project. Each project keeps its own freeze memory here.

## Folder roles

```text
frozen_features_memory/
  Persistent memory of what has already been frozen in this project.

files_to_send_ai/
  Fresh output files that you upload to AI after updating the project.
```

Generated ZIP files may be recreated. The persistent source of truth is inside
`frozen_features_memory/`.
