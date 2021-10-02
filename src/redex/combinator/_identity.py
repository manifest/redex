"""The identity operator."""

from redex.stack import stackmethod, verify_stack_size, Stack
from redex.function import Signature
from redex.combinator._base import Combinator


# pylint: disable=too-few-public-methods
class Identity(Combinator):
    """The identity combinator."""

    @stackmethod
    def __call__(self, stack: Stack) -> Stack:
        verify_stack_size(self, stack, self.signature)
        return stack


def identity(n_in: int = 1) -> Identity:
    """Always returns the same values that were used as arguments.

    >>> from redex import combinator as cb
    >>> identity = cb.identity()
    >>> identity(1) == 1
    True

    Args:
        n_in: a number of inputs.

    Returns:
        a combinator.
    """
    return Identity(signature=Signature(n_in=n_in, n_out=n_in))
