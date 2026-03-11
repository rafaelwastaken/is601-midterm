"""Tests for CalculatorConfig."""

import pytest
from app.calculator_config import CalculatorConfig
from app.exceptions import ConfigurationError


class TestCalculatorConfig:
    def test_default_config(self, tmp_env):
        config = CalculatorConfig(env_path="")
        assert config.max_history_size == 50
        assert config.auto_save is False
        assert config.precision == 8
        assert config.max_input_value == 1000000
        assert config.default_encoding == "utf-8"

    def test_log_dir_created(self, config):
        import os
        assert os.path.isdir(config.log_dir)

    def test_history_dir_created(self, config):
        import os
        assert os.path.isdir(config.history_dir)

    def test_repr(self, config):
        r = repr(config)
        assert "CalculatorConfig" in r

    def test_invalid_int_env(self, monkeypatch, tmp_path):
        monkeypatch.setenv("CALCULATOR_LOG_DIR", str(tmp_path / "logs"))
        monkeypatch.setenv("CALCULATOR_HISTORY_DIR", str(tmp_path / "history"))
        monkeypatch.setenv("CALCULATOR_MAX_HISTORY_SIZE", "not_an_int")
        with pytest.raises(ConfigurationError, match="Invalid integer"):
            CalculatorConfig(env_path="")

    def test_invalid_float_env(self, monkeypatch, tmp_path):
        monkeypatch.setenv("CALCULATOR_LOG_DIR", str(tmp_path / "logs"))
        monkeypatch.setenv("CALCULATOR_HISTORY_DIR", str(tmp_path / "history"))
        monkeypatch.setenv("CALCULATOR_MAX_INPUT_VALUE", "not_a_float")
        with pytest.raises(ConfigurationError, match="Invalid float"):
            CalculatorConfig(env_path="")

    def test_invalid_bool_env(self, monkeypatch, tmp_path):
        monkeypatch.setenv("CALCULATOR_LOG_DIR", str(tmp_path / "logs"))
        monkeypatch.setenv("CALCULATOR_HISTORY_DIR", str(tmp_path / "history"))
        monkeypatch.setenv("CALCULATOR_AUTO_SAVE", "maybe")
        with pytest.raises(ConfigurationError, match="Invalid boolean"):
            CalculatorConfig(env_path="")

    def test_bool_true_values(self, monkeypatch, tmp_path):
        monkeypatch.setenv("CALCULATOR_LOG_DIR", str(tmp_path / "logs"))
        monkeypatch.setenv("CALCULATOR_HISTORY_DIR", str(tmp_path / "history"))
        for val in ("true", "1", "yes"):
            monkeypatch.setenv("CALCULATOR_AUTO_SAVE", val)
            config = CalculatorConfig(env_path="")
            assert config.auto_save is True

    def test_bool_false_values(self, monkeypatch, tmp_path):
        monkeypatch.setenv("CALCULATOR_LOG_DIR", str(tmp_path / "logs"))
        monkeypatch.setenv("CALCULATOR_HISTORY_DIR", str(tmp_path / "history"))
        for val in ("false", "0", "no"):
            monkeypatch.setenv("CALCULATOR_AUTO_SAVE", val)
            config = CalculatorConfig(env_path="")
            assert config.auto_save is False
