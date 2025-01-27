import pytest
import numpy as np
from mst import Graph
from sklearn.metrics import pairwise_distances


def check_mst(adj_mat: np.ndarray, 
              mst: np.ndarray, 
              expected_weight: int, 
              allowed_error: float = 0.0001):
    """
    
    Helper function to check the correctness of the adjacency matrix encoding an MST.
    Note that because the MST of a graph is not guaranteed to be unique, we cannot 
    simply check for equality against a known MST of a graph. 

    Arguments:
        adj_mat: adjacency matrix of full graph
        mst: adjacency matrix of proposed minimum spanning tree
        expected_weight: weight of the minimum spanning tree of the full graph
        allowed_error: allowed difference between proposed MST weight and `expected_weight`

    TODO: Add additional assertions to ensure the correctness of your MST implementation. For
    example, how many edges should a minimum spanning tree have? Are minimum spanning trees
    always connected? What else can you think of?

    """

    # Check the MST is symmetric (a valid undirected adjacency matrix) and
    # is a subset of the adjacency matrix edges
    assert np.allclose(mst, mst.T, atol=allowed_error)
    for i in range(mst.shape[0]):
        for j in range(mst.shape[1]):
            assert mst[i, j] == adj_mat[i, j] or mst[i, j] == 0

    # Assert MST is connected: Adding 1 on diagonal adds edge from each node 
    # to itself. mst^k is non-zero at i,j if a path of length k from j to i. 
    # Then mst_diag^n at i, j is non-zero if <= n steps allows moving from j
    # to i. The MST is connected if entries of mst_diag^n are non-zero
    # (there is a path between any pair of nodes).
    # Alongside the check on number of edges below, this ensures the output is a
    # spanning tree.
    mst_diagonal = mst + np.diag(np.ones(mst.shape[0]))
    assert np.all(np.linalg.matrix_power(mst_diagonal, mst.shape[0]) > 0)

    def approx_equal(a, b):
        return abs(a - b) < allowed_error

    total = 0
    edges = 0
    for i in range(mst.shape[0]):
        for j in range(i+1):
            total += mst[i, j]
            if mst[i, j] > 0:
                edges += 1
    assert approx_equal(total, expected_weight), 'Proposed MST has incorrect expected weight'
    assert edges == mst.shape[0] - 1 # 1 fewer edges than nodes

def test_mst_small():
    """
    
    Unit test for the construction of a minimum spanning tree on a small graph.
    
    """
    file_path = './data/small.csv'
    g = Graph(file_path)
    g.construct_mst()
    check_mst(g.adj_mat, g.mst, 8)


def test_mst_single_cell_data():
    """
    
    Unit test for the construction of a minimum spanning tree using single cell
    data, taken from the Slingshot R package.

    https://bioconductor.org/packages/release/bioc/html/slingshot.html

    """
    file_path = './data/slingshot_example.txt'
    coords = np.loadtxt(file_path) # load coordinates of single cells in low-dimensional subspace
    dist_mat = pairwise_distances(coords) # compute pairwise distances to form graph
    g = Graph(dist_mat)
    g.construct_mst()
    check_mst(g.adj_mat, g.mst, 57.263561605571695)


def test_mst_student():
    """
    
    TODO: Write at least one unit test for MST construction.
    
    """
    # Test 1: Verify the algorithm handles a fully connected graph (5 by 5)
    file_path = './data/fully_connected.csv'
    g = Graph(file_path)
    g.construct_mst()
    check_mst(g.adj_mat, g.mst, 10)

    # Test 2: Verify the algorithm handles a graph where all edges have the
    # same weight (size 10 by 10, edge weight 5)
    file_path = './data/equal_weight.csv'
    g = Graph(file_path)
    g.construct_mst()
    check_mst(g.adj_mat, g.mst, 45)
