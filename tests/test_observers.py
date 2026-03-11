"""Tests for the Observer pattern (LoggingObserver, AutoSaveObserver, ObserverManager)."""

import logging
import pytest
from unittest.mock import MagicMock
from app.calculation import Calculation
from app.history import HistoryManager
from app.observers import (
    LoggingObserver,
    AutoSaveObserver,
    ObserverManager,
    CalculatorObserver,
)


class TestLoggingObserver:
    def test_logs_calculation(self, caplog):
        observer = LoggingObserver()
        calc = Calculation("add", 1, 2, 3)
        with caplog.at_level(logging.INFO):
            observer.update(calc)
        assert "Calculation performed" in caplog.text
        assert "add" in caplog.text


class TestAutoSaveObserver:
    def test_auto_save_triggers(self, tmp_path):
        csv_file = str(tmp_path / "history.csv")
        history_manager = HistoryManager(history_file=csv_file)
        calc = Calculation("add", 1, 2, 3)
        history_manager.add(calc)

        observer = AutoSaveObserver(history_manager)
        observer.update(calc)

        import os
        assert os.path.exists(csv_file)


class TestObserverManager:
    def test_register_and_notify(self):
        manager = ObserverManager()
        mock_observer = MagicMock(spec=CalculatorObserver)
        manager.register(mock_observer)

        calc = Calculation("add", 1, 2, 3)
        manager.notify(calc)
        mock_observer.update.assert_called_once_with(calc)

    def test_unregister(self):
        manager = ObserverManager()
        mock_observer = MagicMock(spec=CalculatorObserver)
        manager.register(mock_observer)
        manager.unregister(mock_observer)

        calc = Calculation("add", 1, 2, 3)
        manager.notify(calc)
        mock_observer.update.assert_not_called()

    def test_register_duplicate_ignored(self):
        manager = ObserverManager()
        mock_observer = MagicMock(spec=CalculatorObserver)
        manager.register(mock_observer)
        manager.register(mock_observer)

        calc = Calculation("add", 1, 2, 3)
        manager.notify(calc)
        mock_observer.update.assert_called_once()

    def test_unregister_nonexistent_no_error(self):
        manager = ObserverManager()
        mock_observer = MagicMock(spec=CalculatorObserver)
        # Should not raise
        manager.unregister(mock_observer)

    def test_multiple_observers(self):
        manager = ObserverManager()
        obs1 = MagicMock(spec=CalculatorObserver)
        obs2 = MagicMock(spec=CalculatorObserver)
        manager.register(obs1)
        manager.register(obs2)

        calc = Calculation("multiply", 3, 4, 12)
        manager.notify(calc)
        obs1.update.assert_called_once_with(calc)
        obs2.update.assert_called_once_with(calc)
