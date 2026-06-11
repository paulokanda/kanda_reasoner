"""Support V10 project reasoning and evidence handling."""

# developer_tools/kanda_reasoner_app/reasoner_engine/v10_conversation_memory.py

from __future__ import annotations

from kanda_reasoner_app.reasoner_engine.v10_models import ConversationTurn


class ConversationMemory:
    def __init__(self) -> None:
        self._turns: list[ConversationTurn] = []

    def add_turn(self, turn: ConversationTurn) -> None:
        self._turns.append(turn)

    def clear(self) -> None:
        self._turns.clear()

    def turns(self) -> list[ConversationTurn]:
        return list(self._turns)

    def last_turn(self) -> ConversationTurn | None:
        if not self._turns:
            return None
        return self._turns[-1]






