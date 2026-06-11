Light refactor only.

Why not a deeper split:
- reasoner_retriever.py is already a public orchestration shell over reasoner_retriever_help/*
- most heavy logic already lives in helper modules
- the safest improvement is cleanup, not more decomposition

What changed:
- cleaned the module header/docstring
- switched helper imports to relative imports
- added _is_section_only_intent() to make retrieve() slightly clearer
- preserved all public names and wrapper methods
