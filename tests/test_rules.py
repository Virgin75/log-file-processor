"""Tests for rule classes."""

import json

import pytest

from rules import DollarSignRule, EndsWithDotRule, JsonRule, MultipleOf5Rule


class TestMultipleOf5Rule:
    def test_applies_for_zero(self):
        assert MultipleOf5Rule().execute(0, "some content") == "Multiple of 5"

    def test_applies_for_five(self):
        assert MultipleOf5Rule().execute(5, "another content") == "Multiple of 5"

    def test_does_not_apply_for_one(self):
        assert MultipleOf5Rule().execute(1, "some content") is None


class TestDollarSignRule:
    def test_applies_when_contains_dollar(self):
        result = DollarSignRule().execute(1, "Process 9000 suc$esfully run")
        assert result == "Process_9000_suc$esfully_run"

    def test_does_not_apply_when_no_dollar(self):
        assert DollarSignRule().execute(1, "no dollar here") is None


class TestEndsWithDotRule:
    def test_applies_when_ends_with_dot(self):
        result = EndsWithDotRule().execute(1, "Process 498758 succesfully run.")
        assert result == "Process 498758 succesfully run."

    def test_does_not_apply_when_no_dot(self):
        assert EndsWithDotRule().execute(1, "no dot at end") is None


class TestJsonRule:
    def test_applies_for_even_id(self):
        result = JsonRule().execute(2, '{"key": "value"}')
        assert result is not None
        data = json.loads(result)
        assert data["key"] == "value"
        assert data["even"] is True

    def test_applies_for_odd_id(self):
        result = JsonRule().execute(1, '{"key": "value"}')
        assert result is not None
        data = json.loads(result)
        assert data["key"] == "value"
        assert data["even"] is False

    def test_does_not_apply_for_non_json(self):
        assert JsonRule().execute(1, "not json") is None


class TestRuleTypeValidation:
    def test_raises_type_error_for_invalid_id(self):
        with pytest.raises(TypeError, match="id must be int"):
            MultipleOf5Rule().execute("not an int", "content")  # ty: ignore

    def test_raises_type_error_for_invalid_content(self):
        with pytest.raises(TypeError, match="content must be str"):
            MultipleOf5Rule().execute(1, 123)  # ty: ignore
