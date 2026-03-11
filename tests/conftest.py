"""Shared test fixtures for the calculator test suite."""

import os
import pytest
from app.calculator_config import CalculatorConfig
from app.logger import Logger


@pytest.fixture(autouse=True)
def _reset_logger():
    """Reset the logger before each test to avoid handler buildup."""
    Logger.reset()
    yield
    Logger.reset()


@pytest.fixture
def tmp_env(tmp_path, monkeypatch):
    """Create a temporary .env-like environment for testing."""
    log_dir = str(tmp_path / "logs")
    history_dir = str(tmp_path / "history")
    monkeypatch.setenv("CALCULATOR_LOG_DIR", log_dir)
    monkeypatch.setenv("CALCULATOR_HISTORY_DIR", history_dir)
    monkeypatch.setenv("CALCULATOR_MAX_HISTORY_SIZE", "50")
    monkeypatch.setenv("CALCULATOR_AUTO_SAVE", "false")
    monkeypatch.setenv("CALCULATOR_PRECISION", "8")
    monkeypatch.setenv("CALCULATOR_MAX_INPUT_VALUE", "1000000")
    monkeypatch.setenv("CALCULATOR_DEFAULT_ENCODING", "utf-8")
    return tmp_path


@pytest.fixture
def config(tmp_env):
    """Provide a CalculatorConfig loaded from temporary environment."""
    return CalculatorConfig(env_path="")
