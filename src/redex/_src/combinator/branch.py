"""The branch combinator."""

from typing import List
from functools import reduce
from redex._src import util
from redex._src import function as fn
from redex._src.function import Fn, FnIter
from redex._src.combinator.serial import serial, Serial
from redex._src.combinator.parallel import parallel
from redex._src.combinator.select import select


def branch(*children: FnIter) -> Serial:
    """Creates a branch combinator.

    The combinator combines multiple branches of combosite functions
    and operate on copy of inputs. Each branch is a function or a serie
    of composite functions.

    >>> import operator as op
    >>> from redex import combinator as cb
    >>> branch = cb.branch(cb.serial(op.add, op.add), op.add)
    >>> branch(1, 2, 3) == (1 + 2 + 3, 1 + 2)
    True

    Args:
        children: a sequence of functions.

    Returns:
        a combinator.
    """
    flat_children = util.flatten(children)
    indices = _estimate_branch_indices(flat_children)
    return serial(
        select(indices=indices),
        parallel(*flat_children),
    )


def _estimate_branch_indices(children: List[Fn]) -> List[int]:
    def count(acc: List[int], child: Fn) -> List[int]:
        signature = fn.infer_signature(child)
        return acc + list(range(0, signature.n_in))

    initializer: List[int] = []
    return reduce(count, children, initializer)
