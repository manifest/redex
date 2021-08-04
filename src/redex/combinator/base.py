"""The combinator base."""

from dataclasses import dataclass
from redex.function import FineCallable

# pylint: disable=too-few-public-methods
class Combinator(FineCallable):
    """The base class for combinators."""

    def __init_subclass__(cls) -> None:
        """Makes subclass a dataclass."""
        super().__init_subclass__()
        dataclass(cls)
