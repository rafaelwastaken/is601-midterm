"""Tests for custom exceptions."""

from app.exceptions import (
    CalculatorError,
    OperationError,
    ValidationError,
    HistoryError,
    ConfigurationError,
    FileOperationError,
)


class TestExceptions:
    def test_calculator_error(self):
        exc = CalculatorError("test")
        assert str(exc) == "test"
        assert isinstance(exc, Exception)

    def test_operation_error_inherits(self):
        exc = OperationError("op error")
        assert isinstance(exc, CalculatorError)

    def test_validation_error_inherits(self):
        exc = ValidationError("val error")
        assert isinstance(exc, CalculatorError)

    def test_history_error_inherits(self):
        exc = HistoryError("hist error")
        assert isinstance(exc, CalculatorError)

    def test_configuration_error_inherits(self):
        exc = ConfigurationError("config error")
        assert isinstance(exc, CalculatorError)

    def test_file_operation_error_inherits(self):
        exc = FileOperationError("file error")
        assert isinstance(exc, CalculatorError)
