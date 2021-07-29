from redex.util import expand_to_tuple, squeeze_tuple, deep_flatten
from hypothesis import given, strategies as st
import unittest


def _any():
    return st.integers() | st.binary() | st.text()


def _anyseq_but_tuple():
    return st.lists(_any()) | st.sets(_any())


class UtilTest(unittest.TestCase):
    @given(a=_anyseq_but_tuple(), b=_anyseq_but_tuple())
    def test_expand_to_tuple(self, a, b):
        test = [
            (a, (a,)),
            ((a,), (a,)),
            ((a, b), (a, b)),
        ]
        [self.assertEqual(expand_to_tuple(value), expect) for (value, expect) in test]

    @given(a=_anyseq_but_tuple(), b=_anyseq_but_tuple())
    def test_squeeze_tuple(self, a, b):
        test = [
            (a, a),
            ((a,), a),
            ((a, b), (a, b)),
        ]
        [self.assertEqual(squeeze_tuple(value), expect) for (value, expect) in test]

    @given(a=_any(), b=_any(), c=_any(), d=_any())
    def test_deep_flatten_on_sequence(self, a, b, c, d):
        test = [
            ([], []),
            ([a], [a]),
            ([a, b, c, d], [a, b, c, d]),
            ([[a, b, c], d], [a, b, c, d]),
            ([a, [b, c, d]], [a, b, c, d]),
            ([a, [[b, c], d]], [a, b, c, d]),
            ([a, [[b, [c]], d]], [a, b, c, d]),
        ]
        [self.assertEqual(deep_flatten(value), expect) for (value, expect) in test]

    def test_deep_flatten_notiterable(self):
        self.assertEqual(deep_flatten(1), 1)
