# HW 3: Prim's algorithm

![BuildStatus](https://github.com/isaiahah/HW3-PRIM-MST/actions/workflows/test.yml/badge.svg)

## Algorithm Description

Prim's algorithm functions constructs a minimum spanning tree greedily by building it from an initial node. In each iteration, it adds the shortest edge from the current MST to a node outside the MST to the MST, and adds the linked node to the MST. This continues until all nodes are in the MST, which is guaranteed to be optimal.

This code performs this using a priority queue. The `Node` dataclass stores a node and its cheapest edge as the weight of that edge and the other node involved in that edge. The edge weight acts as priority, allowing quick access to the node with the cheapest edge weight connecting it to the current MST. After adding a node to the MST (which also removes it from the priority queue), the algorithm updates the cheapest edges to nodes still outside the MST by considering the edges from the new node. If one is cheaper, that node's priority and edge is updated, then the priority queue is re-sorted to reflect these changes.
