"""Observer Design Pattern for calculator events (logging and auto-save)."""

import logging
from abc import ABC, abstractmethod
from app.calculation import Calculation
from app.history import HistoryManager

logger = logging.getLogger(__name__)


class CalculatorObserver(ABC):
    """Abstract base class for calculator observers."""

    @abstractmethod
    def update(self, calculation: Calculation) -> None:
        """Called when a new calculation is performed.

        Args:
            calculation: The new Calculation that was just performed.
        """


class LoggingObserver(CalculatorObserver):
    """Observer that logs each calculation to the log file."""

    def __init__(self):
        """Initialize the LoggingObserver."""
        self._logger = logging.getLogger("calculator.observer.logging")

    def update(self, calculation: Calculation) -> None:
        """Log the calculation details.

        Args:
            calculation: The Calculation to log.
        """
        self._logger.info(
            "Calculation performed: %s(%s, %s) = %s",
            calculation.operation,
            calculation.operand_a,
            calculation.operand_b,
            calculation.result,
        )


class AutoSaveObserver(CalculatorObserver):
    """Observer that auto-saves the history to CSV when a new calculation is added."""

    def __init__(self, history_manager: HistoryManager):
        """Initialize the AutoSaveObserver.

        Args:
            history_manager: The HistoryManager to trigger saves on.
        """
        self._history_manager = history_manager

    def update(self, calculation: Calculation) -> None:
        """Auto-save the history to CSV.

        Args:
            calculation: The new Calculation (used for logging context).
        """
        try:
            self._history_manager.save_to_csv()
            logger.info("Auto-save triggered after calculation: %s", calculation)
        except Exception as exc:  # pragma: no cover
            logger.error("Auto-save failed: %s", exc)


class ObserverManager:
    """Manages a list of observers and notifies them of events."""

    def __init__(self):
        """Initialize with an empty list of observers."""
        self._observers: list = []

    def register(self, observer: CalculatorObserver) -> None:
        """Register an observer.

        Args:
            observer: The observer to register.
        """
        if observer not in self._observers:
            self._observers.append(observer)
            logger.info("Observer registered: %s", type(observer).__name__)

    def unregister(self, observer: CalculatorObserver) -> None:
        """Remove an observer.

        Args:
            observer: The observer to remove.
        """
        if observer in self._observers:
            self._observers.remove(observer)
            logger.info("Observer unregistered: %s", type(observer).__name__)

    def notify(self, calculation: Calculation) -> None:
        """Notify all registered observers of a new calculation.

        Args:
            calculation: The Calculation to notify observers about.
        """
        for observer in self._observers:
            try:
                observer.update(calculation)
            except Exception as exc:  # pragma: no cover
                logger.error("Observer %s failed: %s",
                             type(observer).__name__, exc)
