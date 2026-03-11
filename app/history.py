"""History management for the calculator using pandas for CSV serialization."""

import os
import logging
import pandas as pd
from app.calculation import Calculation
from app.exceptions import FileOperationError, HistoryError

logger = logging.getLogger(__name__)


class HistoryManager:
    """Manages the calculation history with save/load to CSV via pandas."""

    def __init__(self, history_file: str, max_history_size: int = 100,
                 encoding: str = "utf-8"):
        """Initialize the HistoryManager.

        Args:
            history_file: Path to the CSV file for persisting history.
            max_history_size: Maximum number of entries to keep in history.
            encoding: File encoding for CSV operations.
        """
        self._history: list = []
        self._history_file = history_file
        self._max_history_size = max_history_size
        self._encoding = encoding

    @property
    def history(self) -> list:
        """Return the current list of calculations."""
        return list(self._history)

    @property
    def history_ref(self) -> list:
        """Return a reference to the internal history list (for memento)."""
        return self._history

    @history_ref.setter
    def history_ref(self, value: list) -> None:
        """Set the internal history list (used by memento restore)."""
        self._history = value

    def add(self, calculation: Calculation) -> None:
        """Add a calculation to the history.

        Args:
            calculation: The Calculation instance to add.

        Raises:
            HistoryError: If the history has reached maximum capacity.
        """
        if len(self._history) >= self._max_history_size:
            logger.warning("History at max capacity (%d). Removing oldest entry.",
                           self._max_history_size)
            self._history.pop(0)
        self._history.append(calculation)
        logger.info("Added to history: %s", calculation)

    def clear(self) -> None:
        """Clear all calculation history."""
        self._history.clear()
        logger.info("Calculation history cleared.")

    def get_last(self) -> Calculation:
        """Return the most recent calculation.

        Returns:
            The last Calculation in history.

        Raises:
            HistoryError: If the history is empty.
        """
        if not self._history:
            raise HistoryError("No calculations in history.")
        return self._history[-1]

    def save_to_csv(self) -> None:
        """Save the calculation history to a CSV file using pandas.

        Raises:
            FileOperationError: If the file cannot be written.
        """
        try:
            directory = os.path.dirname(self._history_file)
            if directory:
                os.makedirs(directory, exist_ok=True)

            data = [calc.to_dict() for calc in self._history]
            df = pd.DataFrame(data, columns=["operation", "operand_a", "operand_b",
                                              "result", "timestamp"])
            df.to_csv(self._history_file, index=False, encoding=self._encoding)
            logger.info("History saved to %s (%d entries).", self._history_file, len(data))
        except Exception as exc:
            raise FileOperationError(f"Failed to save history to CSV: {exc}") from exc

    def load_from_csv(self) -> None:
        """Load calculation history from a CSV file using pandas.

        Raises:
            FileOperationError: If the file cannot be read or is malformed.
        """
        if not os.path.exists(self._history_file):
            raise FileOperationError(
                f"History file not found: {self._history_file}"
            )
        try:
            df = pd.read_csv(self._history_file, encoding=self._encoding)
            required_cols = {"operation", "operand_a", "operand_b", "result", "timestamp"}
            if not required_cols.issubset(set(df.columns)):
                raise FileOperationError(
                    f"CSV file is missing required columns. Expected: {required_cols}"
                )
            self._history = [
                Calculation.from_dict(row.to_dict()) for _, row in df.iterrows()
            ]
            logger.info("History loaded from %s (%d entries).",
                        self._history_file, len(self._history))
        except FileOperationError:
            raise
        except Exception as exc:
            raise FileOperationError(f"Failed to load history from CSV: {exc}") from exc

    def __len__(self) -> int:
        return len(self._history)
