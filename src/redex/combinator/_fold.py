"""The folding combinator."""

import operator
from functools import reduce
from typing import Any, Callable
from redex.function import Signature
from redex.stack import stackmethod, verify_stack_size, Stack
from redex.combinator._base import Combinator

BinaryOperator = Callable[[Any, Any], Any]

# pylint: disable=too-few-public-methods
class Foldl(Combinator):
    """The left folding combinator."""

    func: BinaryOperator
    """a function of two arguments."""

    @stackmethod
    def __call__(self, stack: Stack) -> Stack:
        verify_stack_size(self, stack, self.signature)
        n_in = self.signature.n_in
        result = reduce(self.func, stack[:n_in])  # type: ignore
        return (result, *stack[n_in:])


def foldl(func: BinaryOperator, n_in: int = 2) -> Foldl:
    """Creates a left folding combinator."""
    return Foldl(func=func, signature=Signature(n_in=n_in, n_out=1))


def add(n_in: int = 2) -> Foldl:
    """Creates an addition combinator.

    >>> from redex import combinator as cb
    >>> add = cb.add()
    >>> add(4, 2) == 6
    True

    Args:
        n_in: a number of inputs.

    Returns:
        a combinator.
    """
    return foldl(func=operator.add, n_in=n_in)


def sub(n_in: int = 2) -> Foldl:
    """Creates an subtraction combinator.

    >>> from redex import combinator as cb
    >>> sub = cb.sub()
    >>> sub(4, 2) == 2
    True

    Args:
        n_in: a number of inputs.

    Returns:
        a combinator.
    """
    return foldl(func=operator.sub, n_in=n_in)


def mul(n_in: int = 2) -> Foldl:
    """Creates a multiplication combinator.

    >>> from redex import combinator as cb
    >>> mul = cb.mul()
    >>> mul(4, 2) == 8
    True

    Args:
        n_in: a number of inputs.

    Returns:
        a combinator.
    """
    return foldl(func=operator.mul, n_in=n_in)


def div(n_in: int = 2) -> Foldl:
    """Creates a division combinator.

    >>> from redex import combinator as cb
    >>> div = cb.div()
    >>> div(4, 2) == 2
    True

    Args:
        n_in: a number of inputs.

    Returns:
        a combinator.
    """
    return foldl(func=operator.truediv, n_in=n_in)


fold = foldl
