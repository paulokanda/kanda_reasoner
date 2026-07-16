# index_loader.py refactor notes

## Goal
Keep `JsonProjectIndex` as the stable public owner while extracting:
- giant state initialization
- giant top-level section loading
- repetitive index builder families
- runtime source-file normalization

## New helper package
- `index_loader_help/state_init.py`
- `index_loader_help/section_loading.py`
- `index_loader_help/path_resolution.py`
- `index_loader_help/index_builders.py`

## Public contract preserved
- `JsonProjectIndex`
- `load_json()`
- `load()`
- all accessor methods
- all `_build_*` method names retained as delegating wrappers

## Practical effect
- `index_loader.py` becomes the public shell
- repeated mechanical code moves out
- test and import surface should remain stable
