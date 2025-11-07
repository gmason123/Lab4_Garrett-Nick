import sys
import unittest
from typing import *
from dataclasses import dataclass
import math 
import matplotlib.pyplot as plt
import numpy as np
import random
import time
sys.setrecursionlimit(10**6)

from bst import *

TREES_PER_RUN : int = 10000
TARGET_SECONDS : tuple[float, float] = (1.5, 2.5)

# Return a BST of size n with random floats in [0, 1]
def random_tree(n: int, *, rng: Optional[random.Random] = None) -> BinarySearchTree:
    def comes_before(a: Any, b: Any) -> bool:
        return a < b

    bst = BinarySearchTree(comes_before, None) 
    for _ in range(n):
        bst = insert(bst, random.random())
    return bst


# helper for height, computes height of a node
def height_node(node: BinTree) -> int:
    if node is None:
        return 0
    return 1 + max(height_node(node.left), height_node(node.right))

# return the height of the entire BST
def height(bst: BinarySearchTree) -> int:
    return height_node(bst.tree)

# Measure time to build + measure TREES_PER_RUN trees of size n
def time_for_n(n: int, trees_per_run: int) -> float:
    start = time.perf_counter()
    for _ in range(trees_per_run):
        bst = random_tree(n)
        _ = height(bst)
    end = time.perf_counter()
    return end - start

# max_n = 80 (print(time_for_n(80, TREES_PER_RUN)) returns 2.0489358339982573 seconds)

# returns the average height for TREES_PER_RUN random trees of size n
def average_height(n: int, trees_per_run: int = TREES_PER_RUN) -> float:
    total = 0
    for _ in range(trees_per_run):
        total = total + height(random_tree(n))
    return total / trees_per_run

# Graph average height of random BSTs vs. N (number of nodes)
def make_average_height_plot(n_max: int, runs: int = TREES_PER_RUN) -> None:
    # evenly spaced N values between 1 and n_max
    N_values: List[int] = [int(i) for i in np.linspace(1, n_max, 50)]
    avg_heights: List[float] = [average_height(n, runs) for n in N_values]

    # convert to numpy arrays for matplotlib
    x_numpy: np.ndarray[Any, np.dtype[Any]] = np.array(N_values)
    y_numpy: np.ndarray[Any, np.dtype[Any]] = np.array(avg_heights)

    # create plot
    _pl: Any = cast(Any, plt)
    _pl.plot(x_numpy, y_numpy, label="Average BST Height", marker="o")
    _pl.xlabel("Number of Nodes (N)")
    _pl.ylabel("Average Height")
    _pl.title(f"Average Height of Random BSTs ({runs} trees per N)")
    _pl.grid(True)
    _pl.legend()
    _pl.show()


# Return average time to insert one random value into a random BST of size n
def time_insert_random_value(n: int, runs: int = TREES_PER_RUN) -> float:
    start = time.perf_counter()
    for _ in range(runs):
        bst = random_tree(n)
        _ = insert(bst, random.random())
    end = time.perf_counter()
    total_time = end - start
    avg_time = total_time / runs
    return avg_time

# max_n = 80, (changed output of time_insert_random_value() to total_time and print(time_insert_random_value(80)) gave 2.013073624999379 seconds)


# Plot average insert-time vs. N for 50 evenly spaced N values
def make_insert_time_plot(n_max: int, runs: int = TREES_PER_RUN) -> None:
    N_values: List[int] = [int(i) for i in np.linspace(1, n_max, 50)]
    avg_times: List[float] = [time_insert_random_value(n, runs) for n in N_values]

    x_numpy = np.array(N_values)
    y_numpy = np.array(avg_times)

    _pl: Any = cast(Any, plt)
    _pl.plot(x_numpy, y_numpy,
             label="Average Insert Time",
             color="green",
             marker="o")
    _pl.xlabel("Number of Nodes (N)")
    _pl.ylabel("Avg Insert Time (seconds)")
    _pl.title(f"Time to Insert into Random BSTs ({runs} trees per N)")
    _pl.grid(True)
    _pl.legend()
    _pl.show()


'''
def example_graph_creation() -> None:
    # Return log-base-2 of 'x' + 5.
    def f_to_graph( x : float ) -> float:
        return math.log2( x ) + 5.0
    
    # here we're using "list comprehensions": more of Python's
    # syntax sugar.
    x_coords : List[float] = [ float(i) for i in range( 1, 100 ) ]
    y_coords : List[float] = [ f_to_graph( x ) for x in x_coords ]
    # Could have just used this type from the start, but I want
    # to emphasize that 'matplotlib' uses 'numpy''s specific array
    # type, which is different from the built-in Python array
    # type.
    x_numpy : np.ndarray = np.array( x_coords )
    y_numpy : np.ndarray = np.array( y_coords )
    
    plt.plot( x_numpy, y_numpy, label = 'log_2(x)' )
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Example Graph")
    plt.grid(True)
    plt.legend() # makes the 'label's show up
    plt.show()

'''


if (__name__ == '__main__'):
    make_average_height_plot(80)
    # make_insert_time_plot(80)

