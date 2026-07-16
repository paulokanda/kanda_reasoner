"""Chunk balancing helpers for Project Reasoner JSON Splitter.

These helpers are intentionally pure and GUI-independent so they can be tested
without importing PySide6.
"""

from __future__ import annotations

from typing import TypeVar

__all__ = [
    "merge_excess_tail_chunks",
]

T = TypeVar("T")


def merge_excess_tail_chunks(
    chunks: list[list[T]],
    n_parts: int,
) -> list[list[T]]:
    """Merge excess chunks without dropping the final chunk.

    The old inline expression `chunks[-1].extend(chunks.pop())` is unsafe
    because it can evaluate the current last chunk as the receiver, pop that
    same chunk, and then extend the removed object. That drops the chunk from
    the returned list.

    This function explicitly pops the tail first and then extends the new last
    chunk.
    """
    if n_parts < 1:
        n_parts = 1

    output = [list(chunk) for chunk in chunks if chunk]

    while len(output) > n_parts and len(output) >= 2:
        tail = output.pop()
        output[-1].extend(tail)

    return output
