"""Tests for the Memento pattern (CalculatorMemento and HistoryCaretaker)."""

import pytest
from app.calculation import Calculation
from app.calculator_memento import CalculatorMemento, HistoryCaretaker


class TestCalculatorMemento:
    def test_save_and_restore_state(self):
        history = [Calculation("add", 1, 2, 3)]
        memento = CalculatorMemento(history)
        restored = memento.get_state()
        assert len(restored) == 1
        assert restored[0].result == 3

    def test_state_is_deep_copy(self):
        history = [Calculation("add", 1, 2, 3)]
        memento = CalculatorMemento(history)
        restored = memento.get_state()
        restored.append(Calculation("multiply", 2, 3, 6))
        assert len(memento.get_state()) == 1

    def test_empty_state(self):
        memento = CalculatorMemento([])
        assert memento.get_state() == []


class TestHistoryCaretaker:
    def test_save_and_undo(self):
        caretaker = HistoryCaretaker()
        memento = CalculatorMemento([Calculation("add", 1, 2, 3)])
        caretaker.save(memento)
        assert caretaker.can_undo

        restored = caretaker.undo()
        state = restored.get_state()
        assert len(state) == 1

    def test_undo_empty_raises(self):
        caretaker = HistoryCaretaker()
        with pytest.raises(IndexError, match="Nothing to undo"):
            caretaker.undo()

    def test_redo_empty_raises(self):
        caretaker = HistoryCaretaker()
        with pytest.raises(IndexError, match="Nothing to redo"):
            caretaker.redo()

    def test_redo_after_push(self):
        caretaker = HistoryCaretaker()
        memento = CalculatorMemento([Calculation("add", 1, 2, 3)])
        caretaker.push_redo(memento)
        assert caretaker.can_redo
        restored = caretaker.redo()
        assert len(restored.get_state()) == 1

    def test_save_clears_redo(self):
        caretaker = HistoryCaretaker()
        caretaker.push_redo(CalculatorMemento([]))
        assert caretaker.can_redo
        caretaker.save(CalculatorMemento([]))
        assert not caretaker.can_redo

    def test_can_undo_false_initially(self):
        caretaker = HistoryCaretaker()
        assert not caretaker.can_undo

    def test_can_redo_false_initially(self):
        caretaker = HistoryCaretaker()
        assert not caretaker.can_redo
