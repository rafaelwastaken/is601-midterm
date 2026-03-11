"""Input validation utilities for the calculator application."""

from app.exceptions import ValidationError


def validate_number(value: str) -> float:
    """Validate and convert a string input to a float.

    Args:
        value: The string to validate and convert.

    Returns:
        The converted float value.

    Raises:
        ValidationError: If the value cannot be converted to a number.
    """
    try:
        return float(value)
    except (ValueError, TypeError) as exc:
        raise ValidationError(f"Invalid number: '{value}'. Please enter a valid numeric value.") from exc


def validate_input_range(value: float, max_value: float) -> float:
    """Validate that a number is within the allowed range.

    Args:
        value: The number to validate.
        max_value: The maximum allowed absolute value.

    Returns:
        The validated value.

    Raises:
        ValidationError: If the value exceeds the maximum allowed range.
    """
    if abs(value) > max_value:
        raise ValidationError(
            f"Input value {value} exceeds maximum allowed value of {max_value}."
        )
    return value


def validate_operands(a: float, b: float, max_value: float) -> tuple:
    """Validate both operands for a calculation.

    Args:
        a: First operand.
        b: Second operand.
        max_value: Maximum allowed absolute value.

    Returns:
        Tuple of validated (a, b).

    Raises:
        ValidationError: If either operand is invalid.
    """
    validate_input_range(a, max_value)
    validate_input_range(b, max_value)
    return a, b
