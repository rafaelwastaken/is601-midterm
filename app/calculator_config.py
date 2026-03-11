"""Configuration management using python-dotenv for the calculator application."""

import os
from dotenv import load_dotenv
from app.exceptions import ConfigurationError


class CalculatorConfig:
    """Manages calculator configuration from environment variables and .env file."""

    def __init__(self, env_path: str = ".env"):
        """Initialize configuration by loading from .env file.

        Args:
            env_path: Path to the .env file. Defaults to '.env' in the project root.
        """
        load_dotenv(dotenv_path=env_path)
        self._load_config()

    def _load_config(self) -> None:
        """Load and validate configuration values from environment variables."""
        # Base directories
        self.log_dir = os.getenv("CALCULATOR_LOG_DIR", "logs")
        self.history_dir = os.getenv("CALCULATOR_HISTORY_DIR", "history")

        # Derived file paths
        self.log_file = os.path.join(self.log_dir, "calculator.log")
        self.history_file = os.path.join(self.history_dir, "history.csv")

        # History settings
        self.max_history_size = self._parse_int(
            "CALCULATOR_MAX_HISTORY_SIZE", default=100
        )
        self.auto_save = self._parse_bool("CALCULATOR_AUTO_SAVE", default=True)

        # Calculation settings
        self.precision = self._parse_int("CALCULATOR_PRECISION", default=10)
        self.max_input_value = self._parse_float(
            "CALCULATOR_MAX_INPUT_VALUE", default=1e10
        )
        self.default_encoding = os.getenv("CALCULATOR_DEFAULT_ENCODING", "utf-8")

        # Ensure directories exist
        os.makedirs(self.log_dir, exist_ok=True)
        os.makedirs(self.history_dir, exist_ok=True)

    @staticmethod
    def _parse_int(env_var: str, default: int) -> int:
        """Parse an integer from an environment variable.

        Args:
            env_var: The environment variable name.
            default: Default value if not set.

        Returns:
            Parsed integer.

        Raises:
            ConfigurationError: If the value is not a valid integer.
        """
        value = os.getenv(env_var)
        if value is None:
            return default
        try:
            return int(value)
        except ValueError as exc:
            raise ConfigurationError(
                f"Invalid integer for {env_var}: '{value}'"
            ) from exc

    @staticmethod
    def _parse_float(env_var: str, default: float) -> float:
        """Parse a float from an environment variable.

        Args:
            env_var: The environment variable name.
            default: Default value if not set.

        Returns:
            Parsed float.

        Raises:
            ConfigurationError: If the value is not a valid float.
        """
        value = os.getenv(env_var)
        if value is None:
            return default
        try:
            return float(value)
        except ValueError as exc:
            raise ConfigurationError(
                f"Invalid float for {env_var}: '{value}'"
            ) from exc

    @staticmethod
    def _parse_bool(env_var: str, default: bool) -> bool:
        """Parse a boolean from an environment variable.

        Args:
            env_var: The environment variable name.
            default: Default value if not set.

        Returns:
            Parsed boolean.

        Raises:
            ConfigurationError: If value is not a recognized boolean string.
        """
        value = os.getenv(env_var)
        if value is None:
            return default
        if value.lower() in ("true", "1", "yes"):
            return True
        if value.lower() in ("false", "0", "no"):
            return False
        raise ConfigurationError(
            f"Invalid boolean for {env_var}: '{value}'. Use true/false."
        )

    def __repr__(self) -> str:
        return (
            f"CalculatorConfig(log_dir='{self.log_dir}', history_dir='{self.history_dir}', "
            f"max_history={self.max_history_size}, auto_save={self.auto_save}, "
            f"precision={self.precision}, max_input={self.max_input_value})"
        )
