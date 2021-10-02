import operator as op
from redex.stack import constrained_call, stackmethod, Stack, verify_stack_size
from redex.function import Signature
import unittest
from hypothesis import given
from helper import type as _t


class ConstrainedCallTest(unittest.TestCase):
    def test_justright_input(self):
        self.assertEqual(constrained_call(func=op.add, stack=(1, 2)), (3,))

    def test_extra_input(self):
        self.assertEqual(constrained_call(func=op.add, stack=(1, 2, 0, 0)), (3, 0, 0))

    def test_less_input(self):
        with self.assertRaises(ValueError):
            constrained_call(func=op.add, stack=(1,))

    def test_supplied_signature(self):
        self.assertEqual(
            constrained_call(
                func=op.add,
                stack=(1, 2),
                signature=Signature(n_in=2, n_out=1),
            ),
            (3,),
        )


class VerifyStackSizeTest(unittest.TestCase):
    def test_justright_input(self):
        self.assertEqual(verify_stack_size(func=op.add, stack=(1, 2)), 2)

    def test_extra_input(self):
        self.assertEqual(verify_stack_size(func=op.add, stack=(1, 2, 3, 4)), 4)

    def test_less_input(self):
        with self.assertRaises(ValueError):
            verify_stack_size(func=op.add, stack=(1,))

    def test_supplied_signature(self):
        self.assertEqual(
            verify_stack_size(
                func=op.add,
                stack=(1, 2),
                signature=Signature(n_in=2, n_out=1),
            ),
            2,
        )


class StackMethodTest(unittest.TestCase):
    @given(a=_t.any(), b=_t.any(), o=_t.any())
    def test_inputs(self, a, b, o):
        class A:
            @stackmethod
            def func(self, stack: Stack) -> Stack:
                return (o,)

        self.assertEqual(A().func(), o)
        self.assertEqual(A().func(a), o)
        self.assertEqual(A().func(a, b), o)

    def test_without_any_output(self):
        class A:
            @stackmethod
            def func(self, stack: Stack) -> Stack:
                return ()

        self.assertEqual(A().func(), ())

    @given(a=_t.any(), b=_t.any())
    def test_many_outputs(self, a, b):
        class A:
            @stackmethod
            def func(self, stack: Stack) -> Stack:
                return (a, b)

        self.assertEqual(A().func(), (a, b))
