"""The identity operator."""

from typing import Any


def identity(value: Any) -> Any:
    """Always returns the same value that was used as its argument.

    >>> from redex import combinator as cb
    >>> 1 == cb.identity(1)
    True

    Args:
        value: an input.

    Returns:
        the same input.
    """
    return value
