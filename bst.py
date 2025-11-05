import sys
import unittest
from typing import *
from dataclasses import dataclass
sys.setrecursionlimit(10**6)

BinTree: TypeAlias = Union["Node", None]

@dataclass(frozen=True)
class Node:
    val: Any
    left: BinTree
    right: BinTree

@dataclass(frozen=True)
class BinarySearchTree:
    comes_before: Callable[[Any, Any], bool]
    tree: BinTree

# return true if the tree is empty and false otherwise
def is_empty(bst: BinarySearchTree) -> bool:
    return bst.tree is None

# helper for insert, returns a new node with value inserted. Goes left if comes_before(value, node.value) is True and right otherwise.
def insert_node(node: BinTree, value: Any, comes_before: Callable[[Any, Any], bool]) -> Node:
    if node is None:
        return Node(value, None, None)
    if comes_before(value, node.val):
        return Node(node.val, insert_node(node.left, value, comes_before), node.right)
    return Node(node.val, node.left, insert_node(node.right, value, comes_before))

# inserts a value into a binary search tree using the comes_before function
def insert(bst: BinarySearchTree, value: Any) -> BinarySearchTree:
    new_root = insert_node(bst.tree, value, bst.comes_before)
    return BinarySearchTree(bst.comes_before, new_root)

# helper for lookup, returns true if a and b are equal and false if not
def equals(a: Any, b: Any, comes_before: Callable[[Any, Any], bool]) -> bool:
    return not comes_before(a, b) and not comes_before(b, a)
    # a ≤ b and b ≤ a implies a = b

# Return True if value is present in the BST, False otherwise.
def lookup(bst: BinarySearchTree, value: Any) -> bool:
    node = bst.tree
    while node is not None:
        if equals(value, node.val, bst.comes_before):
            return True
        if bst.comes_before(value, node.val):
            node = node.left
        else: 
            node = node.right
    return False

# helper for delete, returns the leftmost node in a subtree
def min_node(node: "Node") -> "Node":
    current = node
    while current.left is not None:
        current = current.left
    return current

# helper for delete, returns a new subtree with one occurrence of value removed (if present)
def delete_node(node: BinTree, value: Any, comes_before: Callable[[Any, Any], bool]) -> Optional["Node"]:
    if node is None:
        return None
    # helper, defines equality in terms of comes_before
    def equals(a: Any, b: Any) -> bool:
        return not comes_before(a, b) and not comes_before(b, a)

    if equals(value, node.val):
        if node.left is None and node.right is None:
            return None
        if node.left is None:
            return node.right
        if node.right is None:
            return node.left
        succ = min_node(node.right)
        new_right = delete_node(node.right, succ.val, comes_before)
        return Node(succ.val, node.left, new_right)

    if comes_before(value, node.val):
        return Node(node.val, delete_node(node.left, value, comes_before), node.right)
    else:
        return Node(node.val, node.left, delete_node(node.right, value, comes_before))


#  Removes one occurrence of value from the tree (if present) and returns a new bst
def delete(bst: BinarySearchTree, value: Any) -> BinarySearchTree:
    new_root = delete_node(bst.tree, value, bst.comes_before)
    return BinarySearchTree(bst.comes_before, new_root)
