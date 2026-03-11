"""Tests for the Calculation model."""

import pytest
from app.calculation import Calculation


class TestCalculation:
    def test_create_calculation(self):
        calc = Calculation("add", 2, 3, 5)
        assert calc.operation == "add"
        assert calc.operand_a == 2
        assert calc.operand_b == 3
        assert calc.result == 5
        assert calc.timestamp is not None

    def test_create_with_custom_timestamp(self):
        calc = Calculation("add", 1, 2, 3, timestamp="2025-01-01T00:00:00")
        assert calc.timestamp == "2025-01-01T00:00:00"

    def test_str_representation(self):
        calc = Calculation("multiply", 3, 4, 12)
        assert str(calc) == "multiply(3, 4) = 12"

    def test_repr(self):
        calc = Calculation("divide", 10, 2, 5.0)
        r = repr(calc)
        assert "Calculation(" in r
        assert "divide" in r

    def test_to_dict(self):
        calc = Calculation("subtract", 10, 4, 6, timestamp="2025-01-01T00:00:00")
        d = calc.to_dict()
        assert d["operation"] == "subtract"
        assert d["operand_a"] == 10
        assert d["operand_b"] == 4
        assert d["result"] == 6
        assert d["timestamp"] == "2025-01-01T00:00:00"

    def test_from_dict(self):
        data = {
            "operation": "add",
            "operand_a": "5",
            "operand_b": "3",
            "result": "8",
            "timestamp": "2025-01-01T00:00:00",
        }
        calc = Calculation.from_dict(data)
        assert calc.operation == "add"
        assert calc.operand_a == 5.0
        assert calc.operand_b == 3.0
        assert calc.result == 8.0

    def test_from_dict_without_timestamp(self):
        data = {
            "operation": "multiply",
            "operand_a": "2",
            "operand_b": "3",
            "result": "6",
        }
        calc = Calculation.from_dict(data)
        assert calc.timestamp is not None
