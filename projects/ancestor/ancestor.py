# input: graph of relationships between parents and children & starting_node ID
# format: list of (parent, child) pairs
# output: earliest known ancestor (furthest from starting_node)
# if tie: return lower numeric ID
# if no parents: return -1

def get_parents(ancestors, node):
    # create list to store parents
    parents = set()
    # loop through ancestors
    for (parent, child) in ancestors:
        # if child is node
        if child == node:
            # add to list of parents
            parents.add(parent)
    return parents


def earliest_ancestor(ancestors, starting_node):
    # if starting_node has no parents
    if len(get_parents(ancestors, starting_node)) == 0:
        return -1

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
            for next_vertex in get_parents(ancestors, current):
                new_path = list(current_path)
                new_path.append(next_vertex)
                stack.append(new_path)

    # find longest path(s)
    # find the length of the longest path
    longest = max(map(len, paths))
    longest_paths = [path for path in paths if len(path) == longest]

    # if more than one "earliest" ancestor (more than one longest path), return smallest ID
    earliest = [path[-1] for path in longest_paths]
    # return earliest ancestor (last element in longest list)
    return min(earliest)


test_ancestors = [(1, 3), (2, 3), (3, 6), (5, 6), (5, 7),
                  (4, 5), (4, 8), (8, 9), (11, 8), (10, 1), (12, 2)]

print(earliest_ancestor(test_ancestors, 6))  # expected: 10
