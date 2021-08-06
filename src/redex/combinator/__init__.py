"""Combinator functions compose other functions.

Combinators are essentially just callable objects (or functions).
They may compose, be used by, be mixed with another combinator,
or standard python function.

Combinators operate on stack. They take inputs off the stack, execute
a function, then push its outputs back onto the stack. If function
output is a tuple, it gets flattened before placed on the stack. If
an input argument is a tuple, each tuple parameter is considered as
an independent item on the stack. These parameters are reshaped before
get passed to the function as arguments.

A number of outputs, inputs, and input shapes of the function are
inferred from its type annotation. They also can be set explicitly.
When return annotation isn't available, a single output is assumed
to support buit-in functions. Any input argument without default value
is counted as a single input.

*Note that for the tuples used in type annotations, a number of tuple
parameters must be definite (e.g. tuple parameters must be specified
and variadic tuples must not be used)*.
"""

from redex._src.combinator.base import Combinator
from redex._src.combinator.serial import serial, Serial
from redex._src.combinator.parallel import parallel, Parallel
from redex._src.combinator.select import select, Select
from redex._src.combinator.branch import branch
from redex._src.combinator.residual import residual
from redex._src.combinator.dup import dup, Dup
from redex._src.combinator.drop import drop, Drop

__all__ = [
    "Combinator",
    "serial",
    "Serial",
    "parallel",
    "Parallel",
    "select",
    "Select",
    "branch",
    "residual",
    "dup",
    "Dup",
    "drop",
    "Drop",
]
