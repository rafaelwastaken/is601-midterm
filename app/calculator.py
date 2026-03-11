"""Main Calculator class integrating all components."""

import logging
from app.calculation import Calculation
from app.calculator_config import CalculatorConfig
from app.calculator_memento import CalculatorMemento, HistoryCaretaker
from app.exceptions import HistoryError, OperationError, ValidationError
from app.history import HistoryManager
from app.input_validators import validate_operands
from app.logger import Logger
from app.observers import (
    AutoSaveObserver,
    LoggingObserver,
    ObserverManager,
)
from app.operations import OperationFactory, register_default_operations


class Calculator:
    """Advanced calculator with history, undo/redo, observers, and configuration.

    Integrates:
    - Factory Pattern for operations
    - Memento Pattern for undo/redo
    - Observer Pattern for logging and auto-save
    """

    def __init__(self, config: CalculatorConfig = None):
        """Initialize the Calculator with configuration and all subsystems.

        Args:
            config: CalculatorConfig instance. If None, uses default config.
        """
        self.config = config or CalculatorConfig()

        # Set up logging
        Logger.setup(log_file=self.config.log_file)
        self._logger = logging.getLogger(__name__)
        self._logger.info("Calculator initializing with config: %s", self.config)

        # Register default operations
        register_default_operations()

        # Initialize history manager
        self.history_manager = HistoryManager(
            history_file=self.config.history_file,
            max_history_size=self.config.max_history_size,
            encoding=self.config.default_encoding,
        )

        # Initialize memento caretaker for undo/redo
        self._caretaker = HistoryCaretaker()

        # Initialize observer manager and register observers
        self._observer_manager = ObserverManager()
        self._logging_observer = LoggingObserver()
        self._observer_manager.register(self._logging_observer)

        if self.config.auto_save:
            self._auto_save_observer = AutoSaveObserver(self.history_manager)
            self._observer_manager.register(self._auto_save_observer)

        self._logger.info("Calculator initialized successfully.")

    def calculate(self, operation_name: str, a: float, b: float) -> float:
        """Perform a calculation and record it in history.

        Args:
            operation_name: Name of the operation (e.g., 'add', 'subtract').
            a: First operand.
            b: Second operand.

        Returns:
            The result of the calculation, rounded to configured precision.

        Raises:
            OperationError: If the operation fails.
            ValidationError: If the inputs are invalid.
        """
        # Validate operands
        validate_operands(a, b, self.config.max_input_value)

        # Save current state for undo
        self._caretaker.save(
            CalculatorMemento(self.history_manager.history_ref)
        )

        # Create and execute operation
        operation = OperationFactory.create_operation(operation_name)
        result = operation.execute(a, b)
        result = round(result, self.config.precision)

        # Create calculation record and add to history
        calc = Calculation(operation_name, a, b, result)
        self.history_manager.add(calc)

        # Notify observers
        self._observer_manager.notify(calc)

        self._logger.info("Calculated: %s(%s, %s) = %s", operation_name, a, b, result)
        return result

    def undo(self) -> str:
        """Undo the last calculation.

        Returns:
            A message indicating what was undone.

        Raises:
            HistoryError: If there is nothing to undo.
        """
        if not self._caretaker.can_undo:
            raise HistoryError("Nothing to undo.")

        # Save current state for redo
        current_memento = CalculatorMemento(self.history_manager.history_ref)
        self._caretaker.push_redo(current_memento)

        # Restore previous state
        previous_memento = self._caretaker.undo()
        self.history_manager.history_ref = previous_memento.get_state()

        self._logger.info("Undo performed. History size: %d", len(self.history_manager))
        return "Undo successful."

    def redo(self) -> str:
        """Redo the last undone calculation.

        Returns:
            A message indicating what was redone.

        Raises:
            HistoryError: If there is nothing to redo.
        """
        if not self._caretaker.can_redo:
            raise HistoryError("Nothing to redo.")

        # Restore redo state first
        redo_memento = self._caretaker.redo()

        # Save current state for undo (push directly to undo stack to avoid clearing redo)
        current_memento = CalculatorMemento(self.history_manager.history_ref)
        self._caretaker._undo_stack.append(current_memento)

        self.history_manager.history_ref = redo_memento.get_state()

        self._logger.info("Redo performed. History size: %d", len(self.history_manager))
        return "Redo successful."

    def get_history(self) -> list:
        """Return the calculation history.

        Returns:
            List of Calculation objects.
        """
        return self.history_manager.history

    def clear_history(self) -> None:
        """Clear all calculation history."""
        self._caretaker.save(
            CalculatorMemento(self.history_manager.history_ref)
        )
        self.history_manager.clear()
        self._logger.info("History cleared.")

    def save_history(self) -> None:
        """Save calculation history to CSV file."""
        self.history_manager.save_to_csv()

    def load_history(self) -> None:
        """Load calculation history from CSV file."""
        self.history_manager.load_from_csv()
        self._logger.info("History loaded. Entries: %d", len(self.history_manager))
