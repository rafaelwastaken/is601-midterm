"""Command-Line Interface (REPL) for the Advanced Calculator Application.

Implements optional features:
- Color-coded outputs using colorama
- Dynamic help menu using the Decorator Design Pattern
- Command Design Pattern for encapsulating operations
"""

import sys
import logging
from abc import ABC, abstractmethod
from colorama import init as colorama_init, Fore, Style
from app.calculator import Calculator
from app.calculator_config import CalculatorConfig
from app.exceptions import (
    CalculatorError,
    HistoryError,
    OperationError,
    ValidationError,
    FileOperationError,
)
from app.input_validators import validate_number
from app.operations import OperationFactory

logger = logging.getLogger(__name__)

# Initialize colorama for cross-platform color support
colorama_init(autoreset=True)


# ---------------------------------------------------------------------------
# Command Design Pattern: encapsulate each REPL action as a Command object
# ---------------------------------------------------------------------------

class Command(ABC):
    """Abstract base class for REPL commands (Command Design Pattern)."""

    @abstractmethod
    def execute(self, args: list) -> None:
        """Execute the command.

        Args:
            args: List of string arguments from user input.
        """

    @staticmethod
    @abstractmethod
    def get_name() -> str:
        """Return the command keyword."""

    @staticmethod
    @abstractmethod
    def get_help() -> str:
        """Return a help string for the command."""


# ---------------------------------------------------------------------------
# Decorator for dynamically building the help menu
# ---------------------------------------------------------------------------

_registered_commands: dict = {}


def register_command(cls):
    """Class decorator that registers a command in the global command registry.

    This implements the Decorator Design Pattern to dynamically generate
    the help menu based on available commands.
    """
    instance = cls.__new__(cls)
    _registered_commands[cls.get_name()] = {
        "class": cls,
        "help": cls.get_help(),
    }
    return cls


def get_registered_commands() -> dict:
    """Return the dictionary of all registered commands."""
    return _registered_commands


# ---------------------------------------------------------------------------
# Concrete Command implementations
# ---------------------------------------------------------------------------

@register_command
class CalculationCommand(Command):
    """Handles all arithmetic calculation commands."""

    def __init__(self, calculator: Calculator):
        self._calculator = calculator

    def execute(self, args: list) -> None:
        operation_name = args[0]
        if len(args) != 3:
            print(f"{Fore.RED}Usage: {operation_name} <number1> <number2>{Style.RESET_ALL}")
            return
        try:
            a = validate_number(args[1])
            b = validate_number(args[2])
            result = self._calculator.calculate(operation_name, a, b)
            print(f"{Fore.GREEN}Result: {result}{Style.RESET_ALL}")
        except (OperationError, ValidationError) as exc:
            print(f"{Fore.RED}Error: {exc}{Style.RESET_ALL}")

    @staticmethod
    def get_name() -> str:
        return "calculation"

    @staticmethod
    def get_help() -> str:
        return "Perform a calculation: <operation> <num1> <num2>"


@register_command
class HistoryCommand(Command):
    """Display calculation history."""

    def __init__(self, calculator: Calculator):
        self._calculator = calculator

    def execute(self, args: list) -> None:
        history = self._calculator.get_history()
        if not history:
            print(f"{Fore.YELLOW}No calculations in history.{Style.RESET_ALL}")
            return
        print(f"{Fore.CYAN}--- Calculation History ---{Style.RESET_ALL}")
        for i, calc in enumerate(history, 1):
            print(f"{Fore.CYAN}  {i}. {calc}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}--------------------------{Style.RESET_ALL}")

    @staticmethod
    def get_name() -> str:
        return "history"

    @staticmethod
    def get_help() -> str:
        return "Display the calculation history"


@register_command
class ClearCommand(Command):
    """Clear calculation history."""

    def __init__(self, calculator: Calculator):
        self._calculator = calculator

    def execute(self, args: list) -> None:
        self._calculator.clear_history()
        print(f"{Fore.YELLOW}History cleared.{Style.RESET_ALL}")

    @staticmethod
    def get_name() -> str:
        return "clear"

    @staticmethod
    def get_help() -> str:
        return "Clear the calculation history"


@register_command
class UndoCommand(Command):
    """Undo the last calculation."""

    def __init__(self, calculator: Calculator):
        self._calculator = calculator

    def execute(self, args: list) -> None:
        try:
            msg = self._calculator.undo()
            print(f"{Fore.YELLOW}{msg}{Style.RESET_ALL}")
        except HistoryError as exc:
            print(f"{Fore.RED}Error: {exc}{Style.RESET_ALL}")

    @staticmethod
    def get_name() -> str:
        return "undo"

    @staticmethod
    def get_help() -> str:
        return "Undo the last calculation"


@register_command
class RedoCommand(Command):
    """Redo the last undone calculation."""

    def __init__(self, calculator: Calculator):
        self._calculator = calculator

    def execute(self, args: list) -> None:
        try:
            msg = self._calculator.redo()
            print(f"{Fore.YELLOW}{msg}{Style.RESET_ALL}")
        except HistoryError as exc:
            print(f"{Fore.RED}Error: {exc}{Style.RESET_ALL}")

    @staticmethod
    def get_name() -> str:
        return "redo"

    @staticmethod
    def get_help() -> str:
        return "Redo the last undone calculation"


@register_command
class SaveCommand(Command):
    """Save history to CSV file."""

    def __init__(self, calculator: Calculator):
        self._calculator = calculator

    def execute(self, args: list) -> None:
        try:
            self._calculator.save_history()
            print(f"{Fore.GREEN}History saved successfully.{Style.RESET_ALL}")
        except FileOperationError as exc:
            print(f"{Fore.RED}Error saving history: {exc}{Style.RESET_ALL}")

    @staticmethod
    def get_name() -> str:
        return "save"

    @staticmethod
    def get_help() -> str:
        return "Save calculation history to CSV file"


@register_command
class LoadCommand(Command):
    """Load history from CSV file."""

    def __init__(self, calculator: Calculator):
        self._calculator = calculator

    def execute(self, args: list) -> None:
        try:
            self._calculator.load_history()
            print(f"{Fore.GREEN}History loaded successfully.{Style.RESET_ALL}")
        except FileOperationError as exc:
            print(f"{Fore.RED}Error loading history: {exc}{Style.RESET_ALL}")

    @staticmethod
    def get_name() -> str:
        return "load"

    @staticmethod
    def get_help() -> str:
        return "Load calculation history from CSV file"


@register_command
class HelpCommand(Command):
    """Display available commands (dynamically generated)."""

    def __init__(self, calculator: Calculator = None):
        self._calculator = calculator

    def execute(self, args: list) -> None:
        print(f"\n{Fore.CYAN}{'=' * 50}")
        print(f"  Advanced Calculator - Available Commands")
        print(f"{'=' * 50}{Style.RESET_ALL}")

        # Show arithmetic operations from the factory
        operations = OperationFactory.get_available_operations()
        print(f"\n{Fore.GREEN}  Arithmetic Operations:{Style.RESET_ALL}")
        for name, op_class in sorted(operations.items()):
            op = op_class()
            print(f"    {Fore.WHITE}{name:<15}{Style.RESET_ALL} - {op.get_description()}")

        # Show management commands from the registry
        print(f"\n{Fore.GREEN}  Management Commands:{Style.RESET_ALL}")
        management_cmds = {
            "history": "Display the calculation history",
            "clear": "Clear the calculation history",
            "undo": "Undo the last calculation",
            "redo": "Redo the last undone calculation",
            "save": "Save calculation history to CSV file",
            "load": "Load calculation history from CSV file",
            "help": "Display this help menu",
            "exit": "Exit the application",
        }
        for name, desc in management_cmds.items():
            print(f"    {Fore.WHITE}{name:<15}{Style.RESET_ALL} - {desc}")

        print(f"\n{Fore.CYAN}  Usage: <operation> <number1> <number2>")
        print(f"  Example: add 5 3{Style.RESET_ALL}\n")

    @staticmethod
    def get_name() -> str:
        return "help"

    @staticmethod
    def get_help() -> str:
        return "Display available commands"


@register_command
class ExitCommand(Command):
    """Exit the application."""

    def __init__(self, calculator: Calculator = None):
        self._calculator = calculator

    def execute(self, args: list) -> None:
        print(f"{Fore.CYAN}Thank you for using the Advanced Calculator. Goodbye!{Style.RESET_ALL}")
        sys.exit(0)

    @staticmethod
    def get_name() -> str:
        return "exit"

    @staticmethod
    def get_help() -> str:
        return "Exit the application"


# ---------------------------------------------------------------------------
# REPL class
# ---------------------------------------------------------------------------

class REPL:
    """Read-Eval-Print Loop for the calculator application."""

    # Operations that take two numeric arguments
    OPERATION_COMMANDS = {
        "add", "subtract", "multiply", "divide",
        "power", "root", "modulus", "int_divide",
        "percent", "abs_diff",
    }

    MANAGEMENT_COMMANDS = {
        "history", "clear", "undo", "redo",
        "save", "load", "help", "exit",
    }

    def __init__(self, config: CalculatorConfig = None):
        """Initialize the REPL with a Calculator instance.

        Args:
            config: Optional CalculatorConfig. Uses defaults if not provided.
        """
        self._calculator = Calculator(config=config)
        self._commands = self._build_command_map()

    def _build_command_map(self) -> dict:
        """Build a mapping from command names to Command instances."""
        calc = self._calculator
        commands = {
            "history": HistoryCommand(calc),
            "clear": ClearCommand(calc),
            "undo": UndoCommand(calc),
            "redo": RedoCommand(calc),
            "save": SaveCommand(calc),
            "load": LoadCommand(calc),
            "help": HelpCommand(calc),
            "exit": ExitCommand(calc),
        }
        # All arithmetic operations share CalculationCommand
        calc_cmd = CalculationCommand(calc)
        for op_name in self.OPERATION_COMMANDS:
            commands[op_name] = calc_cmd
        return commands

    def run(self) -> None:  # pragma: no cover
        """Start the REPL loop."""
        print(f"\n{Fore.CYAN}{'=' * 50}")
        print("  Welcome to the Advanced Calculator!")
        print(f"  Type 'help' for available commands.")
        print(f"{'=' * 50}{Style.RESET_ALL}\n")

        while True:
            try:
                user_input = input(f"{Fore.WHITE}calculator> {Style.RESET_ALL}").strip()
                if not user_input:
                    continue
                self._process_input(user_input)
            except KeyboardInterrupt:
                print(f"\n{Fore.CYAN}Goodbye!{Style.RESET_ALL}")
                break
            except EOFError:
                print(f"\n{Fore.CYAN}Goodbye!{Style.RESET_ALL}")
                break

    def _process_input(self, user_input: str) -> None:
        """Parse and execute user input.

        Args:
            user_input: The raw input string from the user.
        """
        parts = user_input.split()
        command_name = parts[0].lower()

        command = self._commands.get(command_name)
        if command is None:
            print(f"{Fore.RED}Unknown command: '{command_name}'. Type 'help' for available commands.{Style.RESET_ALL}")
            return

        try:
            command.execute(parts)
        except SystemExit:
            raise
        except CalculatorError as exc:
            print(f"{Fore.RED}Error: {exc}{Style.RESET_ALL}")
        except Exception as exc:
            logger.error("Unexpected error processing '%s': %s", user_input, exc)
            print(f"{Fore.RED}An unexpected error occurred: {exc}{Style.RESET_ALL}")


def main() -> None:  # pragma: no cover
    """Entry point for the calculator application."""
    config = CalculatorConfig()
    repl = REPL(config=config)
    repl.run()


if __name__ == "__main__":  # pragma: no cover
    main()
