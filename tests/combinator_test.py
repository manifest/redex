import unittest
import operator as op
from redex import combinator as cb
from redex.combinator import Combinator, residual
from redex.combinator.parallel import parallel
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


class SerialTest(unittest.TestCase):
    def test_signature(self):
        serial = cb.serial(op.add, op.add)
        self.assertEqual(serial.signature.n_in, 3)
        self.assertEqual(serial.signature.n_out, 1)
        self.assertEqual(serial.signature.in_shape, ((), (), ()))

    def test_empty(self):
        serial = cb.serial()
        self.assertEqual(serial(1, 2, 3, 4), (1, 2, 3, 4))

    def test_single_child(self):
        serial = cb.serial(op.add)
        self.assertEqual(serial(1, 2), 1 + 2)

    def test_many_children(self):
        serial = cb.serial(op.add, op.sub, op.add)
        self.assertEqual(serial(1, 2, 3, 4), ((1 + 2) - 3) + 4)

    def test_nested(self):
        serial = cb.serial(cb.serial(op.add, op.sub), op.add)
        self.assertEqual(serial(1, 2, 3, 4), ((1 + 2) - 3) + 4)

    def test_extra_input(self):
        serial = cb.serial(op.add)
        self.assertEqual(serial(1, 2, 3, 4), (1 + 2, 3, 4))

    def test_less_input(self):
        serial = cb.serial(op.add)
        with self.assertRaises(ValueError):
            serial(1)


class BranchTest(unittest.TestCase):
    def test_signature(self):
        branch = cb.branch(op.add, op.add)
        self.assertEqual(branch.signature.n_in, 2)
        self.assertEqual(branch.signature.n_out, 2)
        self.assertEqual(branch.signature.in_shape, ((), ()))

    def test_empty(self):
        branch = cb.branch()
        self.assertEqual(branch(1, 2, 3, 4), (1, 2, 3, 4))

    def test_single_child(self):
        branch = cb.branch(op.add)
        self.assertEqual(branch(1, 2), 1 + 2)

    def test_many_children(self):
        branch = cb.branch(op.add, op.add)
        self.assertEqual(branch(1, 2), (1 + 2, 1 + 2))

    def test_nested(self):
        branch = cb.branch(cb.branch(op.add, op.add), op.add)
        self.assertEqual(branch(1, 2), (1 + 2, 1 + 2, 1 + 2))

    def test_extra_input(self):
        branch = cb.branch(op.add)
        self.assertEqual(branch(1, 2, 3, 4), (1 + 2, 3, 4))

    def test_less_input(self):
        branch = cb.branch(op.add)
        with self.assertRaises(ValueError):
            branch(1)


class ParallelTest(unittest.TestCase):
    def test_signature(self):
        parallel = cb.parallel(op.add, op.add)
        self.assertEqual(parallel.signature.n_in, 4)
        self.assertEqual(parallel.signature.n_out, 2)
        self.assertEqual(parallel.signature.in_shape, ((), (), (), ()))

    def test_empty(self):
        parallel = cb.parallel()
        self.assertEqual(parallel(1, 2, 3, 4), (1, 2, 3, 4))

    def test_single_child(self):
        parallel = cb.parallel(op.add)
        self.assertEqual(parallel(1, 2), 1 + 2)

    def test_many_children(self):
        parallel = cb.parallel(op.add, op.sub)
        self.assertEqual(parallel(1, 2, 3, 4), (1 + 2, 3 - 4))

    def test_nested(self):
        parallel = cb.parallel(cb.parallel(op.add, op.sub), op.add)
        self.assertEqual(parallel(1, 2, 3, 4, 5, 6), (1 + 2, 3 - 4, 5 + 6))

    def test_extra_input(self):
        parallel = cb.parallel(op.add)
        self.assertEqual(parallel(1, 2, 3, 4), (1 + 2, 3, 4))

    def test_less_input(self):
        parallel = cb.parallel(op.add)
        with self.assertRaises(ValueError):
            parallel(1)


class ResidualTest(unittest.TestCase):
    def test_signature(self):
        residual = cb.residual(op.add, op.add)
        self.assertEqual(residual.signature.n_in, 3)
        self.assertEqual(residual.signature.n_out, 1)
        self.assertEqual(residual.signature.in_shape, ((), (), ()))

    def test_empty(self):
        with self.assertRaises(ValueError):
            cb.residual()

    def test_single_child(self):
        residual = cb.residual(op.add)
        self.assertEqual(residual(1, 2), (1 + 2) + 1)

    def test_many_children(self):
        residual = cb.residual(op.add, op.sub)
        self.assertEqual(residual(1, 2, 3), ((1 + 2) - 3) + 1)

    def test_single_shortcut(self):
        residual = cb.residual(op.add, shortcut=op.sub)
        self.assertEqual(residual(1, 2), (1 + 2) + (1 - 2))

    def test_many_shortcuts(self):
        residual = cb.residual(op.add, shortcut=cb.serial(op.add, op.sub))
        self.assertEqual(residual(1, 2, 3), (1 + 2) + (1 + 2 - 3))

    def test_nested(self):
        residual = cb.residual(cb.residual(op.add, op.sub), op.add)
        self.assertEqual(residual(1, 2, 3, 4), ((((1 + 2) - 3) + 1) + 4) + 1)

    def test_extra_input(self):
        residual = cb.residual(op.add)
        self.assertEqual(residual(1, 2, 3, 4), ((1 + 2) + 1, 3, 4))

    def test_less_input(self):
        residual = cb.residual(op.add)
        with self.assertRaises(ValueError):
            residual(1)

    def test_extra_output(self):
        with self.assertRaises(ValueError):
            cb.residual(cb.dup())

    def test_less_output(self):
        with self.assertRaises(ValueError):
            cb.residual(cb.drop())

    def test_extra_shortcut_output(self):
        with self.assertRaises(ValueError):
            cb.residual(op.add, shortcut=cb.dup())

    def test_less_shortcut_output(self):
        with self.assertRaises(ValueError):
            cb.residual(op.add, shortcut=cb.drop())


class SelectTest(unittest.TestCase):
    def test_signature(self):
        select = cb.select(indices=[0])
        self.assertEqual(select.signature.n_in, 1)
        self.assertEqual(select.signature.n_out, 1)
        self.assertEqual(select.signature.in_shape, ((),))

    def test_empty(self):
        select = cb.select(indices=[])
        self.assertEqual(select(1, 2, 3, 4), (1, 2, 3, 4))

    def test_single_1st_item(self):
        select = cb.select(indices=[0])
        self.assertEqual(select(1, 2, 3, 4), (1, 2, 3, 4))

    def test_many_1st_items(self):
        select = cb.select(indices=[0, 0])
        self.assertEqual(select(1, 2, 3, 4), (1, 1, 2, 3, 4))

    def test_many_3rd_items(self):
        select = cb.select(indices=[2, 2])
        self.assertEqual(select(1, 2, 3, 4), (3, 3, 4))

    def test_consume_more(self):
        select = cb.select(indices=[0], n_in=2)
        self.assertEqual(select(1, 2, 3, 4), (1, 3, 4))

    def test_consume_less(self):
        select = cb.select(indices=[2], n_in=1)
        self.assertEqual(select(1, 2, 3, 4), (3, 2, 3, 4))

    def test_donot_consume(self):
        select = cb.select(indices=[2], n_in=0)
        self.assertEqual(select(1, 2, 3, 4), (3, 1, 2, 3, 4))

    def test_extra_input(self):
        select = cb.select(indices=[2])
        self.assertEqual(select(1, 2, 3, 4), (3, 4))

    def test_less_input(self):
        select = cb.select(indices=[2])
        with self.assertRaises(IndexError):
            select(1)


class DupTest(unittest.TestCase):
    def test_signature(self):
        dup = cb.dup()
        self.assertEqual(dup.signature.n_in, 1)
        self.assertEqual(dup.signature.n_out, 2)
        self.assertEqual(dup.signature.in_shape, ((),))

    def test_default(self):
        dup = cb.dup()
        self.assertEqual(dup(1), (1, 1))

    def test_single_item(self):
        dup = cb.dup(n_in=1)
        self.assertEqual(dup(1), (1, 1))

    def test_many_items(self):
        dup = cb.dup(n_in=2)
        self.assertEqual(dup(1, 2), (1, 2, 1, 2))

    def test_without_any_item(self):
        dup = cb.dup(n_in=0)
        self.assertEqual(dup(), ())

    def test_extra_input(self):
        dup = cb.dup()
        self.assertEqual(dup(1, 2, 3, 4), (1, 1, 2, 3, 4))

    def test_less_input(self):
        dup = cb.dup(n_in=2)
        with self.assertRaises(ValueError):
            dup(1)


class DropTest(unittest.TestCase):
    def test_signature(self):
        drop = cb.drop()
        self.assertEqual(drop.signature.n_in, 1)
        self.assertEqual(drop.signature.n_out, 0)
        self.assertEqual(drop.signature.in_shape, ((),))

    def test_default(self):
        drop = cb.drop()
        self.assertEqual(drop(1, 2), 2)

    def test_single_item(self):
        drop = cb.drop(n_in=1)
        self.assertEqual(drop(1), ())

    def test_many_items(self):
        drop = cb.drop(n_in=2)
        self.assertEqual(drop(1, 2), ())

    def test_without_any_item(self):
        drop = cb.drop(n_in=0)
        self.assertEqual(drop(), ())

    def test_extra_input(self):
        drop = cb.drop()
        self.assertEqual(drop(1, 2, 3, 4), (2, 3, 4))

    def test_less_input(self):
        drop = cb.drop(n_in=2)
        with self.assertRaises(ValueError):
            drop(1)
