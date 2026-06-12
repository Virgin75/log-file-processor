"""Main module for processing log files."""

import sys
from collections.abc import Generator
from dataclasses import dataclass
from pathlib import Path

from rules import DollarSignRule, EndsWithDotRule, JsonRule, MultipleOf5Rule, Rule


@dataclass
class Log:
    """Represents a log line with its content (extracted from the log file)."""

    id: int
    content: str

    def process(self) -> str:
        """Process the log line according to the rules.

        Returns:
            The processed line content based on the rules.
        """
        rules_to_check: list[Rule] = [
            MultipleOf5Rule(),
            DollarSignRule(),
            EndsWithDotRule(),
            JsonRule(),
        ]
        for rule in rules_to_check:
            if (rule_output := rule.execute(self.id, self.content)) is not None:
                return rule_output
        return "Nothing to display"


class FileReader:
    """Reads a file line by line and yields Log instances."""

    def __init__(self, file_path: str) -> None:
        """Initialize FileReader with the path to the file.

        Args:
            file_path: Path to the file to read.

        Raises:
            FileNotFoundError: If the file does not exist.
        """
        self.file_path: str = file_path
        if not Path(self.file_path).is_file():
            raise FileNotFoundError(f"File not found: {self.file_path}")

    def read_lines(self) -> Generator[Log]:
        """Read the file line by line.

        Yields:
            Log instances with line number and line content.
        """
        with open(self.file_path, "r") as file:
            for line_number, line in enumerate(file):
                yield Log(id=line_number, content=line.rstrip("\r\n"))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <file_path>", file=sys.stderr)
        sys.exit(1)
    reader = FileReader(sys.argv[1])
    for log in reader.read_lines():
        print(f"{log.id} : {log.process()}")
