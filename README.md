### The Ripple-Spreading Algorithm for the Many-to-Many Shortest Path Problem

##### Reference: Hu X B, Wang M, Leeson M S, et al. Deterministic agent-based path optimization by mimicking the spreading of ripples[J]. Evolutionary Computation, 2016, 24(2): 319-346.

The many-to-many shortest path problem has a set of source nodes as well as a set of destination nodes, and its goal is, for every source node, to find the associated shortest path connecting to one node; it does not matter which one, in the destination set.

| Variables     | Meaning                                                      |
| ------------- | ------------------------------------------------------------ |
| network       | Dictionary, {node1: {node2: length, node3: length, ...}, ...} |
| source        | The set of source nodes                                      |
| destination   | The set of destination nodes                                 |
| nn            | The number of nodes                                          |
| neighbor      | Dictionary, {node1: [the neighbor nodes of node1], ...}      |
| v             | The ripple-spreading speed (i.e., the minimum length of arcs) |
| t             | The simulated time index                                     |
| nr            | The number of ripples - 1                                    |
| epicenter_set | List, the epicenter node of the ith ripple is epicenter_set[i] |
| path_set      | List, the path of the ith ripple from the source node to node i is path_set[i] |
| length_set    | List, the length of the path of the ith ripple (i.e., path_set[i]) |
| radius_set    | List, the radius of the ith ripple is radius_set[i]          |
| active_set    | List, active_set contains all active ripples                 |
| Omega         | Dictionary, Omega[n] = i denotes that ripple i is generated at node n |

#### Example

![many-to-many SPP](C:\Users\dell\Desktop\研究生\个人算法主页\The ripple-spreading algorithm for the many-to-many shortest path problem\many-to-many SPP.png)

The source nodes are nodes 1, 3, and 5, and the destination nodes are nodes 0 and 1.

```python
if __name__ == '__main__':
    test_network = {
        0: {1: 10, 2: 1},
        1: {0: 10, 3: 2, 4: 9},
        2: {0: 1, 3: 3, 5: 2},
        3: {1: 2, 2: 3, 4: 5, 5: 6},
        4: {1: 9, 3: 5, 6: 4},
        5: {2: 2, 3: 6, 6: 9},
        6: {4: 4, 5: 9},
    }
    source_nodes = [1, 3, 5]
    destination_nodes = [0, 6]
    print(main(test_network, source_nodes, destination_nodes))
```

##### Output: 

```python
{
    1: {'path': [1, 3, 2, 0], 'length': 6}, 
    3: {'path': [3, 2, 0], 'length': 4}, 
    5: {'path': [5, 2, 0], 'length': 3},
}
```

