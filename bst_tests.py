import sys
import unittest
from typing import *
from dataclasses import dataclass
sys.setrecursionlimit(10**6)
from bst import *

# Numeric ascending order
def int_before(a: int, b: int) -> bool:
    return a < b

# Alphabetical order
def str_before(a: str, b: str):
    return a < b

@dataclass(frozen=True)
class Point2:
   x: float
   y: float

# Order points by squared distance from the origin
def dist_before(a: Point2, b: Point2) -> bool:
    return (a.x * a.x) + (a.y * a.y) < (b.x * b.x) + (b.y * b.y)


def build_bst(comparator: Callable[[Any, Any], bool], values: List[Any]):
    bst = BinarySearchTree(comparator, None)
    for v in values:
        bst = insert(bst, v)
    return bst

class BSTTests(unittest.TestCase):

    def test_insert_and_lookup_integers(self):
        bst = BinarySearchTree(int_before, None)
        self.assertTrue(is_empty(bst))
        for v in [5, 2, 8, 1, 3, 7, 9]:
            bst = insert(bst, v)
        self.assertFalse(is_empty(bst))
        for v in [5, 1, 9]:
            self.assertTrue(lookup(bst, v))
        for v in [0, 4, 6]:
            self.assertFalse(lookup(bst, v))

    def test_insert_and_lookup_strings(self):
        bst = BinarySearchTree(str_before, None)
        for v in ["mango", "apple", "pear", "banana"]:
            bst = insert(bst, v)
        for v in ["apple", "pear"]:
            self.assertTrue(lookup(bst, v))
        for v in ["grape", "cherry"]:
            self.assertFalse(lookup(bst, v))

    def test_insert_and_lookup_points(self):
        bst = BinarySearchTree(dist_before, None)
        points = [Point2(1, 0), Point2(0, 2), Point2(-2, 0), Point2(1, 1)]
        for p in points:
            bst = insert(bst, p)
        self.assertTrue(lookup(bst, Point2(1, 0)))
        self.assertTrue(lookup(bst, Point2(0, 2)))
        self.assertFalse(lookup(bst, Point2(3, 4)))
    
    def test_duplicate_inserts_and_delete_integers(self):
        bst = build_bst(int_before, [5, 5, 5, 2, 8])
        self.assertTrue(lookup(bst, 5))
        bst = delete(bst, 5)
        self.assertTrue(lookup(bst, 5))
        bst = delete(bst, 5)
        bst = delete(bst, 5)
        self.assertFalse(lookup(bst, 5))

    def test_delete_leaf_integer(self):
        bst = build_bst(int_before, [5, 2, 8, 1, 3])
        self.assertTrue(lookup(bst, 1))
        bst = delete(bst, 1)
        self.assertFalse(lookup(bst, 1))
        for v in [5, 2, 8, 3]:
            self.assertTrue(lookup(bst, v))

    def test_delete_node_with_one_child_string(self):
        bst = build_bst(str_before, ["m", "a", "z", "b"])
        self.assertTrue(lookup(bst, "a"))
        bst = delete(bst, "a")
        self.assertFalse(lookup(bst, "a"))
        self.assertTrue(lookup(bst, "b"))


if (__name__ == '__main__'):
 unittest.main() 