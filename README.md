# Log File Processor

A Python application that processes log files line by line, applying configurable transformation rules.

## Setup

This project uses [uv](https://github.com/astral-sh/uv) for dependency management.

```bash
# Install all dependencies (including dev dependencies)
uv sync
```

## Usage

Run the script with a log file path as argument:

```bash
uv run main.py data.log
```

Each line is processed according to the rules defined in `rules.py`, and the output is printed to stdout in the format: `LINE_NUMBER : RESULT`

## Testing

### Run all tests
```bash
uv run pytest
```

### Run pre-commit checks
A script is provided to run all quality checks (linting, formatting, type checking):

```bash
./check.sh
```

This runs:
- `ruff check` - linting
- `ruff format --check` - formatting validation
- `ty check` - type checking

## Architecture

### Core Components

#### main.py

- **FileReader**: Reads files line by line using a generator to avoid loading entire files into memory. Yields `Log` instances for each line.
- **Log**: Dataclass representing a log line with its ID (line number) and content. The `process()` method applies transformation rules in priority order.

#### rules.py

- **Rule** (ABC): Abstract base class defining the interface for processing rules. Uses the Template Method pattern:
  - `execute()` performs type validation, then delegates to `_apply()`
  - `_apply()` is implemented by concrete rule classes
  - Concrete implementations:
    - `MultipleOf5Rule`: Returns "Multiple of 5" for IDs divisible by 5
    - `DollarSignRule`: Replaces spaces with underscores when content contains `$`
    - `EndsWithDotRule`: Returns content as-is when it ends with `.`
    - `JsonRule`: Parses JSON, adds `even` key based on ID parity, re-serializes
