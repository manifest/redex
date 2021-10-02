"""The addition combinator."""

import operator
from functools import reduce
from redex.function import Signature
from redex.stack import stackmethod, verify_stack_size, Stack
from redex.combinator._base import Combinator

# pylint: disable=too-few-public-methods
class Add(Combinator):
    """The addition combinator."""

    @stackmethod
    def __call__(self, stack: Stack) -> Stack:
        verify_stack_size(self, stack, self.signature)
        n_in = self.signature.n_in
        result = reduce(operator.add, stack[:n_in])
        return (result, *stack[n_in:])


def add(n_in: int = 2) -> Add:
    """Creates an addition combinator.

    >>> from redex import combinator as cb
    >>> add = cb.add()
    >>> add(1, 2) == 3
    True

    Args:
        n_in: a number of inputs.

    Returns:
        a combinator.
    """
    return Add(signature=Signature(n_in=n_in, n_out=1))
