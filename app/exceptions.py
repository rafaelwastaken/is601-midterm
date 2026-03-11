"""Custom exception classes for the calculator application."""


class CalculatorError(Exception):
    """Base exception for all calculator-related errors."""


class OperationError(CalculatorError):
    """Raised when an arithmetic operation fails."""


class ValidationError(CalculatorError):
    """Raised when input validation fails."""


class HistoryError(CalculatorError):
    """Raised when a history operation fails (e.g., nothing to undo)."""


class ConfigurationError(CalculatorError):
    """Raised when there is a configuration issue."""


class FileOperationError(CalculatorError):
    """Raised when a file read/write operation fails."""
