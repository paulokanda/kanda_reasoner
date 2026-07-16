"""Support V10 project reasoning and evidence handling."""

from dataclasses import dataclass

@dataclass(frozen=True)
class ScoringConfig:
    # Exact matches
    exact_path_match: int = 120
    exact_filename_match: int = 80
    exact_class_match: int = 180
    exact_class_tail_match: int = 100
    exact_symbol_match: int = 120
    exact_symbol_tail_match: int = 80
    exact_callsite_match: int = 360
    exact_owner_target_match: int = 1000

    # Intent-specific boosts
    main_window_show_call: int = 260
    qtimer_showmaximized_exact: int = 320
    where_is_class_boost: int = 220
    where_is_function_boost: int = 160
    explain_chain_entry_file: int = 80
    named_chain_step: int = 180
    topomap_implementation_owner_path: int = 300
    reset_cleanup_owner_path: int = 160
    # ... add all others

    # Penalties
    direct_showmaximized_without_qtimer: int = -180
    main_window_show_non_ui: int = -180
    # ...





