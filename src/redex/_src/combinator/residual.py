"""The residual combinator."""

from operator import add
from redex._src.operator.identity import identity
from redex._src.function import Fn
from redex._src import function as fn
from redex._src.combinator.serial import serial, Serial
from redex._src.combinator.branch import branch


def residual(*children: Fn, shortcut: Fn = identity) -> Serial:
    """Creates a residual combinator.

    The combinator computes the sum of two branches: main and shortcut.

    >>> import operator as op
    >>> from redex import combinator as cb
    >>> residual = cb.residual(cb.serial(op.add, op.add))
    >>> residual(1, 2, 3) == 1 + 2 + 3 + 1
    True

    Args:
        children: a main sequence of functions.
        shortcut: a skip connection. Defaults to identity function.

    Returns:
        a combinator.
    """
    if len(children) == 1:
        grouped_children = children[0]
    else:
        grouped_children = serial(*children)

    grouped_children_signature = fn.infer_signature(grouped_children)
    if grouped_children_signature.n_out != 1:
        raise ValueError(
            "The main branch of the residual must output exactly one value. "
            f"`{fn.infer_name(grouped_children)}` outputs "
            f"`{grouped_children_signature.n_out}` values."
        )
    shortcut_signature = fn.infer_signature(shortcut)
    if shortcut_signature.n_out != 1:
        raise ValueError(
            "The shortcut branch of the residual must output exactly one value. "
            f"`{fn.infer_name(shortcut)}` outputs `{shortcut_signature.n_out}` values."
        )

    return serial(
        branch(grouped_children, shortcut),
        add,
    )
