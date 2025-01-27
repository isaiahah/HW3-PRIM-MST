import numpy as np
import heapq
from typing import Union
from dataclasses import dataclass, field

# Define a dataclass object to store nodes in the priority queue alongside
# the closest edge to them and the length of that edge
@dataclass(order=True)
class Node:
    priority: int
    name: int=field(compare=False)
    prev: int=field(compare=False)


class Graph:

    def __init__(self, adjacency_mat: Union[np.ndarray, str]):
        """
    
        Unlike the BFS assignment, this Graph class takes an adjacency matrix as input. `adjacency_mat` 
        can either be a 2D numpy array of floats or a path to a CSV file containing a 2D numpy array of floats.

        In this project, we will assume `adjacency_mat` corresponds to the adjacency matrix of an undirected graph.
    
        """
        if type(adjacency_mat) == str:
            self.adj_mat = self._load_adjacency_matrix_from_csv(adjacency_mat)
        elif type(adjacency_mat) == np.ndarray:
            self.adj_mat = adjacency_mat
        else: 
            raise TypeError('Input must be a valid path or an adjacency matrix')
        self.mst = None

    def _load_adjacency_matrix_from_csv(self, path: str) -> np.ndarray:
        with open(path) as f:
            return np.loadtxt(f, delimiter=',')

    def construct_mst(self):
        """
    
        TODO: Given `self.adj_mat`, the adjacency matrix of a connected undirected graph, implement Prim's 
        algorithm to construct an adjacency matrix encoding the minimum spanning tree of `self.adj_mat`. 
            
        `self.adj_mat` is a 2D numpy array of floats. Note that because we assume our input graph is
        undirected, `self.adj_mat` is symmetric. Row i and column j represents the edge weight between
        vertex i and vertex j. An edge weight of zero indicates that no edge exists. 
        
        This function does not return anything. Instead, store the adjacency matrix representation
        of the minimum spanning tree of `self.adj_mat` in `self.mst`. We highly encourage the
        use of priority queues in your implementation. Refer to the heapq module, particularly the 
        `heapify`, `heappop`, and `heappush` functions.

        """
        # Setup helpful constants
        n = self.adj_mat.shape[0] # Number of nodes
        inf = np.max(self.adj_mat) + 1 # Value used to represent no connection
        
        # Initialize nodes in the current mst with node 0
        self.mst = np.zeros((n, n))
        
        # Initialize a list of Node data objects for the priority queue
        # Implicitly: all nodes not in node_pq are in the MST, which is why
        # node 0 is ommitted from node_pq
        node_pq = []
        for i in range(1, n):
            if self.adj_mat[0, i] > 0: # edge from current mst (1) to node
                node_pq.append(Node(self.adj_mat[0, i], i, 0))
            else:
                node_pq.append(Node(inf, i, -1))
        heapq.heapify(node_pq)

        # The main loop of prim's algorithm
        while len(node_pq) > 0:
            # De-queue the node with shortest edge to the MST
            closest_node = heapq.heappop(node_pq)
            # Add the node to the MST and the cheapest edge to the MST
            self.mst[closest_node.name, closest_node.prev] = \
                self.adj_mat[closest_node.name, closest_node.prev]
            self.mst[closest_node.prev, closest_node.name] = \
                self.adj_mat[closest_node.prev, closest_node.name]
            # Update the closest edge for neighbours of the added node
            for node in node_pq:
                if 0 < self.adj_mat[closest_node.name, node.name] < node.priority:
                    node.priority = self.adj_mat[closest_node.name, node.name]
                    node.prev = closest_node.name
            # Resort the heap, as node priorities were updated
            heapq.heapify(node_pq)
