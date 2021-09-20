import rubik
from collections import deque

def neighbors_with_edge(configuration_node):
    result = [(rubik.perm_apply(move, configuration_node), move) for move in rubik.quarter_twists]
    # print('neighbors_with_edge is returning {} for node {}'.format('\n'.join([str('node: {} by move: {}'.format(r[0], r[1])) for r in result]), configuration_node))
    return result


def shortest_path(start, end):
    """
    Using 2-way BFS, finds the shortest path from start_position to
    end_position. Returns a list of moves. 

    You can use the rubik.quarter_twists move set.
    Each move can be applied using rubik.perm_apply
    """
    if start == end:
        return []

    nodes_discovered_forward, nodes_discovered_backward = deque(), deque()

    # start is pre-discovered
    result_forward = {start: {'level': 0, 'parent': None, 'edge_from_parent': None}}
    nodes_discovered_forward.append(start)

    # end is pre-discovered
    result_backward = {end: {'level': 0, 'parent': None, 'edge_from_parent': None}}
    nodes_discovered_backward.append(end)

    path = deque()
    while nodes_discovered_forward and nodes_discovered_backward:
        # forward search
        parent_node_forward = nodes_discovered_forward.popleft()
        for current_node, incoming_edge in neighbors_with_edge(parent_node_forward):
            if current_node not in result_forward:
                # current_node is now discovered
                
                level = result_forward[parent_node_forward]['level'] + 1
                if level > 7:
                    return None
                
                result_forward[current_node] = {'level': level, 'parent': parent_node_forward, 'edge_from_parent': incoming_edge}
                nodes_discovered_forward.append(current_node)
                
                # did we cross?
                if current_node in result_backward:
                    # formulate the path and break
                    p = current_node
                    while p:
                        edge = result_forward[p]['edge_from_parent']
                        if edge is not None:
                            path.appendleft(edge)
                        p = result_forward[p]['parent']
                    
                    p = current_node
                    while p:
                        edge = result_backward[p]['edge_from_parent']
                        if edge is not None:
                            path.append(rubik.perm_inverse(edge))
                        p = result_backward[p]['parent']
                    
                    # print('path up: {}'.format(list(path)))
                    return list(path)

        # backward search
        parent_node_backward = nodes_discovered_backward.popleft()
        for current_node, incoming_edge in neighbors_with_edge(parent_node_backward):
            if current_node not in result_backward:
                # current_node is now discovered

                level = result_backward[parent_node_backward]['level'] + 1
                if level > 7:
                    return None

                result_backward[current_node] = {'level': level, 'parent': parent_node_backward, 'edge_from_parent': incoming_edge}
                nodes_discovered_backward.append(current_node)

                # did we cross?
                if current_node in result_forward:
                    # formulate the path and break
                    p = current_node
                    while p:
                        edge = result_backward[p]['edge_from_parent']
                        if edge is not None:
                            path.append(rubik.perm_inverse(edge))
                        p = result_backward[p]['parent']
                    
                    p = current_node
                    while p:
                        edge = result_forward[p]['edge_from_parent']
                        if edge is not None:
                            path.appendleft(edge)
                        p = result_forward[p]['parent']

                    # print('path down: {}'.format(list(path)))
                    return list(path)
