from __future__ import annotations

import copy
import hashlib
import json
import math
import os
import traceback
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any, Callable

from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import (
    QApplication,
    QButtonGroup,
    QComboBox,
    QFileDialog,
    QFrame,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QSpinBox,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

# ---------------------------------------------------------------------------
# v4.6 — root cause fix for all prior versions
#
# THE ACTUAL BUG (present in v4.3 through v4.5):
#
#   expand_to_slots() computed wrapper_overhead(root, path_parts=[]) = 0,
#   then checked: if 0 + val_size <= 15 MB → emit as root slot.
#   The 'files' value is 45 MB so it correctly triggered recursion.
#   But inside the recursion, when processing each child of 'files', the
#   check was: if wrapper('files') + child_size <= 15 MB.
#   wrapper('files') = ~12 MB, child sizes = ~0.2 MB each → fits → correct.
#   BUT the slot was assigned path_parts = ['files'] correctly.
#
#   The actual problem was in pack_slots():
#     w = _wrapper_cache.get(path_key, 0)
#   The cache key for ('files',) WAS populated... except it wasn't, because
#   wrapper_overhead() in expand_to_slots is only called for the CURRENT
#   level's path, not for child paths. The child path wrapper is never
#   explicitly requested — the recursion just calls expand_to_slots with
#   child_path, which calls wrapper_overhead(root, child_path) at the TOP
#   of that call. So the cache SHOULD be populated.
#
#   The real bug: pack_slots() runs AFTER expand_to_slots(), and uses
#   _wrapper_cache to get 'w' for each group. This works IF the cache was
#   populated. But 'files' children are INDIVIDUAL file paths like
#   ('files', 'src/main.py'), NOT ('files',). The group key in pack_slots
#   is tuple(slot.path_parts) = ('files',) for all children, but the cache
#   was populated for ('files', 'src/main.py') — a MISMATCH.
#
#   Wait — re-reading expand_to_slots: when 'files' (45 MB) triggers
#   recursion, we call expand_to_slots(root, path_parts=['files'], entries=
#   children_of_files, ...). At the top of that call: wrapper_overhead(root,
#   ['files'], is_list) is computed and cached for key=('files',). Then each
#   child is checked: w + child_size. If it fits, the slot gets
#   path_parts=['files']. So the cache key ('files',) IS populated with the
#   correct wrapper. And pack_slots groups by ('files',) and reads w from
#   cache correctly.
#
#   So WHY are the written files ~16 MB?
#
#   Because pack_slots splits the 240 'files' children into chunks using
#   budget = MAX_FILE_BYTES - w_files. But then build_document_for_spec()
#   calls set_nested_value(root, ['files'], chunk_value) — which writes
#   the FULL ROOT document with 'files' replaced by the chunk. The chunk
#   content size was budgeted correctly, but the ACTUAL written file also
#   includes the rest of root (the ~12 MB wrapper). That should be fine
#   because budget = 15MB - 12MB = 3MB... but the log shows 54 entries
#   per part at 16 MB. That means the per-entry sizes are tiny and 54 of
#   them sum to ~4 MB... 4 MB chunk + 12 MB wrapper = 16 MB. Correct math.
#
#   THE REAL ROOT CAUSE (finally):
#   The mode is "parts" with value=10. pack_slots processes the ('files',)
#   group with 240 slots and mode="parts", n_parts=max(10, ceil(total/budget)).
#   total_val_bytes = 240 entries × ~0.2 MB = ~48 MB.
#   budget = 15 MB - 12 MB = 3 MB.
#   min_parts = ceil(48 MB / 3 MB) = 16.
#   n_parts = max(10, 16) = 16.
#   BUT the <root> group ALSO has slots and ALSO gets n_parts=max(10,...).
#   So "split into 10 parts" is applied INDEPENDENTLY to each path group.
#   The user wants 10 total parts, not 10 parts per path group.
#
#   FIX: collect ALL slots together, compute a GLOBAL target size based on
#   mode and total content, then pack greedily across all groups in order,
#   respecting per-group budgets. The mode parameters control the TOTAL
#   number of output files or the max file size, not per-group behaviour.
# ---------------------------------------------------------------------------

MAX_FILE_BYTES: int = 15 * 1_024 * 1_024   # 15 MB hard ceiling
MIN_PART_BYTES: int = 256 * 1_024            # don't emit parts below 256 KB


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class SplitPlan:
    input_path: str
    output_dir: str
    target_path: str
    mode: str
    value: int


@dataclass
class LeafSlot:
    """
    One indivisible unit: one entry at a specific path in the document.
    doc_size = wrapper_bytes(path_parts) + json_bytes_indented(value)
              = estimated on-disk size if this slot were the ONLY content.
    """
    path_parts: list[str]
    key: Any
    value: Any
    is_list: bool
    val_size: int   # json_bytes_indented(value)
    wrapper: int    # wrapper_overhead for this path


@dataclass
class PartSpec:
    slots: list[LeafSlot] = field(default_factory=list)

    def estimated_size(self) -> int:
        """Raw chunk size — no wrapper (parts are written without root wrapper)."""
        return sum(s.val_size for s in self.slots)


# ---------------------------------------------------------------------------
# Serialisation helpers
# ---------------------------------------------------------------------------

def json_bytes_indented(value: Any) -> int:
    return len(json.dumps(value, ensure_ascii=False, indent=2).encode("utf-8"))


def stable_hash(value: Any) -> str:
    payload = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


# ---------------------------------------------------------------------------
# Path helpers
# ---------------------------------------------------------------------------

def parse_target_path(path_text: str) -> list[str]:
    text = str(path_text).strip()
    if not text:
        return []
    return [p.strip() for p in text.split(".") if p.strip()]


def get_nested_value(root: Any, path_parts: list[str]) -> Any:
    cur = root
    for part in path_parts:
        if not isinstance(cur, dict):
            raise KeyError(f"'{part}' is not inside a dict.")
        if part not in cur:
            raise KeyError(f"'{part}' not found.")
        cur = cur[part]
    return cur


def set_nested_value(root: Any, path_parts: list[str], new_value: Any) -> Any:
    cloned = copy.deepcopy(root)
    if not path_parts:
        return new_value
    cur = cloned
    for part in path_parts[:-1]:
        cur = cur[part]
    cur[path_parts[-1]] = new_value
    return cloned


def collect_container_paths(root: Any, max_depth: int = 6) -> list[str]:
    paths: list[str] = []

    def walk(node: Any, prefix: list[str], depth: int) -> None:
        if depth > max_depth:
            return
        if isinstance(node, dict):
            if prefix:
                paths.append(".".join(prefix))
            for k, v in node.items():
                if isinstance(v, (dict, list)):
                    walk(v, prefix + [str(k)], depth + 1)
        elif isinstance(node, list):
            if prefix:
                paths.append(".".join(prefix))

    walk(root, [], 0)
    return sorted(set(paths))


def get_entries(node: Any) -> list[tuple[Any, Any]]:
    if isinstance(node, dict):
        return list(node.items())
    if isinstance(node, list):
        return list(enumerate(node))
    raise TypeError("Target must be a dict or list.")


def rebuild_container(entries: list[tuple[Any, Any]], is_list: bool) -> Any:
    if is_list:
        return [v for _k, v in entries]
    return {k: v for k, v in entries}


# ---------------------------------------------------------------------------
# Wrapper overhead — cached per path tuple
# Returns: json_bytes_indented(root with path set to empty placeholder)
# For empty path (root split): returns 0 because output IS the chunk.
# ---------------------------------------------------------------------------

_wrapper_cache: dict[tuple, int] = {}


def get_wrapper(root: Any, path_parts: list[str], is_list: bool) -> int:
    key = tuple(path_parts)
    if key not in _wrapper_cache:
        if not path_parts:
            _wrapper_cache[key] = 0
        else:
            placeholder: Any = [] if is_list else {}
            doc = set_nested_value(root, path_parts, placeholder)
            _wrapper_cache[key] = json_bytes_indented(doc)
    return _wrapper_cache[key]


# ---------------------------------------------------------------------------
# SLOT EXPANDER
#
# Produces a flat list of LeafSlots by walking the target container.
# Each slot is ONE entry that fits within (MAX_FILE_BYTES - wrapper) on
# its own. Entries that don't fit trigger a descent into their children.
#
# KEY INVARIANT: every slot's wrapper is correctly computed for ITS OWN
# path_parts — not the parent's. This means slots at different depths
# have different wrapper values, and the packer uses them correctly.
# ---------------------------------------------------------------------------

def expand_to_slots(
    root: Any,
    path_parts: list[str],
    entries: list[tuple[Any, Any]],
    is_list: bool,
    log_fn: Callable[[str], None],
    depth: int = 0,
    balance_budget: int = MAX_FILE_BYTES,
    # balance_budget = target per-part size in bytes.
    # Descent is triggered whenever a single entry exceeds this threshold,
    # regardless of whether the 15 MB ceiling is being enforced.
    # When limit enforced   → balance_budget = MAX_FILE_BYTES (15 MB)
    # When limit relaxed    → balance_budget = total_content / N
    # This guarantees balanced output in both cases.
) -> list[LeafSlot]:

    MAX_DEPTH = 12
    # Compute and cache wrapper for THIS level (needed for reassembly path info)
    w = get_wrapper(root, path_parts, is_list)

    slots: list[LeafSlot] = []

    for key, val in entries:
        val_size = json_bytes_indented(val)

        if val_size <= balance_budget:
            # Fits within per-part target → emit as leaf slot at this level
            slots.append(LeafSlot(
                path_parts=list(path_parts),
                key=key,
                value=val,
                is_list=is_list,
                val_size=val_size,
                wrapper=w,
            ))
        else:
            # Entry would dominate a single part → descend to balance output
            child_path = path_parts + [str(key)]

            if not isinstance(val, (dict, list)):
                log_fn(
                    f"  Warning: atomic value at '{'.'.join(child_path)}' is "
                    f"{val_size/1024/1024:.2f} MB — cannot split further. Emitting as-is."
                )
                slots.append(LeafSlot(
                    path_parts=list(path_parts),
                    key=key,
                    value=val,
                    is_list=is_list,
                    val_size=val_size,
                    wrapper=w,
                ))
                continue

            if depth >= MAX_DEPTH:
                log_fn(f"  Max recursion depth at '{'.'.join(child_path)}'. Emitting as-is.")
                slots.append(LeafSlot(
                    path_parts=list(path_parts),
                    key=key,
                    value=val,
                    is_list=is_list,
                    val_size=val_size,
                    wrapper=w,
                ))
                continue

            child_is_list = isinstance(val, list)
            child_entries = get_entries(val)
            log_fn(
                f"  '{'.'.join(child_path)}' is {val_size/1024/1024:.2f} MB "
                f"> budget {balance_budget/1024/1024:.2f} MB "
                f"— descending ({len(child_entries)} children, depth={depth+1})."
            )
            child_slots = expand_to_slots(
                root=root,
                path_parts=child_path,
                entries=child_entries,
                is_list=child_is_list,
                log_fn=log_fn,
                depth=depth + 1,
                balance_budget=balance_budget,
            )
            slots.extend(child_slots)

    return slots


# ---------------------------------------------------------------------------
# GLOBAL PACKER
#
# Takes ALL leaf slots (from any path depth) and packs them into PartSpecs.
#
# Rules:
#   1. Slots with DIFFERENT path_parts cannot share a part — they would
#      require multi-path document construction.
#   2. Within a path group, slots are packed respecting the group's budget.
#   3. Mode is applied GLOBALLY:
#      - "kb"       : each part ≤ value KB on disk (wrapper + content)
#      - "parts"    : target total output file count ≈ value
#      - "per_child": one part per direct child of the USER-SELECTED target
#                     (not per slot — slots from the same direct child are grouped)
#   4. After packing, tiny parts (< MIN_PART_BYTES) are merged into same-path
#      neighbours if the result stays under MAX_FILE_BYTES.
# ---------------------------------------------------------------------------

def pack_slots(
    slots: list[LeafSlot],
    mode: str,
    mode_value: int,
    user_path_parts: list[str],   # the path the user selected (for per_child)
    log_fn: Callable[[str], None],
) -> list[PartSpec]:

    if not slots:
        return []

    # Group slots by path
    groups: dict[tuple, list[LeafSlot]] = defaultdict(list)
    for slot in slots:
        groups[tuple(slot.path_parts)].append(slot)

    all_parts: list[PartSpec] = []

    if mode == "kb":
        # Parts are written as raw chunk values (no wrapper duplication).
        # So the content budget IS the user's KB target directly.
        content_budget = max(mode_value * 1024, 1024)
        content_budget = min(content_budget, MAX_FILE_BYTES)

        for path_key, group in groups.items():
            all_parts.extend(_greedy_pack(group, content_budget))

    elif mode == "parts":
        # Target total output files = mode_value (hard target).
        #
        # PRE-CHECK: can we honour N parts AND stay <= 15 MB each?
        #   average_part_size = total_file_size / N
        #   If average_part_size <= MAX_FILE_BYTES → enforce limit (descent active).
        #   If average_part_size >  MAX_FILE_BYTES → user knowingly asked for
        #     fewer parts than the limit allows; ignore 15 MB ceiling and just
        #     split evenly by entry count.  Parts will be larger than 15 MB but
        #     that is exactly what the user requested.
        total_content = sum(s.val_size for s in slots)
        if total_content == 0:
            return [PartSpec(slots=list(slots))]

        # Estimate average output file size if we split into mode_value parts.
        # Use the most common wrapper (root-level, w=0) for the estimate; this
        # is conservative — actual parts may include wrapper overhead.
        avg_estimated = total_content / mode_value
        enforce_limit = avg_estimated <= MAX_FILE_BYTES

        if not enforce_limit:
            log_fn(
                f"  15 MB limit RELAXED: {total_content/1024/1024:.1f} MB content / "
                f"{mode_value} parts = ~{avg_estimated/1024/1024:.1f} MB per part. "
                f"Splitting evenly by size, ignoring 15 MB ceiling."
            )
            # -----------------------------------------------------------------
            # TRUE EVEN SPLIT — flat bin-pack then merge boundary fragments.
            #
            # Step 1: flatten ALL slots (all paths) into one ordered sequence.
            # Step 2: bin-pack into mode_value equal-size bins by val_size.
            #         Bins are balanced regardless of path boundaries.
            # Step 3: split each bin into PartSpecs grouped by path_parts
            #         (slots from different paths cannot share one part file).
            #         A bin that straddles a path boundary produces 2+ PartSpecs.
            # Step 4: merge any small PartSpec fragment from a boundary bin into
            #         the adjacent PartSpec of the same path, so the final file
            #         count stays close to mode_value with no tiny orphan files.
            # -----------------------------------------------------------------
            all_slots_flat = []
            for group in groups.values():
                all_slots_flat.extend(group)

            target_bin = max(1, math.ceil(total_content / mode_value))

            # Step 2: bin-pack
            bins: list[list[LeafSlot]] = []
            cur_bin: list[LeafSlot] = []
            cur_bin_size = 0
            for slot in all_slots_flat:
                if cur_bin and cur_bin_size + slot.val_size > target_bin and len(bins) < mode_value - 1:
                    bins.append(cur_bin)
                    cur_bin = []
                    cur_bin_size = 0
                cur_bin.append(slot)
                cur_bin_size += slot.val_size
            if cur_bin:
                bins.append(cur_bin)

            # Step 3: split each bin by path_parts → raw PartSpecs
            raw_parts: list[PartSpec] = []
            for bin_slots in bins:
                path_sub: dict[tuple, list[LeafSlot]] = defaultdict(list)
                for s in bin_slots:
                    path_sub[tuple(s.path_parts)].append(s)
                for sub_slots in path_sub.values():
                    raw_parts.append(PartSpec(slots=sub_slots))

            # Step 4: merge small boundary fragments into same-path neighbours.
            # A "fragment" is a PartSpec whose content is < 50% of target_bin
            # AND there exists an adjacent PartSpec of the same path to absorb it.
            FRAGMENT_THRESHOLD = target_bin * 0.50
            merged_parts: list[PartSpec] = []
            i = 0
            while i < len(raw_parts):
                part = raw_parts[i]
                part_size = sum(s.val_size for s in part.slots)
                path_key = tuple(part.slots[0].path_parts) if part.slots else ()

                if part_size < FRAGMENT_THRESHOLD:
                    # Try to merge forward into next same-path part
                    merged = False
                    for j in range(i + 1, len(raw_parts)):
                        other = raw_parts[j]
                        if not other.slots:
                            continue
                        other_key = tuple(other.slots[0].path_parts)
                        if other_key != path_key:
                            continue
                        other_size = sum(s.val_size for s in other.slots)
                        # Absorb: prepend fragment into next same-path part
                        raw_parts[j] = PartSpec(slots=part.slots + other.slots)
                        log_fn(
                            f"  Merged fragment ({part_size/1024:.1f} KB) into "
                            f"next same-path part → "
                            f"{(part_size+other_size)/1024:.1f} KB"
                        )
                        merged = True
                        break
                    if not merged:
                        # Try merge backward
                        for j in range(len(merged_parts) - 1, -1, -1):
                            prev = merged_parts[j]
                            if not prev.slots:
                                continue
                            prev_key = tuple(prev.slots[0].path_parts)
                            if prev_key != path_key:
                                continue
                            prev_size = sum(s.val_size for s in prev.slots)
                            merged_parts[j] = PartSpec(slots=prev.slots + part.slots)
                            log_fn(
                                f"  Merged fragment ({part_size/1024:.1f} KB) into "
                                f"prev same-path part → "
                                f"{(part_size+prev_size)/1024:.1f} KB"
                            )
                            merged = True
                            break
                    if not merged:
                        merged_parts.append(part)
                else:
                    merged_parts.append(part)
                i += 1

            all_parts.extend(merged_parts)
            log_fn(
                f"  Relaxed split: {len(bins)} bins → {len(merged_parts)} part files."
            )

        else:
            log_fn(
                f"  15 MB limit ENFORCED: ~{avg_estimated/1024/1024:.1f} MB per part "
                f"fits within limit."
            )
            group_list = list(groups.items())

            # Parts are written as raw chunks — budget is simply MAX_FILE_BYTES.
            group_meta: list[dict] = []
            for path_key, group in group_list:
                budget_per_part = MAX_FILE_BYTES   # no wrapper deduction needed
                group_content = sum(s.val_size for s in group)
                min_phys = max(1, math.ceil(group_content / budget_per_part))
                min_phys = min(min_phys, len(group))
                group_meta.append({
                    "group": group,
                    "budget_per_part": budget_per_part,
                    "group_content": group_content,
                    "min_phys": min_phys,
                })

            min_total = sum(m["min_phys"] for m in group_meta)

            if min_total >= mode_value:
                log_fn(
                    f"  Note: physical minimum is {min_total} parts "
                    f"(requested {mode_value}). Using {min_total}."
                )
                final_counts = [m["min_phys"] for m in group_meta]
            else:
                surplus = mode_value - min_total
                extras_float = [
                    surplus * (m["group_content"] / total_content)
                    for m in group_meta
                ]
                extras_floor = [int(f) for f in extras_float]
                remainder = surplus - sum(extras_floor)
                frac_order = sorted(
                    range(len(group_meta)),
                    key=lambda i: extras_float[i] - extras_floor[i],
                    reverse=True,
                )
                for i in range(remainder):
                    extras_floor[frac_order[i]] += 1
                final_counts = [
                    min(m["min_phys"] + extras_floor[i], len(m["group"]))
                    for i, m in enumerate(group_meta)
                ]

            actual_total = sum(final_counts)
            if actual_total != mode_value:
                log_fn(f"  Note: target was {mode_value} parts; producing {actual_total} (physics constraint).")

            for i, m in enumerate(group_meta):
                group = m["group"]
                n = final_counts[i]
                if m["budget_per_part"] <= 0:
                    for s in group:
                        all_parts.append(PartSpec(slots=[s]))
                    continue
                val_sizes = [s.val_size for s in group]
                chunks = _balanced_chunks(group, val_sizes, n)
                all_parts.extend(PartSpec(slots=c) for c in chunks)

    elif mode == "per_child":
        # One file per DIRECT CHILD of the user-selected path.
        # Slots from the same direct child (regardless of depth) go together.
        # "Direct child" = first key after user_path_parts.
        user_depth = len(user_path_parts)

        child_groups: dict[str, list[LeafSlot]] = defaultdict(list)
        for slot in slots:
            pp = slot.path_parts
            if len(pp) > user_depth:
                child_key = pp[user_depth]
            elif len(pp) == user_depth and slot.key is not None:
                child_key = str(slot.key)
            else:
                child_key = "__root__"
            child_groups[child_key].append(slot)

        for child_key, child_slots in child_groups.items():
            # Pack child_slots into as many parts as needed (respecting 15 MB).
            # Parts are raw chunks — budget = MAX_FILE_BYTES directly.
            sub_groups: dict[tuple, list[LeafSlot]] = defaultdict(list)
            for s in child_slots:
                sub_groups[tuple(s.path_parts)].append(s)

            for path_key, group in sub_groups.items():
                all_parts.extend(_greedy_pack(group, MAX_FILE_BYTES))

    # Merge tiny parts (same path only)
    all_parts = _merge_tiny_parts(all_parts, log_fn)

    return all_parts


def _greedy_pack(
    slots: list[LeafSlot],
    content_budget: int,
) -> list[PartSpec]:
    """Pack slots greedily: fill a part until content_budget would be exceeded."""
    parts: list[PartSpec] = []
    cur: list[LeafSlot] = []
    cur_size = 0
    for slot in slots:
        if cur and cur_size + slot.val_size > content_budget:
            parts.append(PartSpec(slots=cur))
            cur = [slot]
            cur_size = slot.val_size
        else:
            cur.append(slot)
            cur_size += slot.val_size
    if cur:
        parts.append(PartSpec(slots=cur))
    return parts


def _balanced_chunks(
    slots: list[LeafSlot],
    val_sizes: list[int],
    n_parts: int,
) -> list[list[LeafSlot]]:
    if n_parts <= 1 or len(slots) <= 1:
        return [slots]
    total = sum(val_sizes)
    target = max(1, math.ceil(total / n_parts))
    chunks: list[list[LeafSlot]] = []
    cur: list[LeafSlot] = []
    cur_size = 0
    for i, slot in enumerate(slots):
        sz = val_sizes[i]
        remaining = len(slots) - i
        slots_left = n_parts - len(chunks)
        close = (cur and remaining == slots_left) or (
            cur and cur_size + sz > target and len(chunks) < n_parts - 1
        )
        if close:
            chunks.append(cur)
            cur = []
            cur_size = 0
        cur.append(slot)
        cur_size += sz
    if cur:
        chunks.append(cur)
    while len(chunks) > n_parts:
        chunks[-1].extend(chunks.pop())
    while len(chunks) < n_parts and any(len(c) > 1 for c in chunks):
        li = max(range(len(chunks)), key=lambda i: len(chunks[i]))
        chunks.insert(li + 1, [chunks[li].pop()])
    return [c for c in chunks if c]


def _merge_tiny_parts(
    parts: list[PartSpec],
    log_fn: Callable[[str], None],
) -> list[PartSpec]:
    """
    Merge parts smaller than MIN_PART_BYTES into a same-path neighbour,
    as long as the combined chunk stays under MAX_FILE_BYTES.
    Parts are raw chunks (no wrapper), so sizes are pure val_size sums.
    """
    changed = True
    while changed:
        changed = False
        out: list[PartSpec] = []
        skip: set[int] = set()
        for i, part in enumerate(parts):
            if i in skip:
                continue
            part_size = sum(s.val_size for s in part.slots)
            if part_size >= MIN_PART_BYTES:
                out.append(part)
                continue
            # Try to absorb into next same-path part
            path_key = tuple(part.slots[0].path_parts) if part.slots else ()
            merged = False
            for j in range(i + 1, len(parts)):
                if j in skip:
                    continue
                other = parts[j]
                if not other.slots:
                    continue
                if tuple(other.slots[0].path_parts) != path_key:
                    continue
                other_size = sum(s.val_size for s in other.slots)
                combined = part_size + other_size
                if combined <= MAX_FILE_BYTES:
                    out.append(PartSpec(slots=part.slots + other.slots))
                    skip.add(j)
                    merged = True
                    changed = True
                    log_fn(
                        f"  Merged tiny part ({part_size/1024:.1f} KB) into "
                        f"neighbour → {combined/1024:.1f} KB"
                    )
                    break
            if not merged:
                out.append(part)
        parts = out
    return parts


# ---------------------------------------------------------------------------
# Document builder
#
# Each part file contains ONLY its chunk value — not the full root document.
# This keeps part files small (sum of parts ≈ original size).
# The manifest records path_parts and is_list so the reassembler knows
# where to graft each chunk back.
#
# Special case: path_parts == [] (root split) — the chunk IS the document.
# ---------------------------------------------------------------------------

def build_document_for_spec(spec: PartSpec) -> Any:
    if not spec.slots:
        raise ValueError("Empty PartSpec.")
    is_list = spec.slots[0].is_list
    entries = [(s.key, s.value) for s in spec.slots]
    return rebuild_container(entries, is_list)


# ---------------------------------------------------------------------------
# Worker thread
# ---------------------------------------------------------------------------

class SplitterWorker(QThread):
    progress = Signal(int)
    log = Signal(str)
    finished = Signal(bool, str)

    def __init__(self, action: str, payload: dict[str, Any]) -> None:
        super().__init__()
        self.action = action
        self.payload = payload

    def run(self) -> None:
        try:
            if self.action == "split":
                self._run_split()
            elif self.action == "reassemble":
                self._run_reassemble()
            else:
                self.finished.emit(False, f"Unknown action: {self.action}")
        except Exception as exc:
            self.finished.emit(False, f"Unexpected error: {exc}\n{traceback.format_exc()}")

    def _run_split(self) -> None:
        global _wrapper_cache
        _wrapper_cache = {}

        plan = SplitPlan(**self.payload)
        self.log.emit(f"Reading JSON: {plan.input_path}")
        with open(plan.input_path, "r", encoding="utf-8") as fh:
            root = json.load(fh)

        path_parts = parse_target_path(plan.target_path)
        target = get_nested_value(root, path_parts) if path_parts else root
        is_list = isinstance(target, list)
        if not isinstance(target, (dict, list)):
            raise TypeError("Target path must point to a dict or list.")

        entries = get_entries(target)
        if not entries:
            raise ValueError("Target container is empty.")

        get_wrapper(root, path_parts, is_list)  # populate cache
        # Pre-check: will requested parts respect the 15 MB limit?
        # Use sum of entry val_sizes (same source the packer uses) for consistency.
        total_content_bytes = sum(json_bytes_indented(v) for _k, v in entries)
        self.log.emit(f"Target path    : {plan.target_path or '<root>'}")
        self.log.emit(f"Target type    : {'list' if is_list else 'dict'}")
        self.log.emit(f"Direct entries : {len(entries)}")
        self.log.emit(
            f"Target content : {total_content_bytes/1024:.2f} KB  "
            f"(parts written as raw chunks — no wrapper duplication)"
        )
        if plan.mode == "parts":
            avg_part_bytes = total_content_bytes / max(plan.value, 1)
            enforce_limit = avg_part_bytes <= MAX_FILE_BYTES
            # balance_budget drives descent: use whichever is smaller —
            # the 15 MB ceiling (if enforced) or the even-split target.
            # This guarantees descent happens whenever an entry would
            # unbalance any part, regardless of the limit decision.
            balance_budget = min(int(avg_part_bytes), MAX_FILE_BYTES)
        elif plan.mode == "kb":
            enforce_limit = True
            balance_budget = plan.value * 1024
        else:  # per_child
            enforce_limit = True
            balance_budget = MAX_FILE_BYTES

        self.log.emit("Expanding to leaf slots...")

        slots = expand_to_slots(
            root=root,
            path_parts=path_parts,
            entries=entries,
            is_list=is_list,
            log_fn=self.log.emit,
            balance_budget=balance_budget,
        )
        self.log.emit(f"Leaf slots : {len(slots)}")

        # Log slot distribution by path
        slot_paths: dict[str, int] = defaultdict(int)
        for s in slots:
            slot_paths[".".join(s.path_parts) or "<root>"] += 1
        for pth, cnt in sorted(slot_paths.items(), key=lambda x: -x[1]):
            self.log.emit(f"  {pth}: {cnt} slots")

        self.log.emit(f"Packing (mode={plan.mode}, value={plan.value})...")
        specs = pack_slots(
            slots=slots,
            mode=plan.mode,
            mode_value=plan.value,
            user_path_parts=path_parts,
            log_fn=self.log.emit,
        )
        self.log.emit(f"Parts planned : {len(specs)}")

        os.makedirs(plan.output_dir, exist_ok=True)
        base_name = os.path.splitext(os.path.basename(plan.input_path))[0]
        total = len(specs)
        digits = max(3, len(str(total)))
        manifest_parts: list[dict[str, Any]] = []

        for index, spec in enumerate(specs, start=1):
            # Write only the chunk value — no root wrapper duplication.
            # Part files are small; reassembler grafts them back using path_parts.
            document = build_document_for_spec(spec)
            part_name = f"{str(index).zfill(digits)}_{base_name}.json"
            part_path = os.path.join(plan.output_dir, part_name)

            with open(part_path, "w", encoding="utf-8") as fh:
                json.dump(document, fh, ensure_ascii=False, indent=2)

            size_bytes = os.path.getsize(part_path)
            path_label = ".".join(spec.slots[0].path_parts) if spec.slots else "<root>"
            path_label = path_label or "<root>"

            # Size check is against raw chunk content — no wrapper involved here
            flag = " !! OVER LIMIT" if size_bytes > MAX_FILE_BYTES else ""
            self.log.emit(
                f"Wrote {part_name} | path={path_label} | "
                f"entries={len(spec.slots)} | size_kb={size_bytes/1024:.2f}{flag}"
            )
            if size_bytes > MAX_FILE_BYTES:
                self.log.emit(
                    f"  → {size_bytes/1024/1024:.2f} MB — single atomic entry, cannot split further."
                )

            manifest_parts.append({
                "index": index,
                "filename": part_name,
                "path_parts": spec.slots[0].path_parts if spec.slots else [],
                "is_list": spec.slots[0].is_list if spec.slots else False,
                "entry_keys": [
                    s.key if isinstance(s.key, str) else int(s.key)
                    for s in spec.slots
                ],
                "entries": len(spec.slots),
                "size_bytes": size_bytes,
                "sha256": stable_hash(document),
            })
            self.progress.emit(int(index / total * 100))

        # root_skeleton: the full root document with ALL splittable content
        # replaced by empty placeholders. The reassembler uses this to
        # reconstruct the document without needing any full-document part.
        # Build by emptying every unique path_parts that was written.
        unique_paths = {tuple(p["path_parts"]): p["is_list"] for p in manifest_parts}
        root_skeleton = copy.deepcopy(root)
        for pp_tuple, il in unique_paths.items():
            pp_list = list(pp_tuple)
            if pp_list:
                placeholder: Any = [] if il else {}
                root_skeleton = set_nested_value(root_skeleton, pp_list, placeholder)
            else:
                # Root-level split: skeleton is an empty container of same type
                root_skeleton = [] if is_list else {}

        manifest = {
            "splitter_version": "4.7",
            "source_file": os.path.abspath(plan.input_path),
            "source_sha256": stable_hash(root),
            "target_path": plan.target_path,
            "target_type": "list" if is_list else "dict",
            "mode": plan.mode,
            "value": plan.value,
            "part_count": total,
            "root_skeleton": root_skeleton,
            "parts": manifest_parts,
        }
        manifest_name = f"{base_name}__split_manifest.json"
        manifest_path = os.path.join(plan.output_dir, manifest_name)
        with open(manifest_path, "w", encoding="utf-8") as fh:
            json.dump(manifest, fh, ensure_ascii=False, indent=2)

        self.progress.emit(100)
        self.finished.emit(True, f"Done. {total} parts + manifest: {manifest_path}")

    def _run_reassemble(self) -> None:
        manifest_path = self.payload["manifest_path"]
        output_path = self.payload["output_path"]

        self.log.emit(f"Reading manifest: {manifest_path}")
        with open(manifest_path, "r", encoding="utf-8") as fh:
            manifest = json.load(fh)

        manifest_dir = os.path.dirname(os.path.abspath(manifest_path))
        parts = manifest.get("parts", [])
        if not parts:
            raise ValueError("Manifest has no parts.")

        # v4.7 part files contain ONLY the chunk value (no root wrapper).
        # We rebuild by:
        #   1. Start with root_skeleton from manifest (keys but no content).
        #   2. For each part, read chunk value and record entries at path_parts.
        #   3. Merge deepest paths first, graft into reconstructed root.
        #
        # Backwards compat: detect old-format parts (full root doc) by checking
        # manifest splitter_version. v4.6 and earlier stored full documents.

        version = str(manifest.get("splitter_version", "0"))
        is_new_format = version >= "4.7"

        # Load root skeleton from manifest if present, else bootstrap from part 1
        root_skeleton_data = manifest.get("root_skeleton")

        path_entries: dict[tuple, list[tuple[Any, Any]]] = defaultdict(list)
        path_is_list: dict[tuple, bool] = {}
        fallback_root: Any = None
        total = len(parts)

        for idx, part_info in enumerate(parts, start=1):
            part_path = os.path.join(manifest_dir, str(part_info["filename"]))
            self.log.emit(f"Reading {idx}/{total}: {part_info['filename']}")
            with open(part_path, "r", encoding="utf-8") as fh:
                part_doc = json.load(fh)

            pp = tuple(part_info.get("path_parts", []))
            is_list = bool(part_info.get("is_list", False))
            path_is_list[pp] = is_list

            if is_new_format:
                # part_doc IS the chunk value directly
                chunk_value = part_doc
            else:
                # Legacy: part_doc is full root document — extract target
                if fallback_root is None:
                    fallback_root = copy.deepcopy(part_doc)
                chunk_value = get_nested_value(part_doc, list(pp)) if pp else part_doc

            path_entries[pp].extend(get_entries(chunk_value))
            self.progress.emit(int(idx / total * 50))

        # Build reconstructed root
        if is_new_format:
            if root_skeleton_data is None:
                raise RuntimeError("Manifest missing root_skeleton (required for v4.7+ format).")
            reconstructed = copy.deepcopy(root_skeleton_data)
        else:
            if fallback_root is None:
                raise RuntimeError("No parts could be read.")
            reconstructed = copy.deepcopy(fallback_root)

        # Graft deepest paths first
        sorted_paths = sorted(path_entries.keys(), key=len, reverse=True)
        n = len(sorted_paths)
        for pi, pp in enumerate(sorted_paths):
            merged = rebuild_container(path_entries[pp], path_is_list[pp])
            reconstructed = set_nested_value(reconstructed, list(pp), merged)
            self.progress.emit(50 + int((pi + 1) / n * 50))

        with open(output_path, "w", encoding="utf-8") as fh:
            json.dump(reconstructed, fh, ensure_ascii=False, indent=2)

        ok = stable_hash(reconstructed) == str(manifest.get("source_sha256", ""))
        self.log.emit("Hash check PASSED ✓" if ok
                      else "WARNING: Hash check FAILED — output differs from original.")
        self.progress.emit(100)
        self.finished.emit(True, f"Reassembly complete: {output_path}")


# ---------------------------------------------------------------------------
# GUI
# ---------------------------------------------------------------------------

class JsonSplitterWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.worker: SplitterWorker | None = None
        self.loaded_json: Any = None
        self.setWindowTitle("JSON Splitter 4.7 — Compact Parts, No Wrapper Duplication")
        self.resize(900, 820)
        self._build_ui()

    def _build_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)
        root_layout = QVBoxLayout(central)
        root_layout.setContentsMargins(16, 16, 16, 16)
        root_layout.setSpacing(12)

        file_group = QGroupBox("Input JSON")
        fl = QGridLayout(file_group)
        self.input_edit = QLineEdit()
        self.browse_input_button = QPushButton("Browse JSON")
        self.inspect_button = QPushButton("Inspect")
        fl.addWidget(QLabel("Input file"), 0, 0)
        fl.addWidget(self.input_edit, 0, 1)
        fl.addWidget(self.browse_input_button, 0, 2)
        fl.addWidget(self.inspect_button, 0, 3)

        target_group = QGroupBox("Target Container To Split")
        tl = QGridLayout(target_group)
        self.target_edit = QLineEdit()
        self.target_edit.setPlaceholderText("e.g. project_summary.git_metadata  (leave blank for root)")
        self.target_combo = QComboBox()
        self.apply_target_button = QPushButton("Use Suggested Path")
        tl.addWidget(QLabel("Target path"), 0, 0)
        tl.addWidget(self.target_edit, 0, 1, 1, 3)
        tl.addWidget(QLabel("Detected container paths"), 1, 0)
        tl.addWidget(self.target_combo, 1, 1, 1, 2)
        tl.addWidget(self.apply_target_button, 1, 3)

        mode_group = QGroupBox("Split Mode")
        ml = QGridLayout(mode_group)
        self.parts_radio = QRadioButton("Split by number of parts")
        self.kb_radio = QRadioButton("Split by max size in KB")
        self.child_radio = QRadioButton("One file per direct child")
        self.parts_radio.setChecked(True)
        self.mode_group = QButtonGroup(self)
        for r in (self.parts_radio, self.kb_radio, self.child_radio):
            self.mode_group.addButton(r)
        self.parts_spin = QSpinBox()
        self.parts_spin.setRange(1, 100_000)
        self.parts_spin.setValue(10)
        self.kb_spin = QSpinBox()
        self.kb_spin.setRange(1, 1_024 * 1_024)
        self.kb_spin.setValue(10_240)
        ml.addWidget(self.parts_radio, 0, 0)
        ml.addWidget(self.parts_spin, 0, 1)
        ml.addWidget(self.kb_radio, 1, 0)
        ml.addWidget(self.kb_spin, 1, 1)
        ml.addWidget(self.child_radio, 2, 0, 1, 2)

        output_group = QGroupBox("Output")
        ol = QGridLayout(output_group)
        self.output_edit = QLineEdit()
        self.browse_output_button = QPushButton("Browse Folder")
        ol.addWidget(QLabel("Output folder"), 0, 0)
        ol.addWidget(self.output_edit, 0, 1)
        ol.addWidget(self.browse_output_button, 0, 2)

        action_row = QHBoxLayout()
        self.split_button = QPushButton("Split JSON")
        self.reassemble_button = QPushButton("Reassemble From Manifest")
        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        action_row.addWidget(self.split_button)
        action_row.addWidget(self.reassemble_button)
        action_row.addWidget(self.progress, 1)

        self.summary_label = QLabel("No JSON inspected yet.")
        self.summary_label.setFrameShape(QFrame.Shape.StyledPanel)
        self.summary_label.setMinimumHeight(60)
        self.summary_label.setWordWrap(True)

        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)

        root_layout.addWidget(file_group)
        root_layout.addWidget(target_group)
        root_layout.addWidget(mode_group)
        root_layout.addWidget(output_group)
        root_layout.addLayout(action_row)
        root_layout.addWidget(QLabel("Summary"))
        root_layout.addWidget(self.summary_label)
        root_layout.addWidget(QLabel("Log"))
        root_layout.addWidget(self.log_box, 1)

        self.browse_input_button.clicked.connect(self._browse_input)
        self.browse_output_button.clicked.connect(self._browse_output)
        self.inspect_button.clicked.connect(self._inspect_json)
        self.apply_target_button.clicked.connect(self._apply_target_from_combo)
        self.split_button.clicked.connect(self._start_split)
        self.reassemble_button.clicked.connect(self._start_reassemble)

    def _append_log(self, text: str) -> None:
        self.log_box.append(text)

    def _browse_input(self) -> None:
        path, _ = QFileDialog.getOpenFileName(self, "Select JSON", "", "JSON Files (*.json)")
        if path:
            self.input_edit.setText(path)

    def _browse_output(self) -> None:
        path = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if path:
            self.output_edit.setText(path)

    def _inspect_json(self) -> None:
        input_path = self.input_edit.text().strip()
        if not input_path:
            QMessageBox.warning(self, "Missing file", "Select an input JSON file first.")
            return
        try:
            with open(input_path, "r", encoding="utf-8") as fh:
                self.loaded_json = json.load(fh)
        except Exception as exc:
            QMessageBox.critical(self, "Read error", str(exc))
            return

        self.target_combo.clear()
        self.target_combo.addItem("")
        paths = collect_container_paths(self.loaded_json, max_depth=6)
        for p in paths:
            self.target_combo.addItem(p)

        size_kb = os.path.getsize(input_path) / 1024.0
        self.summary_label.setText(
            f"Root type: {type(self.loaded_json).__name__} | "
            f"File size: {size_kb:.2f} KB | "
            f"Detected container paths: {len(paths)}"
        )
        self._append_log(f"Inspected: {input_path}")
        sizes = []
        for p in paths:
            try:
                val = get_nested_value(self.loaded_json, parse_target_path(p))
                sizes.append((p, json_bytes_indented(val)))
            except Exception:
                continue
        sizes.sort(key=lambda x: x[1], reverse=True)
        self._append_log("Top 10 largest containers:")
        for p, sz in sizes[:10]:
            self._append_log(f"  {p}: {sz/1024:.2f} KB")
        if sizes:
            lp, ls = sizes[0]
            self._append_log(f"Largest: '{lp}' = {ls/1024/1024:.2f} MB")

    def _apply_target_from_combo(self) -> None:
        self.target_edit.setText(self.target_combo.currentText().strip())

    def _start_split(self) -> None:
        input_path = self.input_edit.text().strip()
        output_dir = self.output_edit.text().strip()
        target_path = self.target_edit.text().strip()
        if not input_path or not output_dir:
            QMessageBox.warning(self, "Missing data", "Select input JSON and output folder.")
            return
        if self.parts_radio.isChecked():
            mode, value = "parts", int(self.parts_spin.value())
        elif self.kb_radio.isChecked():
            mode, value = "kb", int(self.kb_spin.value())
        else:
            mode, value = "per_child", 1
        self._start_worker("split", {
            "input_path": input_path,
            "output_dir": output_dir,
            "target_path": target_path,
            "mode": mode,
            "value": value,
        })

    def _start_reassemble(self) -> None:
        manifest_path, _ = QFileDialog.getOpenFileName(
            self, "Select Manifest",
            self.output_edit.text().strip() or "",
            "JSON Files (*.json)",
        )
        if not manifest_path:
            return
        output_path, _ = QFileDialog.getSaveFileName(
            self, "Save Reassembled JSON",
            os.path.join(os.path.dirname(manifest_path), "reassembled.json"),
            "JSON Files (*.json)",
        )
        if not output_path:
            return
        self._start_worker("reassemble", {
            "manifest_path": manifest_path,
            "output_path": output_path,
        })

    def _start_worker(self, action: str, payload: dict[str, Any]) -> None:
        if self.worker is not None and self.worker.isRunning():
            QMessageBox.information(self, "Busy", "Another operation is already running.")
            return
        self.progress.setValue(0)
        self.worker = SplitterWorker(action, payload)
        self.worker.log.connect(self._append_log)
        self.worker.progress.connect(self.progress.setValue)
        self.worker.finished.connect(self._on_worker_finished)
        self.worker.start()

    def _on_worker_finished(self, ok: bool, message: str) -> None:
        self._append_log(message)
        if ok:
            QMessageBox.information(self, "Finished", message)
        else:
            QMessageBox.critical(self, "Error", message)


def main() -> None:
    app = QApplication([])
    window = JsonSplitterWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
