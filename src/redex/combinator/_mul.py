"""The multiplication combinator."""

import operator
from functools import reduce
from redex.function import Signature
from redex.stack import stackmethod, verify_stack_size, Stack
from redex.combinator._base import Combinator

# pylint: disable=too-few-public-methods
class Mul(Combinator):
    """The multiplication combinator."""

    @stackmethod
    def __call__(self, stack: Stack) -> Stack:
        verify_stack_size(self, stack, self.signature)
        n_in = self.signature.n_in
        result = reduce(operator.mul, stack[:n_in])
        return (result, *stack[n_in:])


def mul(n_in: int = 2) -> Mul:
    """Creates a multiplication combinator.

    >>> from redex import combinator as cb
    >>> mul = cb.mul()
    >>> add(2, 3) == 6
    True

    Args:
        n_in: a number of inputs.

    Returns:
        a combinator.
    """
    return Mul(signature=Signature(n_in=n_in, n_out=1))
