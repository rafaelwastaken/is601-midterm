"""Tests for the main Calculator class."""

import pytest
from app.calculator import Calculator
from app.exceptions import HistoryError, OperationError, ValidationError


class TestCalculator:
    """Tests for core calculator functionality."""

    def test_basic_addition(self, config):
        calc = Calculator(config=config)
        result = calc.calculate("add", 2, 3)
        assert result == 5

    def test_basic_subtraction(self, config):
        calc = Calculator(config=config)
        result = calc.calculate("subtract", 10, 4)
        assert result == 6

    def test_basic_multiplication(self, config):
        calc = Calculator(config=config)
        result = calc.calculate("multiply", 3, 4)
        assert result == 12

    def test_basic_division(self, config):
        calc = Calculator(config=config)
        result = calc.calculate("divide", 10, 2)
        assert result == 5

    def test_power(self, config):
        calc = Calculator(config=config)
        result = calc.calculate("power", 2, 10)
        assert result == 1024

    def test_root(self, config):
        calc = Calculator(config=config)
        result = calc.calculate("root", 27, 3)
        assert result == pytest.approx(3.0)

    def test_modulus(self, config):
        calc = Calculator(config=config)
        result = calc.calculate("modulus", 10, 3)
        assert result == 1

    def test_int_divide(self, config):
        calc = Calculator(config=config)
        result = calc.calculate("int_divide", 7, 2)
        assert result == 3

    def test_percentage(self, config):
        calc = Calculator(config=config)
        result = calc.calculate("percent", 50, 200)
        assert result == 25.0

    def test_abs_diff(self, config):
        calc = Calculator(config=config)
        result = calc.calculate("abs_diff", 3, 10)
        assert result == 7

    def test_division_by_zero(self, config):
        calc = Calculator(config=config)
        with pytest.raises(OperationError, match="Division by zero"):
            calc.calculate("divide", 10, 0)

    def test_unknown_operation(self, config):
        calc = Calculator(config=config)
        with pytest.raises(OperationError, match="Unknown operation"):
            calc.calculate("unknown_op", 1, 2)

    def test_input_exceeds_max(self, config):
        calc = Calculator(config=config)
        with pytest.raises(ValidationError, match="exceeds maximum"):
            calc.calculate("add", 1e12, 1)

    def test_precision_rounding(self, config):
        calc = Calculator(config=config)
        result = calc.calculate("divide", 1, 3)
        # Precision is 8 in test config
        assert result == round(1 / 3, 8)


class TestCalculatorHistory:
    """Tests for calculator history management."""

    def test_history_recorded(self, config):
        calc = Calculator(config=config)
        calc.calculate("add", 1, 2)
        calc.calculate("subtract", 5, 3)
        history = calc.get_history()
        assert len(history) == 2

    def test_clear_history(self, config):
        calc = Calculator(config=config)
        calc.calculate("add", 1, 2)
        calc.clear_history()
        assert len(calc.get_history()) == 0


class TestCalculatorUndoRedo:
    """Tests for undo/redo using Memento pattern."""

    def test_undo(self, config):
        calc = Calculator(config=config)
        calc.calculate("add", 1, 2)
        calc.calculate("add", 3, 4)
        assert len(calc.get_history()) == 2

        calc.undo()
        assert len(calc.get_history()) == 1
        assert calc.get_history()[0].result == 3

    def test_undo_all(self, config):
        calc = Calculator(config=config)
        calc.calculate("add", 1, 1)
        calc.undo()
        assert len(calc.get_history()) == 0

    def test_undo_empty(self, config):
        calc = Calculator(config=config)
        with pytest.raises(HistoryError, match="Nothing to undo"):
            calc.undo()

    def test_redo(self, config):
        calc = Calculator(config=config)
        calc.calculate("add", 1, 2)
        calc.calculate("multiply", 3, 4)
        calc.undo()
        assert len(calc.get_history()) == 1

        calc.redo()
        assert len(calc.get_history()) == 2

    def test_redo_empty(self, config):
        calc = Calculator(config=config)
        with pytest.raises(HistoryError, match="Nothing to redo"):
            calc.redo()

    def test_undo_redo_cycle(self, config):
        calc = Calculator(config=config)
        calc.calculate("add", 10, 20)
        calc.calculate("subtract", 50, 20)
        calc.undo()
        calc.redo()
        history = calc.get_history()
        assert len(history) == 2
        assert history[-1].result == 30


class TestCalculatorSaveLoad:
    """Tests for save/load history to CSV."""

    def test_save_and_load(self, config):
        calc = Calculator(config=config)
        calc.calculate("add", 1, 2)
        calc.calculate("multiply", 3, 4)
        calc.save_history()

        # Create new calculator and load
        calc2 = Calculator(config=config)
        calc2.load_history()
        history = calc2.get_history()
        assert len(history) == 2
        assert history[0].result == 3
        assert history[1].result == 12

    def test_load_nonexistent_file(self, config):
        calc = Calculator(config=config)
        from app.exceptions import FileOperationError
        with pytest.raises(FileOperationError, match="not found"):
            calc.load_history()
