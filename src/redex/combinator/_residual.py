"""The residual combinator."""

from redex import util
from redex.function import Fn, FnIter
from redex import function as fn
from redex.combinator._serial import serial, Serial
from redex.combinator._branch import branch
from redex.combinator._identity import identity
from redex.combinator._add import add


def residual(*children: FnIter, shortcut: Fn = identity(n_in=1)) -> Serial:
    """Creates a residual combinator.

    The combinator computes the sum of two branches: main and shortcut.

    >>> from redex import combinator as cb
    >>> residual = cb.residual(cb.serial(cb.add(), cb.add()))
    >>> residual(1, 2, 3) == 1 + 2 + 3 + 1
    True

    Args:
        children: a main sequence of functions.
        shortcut: a skip connection. Defaults to identity function.

    Returns:
        a combinator.
    """
    flat_children = util.flatten(children)
    if len(flat_children) == 1:
        grouped_children = flat_children[0]
    else:
        grouped_children = serial(*flat_children)

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
        add(n_in=2),
    )
