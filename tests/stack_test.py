import operator as op
from redex.stack import constrained_call, stackmethod, Stack
from redex.function import Signature
import unittest
from hypothesis import strategies as st
from hypothesis import given
from helper import type as _t


class StackTest(unittest.TestCase):
    def test_constrained_call(self):
        self.assertEqual(
            constrained_call(
                func=op.add,
                stack=(1, 2),
            ),
            (3,),
        )
        self.assertEqual(
            constrained_call(
                func=op.add,
                stack=(1, 2),
                signature=Signature(n_in=2, n_out=1),
            ),
            (3,),
        )

    def test_constrained_call_extra_stack(self):
        self.assertEqual(constrained_call(func=op.add, stack=(1, 2, 0, 0)), (3, 0, 0))

    def test_constrained_call_less_stack(self):
        with self.assertRaises(ValueError):
            constrained_call(func=op.add, stack=(1,))


class StackMethodTest(unittest.TestCase):
    @given(a=_t.any(), b=_t.any(), o=_t.any())
    def test_stackmethod(self, a, b, o):
        class A:
            @stackmethod
            def func(self, stack: Stack) -> Stack:
                return (o,)

        self.assertEqual(A().func(), o)
        self.assertEqual(A().func(a), o)
        self.assertEqual(A().func(a, b), o)

    def test_stackmethod_without_output(self):
        class A:
            @stackmethod
            def func(self, stack: Stack) -> Stack:
                return ()

        self.assertEqual(A().func(), ())

    @given(a=_t.any(), b=_t.any())
    def test_stackmethod_with_many_outputs(self, a, b):
        class A:
            @stackmethod
            def func(self, stack: Stack) -> Stack:
                return (a, b)

        self.assertEqual(A().func(), (a, b))
