from collections import defaultdict


class Graph:
    def __init__(self):
        self.al = defaultdict(list)

    def add_edge(self, u, v):
        self.al[u].append(v)

    def vertices(self):
        return self.al.keys()

    def neighbors(self, v):
        return self.al[v]
