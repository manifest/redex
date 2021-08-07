import unittest
import operator as op
from redex._src.combinator.base import Combinator
from redex._src.combinator.serial import serial
from redex._src.combinator.parallel import parallel
from redex._src.combinator.branch import branch
from redex._src.combinator.residual import residual
from redex._src.combinator.select import select
from redex._src.combinator.dup import dup
from redex._src.combinator.drop import drop
from redex._src.function import Signature


class CombinatorTest(unittest.TestCase):
    def test_combinator_is_dataclass(self):
        class A(Combinator):
            a: int
            pass

        try:
            A(signature=Signature(n_in=0, n_out=0), a=0)
        except:
            self.fail("__init__ is not implemented for Add class.")


class SerialTest(unittest.TestCase):
    def test_signature(self):
        comb = serial(op.add, op.add)
        self.assertEqual(comb.signature.n_in, 3)
        self.assertEqual(comb.signature.n_out, 1)
        self.assertEqual(comb.signature.in_shape, ((), (), ()))

    def test_empty(self):
        comb = serial()
        self.assertEqual(comb(1, 2, 3, 4), (1, 2, 3, 4))

    def test_single_child(self):
        comb = serial(op.add)
        self.assertEqual(comb(1, 2), 1 + 2)

    def test_many_children(self):
        comb = serial(op.add, op.sub, op.add)
        self.assertEqual(comb(1, 2, 3, 4), ((1 + 2) - 3) + 4)

    def test_nested(self):
        comb = serial(serial(op.add, op.sub), op.add)
        self.assertEqual(comb(1, 2, 3, 4), ((1 + 2) - 3) + 4)

    def test_nested_aslist(self):
        comb = serial([op.add, [op.sub, op.add]])
        self.assertEqual(comb(1, 2, 3, 4), ((1 + 2) - 3) + 4)

    def test_extra_input(self):
        comb = serial(op.add)
        self.assertEqual(comb(1, 2, 3, 4), (1 + 2, 3, 4))

    def test_less_input(self):
        comb = serial(op.add)
        with self.assertRaises(ValueError):
            comb(1)


class BranchTest(unittest.TestCase):
    def test_signature(self):
        comb = branch(op.add, op.add)
        self.assertEqual(comb.signature.n_in, 2)
        self.assertEqual(comb.signature.n_out, 2)
        self.assertEqual(comb.signature.in_shape, ((), ()))

    def test_empty(self):
        comb = branch()
        self.assertEqual(comb(1, 2, 3, 4), (1, 2, 3, 4))

    def test_single_child(self):
        comb = branch(op.add)
        self.assertEqual(comb(1, 2), 1 + 2)

    def test_many_children(self):
        comb = branch(op.add, op.add)
        self.assertEqual(comb(1, 2), (1 + 2, 1 + 2))

    def test_nested(self):
        comb = branch(branch(op.add, op.add), op.add)
        self.assertEqual(comb(1, 2), (1 + 2, 1 + 2, 1 + 2))

    def test_nested_aslist(self):
        comb = branch([op.add, [op.sub, op.add]])
        self.assertEqual(comb(1, 2), (1 + 2, 1 - 2, 1 + 2))

    def test_extra_input(self):
        comb = branch(op.add)
        self.assertEqual(comb(1, 2, 3, 4), (1 + 2, 3, 4))

    def test_less_input(self):
        comb = branch(op.add)
        with self.assertRaises(ValueError):
            comb(1)


class ParallelTest(unittest.TestCase):
    def test_signature(self):
        comb = parallel(op.add, op.add)
        self.assertEqual(comb.signature.n_in, 4)
        self.assertEqual(comb.signature.n_out, 2)
        self.assertEqual(comb.signature.in_shape, ((), (), (), ()))

    def test_empty(self):
        comb = parallel()
        self.assertEqual(comb(1, 2, 3, 4), (1, 2, 3, 4))

    def test_single_child(self):
        comb = parallel(op.add)
        self.assertEqual(comb(1, 2), 1 + 2)

    def test_many_children(self):
        comb = parallel(op.add, op.sub)
        self.assertEqual(comb(1, 2, 3, 4), (1 + 2, 3 - 4))

    def test_nested(self):
        comb = parallel(parallel(op.add, op.sub), op.add)
        self.assertEqual(comb(1, 2, 3, 4, 5, 6), (1 + 2, 3 - 4, 5 + 6))

    def test_nested_aslist(self):
        comb = parallel([[op.add, op.sub], op.add])
        self.assertEqual(comb(1, 2, 3, 4, 5, 6), (1 + 2, 3 - 4, 5 + 6))

    def test_extra_input(self):
        comb = parallel(op.add)
        self.assertEqual(comb(1, 2, 3, 4), (1 + 2, 3, 4))

    def test_less_input(self):
        comb = parallel(op.add)
        with self.assertRaises(ValueError):
            comb(1)


class ResidualTest(unittest.TestCase):
    def test_signature(self):
        comb = residual(op.add, op.add)
        self.assertEqual(comb.signature.n_in, 3)
        self.assertEqual(comb.signature.n_out, 1)
        self.assertEqual(comb.signature.in_shape, ((), (), ()))

    def test_empty(self):
        with self.assertRaises(ValueError):
            residual()

    def test_single_child(self):
        comb = residual(op.add)
        self.assertEqual(comb(1, 2), (1 + 2) + 1)

    def test_many_children(self):
        comb = residual(op.add, op.sub)
        self.assertEqual(comb(1, 2, 3), ((1 + 2) - 3) + 1)

    def test_single_shortcut(self):
        comb = residual(op.add, shortcut=op.sub)
        self.assertEqual(comb(1, 2), (1 + 2) + (1 - 2))

    def test_many_shortcuts(self):
        comb = residual(op.add, shortcut=serial(op.add, op.sub))
        self.assertEqual(comb(1, 2, 3), (1 + 2) + (1 + 2 - 3))

    def test_nested(self):
        comb = residual(residual(op.add, op.sub), op.add)
        self.assertEqual(comb(1, 2, 3, 4), ((((1 + 2) - 3) + 1) + 4) + 1)

    def test_nested_aslist(self):
        comb = residual([op.add, [op.sub, op.add]])
        self.assertEqual(comb(1, 2, 3, 4), ((1 + 2) - 3) + 4 + 1)

    def test_extra_input(self):
        comb = residual(op.add)
        self.assertEqual(comb(1, 2, 3, 4), ((1 + 2) + 1, 3, 4))

    def test_less_input(self):
        comb = residual(op.add)
        with self.assertRaises(ValueError):
            comb(1)

    def test_extra_output(self):
        with self.assertRaises(ValueError):
            residual(dup())

    def test_less_output(self):
        with self.assertRaises(ValueError):
            residual(drop())

    def test_extra_shortcut_output(self):
        with self.assertRaises(ValueError):
            residual(op.add, shortcut=dup())

    def test_less_shortcut_output(self):
        with self.assertRaises(ValueError):
            residual(op.add, shortcut=drop())


class SelectTest(unittest.TestCase):
    def test_signature(self):
        comb = select(indices=[0])
        self.assertEqual(comb.signature.n_in, 1)
        self.assertEqual(comb.signature.n_out, 1)
        self.assertEqual(comb.signature.in_shape, ((),))

    def test_empty(self):
        comb = select(indices=[])
        self.assertEqual(comb(1, 2, 3, 4), (1, 2, 3, 4))

    def test_single_1st_item(self):
        comb = select(indices=[0])
        self.assertEqual(comb(1, 2, 3, 4), (1, 2, 3, 4))

    def test_many_1st_items(self):
        comb = select(indices=[0, 0])
        self.assertEqual(comb(1, 2, 3, 4), (1, 1, 2, 3, 4))

    def test_many_3rd_items(self):
        comb = select(indices=[2, 2])
        self.assertEqual(comb(1, 2, 3, 4), (3, 3, 4))

    def test_consume_more(self):
        comb = select(indices=[0], n_in=2)
        self.assertEqual(comb(1, 2, 3, 4), (1, 3, 4))

    def test_consume_less(self):
        comb = select(indices=[2], n_in=1)
        self.assertEqual(comb(1, 2, 3, 4), (3, 2, 3, 4))

    def test_donot_consume(self):
        comb = select(indices=[2], n_in=0)
        self.assertEqual(comb(1, 2, 3, 4), (3, 1, 2, 3, 4))

    def test_extra_input(self):
        comb = select(indices=[2])
        self.assertEqual(comb(1, 2, 3, 4), (3, 4))

    def test_less_input(self):
        comb = select(indices=[2])
        with self.assertRaises(IndexError):
            comb(1)


class DupTest(unittest.TestCase):
    def test_signature(self):
        comb = dup()
        self.assertEqual(comb.signature.n_in, 1)
        self.assertEqual(comb.signature.n_out, 2)
        self.assertEqual(comb.signature.in_shape, ((),))

    def test_default(self):
        comb = dup()
        self.assertEqual(comb(1), (1, 1))

    def test_single_item(self):
        comb = dup(n_in=1)
        self.assertEqual(comb(1), (1, 1))

    def test_many_items(self):
        comb = dup(n_in=2)
        self.assertEqual(comb(1, 2), (1, 2, 1, 2))

    def test_without_any_item(self):
        comb = dup(n_in=0)
        self.assertEqual(comb(), ())

    def test_extra_input(self):
        comb = dup()
        self.assertEqual(comb(1, 2, 3, 4), (1, 1, 2, 3, 4))

    def test_less_input(self):
        comb = dup(n_in=2)
        with self.assertRaises(ValueError):
            comb(1)


class DropTest(unittest.TestCase):
    def test_signature(self):
        comb = drop()
        self.assertEqual(comb.signature.n_in, 1)
        self.assertEqual(comb.signature.n_out, 0)
        self.assertEqual(comb.signature.in_shape, ((),))

    def test_default(self):
        comb = drop()
        self.assertEqual(comb(1, 2), 2)

    def test_single_item(self):
        comb = drop(n_in=1)
        self.assertEqual(comb(1), ())

    def test_many_items(self):
        comb = drop(n_in=2)
        self.assertEqual(comb(1, 2), ())

    def test_without_any_item(self):
        comb = drop(n_in=0)
        self.assertEqual(comb(), ())

    def test_extra_input(self):
        comb = drop()
        self.assertEqual(comb(1, 2, 3, 4), (2, 3, 4))

    def test_less_input(self):
        comb = drop(n_in=2)
        with self.assertRaises(ValueError):
            comb(1)
