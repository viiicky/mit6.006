from collections import deque

from tabulate import tabulate

from graph import Graph


def bfs(graph, source_node):
    """Time complexity: O(E) where E is the number of edges in the graph.

    ####################################################################################################################
    A note on time complexity of BFS: (E = number of edges in the graph; V = number of vertices in the graph)
    The way this function is implemented, the runtime is O(E).
    You would find many writings where they say the runtime of BFS is O(V + E).
    In fact, the runtime of BFS can very well be O(V^2).
    All of these different runtime depends on the subtle variations that you could do while implementing BFS,
    and, on the fact how tight analysis you are doing. Let's analyse the different cases one by one.

    ################################################## Case #1: O(E) ##################################################
    I say the complexity of this function is O(E). Well, if I am doing an even tighter analysis, the complexity of this
    function also depends on the `source_node`. Yes!! `source_node`.

    If the graph has more than one components,
    then the amount of work this function would have to do would be linearly proportional to
    **the number of edges present in that component of the graph to which the `source_node` belongs.**

    Edges(and vertices for that matter) from all the other components are simply not contributing to the runtime
    because the way this function is written is
    it doesn't do anything with the disconnected components(edges and vertices).

    But to make things easier, we just say that the runtime
    has an upper bound of E i.e. total number of edges in the **whole graph**, not just in a particular component.
    Because in "worst" case, the input graph can have just one component,
    in which case even the tightest analysis gives O(E).

    ################################################ Case #2: O(V + E) ################################################
    The places where you see the time complexity as O(V + E),
    are implementing the BFS in a way where they are processing every single vertex present in the **whole graph**,
    not just in the component to which the `source_node` belongs.

    Some people do it in the beginning
    where they "initialise" the values for each of the vertex present in the whole graph with suitable values.
    Some folks do it at the end,
    where they take care of all such vertices that got missed because of the disconnected nature of the graph.

    For all such cases, the time complexity is indeed O(V + E).
    Since this function doesn't do this either in the beginning or at the end it's complexity remains as O(E).
    In other words, this particular function
    ignores vertices from all the components but the one to which `source_node` belongs.


    Why doesn't it matter in larger scheme of things?
    So even if you are not doing a real tight analysis,
    and coming to a runtime of O(V + E) where you could have have come up with O(E) for case #1,
    if you think bout it, even O(V + E) is "just linear" to the input(graph) we are getting,
    so it becomes a matter of prudent analysis. But the fact of the matter is that for case #1 the tighter bound is O(E)

    ################################################# Case #3: O(V^2) #################################################
    In both the above cases, I conveniently assumed the fact that graph is implemented using an adjacency list
    (because the `Graph` class present in this repo is indeed implemented using an adjacency list).
    But, your runtime would change if this fact changes.

    Had the input graph been implemented using adjacency matrix instead of adjacency list,
    the runtime for both the above cases changes to O(V^2).

    #################################################################################################################"""

    nodes_discovered = deque()

    # source_node is already discovered
    result = {source_node: {'level': 0, 'parent': None}}
    nodes_discovered.append(source_node)

    while nodes_discovered:
        parent_node = nodes_discovered.popleft()
        for current_node in graph.neighbors(parent_node):
            if current_node not in result:
                # current_node is now discovered
                result[current_node] = {'level': result[parent_node]['level'] + 1, 'parent': parent_node}
                nodes_discovered.append(current_node)

    return result


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

    print(tabulate(bfs(g, 1).items()))
