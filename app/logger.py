"""Logger module for the calculator application."""

import os
import logging


class Logger:
    """Configures and provides a logger for the calculator application."""

    _initialized = False

    @classmethod
    def setup(cls, log_file: str = "logs/calculator.log",
              level: int = logging.INFO) -> None:
        """Set up the root logger with file and console handlers.

        Args:
            log_file: Path to the log file.
            level: Logging level (default: INFO).
        """
        if cls._initialized:
            return

        log_dir = os.path.dirname(log_file)
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)

        root_logger = logging.getLogger()
        root_logger.setLevel(level)

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        # File handler
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)

        cls._initialized = True

    @classmethod
    def get_logger(cls, name: str) -> logging.Logger:
        """Get a named logger.

        Args:
            name: The name for the logger (typically __name__).

        Returns:
            A configured Logger instance.
        """
        return logging.getLogger(name)

    @classmethod
    def reset(cls) -> None:
        """Reset the logger (useful for testing)."""
        root_logger = logging.getLogger()
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)
            handler.close()
        cls._initialized = False
