"""General utility functions."""

from functools import reduce
from typing import Any, Callable, Iterable, List
from types import GenericAlias

PredicateFn = Callable[[Any], bool]
TraverseFn = Callable[[Any], Iterable[Any]]


def _identity(item: Iterable[Any]) -> Iterable[Any]:
    """Always returns the same value that was used as its argument."""
    return item


def _generic_arguments(annotation: GenericAlias) -> tuple[Any, ...]:
    """Returns arguments of the parameterized tuple.

    Args:
        annotation: a parameterized tuple annotation.

    Returns:
        tuple arguments.
    """
    return annotation.__args__


def _is_iterable_butnot_stringlike(item: Any) -> bool:
    """Verifies if item instance is an iterator,
    but not of a string or bytes type.

    Args:
        item: an item to verify.

    Returns:
        `True` if verified, `False` otherwise.
    """
    return isinstance(item, Iterable) and not isinstance(item, (bytes, str))


def _is_tuple(item: Any) -> bool:
    """Verifies if item instance is a tuple.

    Args:
        item: an item to verify.

    Returns:
        `True` if verified, `False` otherwise.
    """
    return isinstance(item, tuple)


def _is_parameterized_tuple_anotation(annotation: Any) -> bool:
    """Verifies if type annotation is a parameterized tuple.

    Args:
        item: a type annotation.

    Returns:
        `True` if verified, `False` otherwise.

    Raises:
        ValueError: if the annotation include variadic tuples.
            Variadic tuples nested in other then tuple annotations
            (e.g. `Sequence(tuple[Any, ...])`) are fine.
    """
    if annotation in (tuple, Ellipsis):
        raise ValueError(
            "Connot flatten a variadic tuple annotation such as "
            "`tuple[Any,...]` or `tuple`."
        )
    return isinstance(annotation, GenericAlias) and annotation.__origin__ is tuple


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


def flatten(
    item: Any,
    predicate: PredicateFn = _is_iterable_butnot_stringlike,
    traverse: TraverseFn = _identity,
) -> List[Any]:
    """Recursively flatten a sequence.

    Args:
        item: a sequence or a single item. A single item will be packet into a list.
        predicate: for each item of the sequence, the function determines
            whether the item should be flattened. By default, any sequence but a string or bytes
            will be flattened.
        traverse: determines how to get nested items. Defaults to identity function.

    Returns:
        a list with items determined by `predicate` got flattened.
    """

    def inner(acc: List[Any], item: Any) -> List[Any]:
        if predicate(item):
            return acc + reduce(inner, traverse(item), [])
        return acc + [item]

    if predicate(item):
        return reduce(inner, traverse(item), [])

    return [item]


def flatten_tuples(item: Any) -> List[Any]:
    """Recursively flatten tuples in a sequence.

    Args:
        item: a sequence or a single item. A single item will be packet into a list.

    Returns:
        a list with tuples got flattened.
    """
    return flatten(item, predicate=_is_tuple)


def flatten_tuple_annotations(annotation: Any) -> List[Any]:
    """Recursively flatten tuples in the type annotation.

    Args:
        annotation: a type annotation.

    Returns:
        a list with tuple annotations got flattened.

    Raises:
        ValueError: if the annotation include variadic tuples.
            Variadic tuples nested in other then tuple annotations
            (e.g. `Sequence(tuple[Any, ...])`) are fine.
    """
    return flatten(
        annotation,
        predicate=_is_parameterized_tuple_anotation,
        traverse=_generic_arguments,
    )
