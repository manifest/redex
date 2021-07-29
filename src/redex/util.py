"""General utility functions."""

from typing import Any, Iterable, List
from functools import reduce


def expand_to_tuple(items: Any) -> tuple[Any, ...]:
    """Wraps anything but tuple into a tuple.

    Args:
      items: any sequence or a single item.

    Returns:
      a tuple.
    """
    return items if isinstance(items, tuple) else (items,)


def squeeze_tuple(items: Any) -> Any:
    """Reduces a tuple to a single item if only it consists of
    a single item.

    Args:
      items: any sequence or a single item.

    Returns:
      a single item if possible, or an input sequence if not.
    """
    return items[0] if isinstance(items, tuple) and len(items) == 1 else items


def deep_flatten(items: Iterable[Any]) -> List[Any]:
    """Recursively flatten a sequence.

    Args:
      items: a sequece of items.

    Returns:
      an ierator over flat sequence.
    """

    def consume(acc: List[Any], item: Any) -> List[Any]:
        if isinstance(item, Iterable) and not isinstance(item, (bytes, str)):
            return acc + reduce(consume, item, [])
        return acc + [item]

    if not isinstance(items, Iterable):
        return items

    return reduce(consume, items, [])
