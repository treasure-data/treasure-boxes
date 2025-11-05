"""
Shared utilities for unification models.
"""

import re

# SQL Symbol validation pattern
SQL_SYMBOL_PATTERN = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_]*$')


def validate_sql_symbol(value: str) -> str:
    """Validate that a string is a valid SQL symbol."""
    if not SQL_SYMBOL_PATTERN.match(value):
        raise ValueError(f"'{value}' is not a valid SQL symbol. Must start with letter or underscore and contain only letters, numbers, and underscores.")
    return value