from typing import Any, Sequence
from redex.util import (
    expand_to_tuple,
    squeeze_tuple,
    flatten,
    flatten_tuples,
    flatten_tuple_annotations,
    flatten_tuple_annotation_shape,
    infer_tuple_annotation_shape,
    reshape_tuples,
)
from hypothesis import strategies as st
from hypothesis import given
import unittest
from helper import type as _t


class UtilTest(unittest.TestCase):
    @given(a=_t.seq_butnot_tuple(), b=_t.seq_butnot_tuple())
    def test_expand_to_tuple(self, a, b):
        test = [
            (a, (a,)),
            ((a,), (a,)),
            ((a, b), (a, b)),
        ]
        [self.assertEqual(expand_to_tuple(value), expect) for (value, expect) in test]

    @given(a=_t.seq_butnot_tuple(), b=_t.seq_butnot_tuple())
    def test_squeeze_tuple(self, a, b):
        test = [
            (a, a),
            ((a,), a),
            ((a, b), (a, b)),
        ]
        [self.assertEqual(squeeze_tuple(value), expect) for (value, expect) in test]

    @given(a=_t.any(), b=_t.any(), c=_t.any(), d=_t.any())
    def test_flatten(self, a, b, c, d):
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

    @given(a=_t.any(), b=_t.any(), c=_t.any(), d=_t.any())
    def test_flatten_tuples(self, a, b, c, d):
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

    @given(
        a=_t.annotation_butnot_tuple(),
        b=_t.annotation_butnot_tuple(),
        c=_t.annotation_butnot_tuple(),
        d=_t.annotation_butnot_tuple(),
    )
    def test_flatten_tuple_annotations(self, a, b, c, d):
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

    def test_flatten_nested_variadic_tuple_annotations(self):
        value = Sequence[tuple[Any, ...]]
        self.assertEqual(flatten_tuple_annotations(value), [value])

    def test_flatten_variadic_tuple_annotations(self):
        with self.assertRaises(ValueError):
            flatten_tuple_annotations(tuple[Any, ...])

    def test_flatten_ambiguous_tuple_annotations(self):
        with self.assertRaises(ValueError):
            flatten_tuple_annotations(tuple)

    def test_flatten_tuple_annotation_shape(self):
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

    @given(
        a=_t.annotation_butnot_tuple(),
        b=_t.annotation_butnot_tuple(),
        c=_t.annotation_butnot_tuple(),
        d=_t.annotation_butnot_tuple(),
    )
    def test_infer_tuple_annotation_shape(self, a, b, c, d):
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

    def test_infer_variadic_tuple_annotation_shapes(self):
        value = Sequence[tuple[Any, ...]]
        self.assertEqual(infer_tuple_annotation_shape(value), ())

    def test_flatten_variadic_tuple_annotation_shapes(self):
        with self.assertRaises(ValueError):
            infer_tuple_annotation_shape(tuple[Any, ...])

    def test_flatten_ambiguous_tuple_annotation_shapes(self):
        with self.assertRaises(ValueError):
            infer_tuple_annotation_shape(tuple)

    @given(a=_t.any(), b=_t.any(), c=_t.any(), d=_t.any())
    def test_reshape_tuples(self, a, b, c, d):
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

    def test_reshape_tuples_exceeded_input(self):
        with self.assertRaises(RuntimeError):
            reshape_tuples([1, 2, 3], ((), ()))
