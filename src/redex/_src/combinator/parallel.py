"""The parallel combinator."""

from typing import List
from functools import reduce
from dataclasses import replace
from redex._src import function as fn
from redex._src.function import Fn, Signature
from redex._src.stack import constrained_call, stackmethod, Stack
from redex._src.combinator.base import Combinator


# pylint: disable=too-few-public-methods
class Parallel(Combinator):
    """The parallel combinator."""

    children: List[Fn]
    """composite functions."""

    children_signatures: List[Signature]
    """signatures of the composite functions."""

    @stackmethod
    def __call__(self, stack: Stack) -> Stack:
        outputs = Stack()
        for i, child in enumerate(self.children):
            signature = self.children_signatures[i]
            n_lower, n_upper = signature.index_bounds
            outputs += constrained_call(child, stack[n_lower:n_upper], signature)
        return outputs + stack[self.signature.n_in :]


def parallel(*children: Fn) -> Parallel:
    """Creates a parallel combinator.

    The combinator applies functions in parallel.

    >>> import operator as op
    >>> from redex import combinator as cb
    >>> parallel = cb.parallel(op.add, op.add)
    >>> parallel(1, 2, 3, 4) == (1 + 2, 3 + 4)
    True

    Args:
        children: a sequence of functions.

    Returns:
        a combinator.
    """
    signature, children_signatures = _estimate_parallel_signatures(children)
    return Parallel(
        signature=signature,
        children=children,
        children_signatures=children_signatures,
    )


_Initializer = tuple[int, int, List[Signature]]


def _estimate_parallel_signatures(
    children: tuple[Fn, ...],
) -> tuple[Signature, List[Signature]]:
    def count(acc: _Initializer, child: Fn) -> _Initializer:
        in_total, out_total, signatures = acc
        signature = replace(fn.infer_signature(child), start_index=in_total)
        return (
            in_total + signature.n_in,
            out_total + signature.n_out,
            signatures + [signature],
        )

    initializer: _Initializer = (0, 0, [])
    in_total, out_total, children_signatures = reduce(count, children, initializer)
    return Signature(n_in=in_total, n_out=out_total), children_signatures
