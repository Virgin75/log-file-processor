"""Rule functions for processing log lines."""

import json
import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)
logger.addHandler(logging.FileHandler("json_rule.log"))


class Rule(ABC):
    """Abstract base class defining the interface for a log processing rule."""

    def execute(self, id: int, content: str) -> str | None:
        """Execute the rule with type validation.

        Args:
            id: The line number.
            content: The line content.

        Returns:
            The processed result if the rule applies, None otherwise.

        Raises:
            TypeError: If id is not int or content is not str.
        """
        if not isinstance(id, int):
            raise TypeError(f"id must be int, got {type(id).__name__}")
        if not isinstance(content, str):
            raise TypeError(f"content must be str, got {type(content).__name__}")

        return self._apply(id, content)

    @abstractmethod
    def _apply(self, id: int, content: str) -> str | None:
        """Apply the rule to the given log line.

        Args:
            id: The line number.
            content: The line content.

        Returns:
            The processed result if the rule applies, None otherwise.
        """
        ...


class MultipleOf5Rule(Rule):
    """Rule that returns 'Multiple of 5' when id is a multiple of 5."""

    def _apply(self, id: int, content: str) -> str | None:
        """Return 'Multiple of 5' if id is a multiple of 5."""
        if id % 5 == 0:
            return "Multiple of 5"
        return None


class DollarSignRule(Rule):
    """Rule that replaces spaces with underscores when content contains '$'."""

    def _apply(self, id: int, content: str) -> str | None:
        """Return content with spaces replaced by underscores if it contains '$'."""
        if "$" in content:
            return content.replace(" ", "_")
        return None


class EndsWithDotRule(Rule):
    """Rule that returns content as-is when it ends with '.'."""

    def _apply(self, id: int, content: str) -> str | None:
        """Return content as-is if it ends with '.'."""
        if content.endswith("."):
            return content
        return None


class JsonRule(Rule):
    """Rule that parses JSON, adds 'even' key, and re-serializes."""

    def _apply(self, id: int, content: str) -> str | None:
        """Parse JSON, add 'even' key, and re-serialize if content starts with '{'."""
        if content.startswith("{"):
            try:
                data = json.loads(content)
                data["even"] = id % 2 == 0
                return json.dumps(data, ensure_ascii=False)
            except json.JSONDecodeError:
                logger.warning(f"invalid json for line {id}, rule cannot be applied.")
                return None
        return None
