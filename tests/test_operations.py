"""Tests for arithmetic operations and the OperationFactory."""

import pytest
from app.operations import (
    Addition, Subtraction, Multiplication, Division,
    Power, Root, Modulus, IntegerDivision, Percentage, AbsoluteDifference,
    OperationFactory, register_default_operations,
)
from app.exceptions import OperationError


# ------------------------------------------------------------------ Fixtures
@pytest.fixture(autouse=True)
def _register_ops():
    """Ensure all default operations are registered before each test."""
    register_default_operations()


# --------------------------------------------------------- Parameterized Tests

class TestAddition:
    """Tests for the Addition operation."""

    @pytest.mark.parametrize("a, b, expected", [
        (2, 3, 5),
        (-1, 1, 0),
        (0, 0, 0),
        (1.5, 2.5, 4.0),
        (-3.5, -2.5, -6.0),
    ])
    def test_add(self, a, b, expected):
        op = Addition()
        assert op.execute(a, b) == expected

    def test_name(self):
        assert Addition.get_name() == "add"

    def test_description(self):
        assert "Add" in Addition.get_description()


class TestSubtraction:
    @pytest.mark.parametrize("a, b, expected", [
        (5, 3, 2),
        (0, 0, 0),
        (-1, -1, 0),
        (3.5, 1.5, 2.0),
    ])
    def test_subtract(self, a, b, expected):
        op = Subtraction()
        assert op.execute(a, b) == expected

    def test_name(self):
        assert Subtraction.get_name() == "subtract"


class TestMultiplication:
    @pytest.mark.parametrize("a, b, expected", [
        (2, 3, 6),
        (0, 100, 0),
        (-2, 3, -6),
        (-2, -3, 6),
        (1.5, 2, 3.0),
    ])
    def test_multiply(self, a, b, expected):
        op = Multiplication()
        assert op.execute(a, b) == expected

    def test_name(self):
        assert Multiplication.get_name() == "multiply"


class TestDivision:
    @pytest.mark.parametrize("a, b, expected", [
        (6, 3, 2),
        (7, 2, 3.5),
        (-6, 3, -2),
        (0, 5, 0),
    ])
    def test_divide(self, a, b, expected):
        op = Division()
        assert op.execute(a, b) == expected

    def test_divide_by_zero(self):
        op = Division()
        with pytest.raises(OperationError, match="Division by zero"):
            op.execute(10, 0)

    def test_name(self):
        assert Division.get_name() == "divide"


class TestPower:
    @pytest.mark.parametrize("a, b, expected", [
        (2, 3, 8),
        (5, 0, 1),
        (2, -1, 0.5),
        (9, 0.5, 3.0),
    ])
    def test_power(self, a, b, expected):
        op = Power()
        assert op.execute(a, b) == pytest.approx(expected)

    def test_power_overflow(self):
        op = Power()
        with pytest.raises(OperationError, match="too large"):
            op.execute(10.0, 1000)

    def test_power_complex_result(self):
        op = Power()
        with pytest.raises(OperationError, match="complex number"):
            op.execute(-1, 0.5)

    def test_name(self):
        assert Power.get_name() == "power"


class TestRoot:
    @pytest.mark.parametrize("a, b, expected", [
        (27, 3, 3.0),
        (16, 4, 2.0),
        (8, 3, 2.0),
    ])
    def test_root(self, a, b, expected):
        op = Root()
        assert op.execute(a, b) == pytest.approx(expected)

    def test_root_zero_index(self):
        op = Root()
        with pytest.raises(OperationError, match="0th root"):
            op.execute(8, 0)

    def test_root_negative_even(self):
        op = Root()
        with pytest.raises(OperationError, match="even root"):
            op.execute(-4, 2)

    def test_root_negative_odd(self):
        op = Root()
        result = op.execute(-27, 3)
        assert result == pytest.approx(-3.0)

    def test_name(self):
        assert Root.get_name() == "root"


class TestModulus:
    @pytest.mark.parametrize("a, b, expected", [
        (10, 3, 1),
        (10, 5, 0),
        (7.5, 2, 1.5),
    ])
    def test_modulus(self, a, b, expected):
        op = Modulus()
        assert op.execute(a, b) == pytest.approx(expected)

    def test_modulus_by_zero(self):
        op = Modulus()
        with pytest.raises(OperationError, match="Modulus by zero"):
            op.execute(10, 0)

    def test_name(self):
        assert Modulus.get_name() == "modulus"


class TestIntegerDivision:
    @pytest.mark.parametrize("a, b, expected", [
        (7, 2, 3),
        (10, 3, 3),
        (-7, 2, -4.0),
        (0, 5, 0),
    ])
    def test_int_divide(self, a, b, expected):
        op = IntegerDivision()
        assert op.execute(a, b) == expected

    def test_int_divide_by_zero(self):
        op = IntegerDivision()
        with pytest.raises(OperationError, match="Integer division by zero"):
            op.execute(10, 0)

    def test_name(self):
        assert IntegerDivision.get_name() == "int_divide"


class TestPercentage:
    @pytest.mark.parametrize("a, b, expected", [
        (50, 200, 25.0),
        (1, 4, 25.0),
        (3, 4, 75.0),
    ])
    def test_percent(self, a, b, expected):
        op = Percentage()
        assert op.execute(a, b) == pytest.approx(expected)

    def test_percent_zero_base(self):
        op = Percentage()
        with pytest.raises(OperationError, match="zero as the base"):
            op.execute(10, 0)

    def test_name(self):
        assert Percentage.get_name() == "percent"


class TestAbsoluteDifference:
    @pytest.mark.parametrize("a, b, expected", [
        (10, 3, 7),
        (3, 10, 7),
        (-5, 5, 10),
        (0, 0, 0),
    ])
    def test_abs_diff(self, a, b, expected):
        op = AbsoluteDifference()
        assert op.execute(a, b) == expected

    def test_name(self):
        assert AbsoluteDifference.get_name() == "abs_diff"


# ------------------------------------------------------- Factory Pattern Tests

class TestOperationFactory:
    def test_create_known_operation(self):
        op = OperationFactory.create_operation("add")
        assert isinstance(op, Addition)

    def test_create_unknown_operation(self):
        with pytest.raises(OperationError, match="Unknown operation"):
            OperationFactory.create_operation("nonexistent")

    def test_get_available_operations(self):
        ops = OperationFactory.get_available_operations()
        assert "add" in ops
        assert "subtract" in ops
        assert "power" in ops
        assert "root" in ops
        assert "modulus" in ops
        assert "int_divide" in ops
        assert "percent" in ops
        assert "abs_diff" in ops

    def test_register_custom_operation(self):
        class CustomOp(Addition):
            @staticmethod
            def get_name():
                return "custom"
            @staticmethod
            def get_description():
                return "Custom operation"

        OperationFactory.register_operation("custom", CustomOp)
        op = OperationFactory.create_operation("custom")
        assert isinstance(op, CustomOp)
        # Clean up
        del OperationFactory._operations["custom"]

    def test_all_operations_have_descriptions(self):
        ops = OperationFactory.get_available_operations()
        for name, op_class in ops.items():
            op = op_class()
            assert op.get_name() == name
            assert len(op.get_description()) > 0
