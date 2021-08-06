from typing import Any, Sequence
from redex._src.util import (
    expand_to_tuple,
    squeeze_tuple,
    flatten,
    flatten_tuples,
    flatten_tuple_annotations,
    flatten_tuple_annotation_shape,
    infer_tuple_annotation_shape,
    reshape_tuples,
)
from hypothesis import given
import unittest
from helper import type as _t


class ExpandToTupleTest(unittest.TestCase):
    @given(a=_t.seq_butnot_tuple(), b=_t.seq_butnot_tuple())
    def test_justright_input(self, a, b):
        test = [
            (a, (a,)),
            ((a,), (a,)),
            ((a, b), (a, b)),
        ]
        [self.assertEqual(expand_to_tuple(value), expect) for (value, expect) in test]


class SqueezeTupleTest(unittest.TestCase):
    @given(a=_t.seq_butnot_tuple(), b=_t.seq_butnot_tuple())
    def test_justright_input(self, a, b):
        test = [
            (a, a),
            ((a,), a),
            ((a, b), (a, b)),
        ]
        [self.assertEqual(squeeze_tuple(value), expect) for (value, expect) in test]


class FlattenTest(unittest.TestCase):
    @given(a=_t.any(), b=_t.any(), c=_t.any(), d=_t.any())
    def test_justright(self, a, b, c, d):
        test = [
            ([], []),
            ([a], [a]),
            ([a, b, c, d], [a, b, c, d]),
            ([[a, b, c], d], [a, b, c, d]),
            ([a, [b, c, d]], [a, b, c, d]),
            ([a, [[b, c], d]], [a, b, c, d]),
            ([a, [[b, [c]], d]], [a, b, c, d]),
            (a, [a]),
        ]
        [self.assertEqual(flatten(value), expect) for (value, expect) in test]


class FlattenTuples(unittest.TestCase):
    @given(a=_t.any(), b=_t.any(), c=_t.any(), d=_t.any())
    def test_justright(self, a, b, c, d):
        test = [
            ((), []),
            ((a,), [a]),
            ((a, b, c, d), [a, b, c, d]),
            (((a, b, c), d), [a, b, c, d]),
            ((a, (b, c, d)), [a, b, c, d]),
            ((a, ((b, c), d)), [a, b, c, d]),
            ((a, ((b, (c)), d)), [a, b, c, d]),
            (a, [a]),
        ]
        [self.assertEqual(flatten_tuples(value), expect) for (value, expect) in test]


class FlattenTupleAnnotations(unittest.TestCase):
    @given(
        a=_t.annotation_butnot_tuple(),
        b=_t.annotation_butnot_tuple(),
        c=_t.annotation_butnot_tuple(),
        d=_t.annotation_butnot_tuple(),
    )
    def test_justright(self, a, b, c, d):
        test = [
            (tuple[a], [a]),
            (tuple[a, b, c, d], [a, b, c, d]),
            (tuple[tuple[a, b, c], d], [a, b, c, d]),
            (tuple[a, tuple[b, c, d]], [a, b, c, d]),
            (tuple[a, tuple[tuple[b, c], d]], [a, b, c, d]),
            (tuple[a, tuple[tuple[b, tuple[c]], d]], [a, b, c, d]),
            (a, [a]),
        ]
        [
            self.assertEqual(flatten_tuple_annotations(value), expect)
            for (value, expect) in test
        ]

    def test_nested(self):
        value = Sequence[tuple[Any, ...]]
        self.assertEqual(flatten_tuple_annotations(value), [value])

    def test_variadic_tuple_annotation(self):
        with self.assertRaises(ValueError):
            flatten_tuple_annotations(tuple[Any, ...])

    def test_ambiguous_tuple_annotation(self):
        with self.assertRaises(ValueError):
            flatten_tuple_annotations(tuple)


class FlattenTupleAnnotationShape(unittest.TestCase):
    def test_justright_input(self):
        test = [
            ((), [()]),
            (((),), [()]),
            (((), (), (), ()), [(), (), (), ()]),
            ((((), (), ()), ()), [(), (), (), ()]),
            (((), ((), (), ())), [(), (), (), ()]),
            (((), (((), ()), ())), [(), (), (), ()]),
            (((), (((), (())), ())), [(), (), (), ()]),
        ]
        [
            self.assertEqual(flatten_tuple_annotation_shape(value), expect)
            for (value, expect) in test
        ]

    def test_variadic_tuple_annotation(self):
        with self.assertRaises(ValueError):
            infer_tuple_annotation_shape(tuple[Any, ...])

    def test_ambiguous_tuple_annotation(self):
        with self.assertRaises(ValueError):
            infer_tuple_annotation_shape(tuple)


class InferTupleAnnotationShapeTest(unittest.TestCase):
    @given(
        a=_t.annotation_butnot_tuple(),
        b=_t.annotation_butnot_tuple(),
        c=_t.annotation_butnot_tuple(),
        d=_t.annotation_butnot_tuple(),
    )
    def test_justright_input(self, a, b, c, d):
        test = [
            (tuple[a], ((),)),
            (tuple[a, b, c, d], ((), (), (), ())),
            (tuple[tuple[a, b, c], d], (((), (), ()), ())),
            (tuple[a, tuple[b, c, d]], ((), ((), (), ()))),
            (tuple[a, tuple[tuple[b, c], d]], ((), (((), ()), ()))),
            (tuple[a, tuple[tuple[b, tuple[c]], d]], ((), (((), ((),)), ()))),
            (a, ()),
        ]
        [
            self.assertEqual(infer_tuple_annotation_shape(value), expect)
            for (value, expect) in test
        ]

    def test_embeded_variadic_tuple_annotation(self):
        value = Sequence[tuple[Any, ...]]
        self.assertEqual(infer_tuple_annotation_shape(value), ())


class ReshapeTuplesTest(unittest.TestCase):
    @given(a=_t.any(), b=_t.any(), c=_t.any(), d=_t.any())
    def test_justright_input(self, a, b, c, d):
        test = [
            (((a), ((),)), (a,)),
            (((a, b, c, d), ((), (), (), ())), (a, b, c, d)),
            (((a, b, c, d), (((), (), ()), ())), ((a, b, c), d)),
            (((a, b, c, d), ((), ((), (), ()))), (a, (b, c, d))),
            (((a, b, c, d), ((), (((), ()), ()))), (a, ((b, c), d))),
            (((a, b, c, d), ((), (((), ((),)), ()))), (a, ((b, (c,)), d))),
            ((a, ()), a),
        ]
        [self.assertEqual(reshape_tuples(*values), expect) for (values, expect) in test]

    def test_exceeded_input(self):
        with self.assertRaises(RuntimeError):
            reshape_tuples([1, 2, 3], ((), ()))
