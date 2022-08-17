#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/17 7:18
# @Author  : Xavier Ma
# @Email   : xavier_mayiming@163.com
# @File    : RSA4many_to_many_SPP.py
# @Statement : The ripple-spreading algorithm for the many-to-many shortest path problem
# @Reference : Hu X B, Wang M, Leeson M S, et al. Deterministic agent-based path optimization by mimicking the spreading of ripples[J]. Evolutionary Computation, 2016, 24(2): 319-346.
import copy


def find_neighbor(network):
    """
    Find the neighbor of each node
    :param network:
    :return: {node 1: [the neighbor nodes of node 1], ...}
    """
    nn = len(network)
    neighbor = []
    for i in range(nn):
        neighbor.append(list(network[i].keys()))
    return neighbor


def find_speed(network, neighbor):
    """
    Find the ripple-spreading speed
    :param network:
    :param neighbor:
    :return:
    """
    speed = 1e10
    for i in range(len(network)):
        for j in neighbor[i]:
            speed = min(speed, network[i][j])
    return speed


def reverse(network):
    """reverse the network"""
    new_network = {}
    for i in range(len(network)):
        new_network[i] = {}
    for i in range(len(network)):
        for j in network[i].keys():
            new_network[j][i] = network[i][j]
    return new_network


def main(network, source, destination):
    """
    The main function
    :param network: {node1: {node2: length, node3: length, ...}, ...}
    :param source: The set of source nodes
    :param destination: The set of destination nodes
    :return:
    """
    # Step 1. Initialization
    network = reverse(network)  # reverse the network
    nn = len(network)  # node number
    neighbor = find_neighbor(network)  # the neighbor set
    v = find_speed(network, neighbor)  # the ripple-spreading speed
    t = 0  # simulated time index
    nr = 0  # the current number of ripples - 1
    epicenter_set = []  # epicenter set
    radius_set = []  # radius set
    length_set = []  # length set
    path_set = []  # path set
    active_set = []  # the set containing all active ripples
    omega = {}  # the set that records the ripple generated at each node
    for node in range(nn):
        omega[node] = -1

    # Step 2. Initialize the first ripples
    for node in destination:
        epicenter_set.append(node)
        radius_set.append(0)
        length_set.append(0)
        path_set.append([node])
        active_set.append(nr)
        omega[node] = nr
        nr += 1

    # Step 3. The main loop
    while True:

        # Step 3.1. Termination judgment
        flag = True
        for node in source:
            if omega[node] == -1:
                flag = False
                break
        if flag:
            break

        # Step 3.2. If there is feasible solution
        if not active_set:
            print('No feasible solution!')
            return {}

        # Step 3.3. Time updates
        t += 1
        incoming_ripples = {}

        for ripple in active_set:

            # Step 3.4. Active ripples spread out
            radius_set[ripple] += v

            # Step 3.5. New incoming ripples
            epicenter = epicenter_set[ripple]
            path = path_set[ripple]
            radius = radius_set[ripple]
            length = length_set[ripple]
            for node in neighbor[epicenter]:
                if omega[node] == -1:  # the node is unvisited
                    temp_length = network[epicenter][node]
                    if temp_length <= radius < temp_length + v:
                        temp_path = copy.deepcopy(path)
                        temp_path.append(node)
                        if node in incoming_ripples.keys():
                            incoming_ripples[node].append({
                                'path': temp_path,
                                'radius': radius - temp_length,
                                'length': length + temp_length,
                            })
                        else:
                            incoming_ripples[node] = [{
                                'path': temp_path,
                                'radius': radius - temp_length,
                                'length': length + temp_length
                            }]

        # Step 3.6. Generate new ripples
        for node in incoming_ripples.keys():
            new_ripple = sorted(incoming_ripples[node], key=lambda x: x['radius'], reverse=True)[0]
            path_set.append(new_ripple['path'])
            epicenter_set.append(node)
            radius_set.append(new_ripple['radius'])
            active_set.append(nr)
            omega[node] = nr
            length_set.append(new_ripple['length'])
            nr += 1

        # Step 3.7. Active -> inactive
        remove_ripple = []
        for ripple in active_set:
            epicenter = epicenter_set[ripple]
            flag_inactive = True
            for node in neighbor[epicenter]:
                if omega[node] == -1:
                    flag_inactive = False
                    break
            if flag_inactive:
                remove_ripple.append(ripple)
        for ripple in remove_ripple:
            active_set.remove(ripple)

    # Step 4. Sort the results
    result = {}
    for node in source:
        ripple = omega[node]
        path = path_set[ripple]
        path.reverse()
        result[node] = {
            'path': path,
            'length': length_set[ripple],
        }
    return result


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
