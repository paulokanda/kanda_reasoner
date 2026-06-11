# project_profile.py refactor notes

This refactor keeps `project_profile.py` as the public API while extracting the
implementation into `project_profile_help/`.

Split:
- `profile_types.py`: `ProjectProfile` dataclass and `to_dict()`
- `built_in_profiles.py`: built-in profile constants
- `registry.py`: `PROJECT_PROFILES`, lookup, iteration
- `inference.py`: metadata-driven profile inference

Compatibility preserved:
- Public imports still come from `project_profile.py`
- Existing root package exports continue to work
- All previous public constants and helper functions remain available
