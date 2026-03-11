"""Tests for the REPL and Command classes."""

import pytest
from unittest.mock import patch
from app.calculator_config import CalculatorConfig
from main import (
    REPL, CalculationCommand, HistoryCommand, ClearCommand,
    UndoCommand, RedoCommand, SaveCommand, LoadCommand,
    HelpCommand, ExitCommand, get_registered_commands,
)
from app.calculator import Calculator


@pytest.fixture
def repl(config):
    """Provide a REPL instance with test config."""
    return REPL(config=config)


class TestREPLProcessInput:
    def test_unknown_command(self, repl, capsys):
        repl._process_input("foobar")
        captured = capsys.readouterr()
        assert "Unknown command" in captured.out

    def test_add_command(self, repl, capsys):
        repl._process_input("add 2 3")
        captured = capsys.readouterr()
        assert "5" in captured.out

    def test_subtract_command(self, repl, capsys):
        repl._process_input("subtract 10 4")
        captured = capsys.readouterr()
        assert "6" in captured.out

    def test_multiply_command(self, repl, capsys):
        repl._process_input("multiply 3 4")
        captured = capsys.readouterr()
        assert "12" in captured.out

    def test_divide_command(self, repl, capsys):
        repl._process_input("divide 10 2")
        captured = capsys.readouterr()
        assert "5" in captured.out

    def test_power_command(self, repl, capsys):
        repl._process_input("power 2 3")
        captured = capsys.readouterr()
        assert "8" in captured.out

    def test_root_command(self, repl, capsys):
        repl._process_input("root 27 3")
        captured = capsys.readouterr()
        assert "3" in captured.out

    def test_modulus_command(self, repl, capsys):
        repl._process_input("modulus 10 3")
        captured = capsys.readouterr()
        assert "1" in captured.out

    def test_int_divide_command(self, repl, capsys):
        repl._process_input("int_divide 7 2")
        captured = capsys.readouterr()
        assert "3" in captured.out

    def test_percent_command(self, repl, capsys):
        repl._process_input("percent 50 200")
        captured = capsys.readouterr()
        assert "25" in captured.out

    def test_abs_diff_command(self, repl, capsys):
        repl._process_input("abs_diff 3 10")
        captured = capsys.readouterr()
        assert "7" in captured.out

    def test_division_by_zero(self, repl, capsys):
        repl._process_input("divide 10 0")
        captured = capsys.readouterr()
        assert "Error" in captured.out

    def test_invalid_number_input(self, repl, capsys):
        repl._process_input("add abc 3")
        captured = capsys.readouterr()
        assert "Error" in captured.out

    def test_missing_arguments(self, repl, capsys):
        repl._process_input("add 5")
        captured = capsys.readouterr()
        assert "Usage" in captured.out

    def test_history_empty(self, repl, capsys):
        repl._process_input("history")
        captured = capsys.readouterr()
        assert "No calculations" in captured.out

    def test_history_with_entries(self, repl, capsys):
        repl._process_input("add 1 2")
        repl._process_input("history")
        captured = capsys.readouterr()
        assert "History" in captured.out

    def test_clear_command(self, repl, capsys):
        repl._process_input("add 1 2")
        repl._process_input("clear")
        captured = capsys.readouterr()
        assert "cleared" in captured.out

    def test_undo_command(self, repl, capsys):
        repl._process_input("add 1 2")
        repl._process_input("undo")
        captured = capsys.readouterr()
        assert "Undo successful" in captured.out

    def test_undo_empty(self, repl, capsys):
        repl._process_input("undo")
        captured = capsys.readouterr()
        assert "Error" in captured.out

    def test_redo_command(self, repl, capsys):
        repl._process_input("add 1 2")
        repl._process_input("undo")
        repl._process_input("redo")
        captured = capsys.readouterr()
        assert "Redo successful" in captured.out

    def test_redo_empty(self, repl, capsys):
        repl._process_input("redo")
        captured = capsys.readouterr()
        assert "Error" in captured.out

    def test_save_command(self, repl, capsys):
        repl._process_input("add 1 2")
        repl._process_input("save")
        captured = capsys.readouterr()
        assert "saved" in captured.out

    def test_load_command_no_file(self, repl, capsys):
        repl._process_input("load")
        captured = capsys.readouterr()
        assert "Error" in captured.out

    def test_load_command_after_save(self, repl, capsys):
        repl._process_input("add 5 5")
        repl._process_input("save")
        repl._process_input("clear")
        repl._process_input("load")
        captured = capsys.readouterr()
        assert "loaded" in captured.out

    def test_help_command(self, repl, capsys):
        repl._process_input("help")
        captured = capsys.readouterr()
        assert "Available Commands" in captured.out
        assert "add" in captured.out

    def test_exit_command(self, repl):
        with pytest.raises(SystemExit):
            repl._process_input("exit")


class TestRegisteredCommands:
    def test_all_commands_registered(self):
        cmds = get_registered_commands()
        assert "history" in cmds
        assert "clear" in cmds
        assert "undo" in cmds
        assert "redo" in cmds
        assert "save" in cmds
        assert "load" in cmds
        assert "help" in cmds
        assert "exit" in cmds
        assert "calculation" in cmds

    def test_commands_have_help_text(self):
        cmds = get_registered_commands()
        for name, info in cmds.items():
            assert len(info["help"]) > 0
