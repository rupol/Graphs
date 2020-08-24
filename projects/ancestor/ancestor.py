# input: graph of relationships between parents and children & starting_node ID
# format: list of (parent, child) pairs
# output: earliest known ancestor (furthest from starting_node)
# if tie: return lower numeric ID
# if no parents: return -1


class Graph:

    def __init__(self):
        self.vertices = {}

    def add_vertex(self, vertex_id):
        if vertex_id not in self.vertices:
            self.vertices[vertex_id] = set()

    def add_edge(self, v1, v2):
        if v1 in self.vertices and v2 in self.vertices:
            self.vertices[v1].add(v2)

    def get_parents(self, vertex_id):
        return self.vertices[vertex_id]


def earliest_ancestor(ancestors, starting_node):
    # build the graph
    graph = Graph()
    # loop through ancestors pair by pair
    for (parent, child) in ancestors:
        # if parent doesn't already exist in graph
        if parent not in graph.vertices:
            # add parent
            graph.add_vertex(parent)
        # if child doesn't already exist in graph
        if child not in graph.vertices:
            # add child
            graph.add_vertex(child)
        # add edge (from child -> parent) - so we can work our way backward
        graph.add_edge(child, parent)
    # graph is now created

    # traverse the graph, depth first
    # create stack w/starting vertex, visited, paths
    stack = [[starting_node]]
    visited = set()
    # create list of paths (to find longest later)
    paths = []
    # while queue isn't empty
    while stack:
        # get current vertex (pop from stack)
        current_path = stack.pop(-1)
        current = current_path[-1]
        # check if current vertex has been visited
        if current not in visited:
            # add current vertex to visited
            visited.add(current)
            # save to list of paths
            paths.append(current_path)
            # find all vertices connected to current vertex and add to stack
            for next_vertex in graph.get_parents(current):
                new_path = list(current_path)
                new_path.append(next_vertex)
                stack.append(new_path)
    # paths are now all added

    # find longest path(s)
    # find the length of the longest path
    longest = max(map(len, paths))
    # if starting_node has no parents
    if longest == 1:
        return -1

    longest_paths = [path for path in paths if len(path) == longest]

    # if more than one "earliest" ancestor (more than one longest path), return smallest ID
    earliest = [path[-1] for path in longest_paths]
    # return earliest ancestor (last element in longest list)
    return min(earliest)


test_ancestors = [(1, 3), (2, 3), (3, 6), (5, 6), (5, 7),
                  (4, 5), (4, 8), (8, 9), (11, 8), (10, 1), (12, 2)]

print(earliest_ancestor(test_ancestors, 6))  # expected: 10
