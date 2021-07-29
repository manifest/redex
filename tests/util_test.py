from redex.util import expand_to_tuple, squeeze_tuple, deep_flatten
import unittest


class UtilTest(unittest.TestCase):
    def test_expand_to_tuple(self):
        test = [
            (1, (1,)),
            ((1,), (1,)),
            ((1, 2), (1, 2)),
            ("ab", ("ab",)),
            (("ab", "cd"), ("ab", "cd")),
            ([1, 2], ([1, 2],)),
            ([1], ([1],)),
            ([], ([],)),
        ]
        [self.assertEqual(expand_to_tuple(a), b) for (a, b) in test]

    def test_squeeze(self):
        test = [
            (1, 1),
            ((1,), 1),
            ((1, 2), (1, 2)),
            ("ab", "ab"),
            (("ab", "cd"), ("ab", "cd")),
            ([1, 2], [1, 2]),
            ([1], [1]),
            ([], []),
        ]
        [self.assertEqual(squeeze_tuple(a), b) for (a, b) in test]

    def test_deep_flatten_on_sequence(self):
        test = [
            ([1], [1]),
            ([1, 2, 3, 4], [1, 2, 3, 4]),
            ([[1, 2, 3], 4], [1, 2, 3, 4]),
            ([1, [2, 3, 4]], [1, 2, 3, 4]),
            ([[1, [2, 3]], 4], [1, 2, 3, 4]),
            ([[1, [[2], 3]], 4], [1, 2, 3, 4]),
            ([1, [[2, 3], 4]], [1, 2, 3, 4]),
            ([["ab", "cd", "ef"], "gh"], ["a", "b", "c", "d", "e", "f", "g", "h"]),
            (["ab", ["cd", "ef", "gh"]], ["a", "b", "c", "d", "e", "f", "g", "h"]),
            (["ab", [["cd", "ef"], "gh"]], ["a", "b", "c", "d", "e", "f", "g", "h"]),
            (["ab", [[["cd"], "ef"], "gh"]], ["a", "b", "c", "d", "e", "f", "g", "h"]),
            (["ab", "cd", "ef", "gh"], ["a", "b", "c", "d", "e", "f", "g", "h"]),
            ("ab", ["a", "b"]),
        ]
        [self.assertEqual(deep_flatten(a), b) for (a, b) in test]

    def test_deep_flatten_on_item(self):
        self.assertRaises(TypeError, deep_flatten(()))
