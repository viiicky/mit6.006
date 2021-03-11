#!/usr/bin/env python

import bst


def height(node):
    if node is None:
        return -1
    else:
        return node.height


def update_height(node):
    node.height = max(height(node.left), height(node.right)) + 1


def size(node):
    if node is None:
        return 0

    return node.size


def update_size(node):
    node.size = size(node.left) + size(node.right) + 1


class AVL(bst.BST):
    """
AVL binary search tree implementation.
Supports insert, delete, find, find_min, next_larger each in O(lg n) time.
"""

    def left_rotate(self, x):
        y = x.right
        y.parent = x.parent
        if y.parent is None:
            self.root = y
        else:
            if y.parent.left is x:
                y.parent.left = y
            elif y.parent.right is x:
                y.parent.right = y
        x.right = y.left
        if x.right is not None:
            x.right.parent = x
        y.left = x
        x.parent = y
        update_height(x)
        update_height(y)

    def right_rotate(self, x):
        y = x.left
        y.parent = x.parent
        if y.parent is None:
            self.root = y
        else:
            if y.parent.left is x:
                y.parent.left = y
            elif y.parent.right is x:
                y.parent.right = y
        x.left = y.right
        if x.left is not None:
            x.left.parent = x
        y.right = x
        x.parent = y
        update_height(x)
        update_height(y)

    def rebalance(self, node):
        while node is not None:
            update_height(node)
            if height(node.left) >= 2 + height(node.right):
                if height(node.left.left) >= height(node.left.right):
                    self.right_rotate(node)
                else:
                    self.left_rotate(node.left)
                    self.right_rotate(node)
            elif height(node.right) >= 2 + height(node.left):
                if height(node.right.right) >= height(node.right.left):
                    self.left_rotate(node)
                else:
                    self.right_rotate(node.right)
                    self.left_rotate(node)
            node = node.parent

    # find(k), find_min(), and next_larger(k) inherited from bst.BST

    def insert(self, k):
        """Inserts a node with key k into the subtree rooted at this node.
        This AVL version guarantees the balance property: h = O(lg n).

        Args:
            k: The key of the node to be inserted.
        """
        node = super(AVL, self).insert(k)
        self.rebalance(node)

    def delete(self, k):
        """Deletes and returns a node with key k if it exists from the BST.
        This AVL version guarantees the balance property: h = O(lg n).

        Args:
            k: The key of the node that we want to delete.

        Returns:
            The deleted node with key k.
        """
        node = super(AVL, self).delete(k)
        # node.parent is actually the old parent of the node,
        # which is the first potentially out-of-balance node.
        self.rebalance(node.parent)
        return node

    def check_ri(self, height_augmentation=True, avl=True, size_augmentation=False):
        super(AVL, self).check_ri(height_augmentation=height_augmentation, avl=avl, size_augmentation=size_augmentation)


class SizeAVL(AVL):
    """
AVL binary search tree implementation where each node is also augmented to have the size of the subtree rooted at them.
Supports insert, delete, find, find_min, next_larger each in O(lg n) time.
"""

    def left_rotate(self, x):
        y = x.right
        super(SizeAVL, self).left_rotate(x)
        update_size(x)
        update_size(y)

    def right_rotate(self, x):
        y = x.left
        super(SizeAVL, self).right_rotate(x)
        update_size(x)
        update_size(y)

    def rebalance(self, node):
        while node is not None:
            update_height(node)
            update_size(node)
            if height(node.left) >= 2 + height(node.right):
                if height(node.left.left) >= height(node.left.right):
                    self.right_rotate(node)
                else:
                    self.left_rotate(node.left)
                    self.right_rotate(node)
            elif height(node.right) >= 2 + height(node.left):
                if height(node.right.right) >= height(node.right.left):
                    self.left_rotate(node)
                else:
                    self.right_rotate(node.right)
                    self.left_rotate(node)
            node = node.parent

    # find(k), find_min(), and next_larger(k) inherited from bst.BST
    # insert(k), delete(k) inherited from AVL

    def rank(self, k):
        """Returns the number of keys in the index that are smaller or equal to `k` (informally,
        if the keys were listed in ascending order, x's rank would indicate its position in the sorted array).

        Time complexity: O(log N), where N is the number of nodes in the tree.
        The structure is very similar to that of find() - in the worst case,
        rank() visits all the nodes on a path from the root to a leaf,
        and does a constant amount of computation at each node on the path."""
        r = 0
        node = self.root
        while node is not None:
            if k < node.key:
                node = node.left
            else:
                if node.left is not None:
                    r = r + 1 + node.left.size
                else:
                    r = r + 1
                if node.key == k:
                    return r
                node = node.right
        return r

    def count(self, low, high):
        """Returns the number of keys in the tree that are between `low` and `high`
        (formally, keys k such that low <= k <= high).

        As it just does some constant number of find() and rank() operations,
        time complexity for this is O(log N) where N is the number of nodes present in the tree."""
        if low > high:
            return 0

        count = self.rank(high) - self.rank(low)

        return count + 1 if self.find(low) is not None else count

    def list(self, low, high):
        """Returns all the keys between low and high.

        list(low, high) cannot be sub-linear in the worst case,
        because list(float('-inf'), float('inf')) must return all the keys in the tree,
        which takes at least linear time.
        However, if list() only has to return a few elements, it would run in sub-linear time, formally T(N) + theta(L),
        where L is the length of the list of keys output by list, and T(N) is sub-linear."""
        lca = self.lca(low, high)
        result = []
        self._node_list(lca, low, high, result)
        return result

    def _node_list(self, node, low, high, result):
        if node is None:
            return
        if low <= node.key <= high:
            result.append(node.key)
        if node.key >= low:
            self._node_list(node.left, low, high, result)
        if node.key <= high:
            self._node_list(node.right, low, high, result)

    def lca(self, low, high):
        node = self.root

        while node is not None and not (low <= node.key <= high):
            if low < node.key:
                node = node.left
            else:
                node = node.right

        return node

    def check_ri(self, height_augmentation=True, avl=True, size_augmentation=True):
        super(SizeAVL, self).check_ri(height_augmentation=height_augmentation, avl=avl,
                                      size_augmentation=size_augmentation)


def test(args=None):
    bst.test(args, BSTtype=AVL)


if __name__ == '__main__':
    test()
