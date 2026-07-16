# help_index.py refactor notes

## Goal

Keep the public `HELP_INDEX` contract stable while shrinking the root module.

## New structure

- `help_index.py` is now a thin facade.
- `help_index_help/help_index_raw.py` holds the large static literal.
- `help_index_help/help_index_normalization.py` repairs repeated mojibake text.
- `help_index_help/help_index_data.py` builds the exported normalized `HELP_INDEX`.

## Why this split

- easier maintenance
- smaller public module
- safer future edits
- preserves all existing callers that import `HELP_INDEX` from `help_index.py`
