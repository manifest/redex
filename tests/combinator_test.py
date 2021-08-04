import unittest
from redex.combinator import Combinator
from redex.function import Signature


class CombinatorTest(unittest.TestCase):
    def test_combinator_is_dataclass(self):
        class A(Combinator):
            a: int
            pass

        try:
            A(signature=Signature(n_in=0, n_out=0), a=0)
        except:
            self.fail("__init__ is not implemented for Add class.")
