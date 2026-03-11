"""Memento Design Pattern implementation for calculator undo/redo support."""

from copy import deepcopy
from app.calculation import Calculation


class CalculatorMemento:
    """Stores a snapshot of the calculator's history state.

    This is the Memento in the Memento Design Pattern, capturing
    the state of the history at a particular point in time.
    """

    def __init__(self, history: list):
        """Initialize a memento with a copy of the history.

        Args:
            history: List of Calculation objects to snapshot.
        """
        self._state = deepcopy(history)

    def get_state(self) -> list:
        """Retrieve the stored history state.

        Returns:
            A deep copy of the stored history list.
        """
        return deepcopy(self._state)


class HistoryCaretaker:
    """Manages saving and restoring mementos for undo/redo.

    This is the Caretaker in the Memento Design Pattern.
    """

    def __init__(self):
        """Initialize the caretaker with empty undo/redo stacks."""
        self._undo_stack: list = []
        self._redo_stack: list = []

    def save(self, memento: CalculatorMemento) -> None:
        """Save a memento to the undo stack and clear the redo stack.

        Args:
            memento: The memento to save.
        """
        self._undo_stack.append(memento)
        self._redo_stack.clear()

    def undo(self) -> CalculatorMemento:
        """Pop and return the most recent memento from the undo stack.

        Returns:
            The most recent CalculatorMemento.

        Raises:
            IndexError: If there is nothing to undo.
        """
        if not self._undo_stack:
            raise IndexError("Nothing to undo.")
        memento = self._undo_stack.pop()
        return memento

    def redo(self) -> CalculatorMemento:
        """Pop and return the most recent memento from the redo stack.

        Returns:
            The most recent CalculatorMemento from redo stack.

        Raises:
            IndexError: If there is nothing to redo.
        """
        if not self._redo_stack:
            raise IndexError("Nothing to redo.")
        return self._redo_stack.pop()

    def push_redo(self, memento: CalculatorMemento) -> None:
        """Push a memento to the redo stack.

        Args:
            memento: The memento to push.
        """
        self._redo_stack.append(memento)

    @property
    def can_undo(self) -> bool:
        """Check if undo is available."""
        return len(self._undo_stack) > 0

    @property
    def can_redo(self) -> bool:
        """Check if redo is available."""
        return len(self._redo_stack) > 0
