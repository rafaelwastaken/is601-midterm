# Advanced Calculator Application

## Project Description

An advanced command-line calculator application built in Python featuring multiple arithmetic operations, a REPL (Read-Eval-Print Loop) interface, comprehensive error handling, and persistent history management. The application demonstrates several software design patterns and best practices:

- **Factory Design Pattern** – Manages creation of different arithmetic operation instances.
- **Memento Design Pattern** – Provides undo/redo functionality for calculations.
- **Observer Design Pattern** – Enables automatic logging and auto-save of calculation history.
- **Command Design Pattern** – Encapsulates REPL commands as objects for clean separation of concerns.
- **Decorator Design Pattern** – Dynamically generates the help menu from registered commands.

### Features

- **10 Arithmetic Operations**: add, subtract, multiply, divide, power, root, modulus, integer division, percentage, absolute difference
- **History Management**: View, clear, save, and load calculation history using pandas/CSV
- **Undo/Redo**: Revert or redo calculations using the Memento pattern
- **Auto-Save**: Automatically saves history after each calculation (configurable)
- **Logging**: Comprehensive logging of all operations with configurable log levels
- **Color-Coded Output**: Enhanced CLI readability using colorama
- **Configuration via .env**: All settings managed through environment variables
- **90%+ Test Coverage**: Comprehensive unit tests with pytest

---

## Installation Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <project-directory>
```

### 2. Create and Activate Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configuration Setup

The application uses a `.env` file for configuration. A default `.env` file is included in the project:

```env
# Base Directories
CALCULATOR_LOG_DIR=logs
CALCULATOR_HISTORY_DIR=history

# History Settings
CALCULATOR_MAX_HISTORY_SIZE=100
CALCULATOR_AUTO_SAVE=true

# Calculation Settings
CALCULATOR_PRECISION=10
CALCULATOR_MAX_INPUT_VALUE=10000000000
CALCULATOR_DEFAULT_ENCODING=utf-8
```

### Configuration Parameters

| Variable | Description | Default |
|---|---|---|
| `CALCULATOR_LOG_DIR` | Directory for log files | `logs` |
| `CALCULATOR_HISTORY_DIR` | Directory for history CSV files | `history` |
| `CALCULATOR_MAX_HISTORY_SIZE` | Maximum number of history entries | `100` |
| `CALCULATOR_AUTO_SAVE` | Auto-save history after each calculation (`true`/`false`) | `true` |
| `CALCULATOR_PRECISION` | Decimal places for calculation results | `10` |
| `CALCULATOR_MAX_INPUT_VALUE` | Maximum allowed input value | `10000000000` |
| `CALCULATOR_DEFAULT_ENCODING` | File encoding for CSV operations | `utf-8` |

### Logging Configuration

Logs are written to `<CALCULATOR_LOG_DIR>/calculator.log`. The log file records:
- All calculations performed (INFO level)
- Validation and operation errors (ERROR level)
- History save/load events (INFO level)
- Observer notifications (INFO level)

---

## Usage Guide

### Starting the Application

```bash
python main.py
```

### Supported Commands

#### Arithmetic Operations

All operations take two numeric arguments: `<operation> <number1> <number2>`

| Command | Description | Example |
|---|---|---|
| `add` | Addition (a + b) | `add 5 3` → `8` |
| `subtract` | Subtraction (a - b) | `subtract 10 4` → `6` |
| `multiply` | Multiplication (a × b) | `multiply 3 4` → `12` |
| `divide` | Division (a / b) | `divide 10 2` → `5` |
| `power` | Power (a ^ b) | `power 2 3` → `8` |
| `root` | Nth root (b√a) | `root 27 3` → `3` |
| `modulus` | Remainder (a % b) | `modulus 10 3` → `1` |
| `int_divide` | Integer division (a // b) | `int_divide 7 2` → `3` |
| `percent` | Percentage ((a/b)×100) | `percent 50 200` → `25` |
| `abs_diff` | Absolute difference \|a - b\| | `abs_diff 3 10` → `7` |

#### Management Commands

| Command | Description |
|---|---|
| `history` | Display all calculations in history |
| `clear` | Clear the calculation history |
| `undo` | Undo the last calculation |
| `redo` | Redo the last undone calculation |
| `save` | Manually save history to CSV file |
| `load` | Load history from CSV file |
| `help` | Display available commands and usage |
| `exit` | Exit the application |

### Example Session

```
calculator> add 10 20
Result: 30.0
calculator> multiply 5 6
Result: 30.0
calculator> history
--- Calculation History ---
  1. add(10.0, 20.0) = 30.0
  2. multiply(5.0, 6.0) = 30.0
--------------------------
calculator> undo
Undo successful.
calculator> history
--- Calculation History ---
  1. add(10.0, 20.0) = 30.0
--------------------------
calculator> redo
Redo successful.
calculator> save
History saved successfully.
calculator> exit
Thank you for using the Advanced Calculator. Goodbye!
```

---

## Testing Instructions

### Running Tests

```bash
pytest
```

### Running Tests with Coverage Report

```bash
pytest --cov=app --cov-report=term-missing
```

### Enforcing 90% Coverage Threshold

```bash
pytest --cov=app --cov-fail-under=90
```

### Test Structure

| Test File | Covers |
|---|---|
| `tests/test_operations.py` | All arithmetic operations and Factory pattern |
| `tests/test_calculation.py` | Calculation model (creation, serialization) |
| `tests/test_calculator.py` | Main Calculator class (compute, undo/redo, save/load) |
| `tests/test_history.py` | HistoryManager (add, clear, CSV save/load) |
| `tests/test_memento.py` | Memento and Caretaker (undo/redo stacks) |
| `tests/test_observers.py` | Observer pattern (logging, auto-save) |
| `tests/test_config.py` | Configuration loading and validation |
| `tests/test_logger.py` | Logger setup and management |
| `tests/test_input_validators.py` | Input validation and range checking |
| `tests/test_repl.py` | REPL command processing and output |
| `tests/test_exceptions.py` | Custom exception hierarchy |

---

## CI/CD Information

### GitHub Actions Workflow

The project includes a GitHub Actions workflow (`.github/workflows/python-app.yml`) that:

1. **Triggers** on every push or pull request to the `main` branch
2. **Sets up** a Python environment on Ubuntu
3. **Installs** all dependencies from `requirements.txt`
4. **Runs** the full test suite with pytest
5. **Enforces** a minimum 90% code coverage threshold

If coverage falls below 90%, the CI pipeline will fail, preventing the merge.

---

## Design Patterns Used

### Factory Pattern (`app/operations.py`)
The `OperationFactory` class manages the creation of arithmetic operation instances. New operations can be registered with `register_operation()`, and the factory creates them by name with `create_operation()`.

### Memento Pattern (`app/calculator_memento.py`)
`CalculatorMemento` captures snapshots of the history state. `HistoryCaretaker` manages undo/redo stacks, allowing users to revert or replay calculations.

### Observer Pattern (`app/observers.py`)
`LoggingObserver` logs each calculation to the log file. `AutoSaveObserver` saves history to CSV after each calculation. The `ObserverManager` notifies all registered observers when a new calculation is performed.

### Command Pattern (`main.py`)
Each REPL action (help, undo, save, etc.) is encapsulated as a `Command` object with an `execute()` method, enabling clean separation and extensibility.

### Decorator Pattern (`main.py`)
The `@register_command` decorator dynamically registers commands, enabling the help menu to be automatically generated from all registered commands without manual updates.

---

## Project Structure

```
project_root/
├── app/
│   ├── __init__.py
│   ├── calculator.py          # Main Calculator class
│   ├── calculation.py         # Calculation data model
│   ├── calculator_config.py   # Configuration management
│   ├── calculator_memento.py  # Memento pattern for undo/redo
│   ├── exceptions.py          # Custom exception classes
│   ├── history.py             # History management with pandas
│   ├── input_validators.py    # Input validation utilities
│   ├── operations.py          # Arithmetic operations + Factory
│   ├── observers.py           # Observer pattern implementation
│   └── logger.py              # Logging configuration
├── tests/
│   ├── __init__.py
│   ├── conftest.py            # Shared test fixtures
│   ├── test_calculator.py
│   ├── test_calculation.py
│   ├── test_operations.py
│   ├── test_history.py
│   ├── test_memento.py
│   ├── test_observers.py
│   ├── test_config.py
│   ├── test_logger.py
│   ├── test_input_validators.py
│   ├── test_repl.py
│   └── test_exceptions.py
├── main.py                    # REPL entry point
├── .env                       # Configuration file
├── .gitignore
├── requirements.txt
├── README.md
└── .github/
    └── workflows/
        └── python-app.yml     # CI/CD pipeline
```
