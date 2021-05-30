from tabulate import tabulate

from graph import Graph


class DFSResult:
    def __init__(self):
        self.parents = {}
        self.start_times = {}
        self.finish_times = {}
        self.edges = []

        self.order = []
        self.time = 0

    def __str__(self):
        order_output = tabulate([(n, self.parents[n], self.start_times[n], self.finish_times[n]) for n in self.order],
                                headers=['Vertex', 'Parent', 'Start time', 'Finish time'])

        edge_classification_output = tabulate(self.edges)

        # An undirected graph may entail some ambiguity, since (u, v) and (v, u) are really the same
        # edge. In such a case, we classify the edge as the first type in the classification list that applies, i.e.,
        # we classify the edge according to whichever of (u, v) or (v, u) the search encounters first. Note
        # that undirected graphs cannot contain forward edges and cross edges, since in those cases, the
        # edge (v, u) would have already been traversed (classified) during DFS before we reach u and try
        # to visit v.
        edges_undirected = {}
        for (u, v), kind in self.edges:
            if (v, u) not in edges_undirected:
                edges_undirected[(u, v)] = kind

        undirected_edge_classification_output = tabulate(edges_undirected.items())

        return f"Vertices in the order they are finished:\n{order_output}" \
               f"\nEdge classification if it's a directed graph:\n{edge_classification_output}" \
               f"\nEdge classification if it's an undirected graph:\n{undirected_edge_classification_output}"


def dfs(graph):
    """Time complexity: O(V + E) where E is the number of edges in `graph` and V is the number of vertices.

    dfs_visit() takes O(E) for the edges that's present in the "sub-graph" it works on,
    and this method calls dfs_visit() V times - even then the "worst" time complexity of this method is not V.E
    because if we do the careful overall analysis of the algorithm,
    we find that the `if` checks present to check if a vertex/node is already visited reduces the number of operations,
    and the total number of operations that we actually end up doing is V + E, just linear."""

    result = DFSResult()
    for vertex in graph.vertices():  # give every vertex a chance to become source
        if vertex not in result.parents:  # if not already discovered
            dfs_visit(graph, vertex, result)  # visit it
    return result


def dfs_visit(graph, source_node, result, parent_node=None):
    """Time complexity: O(E) where E is the number of edges in the "sub-graph" as seen from the source `source_node`."""

    # source_node's visit starts here
    result.parents[source_node] = parent_node
    result.time += 1
    result.start_times[source_node] = result.time

    if parent_node:
        # If source_node is visited for the first time as we traverse the edge (parent_node, source_node), then the edge is a tree edge
        result.edges.append(((parent_node, source_node), 'tree'))

    for current_node in graph.neighbors(source_node):
        if current_node not in result.parents:
            # current_node is now discovered, so let's visit it
            dfs_visit(graph, current_node, result, source_node)

        # If current_node has already been visited...
        elif current_node not in result.finish_times:
            # ...and current_node is an ancestor of source_node, then edge (source_node, current_node) is a back edge
            result.edges.append(((source_node, current_node), 'backward'))
        elif result.start_times[source_node] < result.start_times[current_node]:
            # ... and current_node is a descendant of source_node, then edge (source_node, current_node) is a forward edge
            result.edges.append(((source_node, current_node), 'forward'))
        else:
            # ... and current_node is neither an ancestor or descendant of source_node, then edge (source_node, current_node) is a cross edge
            result.edges.append(((source_node, current_node), 'cross'))

    result.time += 1
    result.finish_times[source_node] = result.time
    # source_node's visit ends here
    result.order.append(source_node)


def topological_sort(graph):
    result = dfs(graph)
    result.order.reverse()
    return result.order


if __name__ == '__main__':
    g = Graph()
    g.add_edge(1, 2)
    g.add_edge(2, 1)
    g.add_edge(1, 5)
    g.add_edge(5, 1)

    g.add_edge(2, 5)
    g.add_edge(5, 2)
    g.add_edge(2, 4)
    g.add_edge(4, 2)
    g.add_edge(2, 3)
    g.add_edge(3, 2)

    g.add_edge(5, 4)
    g.add_edge(4, 5)
    g.add_edge(4, 3)
    g.add_edge(3, 4)

    dfs_result = dfs(g)
    print(dfs_result)
    print(f'{topological_sort(g)=}')
