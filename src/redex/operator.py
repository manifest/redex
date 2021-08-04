"""A collection of operators."""

from typing import Any
import operator


def identity(value: Any) -> Any:
    """Always returns the same value that was used as its argument."""
    return value


add = operator.add
sub = operator.sub
