"""The combinator base."""

import typing
from typing import Any
from dataclasses import dataclass
from redex.function import FineCallable

# pylint: disable=too-few-public-methods
class Combinator(FineCallable):
    """The base class for combinators."""

    if typing.TYPE_CHECKING:

        def __init__(self, *args: Any, **kwargs: Any) -> None:
            # this stub makes sure pytype accepts constructor arguments.
            pass

    def __init_subclass__(cls) -> None:
        """Makes subclass a dataclass."""
        super().__init_subclass__()
        dataclass(cls)
