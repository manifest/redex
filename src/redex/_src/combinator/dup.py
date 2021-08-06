"""The duplicate combinator."""

from redex._src.stack import stackmethod, verify_stack_size, Stack
from redex._src.function import Signature
from redex._src.combinator.base import Combinator

# pylint: disable=too-few-public-methods
class Dup(Combinator):
    """The duplicate combinator."""

    @stackmethod
    def __call__(self, stack: Stack) -> Stack:
        verify_stack_size(self, stack, self.signature)
        n_in = self.signature.n_in
        head, tail = stack[:n_in], stack[n_in:]
        return (*head, *head, *tail)


def dup(n_in: int = 1) -> Dup:
    """Creates a duplicate combinator.

    The combinator makes a copy of the top items on the stack.

    >>> from redex import combinator as cb
    >>> dup = cb.dup()
    >>> dup(1) == (1, 1)
    True

    Args:
        n_in: a number of inputs.

    Returns:
        a combinator.
    """
    return Dup(signature=Signature(n_in=n_in, n_out=n_in * 2))
