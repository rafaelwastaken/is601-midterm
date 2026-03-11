"""Arithmetic operations using the Factory Design Pattern."""

from abc import ABC, abstractmethod
from app.exceptions import OperationError


class Operation(ABC):
    """Abstract base class for all arithmetic operations."""

    @abstractmethod
    def execute(self, a: float, b: float) -> float:
        """Execute the operation on two operands.

        Args:
            a: First operand.
            b: Second operand.

        Returns:
            The result of the operation.
        """

    @staticmethod
    @abstractmethod
    def get_name() -> str:
        """Return the display name of the operation."""

    @staticmethod
    @abstractmethod
    def get_description() -> str:
        """Return a description of the operation for the help menu."""


class Addition(Operation):
    """Addition operation: a + b."""

    def execute(self, a: float, b: float) -> float:
        return a + b

    @staticmethod
    def get_name() -> str:
        return "add"

    @staticmethod
    def get_description() -> str:
        return "Add two numbers (a + b)"


class Subtraction(Operation):
    """Subtraction operation: a - b."""

    def execute(self, a: float, b: float) -> float:
        return a - b

    @staticmethod
    def get_name() -> str:
        return "subtract"

    @staticmethod
    def get_description() -> str:
        return "Subtract two numbers (a - b)"


class Multiplication(Operation):
    """Multiplication operation: a * b."""

    def execute(self, a: float, b: float) -> float:
        return a * b

    @staticmethod
    def get_name() -> str:
        return "multiply"

    @staticmethod
    def get_description() -> str:
        return "Multiply two numbers (a * b)"


class Division(Operation):
    """Division operation: a / b."""

    def execute(self, a: float, b: float) -> float:
        if b == 0:
            raise OperationError("Division by zero is not allowed.")
        return a / b

    @staticmethod
    def get_name() -> str:
        return "divide"

    @staticmethod
    def get_description() -> str:
        return "Divide two numbers (a / b)"


class Power(Operation):
    """Power operation: a ** b."""

    def execute(self, a: float, b: float) -> float:
        try:
            result = a ** b
            if isinstance(result, complex):
                raise OperationError(
                    f"Result of {a} ** {b} is a complex number, which is not supported."
                )
            return result
        except OverflowError as exc:
            raise OperationError(f"Result of {a} ** {b} is too large.") from exc

    @staticmethod
    def get_name() -> str:
        return "power"

    @staticmethod
    def get_description() -> str:
        return "Raise a to the power of b (a ^ b)"


class Root(Operation):
    """Root operation: a ** (1/b) — the bth root of a."""

    def execute(self, a: float, b: float) -> float:
        if b == 0:
            raise OperationError("Cannot compute the 0th root (division by zero in exponent).")
        if a < 0 and b % 2 == 0:
            raise OperationError(
                f"Cannot compute even root ({b}) of a negative number ({a})."
            )
        if a < 0:
            return -(abs(a) ** (1 / b))
        return a ** (1 / b)

    @staticmethod
    def get_name() -> str:
        return "root"

    @staticmethod
    def get_description() -> str:
        return "Compute the bth root of a"


class Modulus(Operation):
    """Modulus operation: a % b."""

    def execute(self, a: float, b: float) -> float:
        if b == 0:
            raise OperationError("Modulus by zero is not allowed.")
        return a % b

    @staticmethod
    def get_name() -> str:
        return "modulus"

    @staticmethod
    def get_description() -> str:
        return "Compute the remainder of a / b (a % b)"


class IntegerDivision(Operation):
    """Integer division operation: a // b."""

    def execute(self, a: float, b: float) -> float:
        if b == 0:
            raise OperationError("Integer division by zero is not allowed.")
        return float(int(a // b))

    @staticmethod
    def get_name() -> str:
        return "int_divide"

    @staticmethod
    def get_description() -> str:
        return "Integer division of a by b (a // b)"


class Percentage(Operation):
    """Percentage calculation: (a / b) * 100."""

    def execute(self, a: float, b: float) -> float:
        if b == 0:
            raise OperationError("Cannot calculate percentage with zero as the base.")
        return (a / b) * 100

    @staticmethod
    def get_name() -> str:
        return "percent"

    @staticmethod
    def get_description() -> str:
        return "Calculate percentage of a relative to b ((a/b)*100)"


class AbsoluteDifference(Operation):
    """Absolute difference: |a - b|."""

    def execute(self, a: float, b: float) -> float:
        return abs(a - b)

    @staticmethod
    def get_name() -> str:
        return "abs_diff"

    @staticmethod
    def get_description() -> str:
        return "Compute the absolute difference |a - b|"


class OperationFactory:
    """Factory class for creating operation instances.

    Uses the Factory Design Pattern to manage creation of different
    operation instances based on the operation name.
    """

    _operations: dict = {}

    @classmethod
    def register_operation(cls, name: str, operation_class: type) -> None:
        """Register a new operation class with the factory.

        Args:
            name: The command name for the operation.
            operation_class: The Operation subclass to register.
        """
        cls._operations[name] = operation_class

    @classmethod
    def create_operation(cls, name: str) -> Operation:
        """Create an operation instance by name.

        Args:
            name: The operation name (e.g., 'add', 'subtract').

        Returns:
            An instance of the requested Operation.

        Raises:
            OperationError: If the operation name is not recognized.
        """
        operation_class = cls._operations.get(name)
        if operation_class is None:
            available = ", ".join(sorted(cls._operations.keys()))
            raise OperationError(
                f"Unknown operation: '{name}'. Available operations: {available}"
            )
        return operation_class()

    @classmethod
    def get_available_operations(cls) -> dict:
        """Return a dictionary of all registered operations.

        Returns:
            Dict mapping operation names to their classes.
        """
        return dict(cls._operations)


def register_default_operations() -> None:
    """Register all default arithmetic operations with the factory."""
    default_ops = [
        Addition, Subtraction, Multiplication, Division,
        Power, Root, Modulus, IntegerDivision, Percentage, AbsoluteDifference,
    ]
    for op_class in default_ops:
        instance = op_class()
        OperationFactory.register_operation(instance.get_name(), op_class)
