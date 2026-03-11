"""Calculation model representing a single arithmetic calculation."""

from datetime import datetime


class Calculation:
    """Represents a single calculation with its operation, operands, result, and timestamp."""

    def __init__(self, operation: str, operand_a: float, operand_b: float,
                 result: float, timestamp: str = None):
        """Initialize a Calculation instance.

        Args:
            operation: The name of the operation performed.
            operand_a: The first operand.
            operand_b: The second operand.
            result: The computed result.
            timestamp: ISO-format timestamp string; defaults to current time.
        """
        self.operation = operation
        self.operand_a = operand_a
        self.operand_b = operand_b
        self.result = result
        self.timestamp = timestamp or datetime.now().isoformat()

    def __repr__(self) -> str:
        return (
            f"Calculation(operation='{self.operation}', a={self.operand_a}, "
            f"b={self.operand_b}, result={self.result}, timestamp='{self.timestamp}')"
        )

    def __str__(self) -> str:
        return f"{self.operation}({self.operand_a}, {self.operand_b}) = {self.result}"

    def to_dict(self) -> dict:
        """Convert the calculation to a dictionary for serialization.

        Returns:
            Dictionary with operation, operand_a, operand_b, result, and timestamp.
        """
        return {
            "operation": self.operation,
            "operand_a": self.operand_a,
            "operand_b": self.operand_b,
            "result": self.result,
            "timestamp": self.timestamp,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Calculation":
        """Create a Calculation instance from a dictionary.

        Args:
            data: Dictionary with keys operation, operand_a, operand_b, result, timestamp.

        Returns:
            A new Calculation instance.
        """
        return cls(
            operation=data["operation"],
            operand_a=float(data["operand_a"]),
            operand_b=float(data["operand_b"]),
            result=float(data["result"]),
            timestamp=data.get("timestamp"),
        )
