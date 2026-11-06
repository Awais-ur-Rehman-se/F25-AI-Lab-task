GRAPH = {'A': ['B', 'C'], 'B': ['D', 'E'], 'C': ['F'],
         'D': [], 'E': ['G'], 'F': [], 'G': []}
FOUND, CUTOFF, FAILURE = 'FOUND', 'CUTOFF', 'FAILURE'
def dls(graph, start, goal, limit):
    order = []
    def visit(node, path, depth_left):
        order.append(node)
        if node == goal:
            return FOUND, path
        nxt = [n for n in graph.get(node, []) if n not in path]
        if depth_left == 0:
            return (CUTOFF if nxt else FAILURE), None
        cutoff = False
        for n in nxt:
            status, result = visit(n, path + [n], depth_left - 1)
            if status == FOUND:
                return FOUND, result
            if status == CUTOFF:
                cutoff = True
        return (CUTOFF if cutoff else FAILURE), None
    status, path = visit(start, [start], limit)
    return status, path, order
def iddfs(graph, start, goal, max_depth):
    attempts = []
    for limit in range(max_depth + 1):
        status, path, order = dls(graph, start, goal, limit)
        attempts.append((limit, status, len(order)))
        if status != CUTOFF:
            return status, path, attempts
    return CUTOFF, None, attempts
def dls_global(graph, node, goal, limit, visited):
    visited.add(node)
    if node == goal:
        return FOUND
    if limit == 0:
        return CUTOFF
    result = FAILURE
    for n in graph.get(node, []):
        if n not in visited:
            r = dls_global(graph, n, goal, limit - 1, visited)
            if r == FOUND:
                return FOUND
            if r == CUTOFF:
                result = CUTOFF
    return result
if __name__ == '__main__':
    print('TASK 2: DLS and IDDFS on the A-G graph (start A, goal G)')
    print('Prediction: limits 1,2 -> CUTOFF ; limits 3,4 -> FOUND (G is at depth 3)')
    print('\nDLS results')
    for limit in [1, 2, 3, 4]:
        status, path, order = dls(GRAPH, 'A', 'G', limit)
        print(' ', 'limit', limit, '|', status, '| path', path, '| processed', order, len(order))
    print('\nIDDFS results')
    for max_depth in [1, 2, 3, 4]:
        status, path, attempts = iddfs(GRAPH, 'A', 'G', max_depth)
        print(' ', 'max depth', max_depth, '|', status, '| path', path)
        print('     limits attempted (limit, status, nodes):', attempts)
        print('     total nodes processed:', sum(a[2] for a in attempts))
    print('\nPrediction check')
    for limit, expected in [(1, CUTOFF), (2, CUTOFF), (3, FOUND), (4, FOUND)]:
        print('  limit', limit, 'as predicted:', dls(GRAPH, 'A', 'G', limit)[0] == expected)
    print('\nEdge-case tests')
    cyc = {'A': ['B'], 'B': ['C'], 'C': ['A', 'D'], 'D': []}
    diamond = {'S': ['X', 'Y'], 'X': ['Y'], 'Y': ['G'], 'G': []}
    print('  Start == goal, DLS limit 0:', dls(GRAPH, 'A', 'A', 0)[:2])
    print('  Start == goal, IDDFS max 3:', iddfs(GRAPH, 'A', 'A', 3)[:2])
    print('  Unreachable Z, DLS limit 2:', dls(GRAPH, 'A', 'Z', 2)[:2])
    print('  Unreachable Z, DLS limit 3:', dls(GRAPH, 'A', 'Z', 3)[:2])
    s, p, att = iddfs(GRAPH, 'A', 'Z', 5)
    print('  Unreachable Z, IDDFS max 5:', s, att)
    print('  Cycle graph, goal D, DLS limit 5:', dls(cyc, 'A', 'D', 5)[:2])
    print('  Cycle graph, goal D, DLS limit 2:', dls(cyc, 'A', 'D', 2)[:2])
    print('  Cycle graph, goal Z, IDDFS max 6:', iddfs(cyc, 'A', 'Z', 6)[:2])
    print('  Diamond graph, limit 2, path-local check:', dls(diamond, 'S', 'G', 2)[:2])
    print('  Diamond graph, limit 2, WRONG global visited:', dls_global(diamond, 'S', 'G', 2, set()),
          '<- misses the goal')
