"""Tests for input validators."""

import pytest
from app.input_validators import validate_number, validate_input_range, validate_operands
from app.exceptions import ValidationError


class TestValidateNumber:
    @pytest.mark.parametrize("value, expected", [
        ("5", 5.0),
        ("-3.14", -3.14),
        ("0", 0.0),
        ("1e5", 100000.0),
    ])
    def test_valid_numbers(self, value, expected):
        assert validate_number(value) == expected

    @pytest.mark.parametrize("value", ["abc", "", "12.34.56", None])
    def test_invalid_numbers(self, value):
        with pytest.raises(ValidationError, match="Invalid number"):
            validate_number(value)


class TestValidateInputRange:
    def test_within_range(self):
        assert validate_input_range(50, 100) == 50

    def test_at_boundary(self):
        assert validate_input_range(100, 100) == 100

    def test_exceeds_range(self):
        with pytest.raises(ValidationError, match="exceeds maximum"):
            validate_input_range(150, 100)

    def test_negative_within_range(self):
        assert validate_input_range(-50, 100) == -50

    def test_negative_exceeds_range(self):
        with pytest.raises(ValidationError, match="exceeds maximum"):
            validate_input_range(-150, 100)


class TestValidateOperands:
    def test_valid_operands(self):
        a, b = validate_operands(10, 20, 1000)
        assert a == 10
        assert b == 20

    def test_first_operand_invalid(self):
        with pytest.raises(ValidationError):
            validate_operands(2000, 20, 1000)

    def test_second_operand_invalid(self):
        with pytest.raises(ValidationError):
            validate_operands(10, 2000, 1000)
