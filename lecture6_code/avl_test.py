import unittest
from avl import *


class AVLTest(unittest.TestCase):
    def setUp(self):
        self.tree1 = AVL()
        self.tree1.insert(23)
        self.tree1.insert(8)
        self.tree1.insert(4)
        self.tree1.insert(16)
        self.tree1.insert(15)
        self.tree1.insert(42)

    def testInsert(self):
        tree2 = AVL()
        tree2.insert(5)
        tree2.check_ri()
        self.assertEqual(5, tree2.find(5).key)
        tree2.insert(3)
        tree2.check_ri()
        self.assertEqual(3, tree2.find(3).key)
        tree2.insert(4)
        tree2.check_ri()
        self.assertEqual(4, tree2.find(4).key)
        tree2.insert(4)
        tree2.check_ri()
        self.assertEqual(4, tree2.find(4).key)

    def testFind(self):
        tree2 = AVL()
        self.assertIsNone(tree2.find(3))
        tree2.insert(4)
        self.assertIsNone(tree2.find(3))

    def testDeleteNodeWithoutChildren(self):
        d = self.tree1.delete(15)
        self.tree1.check_ri()
        self.assertEqual(15, d.key)
        self.assertIsNone(self.tree1.find(15))

    def testDeleteNodeWithOneChild(self):
        d = self.tree1.delete(16)
        self.tree1.check_ri()
        self.assertEqual(16, d.key)
        self.assertIsNone(self.tree1.find(16))

    def testDeleteNodeWithTwoChildren(self):
        d = self.tree1.delete(8)
        self.tree1.check_ri()
        self.assertEqual(8, d.key)
        self.assertIsNone(self.tree1.find(8))

    def testDeleteRoot(self):
        d = self.tree1.delete(23)
        self.tree1.check_ri()
        self.assertEqual(23, d.key)
        self.assertIsNone(self.tree1.find(23))
        self.assertEqual(42, self.tree1.find(42).key)

    def testDeleteLastNode(self):
        tree2 = AVL()
        tree2.insert(1)
        deleted = tree2.delete(1)
        self.assertEqual(1, deleted.key)
        tree2.check_ri()
        tree2.insert(2)
        tree2.check_ri()

    def testNextLarger(self):
        self.assertEqual(15, self.tree1.next_larger(8).key)
        self.assertEqual(23, self.tree1.next_larger(16).key)

    def testFindMin(self):
        tree2 = AVL()
        self.assertIsNone(tree2.find_min())
        tree2.insert(5)
        self.assertEqual(5, tree2.find(5).key)
        self.assertEqual(5, tree2.find_min().key)
        self.assertEqual(4, self.tree1.find_min().key)


class SizeAVLTest(unittest.TestCase):
    def setUp(self):
        self.tree1 = SizeAVL()

        self.tree1.insert(23)
        self.assertEqual(1, self.tree1.rank(23))

        self.tree1.insert(8)
        self.assertEqual(2, self.tree1.rank(23))
        self.assertEqual(1, self.tree1.rank(8))

        self.tree1.insert(4)
        self.assertEqual(3, self.tree1.rank(23))
        self.assertEqual(2, self.tree1.rank(8))
        self.assertEqual(1, self.tree1.rank(4))

        self.tree1.insert(16)
        self.assertEqual(4, self.tree1.rank(23))
        self.assertEqual(2, self.tree1.rank(8))
        self.assertEqual(1, self.tree1.rank(4))
        self.assertEqual(3, self.tree1.rank(16))

        self.tree1.insert(15)
        self.assertEqual(5, self.tree1.rank(23))
        self.assertEqual(2, self.tree1.rank(8))
        self.assertEqual(1, self.tree1.rank(4))
        self.assertEqual(4, self.tree1.rank(16))
        self.assertEqual(3, self.tree1.rank(15))

        self.tree1.insert(42)
        self.assertEqual(5, self.tree1.rank(23))
        self.assertEqual(2, self.tree1.rank(8))
        self.assertEqual(1, self.tree1.rank(4))
        self.assertEqual(4, self.tree1.rank(16))
        self.assertEqual(3, self.tree1.rank(15))
        self.assertEqual(6, self.tree1.rank(42))

        self.assertEqual(0, self.tree1.rank(3))
        self.assertEqual(6, self.tree1.rank(43))
        self.assertEqual(4, self.tree1.rank(20))

    def testInsert(self):
        tree2 = SizeAVL()

        tree2.insert(5)
        tree2.check_ri()
        self.assertEqual(5, tree2.find(5).key)
        self.assertEqual(1, tree2.rank(5))

        tree2.insert(3)
        tree2.check_ri()
        self.assertEqual(3, tree2.find(3).key)
        self.assertEqual(2, tree2.rank(5))
        self.assertEqual(1, tree2.rank(3))

        tree2.insert(4)
        tree2.check_ri()
        self.assertEqual(4, tree2.find(4).key)
        self.assertEqual(3, tree2.rank(5))
        self.assertEqual(1, tree2.rank(3))
        self.assertEqual(2, tree2.rank(4))

        tree2.insert(4)
        tree2.check_ri()
        self.assertEqual(4, tree2.find(4).key)
        self.assertEqual(4, tree2.rank(5))
        self.assertEqual(1, tree2.rank(3))
        self.assertEqual(2, tree2.rank(4))

    def testFind(self):
        tree2 = SizeAVL()
        self.assertIsNone(tree2.find(3))
        tree2.insert(4)
        self.assertIsNone(tree2.find(3))

    def testDeleteNodeWithoutChildren(self):
        d = self.tree1.delete(15)
        self.tree1.check_ri()
        self.assertEqual(15, d.key)
        self.assertIsNone(self.tree1.find(15))
        self.assertEqual(4, self.tree1.rank(23))
        self.assertEqual(2, self.tree1.rank(8))
        self.assertEqual(1, self.tree1.rank(4))
        self.assertEqual(3, self.tree1.rank(16))
        self.assertEqual(5, self.tree1.rank(42))

    def testDeleteNodeWithOneChild(self):
        d = self.tree1.delete(16)
        self.tree1.check_ri()
        self.assertEqual(16, d.key)
        self.assertIsNone(self.tree1.find(16))
        self.assertEqual(4, self.tree1.rank(23))
        self.assertEqual(2, self.tree1.rank(8))
        self.assertEqual(1, self.tree1.rank(4))
        self.assertEqual(3, self.tree1.rank(15))
        self.assertEqual(5, self.tree1.rank(42))

    def testDeleteNodeWithTwoChildren(self):
        d = self.tree1.delete(8)
        self.tree1.check_ri()
        self.assertEqual(8, d.key)
        self.assertIsNone(self.tree1.find(8))
        self.assertEqual(4, self.tree1.rank(23))
        self.assertEqual(1, self.tree1.rank(4))
        self.assertEqual(3, self.tree1.rank(16))
        self.assertEqual(2, self.tree1.rank(15))
        self.assertEqual(5, self.tree1.rank(42))

    def testDeleteRoot(self):
        d = self.tree1.delete(23)
        self.tree1.check_ri()
        self.assertEqual(23, d.key)
        self.assertIsNone(self.tree1.find(23))
        self.assertEqual(42, self.tree1.find(42).key)
        self.assertEqual(2, self.tree1.rank(8))
        self.assertEqual(1, self.tree1.rank(4))
        self.assertEqual(4, self.tree1.rank(16))
        self.assertEqual(3, self.tree1.rank(15))
        self.assertEqual(5, self.tree1.rank(42))

    def testDeleteLastNode(self):
        tree2 = SizeAVL()

        tree2.insert(1)
        deleted = tree2.delete(1)
        self.assertEqual(1, deleted.key)
        tree2.check_ri()

        tree2.insert(2)
        tree2.check_ri()
        self.assertEqual(1, tree2.rank(2))

    def testNextLarger(self):
        self.assertEqual(15, self.tree1.next_larger(8).key)
        self.assertEqual(23, self.tree1.next_larger(16).key)

    def testFindMin(self):
        tree2 = SizeAVL()
        self.assertIsNone(tree2.find_min())
        tree2.insert(5)
        self.assertEqual(5, tree2.find(5).key)
        self.assertEqual(5, tree2.find_min().key)
        self.assertEqual(4, self.tree1.find_min().key)

    def testCount(self):
        self.assertEqual(6, self.tree1.count(4, 42))
        self.assertEqual(6, self.tree1.count(3, 42))
        self.assertEqual(6, self.tree1.count(4, 43))
        self.assertEqual(6, self.tree1.count(3, 43))

        self.assertEqual(3, self.tree1.count(15, 23))
        self.assertEqual(3, self.tree1.count(14, 23))
        self.assertEqual(3, self.tree1.count(15, 24))
        self.assertEqual(3, self.tree1.count(14, 24))

        self.assertEqual(3, self.tree1.count(16, 50))
        self.assertEqual(1, self.tree1.count(41, 43))
        self.assertEqual(1, self.tree1.count(42, 43))
        self.assertEqual(1, self.tree1.count(41, 42))
        self.assertEqual(0, self.tree1.count(24, 41))

        self.assertEqual(4, self.tree1.count(1, 16))
        self.assertEqual(1, self.tree1.count(3, 5))
        self.assertEqual(1, self.tree1.count(4, 5))
        self.assertEqual(1, self.tree1.count(3, 4))
        self.assertEqual(0, self.tree1.count(5, 7))

        self.assertEqual(0, self.tree1.count(14, 14))
        self.assertEqual(1, self.tree1.count(16, 16))
        self.assertEqual(0, self.tree1.count(16, 15))
        self.assertEqual(0, self.tree1.count(16, 10))
        self.assertEqual(0, self.tree1.count(20, 15))

    def testList(self):
        self.assertItemsEqual([4, 8, 15, 16, 23, 42], self.tree1.list(4, 42))
        self.assertItemsEqual([4, 8, 15, 16, 23, 42], self.tree1.list(3, 42))
        self.assertItemsEqual([4, 8, 15, 16, 23, 42], self.tree1.list(4, 43))
        self.assertItemsEqual([4, 8, 15, 16, 23, 42], self.tree1.list(3, 43))

        self.assertItemsEqual([15, 16, 23], self.tree1.list(15, 23))
        self.assertItemsEqual([15, 16, 23], self.tree1.list(14, 23))
        self.assertItemsEqual([15, 16, 23], self.tree1.list(15, 24))
        self.assertItemsEqual([15, 16, 23], self.tree1.list(14, 24))

        self.assertItemsEqual([16, 23, 42], self.tree1.list(16, 50))
        self.assertItemsEqual([42], self.tree1.list(41, 43))
        self.assertItemsEqual([42], self.tree1.list(42, 43))
        self.assertItemsEqual([42], self.tree1.list(41, 42))
        self.assertItemsEqual([], self.tree1.list(24, 41))

        self.assertItemsEqual([4, 8, 15, 16], self.tree1.list(1, 16))
        self.assertItemsEqual([4], self.tree1.list(3, 5))
        self.assertItemsEqual([4], self.tree1.list(4, 5))
        self.assertItemsEqual([4], self.tree1.list(3, 4))
        self.assertItemsEqual([], self.tree1.list(5, 7))

        self.assertItemsEqual([], self.tree1.list(14, 14))
        self.assertItemsEqual([16], self.tree1.list(16, 16))
        self.assertItemsEqual([], self.tree1.list(16, 15))
        self.assertItemsEqual([], self.tree1.list(16, 10))
        self.assertItemsEqual([], self.tree1.list(20, 15))


if __name__ == '__main__':
    unittest.main()
