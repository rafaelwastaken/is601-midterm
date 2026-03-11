"""Tests for the HistoryManager class."""

import os
import pytest
import pandas as pd
from app.calculation import Calculation
from app.history import HistoryManager
from app.exceptions import FileOperationError, HistoryError


@pytest.fixture
def history_manager(tmp_path):
    """Create a HistoryManager with a temp CSV path."""
    csv_file = str(tmp_path / "history.csv")
    return HistoryManager(history_file=csv_file, max_history_size=5)


class TestHistoryManager:
    def test_add_calculation(self, history_manager):
        calc = Calculation("add", 1, 2, 3)
        history_manager.add(calc)
        assert len(history_manager) == 1

    def test_history_property(self, history_manager):
        calc = Calculation("add", 1, 2, 3)
        history_manager.add(calc)
        history = history_manager.history
        assert len(history) == 1
        # Ensure it's a copy
        history.clear()
        assert len(history_manager) == 1

    def test_clear_history(self, history_manager):
        history_manager.add(Calculation("add", 1, 2, 3))
        history_manager.clear()
        assert len(history_manager) == 0

    def test_get_last(self, history_manager):
        history_manager.add(Calculation("add", 1, 2, 3))
        history_manager.add(Calculation("multiply", 3, 4, 12))
        last = history_manager.get_last()
        assert last.result == 12

    def test_get_last_empty(self, history_manager):
        with pytest.raises(HistoryError, match="No calculations"):
            history_manager.get_last()

    def test_max_history_size(self, history_manager):
        for i in range(7):
            history_manager.add(Calculation("add", i, 1, i + 1))
        assert len(history_manager) == 5

    def test_save_to_csv(self, history_manager):
        history_manager.add(Calculation("add", 1, 2, 3, "2025-01-01T00:00:00"))
        history_manager.save_to_csv()
        assert os.path.exists(history_manager._history_file)
        df = pd.read_csv(history_manager._history_file)
        assert len(df) == 1
        assert df.iloc[0]["operation"] == "add"

    def test_load_from_csv(self, history_manager):
        history_manager.add(Calculation("add", 1, 2, 3, "2025-01-01T00:00:00"))
        history_manager.add(Calculation("multiply", 3, 4, 12, "2025-01-01T00:00:01"))
        history_manager.save_to_csv()

        new_manager = HistoryManager(
            history_file=history_manager._history_file, max_history_size=10
        )
        new_manager.load_from_csv()
        assert len(new_manager) == 2
        assert new_manager.history[0].operation == "add"
        assert new_manager.history[1].result == 12

    def test_load_nonexistent_file(self, tmp_path):
        manager = HistoryManager(history_file=str(tmp_path / "nope.csv"))
        with pytest.raises(FileOperationError, match="not found"):
            manager.load_from_csv()

    def test_load_malformed_csv(self, tmp_path):
        csv_file = str(tmp_path / "bad.csv")
        with open(csv_file, "w") as f:
            f.write("col1,col2\n1,2\n")
        manager = HistoryManager(history_file=csv_file)
        with pytest.raises(FileOperationError, match="missing required columns"):
            manager.load_from_csv()

    def test_save_empty_history(self, history_manager):
        history_manager.save_to_csv()
        assert os.path.exists(history_manager._history_file)
        df = pd.read_csv(history_manager._history_file)
        assert len(df) == 0

    def test_history_ref_setter(self, history_manager):
        calcs = [Calculation("add", 1, 2, 3)]
        history_manager.history_ref = calcs
        assert len(history_manager) == 1
