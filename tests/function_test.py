from typing import Any, NoReturn
import inspect
import functools
import unittest
import operator as op
from redex._src.function import infer_signature, infer_name, FineCallable, Signature
from redex._src.function import _count_outputs, _infer_input_shape


class InferSignatureTest(unittest.TestCase):
    def test_index_bounds(self):
        self.assertEqual(Signature(n_in=2, n_out=0, start_index=0).index_bounds, (0, 2))
        self.assertEqual(Signature(n_in=2, n_out=0, start_index=0).index_bounds, (0, 2))
        self.assertEqual(Signature(n_in=2, n_out=0, start_index=1).index_bounds, (1, 3))

    def test_without_any_input_annotation(self):
        def func() -> None:
            pass

        self.assertEqual(infer_signature(func=func), Signature(n_in=0, n_out=0))

    def test_single_input(self):
        def func(a: int) -> None:
            pass

        self.assertEqual(infer_signature(func=func), Signature(n_in=1, n_out=0))

    def test_single_required_input(self):
        def func(a: int, b: int = 0) -> None:
            pass

        self.assertEqual(infer_signature(func=func), Signature(n_in=1, n_out=0))

    def test_none_type_input(self):
        def func(a: None) -> None:
            pass

        self.assertEqual(infer_signature(func=func), Signature(n_in=0, n_out=0))

    def test_tuple_input(self):
        def func(a: tuple[Any, tuple[Any, Any]]) -> None:
            pass

        self.assertEqual(
            infer_signature(func=func),
            Signature(n_in=3, n_out=0, in_shape=(((), ((), ())),)),
        )

    def test_mixed_input(self):
        def func(a: tuple[Any, tuple[Any, Any]], b: int) -> None:
            pass

        self.assertEqual(
            infer_signature(func=func),
            Signature(n_in=4, n_out=0, in_shape=(((), ((), ())), ())),
        )

    def test_variadic_tuple_input(self):
        def func(a: tuple[Any, ...]) -> None:
            pass

        with self.assertRaises(ValueError):
            infer_signature(func=func)

    def test_without_any_output_annotation(self):
        def func():
            pass

        self.assertEqual(infer_signature(func=func), Signature(n_in=0, n_out=1))

    def test_none_output(self):
        def func() -> None:
            pass

        self.assertEqual(infer_signature(func=func), Signature(n_in=0, n_out=0))

    def test_single_output(self):
        def func() -> Any:
            pass

        self.assertEqual(infer_signature(func=func), Signature(n_in=0, n_out=1))

    def test_tuple_single_output(self):
        def func() -> tuple[Any]:
            pass

        self.assertEqual(infer_signature(func=func), Signature(n_in=0, n_out=1))

    def test_tuple_many_outputs(self):
        def func() -> tuple[Any, Any]:
            pass

        self.assertEqual(infer_signature(func=func), Signature(n_in=0, n_out=2))

    def test_variadic_tuple_output(self):
        def func() -> tuple[Any, ...]:
            pass

        with self.assertRaises(ValueError):
            infer_signature(func=func)

    def test_noreturn_output(self):
        def func() -> NoReturn:
            pass

        with self.assertRaises(ValueError):
            infer_signature(func=func)

    def test_finecallable_signature(self):
        class A(FineCallable):
            pass

        a = A(signature=Signature(n_in=2, n_out=1))
        self.assertEqual(infer_signature(func=a), Signature(n_in=2, n_out=1))

    def test_supplied_signature(self):
        self.assertEqual(infer_signature(func=op.add), Signature(n_in=2, n_out=1))


class CountOutputsTest(unittest.TestCase):
    def test(self):
        self.assertEqual(_count_outputs(func=op.add), 1)
        self.assertEqual(
            _count_outputs(func=op.add, signature=inspect.signature(op.add)), 1
        )


class InputShapeTest(unittest.TestCase):
    def test(self):
        self.assertEqual(_infer_input_shape(func=op.add), ((), ()))
        self.assertEqual(
            _infer_input_shape(func=op.add, signature=inspect.signature(op.add)),
            ((), ()),
        )


class FunctionNameTest(unittest.TestCase):
    def test_builtin_function_name(self):
        self.assertEqual(infer_name(func=op.add), "add")

    def test_builtin_method_name(self):
        self.assertEqual(infer_name(func=functools.reduce), "reduce")

    def test_function_name(self):
        def a():
            pass

        self.assertEqual(infer_name(func=a), "a")

    def test_method_name(self):
        class A:
            def a(self):
                pass

        self.assertEqual(infer_name(func=A().a), "a")

    def test_callable_object_name(self):
        class A:
            def __call__(self):
                pass

        self.assertEqual(infer_name(func=A()), "A")

    def test_any_object_name(self):
        class A:
            pass

        self.assertEqual(infer_name(func=A()), "A")
