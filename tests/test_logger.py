"""Tests for the Logger module."""

import logging
import os
import pytest
from app.logger import Logger


class TestLogger:
    def test_setup_creates_log_file(self, tmp_path):
        log_file = str(tmp_path / "test.log")
        Logger.setup(log_file=log_file)
        test_logger = Logger.get_logger("test")
        test_logger.info("Test message")
        assert os.path.exists(log_file)

    def test_get_logger_returns_logger(self):
        lgr = Logger.get_logger("mymodule")
        assert isinstance(lgr, logging.Logger)
        assert lgr.name == "mymodule"

    def test_setup_only_once(self, tmp_path):
        log_file = str(tmp_path / "test2.log")
        Logger.setup(log_file=log_file)
        Logger.setup(log_file=log_file)
        root = logging.getLogger()
        # Should only have handlers from one setup
        handler_count = len(root.handlers)
        Logger.setup(log_file=log_file)
        assert len(root.handlers) == handler_count

    def test_reset(self, tmp_path):
        log_file = str(tmp_path / "test3.log")
        Logger.setup(log_file=log_file)
        Logger.reset()
        root = logging.getLogger()
        assert len(root.handlers) == 0
        assert Logger._initialized is False
