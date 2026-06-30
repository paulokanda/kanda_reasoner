"""Support V10 project reasoning and evidence handling."""

# kanda_reasoner/kanda_reasoner_app/reasoner_engine/v10_conversation_memory.py

from __future__ import annotations

from kanda_reasoner_app.reasoner_engine.v10_models import ConversationTurn


class ConversationMemory:
    """Represent conversation memory."""
    
    def __init__(self) -> None:
        """Support init behavior.
        """
        
        self._turns: list[ConversationTurn] = []

    def add_turn(self, turn: ConversationTurn) -> None:
        """Support add turn behavior.
        
        Parameters
        ----------
        turn : ConversationTurn
            The turn value.
        """
        
        self._turns.append(turn)

    def clear(self) -> None:
        """Support clear behavior.
        """
        
        self._turns.clear()

    def turns(self) -> list[ConversationTurn]:
        """Support turns behavior.
        
        Returns
        -------
        list[ConversationTurn]
            The list of values.
        """
        
        return list(self._turns)

    def last_turn(self) -> ConversationTurn | None:
        """Support last turn behavior.
        
        Returns
        -------
        ConversationTurn | None
            The conversation turn result.
        """
        
        if not self._turns:
            return None
        return self._turns[-1]






